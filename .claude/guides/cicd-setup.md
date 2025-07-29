# CI/CD Configuration Guide

## Overview

Continuous Integration and Continuous Deployment (CI/CD) automates the software delivery process from code commit to production deployment. This guide provides comprehensive templates and best practices for setting up CI/CD pipelines across multiple platforms.

### Why CI/CD Matters

1. **Consistency**: Every change goes through the same validation process
2. **Early Detection**: Issues are caught immediately, not days later
3. **Faster Delivery**: Automated processes reduce manual overhead
4. **Quality Assurance**: Enforces standards through automated checks
5. **Documentation**: Pipeline definitions serve as deployment documentation

## Decision Framework for CI/CD Platform Selection

### Key Considerations

```yaml
evaluation_criteria:
  cost:
    - free_tier_limits
    - paid_tier_pricing
    - compute_minutes
    - storage_costs
  
  integration:
    - version_control_system
    - artifact_registries
    - deployment_targets
    - third_party_services
  
  features:
    - parallel_execution
    - matrix_builds
    - caching_capabilities
    - secret_management
    - environment_management
  
  complexity:
    - learning_curve
    - maintenance_overhead
    - debugging_capabilities
    - community_support
```

### Platform Comparison Matrix

| Platform | Best For | Strengths | Limitations |
|----------|----------|-----------|-------------|
| GitHub Actions | GitHub-hosted projects | Deep GitHub integration, free for public repos | Limited free minutes for private repos |
| GitLab CI | GitLab users, self-hosted | Integrated DevOps platform, great UI | Complex for simple projects |
| Jenkins | Enterprise, custom needs | Highly customizable, plugin ecosystem | High maintenance overhead |
| CircleCI | Fast builds, parallelization | Excellent caching, fast execution | Pricing can escalate quickly |

## GitHub Actions

### Complete Template

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  release:
    types: [ created ]

env:
  # Global environment variables
  NODE_VERSION: '20.x'
  PYTHON_VERSION: '3.11'
  GO_VERSION: '1.21'
  DOCKER_BUILDKIT: 1
  COMPOSE_DOCKER_CLI_BUILD: 1

jobs:
  # Job 1: Linting and Code Quality
  lint:
    name: Lint and Code Quality
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for better analysis

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint:js

      - name: Run Prettier
        run: npm run lint:format

      - name: Run markdownlint
        run: npm run lint:md

      - name: Check TypeScript
        if: hashFiles('tsconfig.json') != ''
        run: npm run type-check

  # Job 2: Security Scanning
  security:
    name: Security Scanning
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

      - name: Run CodeQL Analysis
        uses: github/codeql-action/analyze@v2
        with:
          languages: javascript,python,go

      - name: Dependency Review
        uses: actions/dependency-review-action@v3
        if: github.event_name == 'pull_request'

  # Job 3: Build and Test (Matrix Strategy)
  test:
    name: Test (${{ matrix.os }}, ${{ matrix.node-version }})
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node-version: ['18.x', '20.x']
        exclude:
          # Exclude specific combinations if needed
          - os: windows-latest
            node-version: '18.x'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Cache node modules
        uses: actions/cache@v3
        with:
          path: node_modules
          key: ${{ runner.os }}-node-${{ matrix.node-version }}-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-${{ matrix.node-version }}-

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm test -- --coverage --watchAll=false

      - name: Run integration tests
        run: npm run test:integration

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info
          flags: unittests
          name: codecov-${{ matrix.os }}-${{ matrix.node-version }}

      - name: Archive test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results-${{ matrix.os }}-${{ matrix.node-version }}
          path: |
            coverage/
            test-results/

  # Job 4: Build Docker Images
  docker:
    name: Build Docker Images
    runs-on: ubuntu-latest
    needs: [lint, security, test]
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: |
            ${{ secrets.DOCKER_USERNAME }}/myapp
            ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            BUILD_DATE=${{ github.event.head_commit.timestamp }}
            VCS_REF=${{ github.sha }}
            VERSION=${{ steps.meta.outputs.version }}

  # Job 5: Generate and Sign Artifacts
  artifacts:
    name: Generate Artifacts
    runs-on: ubuntu-latest
    needs: [docker]
    permissions:
      contents: write
      id-token: write
      attestations: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Build production bundle
        run: |
          npm ci --production
          npm run build

      - name: Create release artifacts
        run: |
          tar -czf dist.tar.gz dist/
          zip -r dist.zip dist/

      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          artifact-name: sbom.spdx.json
          format: spdx-json

      - name: Sign artifacts with Sigstore
        uses: sigstore/cosign-installer@v3
      
      - name: Sign artifacts
        run: |
          cosign sign-blob --yes dist.tar.gz > dist.tar.gz.sig
          cosign sign-blob --yes dist.zip > dist.zip.sig

      - name: Generate attestation
        uses: actions/attest-build-provenance@v1
        with:
          subject-path: |
            dist.tar.gz
            dist.zip

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: release-artifacts
          path: |
            dist.tar.gz
            dist.tar.gz.sig
            dist.zip
            dist.zip.sig
            sbom.spdx.json

  # Job 6: Deploy to Environments
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [artifacts]
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster staging-cluster \
            --service myapp-staging \
            --force-new-deployment

      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster staging-cluster \
            --services myapp-staging

      - name: Run smoke tests
        run: |
          npm run test:smoke -- --url https://staging.example.com

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [deploy-staging]
    if: github.event_name == 'release'
    environment:
      name: production
      url: https://example.com
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_PROD_ROLE_ARN }}
          aws-region: us-east-1

      - name: Deploy to production
        run: |
          # Blue-green deployment
          ./scripts/deploy-production.sh ${{ github.event.release.tag_name }}

      - name: Verify deployment
        run: |
          npm run test:smoke -- --url https://example.com

      - name: Notify deployment
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Production deployment ${{ github.event.release.tag_name }} completed'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### GitHub Actions Best Practices

1. **Use Composite Actions for Reusability**

```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Common setup steps for all jobs'
inputs:
  node-version:
    description: 'Node.js version to use'
    required: false
    default: '20.x'
outputs:
  cache-hit:
    description: 'Whether the cache was hit'
    value: ${{ steps.cache.outputs.cache-hit }}
runs:
  using: "composite"
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'
    
    - name: Cache dependencies
      id: cache
      uses: actions/cache@v3
      with:
        path: node_modules
        key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    
    - name: Install dependencies
      if: steps.cache.outputs.cache-hit != 'true'
      shell: bash
      run: npm ci
```

2. **Implement Proper Secret Management**

```yaml
# Use GitHub Environments for secret scoping
deploy:
  environment:
    name: ${{ github.event_name == 'release' && 'production' || 'staging' }}
  steps:
    - name: Deploy
      env:
        # Secrets are automatically scoped to environment
        API_KEY: ${{ secrets.API_KEY }}
        DATABASE_URL: ${{ secrets.DATABASE_URL }}
      run: |
        # Never echo secrets
        ./deploy.sh
```

3. **Optimize Caching Strategy**

```yaml
# Multi-level caching example
- name: Cache Docker layers
  uses: actions/cache@v3
  with:
    path: /tmp/.buildx-cache
    key: ${{ runner.os }}-buildx-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-buildx-

- name: Cache Gradle dependencies
  uses: actions/cache@v3
  with:
    path: |
      ~/.gradle/caches
      ~/.gradle/wrapper
    key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
    restore-keys: |
      ${{ runner.os }}-gradle-
```

## GitLab CI

### Complete Template

```yaml
# .gitlab-ci.yml
variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  FF_USE_FASTZIP: "true"
  ARTIFACT_COMPRESSION_LEVEL: "fast"
  CACHE_COMPRESSION_LEVEL: "fast"
  NODE_VERSION: "20"
  POSTGRES_VERSION: "15"

stages:
  - build
  - test
  - security
  - package
  - deploy
  - verify

# Global cache configuration
.cache_template: &cache_config
  key:
    files:
      - package-lock.json
      - Gemfile.lock
      - go.sum
  paths:
    - node_modules/
    - vendor/ruby/
    - vendor/go/
  policy: pull

# Build stage
build:dependencies:
  stage: build
  image: node:${NODE_VERSION}-alpine
  before_script:
    - apk add --no-cache git python3 make g++
  script:
    - npm ci --prefer-offline --no-audit
    - npm run build
  artifacts:
    name: "build-$CI_COMMIT_REF_SLUG"
    paths:
      - dist/
      - node_modules/
    expire_in: 1 day
  cache:
    <<: *cache_config
    policy: pull-push

# Parallel testing with coverage
test:unit:
  stage: test
  image: node:${NODE_VERSION}-alpine
  needs: ["build:dependencies"]
  parallel:
    matrix:
      - TEST_SUITE: [unit, integration, e2e]
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  before_script:
    - apk add --no-cache chromium
    - export CHROME_BIN=/usr/bin/chromium-browser
  script:
    - npm run test:${TEST_SUITE} -- --coverage
    - npm run coverage:merge
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
      junit: test-results/junit.xml
    paths:
      - coverage/
    expire_in: 1 week
  cache:
    <<: *cache_config

# Code quality checks
code_quality:
  stage: test
  image: docker:stable
  services:
    - docker:dind
  script:
    - docker run --rm 
        --volume "$PWD":/code 
        --volume /var/run/docker.sock:/var/run/docker.sock 
        codeclimate/codeclimate analyze
  artifacts:
    reports:
      codequality: gl-code-quality-report.json
    expire_in: 1 week
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'

# Security scanning
security:scan:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy fs --security-checks vuln,config --format template --template "@/contrib/gitlab.tpl" -o gl-container-scanning-report.json .
    - trivy image --format template --template "@/contrib/gitlab.tpl" -o gl-dependency-scanning-report.json ${CI_PROJECT_NAME}:${CI_COMMIT_SHA}
  artifacts:
    reports:
      container_scanning: gl-container-scanning-report.json
      dependency_scanning: gl-dependency-scanning-report.json
  allow_failure: true

# SAST scanning
sast:
  stage: security
  include:
    - template: Security/SAST.gitlab-ci.yml

# Build Docker images
package:docker:
  stage: package
  image: docker:stable
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - apk add --no-cache git
    - export VERSION=$(git describe --tags --always --dirty)
  script:
    # Build multi-arch images
    - docker buildx create --use
    - docker buildx build
        --platform linux/amd64,linux/arm64
        --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
        --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG
        --tag $CI_REGISTRY_IMAGE:$VERSION
        --cache-from $CI_REGISTRY_IMAGE:cache
        --cache-to $CI_REGISTRY_IMAGE:cache
        --push .
    # Generate SBOM
    - docker sbom $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA > sbom.json
    # Sign image
    - echo "$COSIGN_KEY" | base64 -d > /tmp/cosign.key
    - cosign sign --key /tmp/cosign.key $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - rm /tmp/cosign.key
  artifacts:
    paths:
      - sbom.json
    reports:
      sbom: sbom.json

# Deploy to staging
deploy:staging:
  stage: deploy
  image: bitnami/kubectl:latest
  environment:
    name: staging
    url: https://staging.example.com
    on_stop: stop:staging
  before_script:
    - kubectl config set-cluster k8s --server="$KUBE_URL" --insecure-skip-tls-verify=true
    - kubectl config set-credentials admin --token="$KUBE_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=admin --namespace=staging
    - kubectl config use-context default
  script:
    - envsubst < k8s/deployment.yaml | kubectl apply -f -
    - kubectl rollout status deployment/${CI_PROJECT_NAME} -n staging
    - kubectl wait --for=condition=ready pod -l app=${CI_PROJECT_NAME} -n staging --timeout=300s
  only:
    - develop

# Stop staging environment
stop:staging:
  stage: deploy
  image: bitnami/kubectl:latest
  environment:
    name: staging
    action: stop
  script:
    - kubectl delete deployment ${CI_PROJECT_NAME} -n staging
  when: manual
  only:
    - develop

# Deploy to production with manual approval
deploy:production:
  stage: deploy
  image: bitnami/kubectl:latest
  environment:
    name: production
    url: https://example.com
  before_script:
    - kubectl config set-cluster k8s --server="$PROD_KUBE_URL" --insecure-skip-tls-verify=true
    - kubectl config set-credentials admin --token="$PROD_KUBE_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=admin --namespace=production
    - kubectl config use-context default
  script:
    # Blue-green deployment
    - ./scripts/blue-green-deploy.sh ${CI_PROJECT_NAME} ${CI_COMMIT_SHA}
    # Verify deployment
    - kubectl wait --for=condition=ready pod -l app=${CI_PROJECT_NAME},version=${CI_COMMIT_SHA} -n production --timeout=600s
    # Run health checks
    - ./scripts/health-check.sh https://example.com
  when: manual
  only:
    - tags

# Post-deployment verification
verify:production:
  stage: verify
  image: node:${NODE_VERSION}-alpine
  needs: ["deploy:production"]
  script:
    - npm run test:smoke -- --url https://example.com
    - npm run test:performance -- --url https://example.com
  only:
    - tags

# Scheduled security audit
security:audit:
  stage: security
  image: node:${NODE_VERSION}-alpine
  script:
    - npm audit --production
    - npm outdated
  only:
    - schedules
  allow_failure: true

# Include templates for additional functionality
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/License-Scanning.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
```

### GitLab CI Best Practices

1. **Use GitLab Features Effectively**

```yaml
# Use extends for DRY configuration
.deploy_template:
  image: alpine:latest
  before_script:
    - apk add --no-cache curl
    - echo "Setting up deployment environment"
  after_script:
    - echo "Cleaning up deployment"

deploy:staging:
  extends: .deploy_template
  script:
    - ./deploy.sh staging

deploy:production:
  extends: .deploy_template
  script:
    - ./deploy.sh production
  when: manual
```

2. **Optimize with DAG (Directed Acyclic Graph)**

```yaml
# Define job dependencies for parallel execution
build:frontend:
  stage: build
  script:
    - npm run build:frontend

build:backend:
  stage: build
  script:
    - npm run build:backend

test:frontend:
  stage: test
  needs: ["build:frontend"]
  script:
    - npm run test:frontend

test:backend:
  stage: test  
  needs: ["build:backend"]
  script:
    - npm run test:backend

deploy:all:
  stage: deploy
  needs: ["test:frontend", "test:backend"]
  script:
    - ./deploy.sh
```

## Jenkins

### Complete Jenkinsfile

```groovy
// Jenkinsfile
@Library('shared-library@main') _

pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: node
    image: node:20-alpine
    command: ['cat']
    tty: true
    resources:
      requests:
        memory: "2Gi"
        cpu: "1"
      limits:
        memory: "4Gi"
        cpu: "2"
  - name: docker
    image: docker:dind
    securityContext:
      privileged: true
    env:
    - name: DOCKER_TLS_CERTDIR
      value: ""
  - name: kubectl
    image: bitnami/kubectl:latest
    command: ['cat']
    tty: true
  - name: trivy
    image: aquasec/trivy:latest
    command: ['cat']
    tty: true
"""
        }
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '10'))
        timestamps()
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
        skipDefaultCheckout()
    }

    environment {
        // Global environment variables
        DOCKER_REGISTRY = credentials('docker-registry')
        SONAR_TOKEN = credentials('sonar-token')
        SLACK_WEBHOOK = credentials('slack-webhook')
        NODE_OPTIONS = '--max-old-space-size=4096'
        
        // Dynamic variables
        VERSION = sh(script: "echo \${BUILD_NUMBER}-\${GIT_COMMIT:0:7}", returnStdout: true).trim()
        IMAGE_NAME = "${DOCKER_REGISTRY}/myapp"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "${GIT_BRANCH}"]],
                    extensions: [
                        [$class: 'CloneOption', depth: 0, noTags: false, shallow: false],
                        [$class: 'CleanBeforeCheckout'],
                        [$class: 'SubmoduleOption', recursiveSubmodules: true]
                    ],
                    userRemoteConfigs: [[
                        credentialsId: 'github-credentials',
                        url: "${GIT_URL}"
                    ]]
                ])
                
                script {
                    // Set build description
                    currentBuild.description = "Branch: ${GIT_BRANCH}, Commit: ${GIT_COMMIT[0..7]}"
                }
            }
        }

        stage('Setup') {
            steps {
                container('node') {
                    sh '''
                        echo "Node version: $(node --version)"
                        echo "NPM version: $(npm --version)"
                        
                        # Install dependencies with caching
                        if [ -f "package-lock.json" ]; then
                            npm ci --prefer-offline --no-audit
                        else
                            npm install
                        fi
                    '''
                }
            }
        }

        stage('Quality Gates') {
            parallel {
                stage('Lint') {
                    steps {
                        container('node') {
                            sh '''
                                echo "Running linters..."
                                npm run lint:js || true
                                npm run lint:css || true
                                npm run lint:md || true
                            '''
                        }
                    }
                }

                stage('Unit Tests') {
                    steps {
                        container('node') {
                            sh '''
                                echo "Running unit tests..."
                                npm run test:unit -- --coverage --ci --reporters=default --reporters=jest-junit
                            '''
                            
                            // Publish test results
                            junit 'test-results/**/*.xml'
                            
                            // Publish coverage
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'coverage/lcov-report',
                                reportFiles: 'index.html',
                                reportName: 'Coverage Report'
                            ])
                        }
                    }
                }

                stage('Security Scan') {
                    steps {
                        container('trivy') {
                            sh '''
                                echo "Running security scan..."
                                trivy fs --severity HIGH,CRITICAL --exit-code 1 .
                            '''
                        }
                        
                        container('node') {
                            sh '''
                                echo "Running npm audit..."
                                npm audit --production --audit-level=moderate
                            '''
                        }
                    }
                }

                stage('SonarQube Analysis') {
                    when {
                        branch 'main'
                    }
                    steps {
                        container('node') {
                            withSonarQubeEnv('sonarqube') {
                                sh '''
                                    npm run sonar-scanner \
                                        -Dsonar.projectKey=${JOB_NAME} \
                                        -Dsonar.projectVersion=${VERSION} \
                                        -Dsonar.sources=src \
                                        -Dsonar.tests=tests \
                                        -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info
                                '''
                            }
                        }
                    }
                }
            }
        }

        stage('Quality Gate Check') {
            when {
                branch 'main'
            }
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build') {
            steps {
                container('node') {
                    sh '''
                        echo "Building application..."
                        npm run build
                        
                        # Create artifacts
                        tar -czf dist.tar.gz dist/
                    '''
                    
                    // Archive artifacts
                    archiveArtifacts artifacts: 'dist.tar.gz', fingerprint: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                container('docker') {
                    script {
                        docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-credentials') {
                            def customImage = docker.build("${IMAGE_NAME}:${VERSION}", 
                                "--build-arg VERSION=${VERSION} " +
                                "--build-arg BUILD_DATE=${sh(returnStdout: true, script: 'date -u +"%Y-%m-%dT%H:%M:%SZ"').trim()} " +
                                "--build-arg VCS_REF=${GIT_COMMIT} " +
                                "--label org.opencontainers.image.source=${GIT_URL} " +
                                "--cache-from ${IMAGE_NAME}:cache-${GIT_BRANCH} " +
                                ".")
                            
                            // Push with multiple tags
                            customImage.push()
                            customImage.push('latest')
                            customImage.push("${GIT_BRANCH}-latest")
                            
                            // Push cache layer
                            sh "docker tag ${IMAGE_NAME}:${VERSION} ${IMAGE_NAME}:cache-${GIT_BRANCH}"
                            sh "docker push ${IMAGE_NAME}:cache-${GIT_BRANCH}"
                        }
                    }
                }
            }
        }

        stage('Integration Tests') {
            steps {
                container('docker') {
                    sh '''
                        # Start test environment
                        docker-compose -f docker-compose.test.yml up -d
                        
                        # Wait for services
                        sleep 30
                        
                        # Run integration tests
                        docker-compose -f docker-compose.test.yml run --rm tests npm run test:integration
                    '''
                }
            }
            post {
                always {
                    container('docker') {
                        sh 'docker-compose -f docker-compose.test.yml down -v'
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                    tag pattern: "v\\d+\\.\\d+\\.\\d+", comparator: "REGEXP"
                }
            }
            steps {
                script {
                    def deployEnv = ""
                    def deployNamespace = ""
                    
                    if (env.BRANCH_NAME == 'develop') {
                        deployEnv = 'staging'
                        deployNamespace = 'staging'
                    } else if (env.BRANCH_NAME == 'main' || env.TAG_NAME) {
                        deployEnv = 'production'
                        deployNamespace = 'production'
                    }
                    
                    container('kubectl') {
                        withCredentials([file(credentialsId: "kubeconfig-${deployEnv}", variable: 'KUBECONFIG')]) {
                            sh """
                                # Update deployment
                                kubectl set image deployment/myapp myapp=${IMAGE_NAME}:${VERSION} -n ${deployNamespace}
                                
                                # Wait for rollout
                                kubectl rollout status deployment/myapp -n ${deployNamespace} --timeout=10m
                                
                                # Verify deployment
                                kubectl get pods -n ${deployNamespace} -l app=myapp
                            """
                        }
                    }
                }
            }
        }

        stage('Smoke Tests') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                container('node') {
                    script {
                        def testUrl = ""
                        if (env.BRANCH_NAME == 'develop') {
                            testUrl = 'https://staging.example.com'
                        } else if (env.BRANCH_NAME == 'main') {
                            testUrl = 'https://example.com'
                        }
                        
                        if (testUrl) {
                            sh "npm run test:smoke -- --url ${testUrl}"
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean workspace
            cleanWs()
        }
        success {
            script {
                if (env.BRANCH_NAME == 'main' || env.TAG_NAME) {
                    // Send success notification
                    slackSend(
                        color: 'good',
                        message: "Deployment successful: ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
                    )
                }
            }
        }
        failure {
            // Send failure notification
            slackSend(
                color: 'danger',
                message: "Build failed: ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
            )
        }
        unstable {
            // Send unstable notification
            slackSend(
                color: 'warning',
                message: "Build unstable: ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
            )
        }
    }
}

// Shared library functions
def getVersion() {
    def version = sh(
        script: "git describe --tags --always --dirty",
        returnStdout: true
    ).trim()
    return version
}

def deployToKubernetes(environment, namespace, image) {
    sh """
        helm upgrade --install myapp ./charts/myapp \
            --namespace ${namespace} \
            --set image.repository=${image.split(':')[0]} \
            --set image.tag=${image.split(':')[1]} \
            --set environment=${environment} \
            --wait \
            --timeout 10m
    """
}
```

### Jenkins Best Practices

1. **Use Shared Libraries**

```groovy
// vars/standardPipeline.groovy
def call(Map config) {
    pipeline {
        agent any
        
        stages {
            stage('Build') {
                steps {
                    script {
                        buildApp(config)
                    }
                }
            }
            
            stage('Test') {
                steps {
                    script {
                        testApp(config)
                    }
                }
            }
            
            stage('Deploy') {
                when {
                    expression { config.deploy == true }
                }
                steps {
                    script {
                        deployApp(config)
                    }
                }
            }
        }
    }
}
```

2. **Implement Blue Ocean Compatible Pipelines**

```groovy
pipeline {
    agent any
    
    stages {
        stage('Parallel Tests') {
            parallel {
                stage('Chrome Tests') {
                    steps {
                        sh 'npm run test:chrome'
                    }
                }
                stage('Firefox Tests') {
                    steps {
                        sh 'npm run test:firefox'
                    }
                }
                stage('Safari Tests') {
                    steps {
                        sh 'npm run test:safari'
                    }
                }
            }
        }
    }
}
```

## CircleCI

### Complete Template

```yaml
# .circleci/config.yml
version: 2.1

# Orbs provide reusable commands and jobs
orbs:
  node: circleci/node@5.1.0
  docker: circleci/docker@2.2.0
  aws-ecr: circleci/aws-ecr@8.2.1
  slack: circleci/slack@4.12.1
  codecov: codecov/codecov@3.2.4

# Reusable executors
executors:
  node-executor:
    docker:
      - image: cimg/node:20.10
    working_directory: ~/repo
    resource_class: large
    environment:
      NODE_ENV: test
      NODE_OPTIONS: --max-old-space-size=4096

  docker-executor:
    docker:
      - image: cimg/base:stable
    working_directory: ~/repo
    resource_class: medium

# Reusable commands
commands:
  restore_deps:
    description: "Restore cached dependencies"
    steps:
      - restore_cache:
          keys:
            - v2-deps-{{ .Branch }}-{{ checksum "package-lock.json" }}
            - v2-deps-{{ .Branch }}-
            - v2-deps-

  save_deps:
    description: "Save dependencies to cache"
    steps:
      - save_cache:
          key: v2-deps-{{ .Branch }}-{{ checksum "package-lock.json" }}
          paths:
            - node_modules
            - ~/.npm
            - ~/.cache

  setup_test_results:
    description: "Setup test result directories"
    steps:
      - run:
          name: Create test result directories
          command: |
            mkdir -p test-results/jest
            mkdir -p test-results/cypress
            mkdir -p coverage

# Jobs
jobs:
  # Install and cache dependencies
  install:
    executor: node-executor
    steps:
      - checkout
      - restore_deps
      - run:
          name: Install dependencies
          command: |
            npm ci --prefer-offline --no-audit
            npm ls || true
      - save_deps
      - persist_to_workspace:
          root: ~/repo
          paths:
            - node_modules
            - .

  # Run linting and static analysis
  lint:
    executor: node-executor
    steps:
      - attach_workspace:
          at: ~/repo
      - run:
          name: Run ESLint
          command: |
            npm run lint:js -- --format junit --output-file test-results/jest/eslint.xml
      - run:
          name: Run Prettier check
          command: npm run lint:format
      - run:
          name: Run TypeScript check
          command: npm run type-check
      - store_test_results:
          path: test-results

  # Run unit tests with coverage
  test-unit:
    executor: node-executor
    parallelism: 4
    steps:
      - attach_workspace:
          at: ~/repo
      - setup_test_results
      - run:
          name: Run unit tests
          command: |
            TESTFILES=$(circleci tests glob "src/**/*.test.{js,ts}" | circleci tests split --split-by=timings)
            npm run test:unit -- \
              --ci \
              --coverage \
              --coverageDirectory=coverage/unit-$CIRCLE_NODE_INDEX \
              --maxWorkers=2 \
              --reporters=default \
              --reporters=jest-junit \
              --testPathPattern="$TESTFILES"
          environment:
            JEST_JUNIT_OUTPUT_DIR: test-results/jest
            JEST_JUNIT_OUTPUT_NAME: unit-results.xml
      - store_test_results:
          path: test-results
      - store_artifacts:
          path: coverage
      - persist_to_workspace:
          root: ~/repo
          paths:
            - coverage/unit-*

  # Run integration tests
  test-integration:
    executor: node-executor
    docker:
      - image: cimg/node:20.10
      - image: cimg/postgres:15.1
        environment:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
      - image: cimg/redis:7.0
    steps:
      - attach_workspace:
          at: ~/repo
      - setup_test_results
      - run:
          name: Wait for services
          command: |
            dockerize -wait tcp://localhost:5432 -wait tcp://localhost:6379 -timeout 1m
      - run:
          name: Run integration tests
          command: |
            npm run test:integration -- \
              --ci \
              --coverage \
              --coverageDirectory=coverage/integration \
              --reporters=default \
              --reporters=jest-junit
          environment:
            DATABASE_URL: postgresql://test:test@localhost:5432/test_db
            REDIS_URL: redis://localhost:6379
            JEST_JUNIT_OUTPUT_DIR: test-results/jest
            JEST_JUNIT_OUTPUT_NAME: integration-results.xml
      - store_test_results:
          path: test-results
      - store_artifacts:
          path: coverage
      - persist_to_workspace:
          root: ~/repo
          paths:
            - coverage/integration

  # Run E2E tests
  test-e2e:
    docker:
      - image: cypress/browsers:node18.12.0-chrome107
    working_directory: ~/repo
    parallelism: 2
    steps:
      - attach_workspace:
          at: ~/repo
      - run:
          name: Run E2E tests
          command: |
            TESTFILES=$(circleci tests glob "cypress/e2e/**/*.cy.{js,ts}" | circleci tests split)
            npm run test:e2e -- \
              --spec "$TESTFILES" \
              --record \
              --parallel \
              --ci-build-id $CIRCLE_SHA1 \
              --group "CircleCI-$CIRCLE_NODE_INDEX"
          environment:
            CYPRESS_RECORD_KEY: $CYPRESS_RECORD_KEY
      - store_test_results:
          path: test-results
      - store_artifacts:
          path: cypress/screenshots
      - store_artifacts:
          path: cypress/videos

  # Merge coverage reports
  coverage:
    executor: node-executor
    steps:
      - attach_workspace:
          at: ~/repo
      - run:
          name: Merge coverage reports
          command: |
            npm run coverage:merge
            npm run coverage:report
      - codecov/upload:
          file: coverage/lcov.info
      - store_artifacts:
          path: coverage

  # Security scanning
  security-scan:
    executor: node-executor
    steps:
      - attach_workspace:
          at: ~/repo
      - run:
          name: Run npm audit
          command: |
            npm audit --production --audit-level=moderate || true
            npm audit --production --json > audit-report.json || true
      - run:
          name: Run Snyk scan
          command: |
            npm install -g snyk
            snyk auth $SNYK_TOKEN
            snyk test --severity-threshold=high
            snyk monitor
      - store_artifacts:
          path: audit-report.json

  # Build application
  build:
    executor: node-executor
    steps:
      - attach_workspace:
          at: ~/repo
      - run:
          name: Build application
          command: |
            npm run build
            tar -czf dist.tar.gz dist/
      - store_artifacts:
          path: dist.tar.gz
      - persist_to_workspace:
          root: ~/repo
          paths:
            - dist
            - dist.tar.gz

  # Build and push Docker image
  docker-build:
    executor: docker-executor
    steps:
      - attach_workspace:
          at: ~/repo
      - setup_remote_docker:
          version: 20.10.14
          docker_layer_caching: true
      - run:
          name: Build Docker image
          command: |
            docker build \
              --build-arg VERSION=$CIRCLE_SHA1 \
              --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
              --build-arg VCS_REF=$CIRCLE_SHA1 \
              --tag myapp:$CIRCLE_SHA1 \
              --tag myapp:latest \
              .
      - run:
          name: Run Trivy scan
          command: |
            docker run --rm \
              -v /var/run/docker.sock:/var/run/docker.sock \
              -v $HOME/.cache/trivy:/root/.cache/trivy \
              aquasec/trivy:latest \
              image --exit-code 1 --severity HIGH,CRITICAL myapp:$CIRCLE_SHA1
      - aws-ecr/build-and-push-image:
          repo: myapp
          tag: $CIRCLE_SHA1,latest,$CIRCLE_BRANCH
          extra-build-args: |
            --cache-from=myapp:latest

  # Deploy to staging
  deploy-staging:
    executor: node-executor
    steps:
      - attach_workspace:
          at: ~/repo
      - run:
          name: Install AWS CLI
          command: |
            curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
            unzip awscliv2.zip
            sudo ./aws/install
      - run:
          name: Deploy to ECS Staging
          command: |
            aws ecs update-service \
              --cluster staging-cluster \
              --service myapp-staging \
              --force-new-deployment \
              --region us-east-1
      - run:
          name: Wait for deployment
          command: |
            aws ecs wait services-stable \
              --cluster staging-cluster \
              --services myapp-staging \
              --region us-east-1
      - slack/notify:
          event: pass
          template: basic_success_1
          mentions: '@oncall'

  # Deploy to production
  deploy-production:
    executor: node-executor
    steps:
      - attach_workspace:
          at: ~/repo
      - run:
          name: Install deployment tools
          command: |
            curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
            sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
            curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
      - run:
          name: Deploy to Kubernetes
          command: |
            echo "$KUBE_CONFIG" | base64 -d > kubeconfig
            export KUBECONFIG=kubeconfig
            
            helm upgrade --install myapp ./charts/myapp \
              --namespace production \
              --set image.tag=$CIRCLE_SHA1 \
              --set replicaCount=3 \
              --wait \
              --timeout 10m
      - run:
          name: Run smoke tests
          command: |
            npm run test:smoke -- --url https://example.com
      - slack/notify:
          event: pass
          template: basic_success_1
          mentions: '@channel'

# Workflows
workflows:
  version: 2
  
  # Main CI/CD workflow
  build-test-deploy:
    jobs:
      - install:
          filters:
            tags:
              only: /.*/

      - lint:
          requires:
            - install
          filters:
            tags:
              only: /.*/

      - test-unit:
          requires:
            - install
          filters:
            tags:
              only: /.*/

      - test-integration:
          requires:
            - install
          filters:
            tags:
              only: /.*/

      - test-e2e:
          requires:
            - install
          filters:
            tags:
              only: /.*/

      - coverage:
          requires:
            - test-unit
            - test-integration
          filters:
            tags:
              only: /.*/

      - security-scan:
          requires:
            - install
          filters:
            tags:
              only: /.*/

      - build:
          requires:
            - lint
            - test-unit
            - test-integration
          filters:
            tags:
              only: /.*/

      - docker-build:
          requires:
            - build
          filters:
            branches:
              only:
                - main
                - develop
            tags:
              only: /^v.*/

      - deploy-staging:
          requires:
            - docker-build
          filters:
            branches:
              only: develop

      - hold-production:
          type: approval
          requires:
            - docker-build
            - test-e2e
            - security-scan
          filters:
            branches:
              only: main
            tags:
              only: /^v.*/

      - deploy-production:
          requires:
            - hold-production
          filters:
            branches:
              only: main
            tags:
              only: /^v.*/

  # Nightly security scan
  nightly-security:
    triggers:
      - schedule:
          cron: "0 2 * * *"
          filters:
            branches:
              only:
                - main
    jobs:
      - install
      - security-scan:
          requires:
            - install

  # Weekly dependency update check
  weekly-updates:
    triggers:
      - schedule:
          cron: "0 9 * * 1"
          filters:
            branches:
              only:
                - main
    jobs:
      - install
      - update-dependencies:
          requires:
            - install

# Additional job for dependency updates
jobs:
  update-dependencies:
    executor: node-executor
    steps:
      - attach_workspace:
          at: ~/repo
      - run:
          name: Check for updates
          command: |
            npm outdated || true
            npm update
            npm audit fix
      - run:
          name: Create PR if changes
          command: |
            if [[ `git status --porcelain` ]]; then
              git config user.name "CircleCI Bot"
              git config user.email "bot@circleci.com"
              git checkout -b update-dependencies-$CIRCLE_BUILD_NUM
              git add .
              git commit -m "chore: update dependencies [skip ci]"
              git push origin update-dependencies-$CIRCLE_BUILD_NUM
              
              # Create PR using GitHub API
              curl -X POST \
                -H "Authorization: token $GITHUB_TOKEN" \
                -H "Accept: application/vnd.github.v3+json" \
                https://api.github.com/repos/$CIRCLE_PROJECT_USERNAME/$CIRCLE_PROJECT_REPONAME/pulls \
                -d '{
                  "title": "chore: update dependencies",
                  "body": "Automated dependency update from CircleCI",
                  "head": "update-dependencies-'$CIRCLE_BUILD_NUM'",
                  "base": "main"
                }'
            fi
```

### CircleCI Best Practices

1. **Optimize with Workspaces and Caching**

```yaml
# Efficient caching strategy
version: 2.1

jobs:
  setup:
    steps:
      - checkout
      
      # Multiple cache keys for fallback
      - restore_cache:
          keys:
            - v3-{{ .Environment.CIRCLE_JOB }}-{{ arch }}-{{ checksum "package-lock.json" }}
            - v3-{{ .Environment.CIRCLE_JOB }}-{{ arch }}-
            - v3-{{ .Environment.CIRCLE_JOB }}-
      
      - run: npm ci
      
      - save_cache:
          key: v3-{{ .Environment.CIRCLE_JOB }}-{{ arch }}-{{ checksum "package-lock.json" }}
          paths:
            - ~/.npm
            - node_modules
      
      # Persist for downstream jobs
      - persist_to_workspace:
          root: .
          paths:
            - .
```

2. **Use Matrix Jobs for Comprehensive Testing**

```yaml
jobs:
  test:
    parameters:
      node-version:
        type: string
      os:
        type: string
    docker:
      - image: cimg/node:<< parameters.node-version >>
    steps:
      - checkout
      - run: npm test

workflows:
  test-matrix:
    jobs:
      - test:
          matrix:
            parameters:
              node-version: ["16.20", "18.18", "20.10"]
              os: ["linux", "macos", "windows"]
```

## Secret Management Best Practices

### 1. Never Hardcode Secrets

```yaml
# BAD - Never do this
env:
  API_KEY: "sk-1234567890abcdef"

# GOOD - Use secret management
env:
  API_KEY: ${{ secrets.API_KEY }}
```

### 2. Use Least Privilege Principle

```yaml
# GitHub Actions - Minimal permissions
permissions:
  contents: read
  issues: write
  pull-requests: write
```

### 3. Rotate Secrets Regularly

```yaml
# Implement secret rotation
- name: Rotate credentials
  run: |
    # Generate new credentials
    NEW_KEY=$(openssl rand -hex 32)
    
    # Update in secret manager
    aws secretsmanager update-secret \
      --secret-id prod/api-key \
      --secret-string "$NEW_KEY"
    
    # Update in CI/CD platform
    gh secret set API_KEY --body "$NEW_KEY"
```

## Caching Strategies

### 1. Multi-Level Caching

```yaml
# Language-specific dependency caching
- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

# Build artifact caching
- name: Cache build artifacts
  uses: actions/cache@v3
  with:
    path: |
      dist/
      .next/cache
    key: ${{ runner.os }}-build-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-build-

# Docker layer caching
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v2
  with:
    driver-opts: |
      image=moby/buildkit:master
      network=host

- name: Build with cache
  uses: docker/build-push-action@v4
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### 2. Intelligent Cache Invalidation

```yaml
# Use multiple cache keys for granular control
- name: Cache with fallback
  uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ env.NODE_VERSION }}-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-${{ env.NODE_VERSION }}-
      ${{ runner.os }}-node-
```

## Docker Integration

### Multi-Stage Build Example

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Development dependencies for building
COPY . .
RUN npm ci && npm run build

# Production stage
FROM node:20-alpine AS production
WORKDIR /app

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy built application
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package*.json ./

USER nodejs
EXPOSE 3000

ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/index.js"]
```

### CI/CD Docker Build

```yaml
# Efficient Docker builds in CI/CD
- name: Build and push Docker image
  uses: docker/build-push-action@v4
  with:
    context: .
    platforms: linux/amd64,linux/arm64
    target: production
    build-args: |
      VERSION=${{ github.sha }}
      BUILD_DATE=${{ steps.date.outputs.date }}
    tags: |
      myapp:${{ github.sha }}
      myapp:${{ github.ref_name }}
      myapp:latest
    cache-from: |
      type=gha
      type=registry,ref=myapp:buildcache
    cache-to: |
      type=gha,mode=max
      type=registry,ref=myapp:buildcache,mode=max
```

## Nix Integration

### Nix in CI/CD

```yaml
# GitHub Actions with Nix
- uses: cachix/install-nix-action@v22
  with:
    nix_path: nixpkgs=channel:nixos-unstable

- uses: cachix/cachix-action@v12
  with:
    name: myproject
    authToken: '${{ secrets.CACHIX_AUTH_TOKEN }}'

- run: nix build
- run: nix flake check
```

### Reproducible Builds

```nix
# flake.nix for CI/CD
{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  
  outputs = { self, nixpkgs }: {
    packages.x86_64-linux.default = nixpkgs.legacyPackages.x86_64-linux.mkDerivation {
      pname = "myapp";
      version = "1.0.0";
      src = ./.;
      
      buildPhase = ''
        npm ci
        npm run build
      '';
      
      installPhase = ''
        mkdir -p $out
        cp -r dist/* $out/
      '';
    };
    
    devShells.x86_64-linux.default = nixpkgs.legacyPackages.x86_64-linux.mkShell {
      packages = with nixpkgs.legacyPackages.x86_64-linux; [
        nodejs_20
        nodePackages.npm
      ];
    };
  };
}
```

## Environment-Specific Configurations

### Development Environment

```yaml
deploy-dev:
  environment:
    name: development
    url: https://dev.example.com
  variables:
    NODE_ENV: development
    LOG_LEVEL: debug
    ENABLE_DEBUG: "true"
  script:
    - npm run deploy:dev
```

### Staging Environment

```yaml
deploy-staging:
  environment:
    name: staging
    url: https://staging.example.com
  variables:
    NODE_ENV: staging
    LOG_LEVEL: info
    ENABLE_MONITORING: "true"
  script:
    - npm run deploy:staging
    - npm run test:smoke
```

### Production Environment

```yaml
deploy-production:
  environment:
    name: production
    url: https://example.com
  variables:
    NODE_ENV: production
    LOG_LEVEL: warn
    ENABLE_MONITORING: "true"
    ENABLE_APM: "true"
  script:
    - npm run deploy:production
    - npm run test:smoke
    - npm run test:performance
```

## Attestation and Verification

### Supply Chain Security

```yaml
# Generate SBOM and sign artifacts
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    format: spdx-json
    artifact-name: sbom

- name: Attest Build Provenance
  uses: actions/attest-build-provenance@v1
  with:
    subject-path: ./dist/**/*.js

- name: Sign with Sigstore
  run: |
    cosign sign-blob \
      --output-signature artifact.sig \
      --output-certificate artifact.crt \
      artifact.tar.gz
```

### Verification in Deployment

```yaml
- name: Verify artifact signature
  run: |
    cosign verify-blob \
      --signature artifact.sig \
      --certificate artifact.crt \
      --certificate-oidc-issuer https://token.actions.githubusercontent.com \
      --certificate-identity-regexp "https://github.com/${{ github.repository }}/.github/workflows/" \
      artifact.tar.gz
```

## Monitoring and Alerting

### Pipeline Metrics

```yaml
# Send metrics to monitoring system
- name: Report pipeline metrics
  if: always()
  run: |
    curl -X POST $METRICS_ENDPOINT \
      -H "Content-Type: application/json" \
      -d '{
        "pipeline": "${{ github.workflow }}",
        "status": "${{ job.status }}",
        "duration": "${{ steps.timer.outputs.duration }}",
        "branch": "${{ github.ref }}",
        "commit": "${{ github.sha }}"
      }'
```

## Conclusion

This guide provides comprehensive CI/CD configurations for major platforms. Key takeaways:

1. **Start Simple**: Begin with basic pipelines and add complexity as needed
2. **Prioritize Speed**: Use caching, parallelization, and efficient workflows
3. **Ensure Security**: Implement scanning, secret management, and attestation
4. **Monitor Everything**: Track metrics, failures, and performance
5. **Document Pipelines**: Your CI/CD configuration is documentation

Remember: The best CI/CD pipeline is one that catches issues early, provides fast feedback, and doesn't get in the way of development.