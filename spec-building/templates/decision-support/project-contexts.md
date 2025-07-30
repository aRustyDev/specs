# Project Context Templates

## Overview
Different project types have different requirements. This framework provides context-specific requirement sets that are loaded based on project type.

## Core Requirements (Always Applied)

### Functional Requirements
- Primary use cases and user stories
- Core business logic and rules
- Data models and structures
- Key workflows and processes

### Non-Functional Requirements
- Performance targets (response time, throughput)
- Security requirements (authentication, authorization)
- Scalability needs (user count, data volume)
- Reliability targets (uptime, error rates)

### Quality Requirements
- Code quality standards
- Testing requirements (unit, integration, e2e)
- Documentation standards
- Maintenance considerations

## Context Templates

### 1. Web Application Context

**Additional Requirements:**
- Frontend framework and UI/UX requirements
- API design (REST/GraphQL/gRPC)
- State management approach
- Browser compatibility targets
- Responsive design requirements
- SEO considerations

**CI/CD Requirements:**
- Build process (bundling, minification)
- Deployment targets (cloud platforms)
- Environment management (dev/staging/prod)
- SSL/TLS certificate management
- CDN configuration
- Monitoring and alerting

**Testing Requirements:**
- Component testing
- E2E testing framework
- Visual regression testing
- Performance testing
- Accessibility testing

### 2. Library/Package Context

**Additional Requirements:**
- API design and versioning strategy
- Dependency management
- Platform compatibility (Node versions, etc.)
- Bundle size targets
- Tree-shaking support
- TypeScript definitions

**CI/CD Requirements:**
- Package registry publishing
- Version management (semantic versioning)
- Release automation
- Changelog generation
- Documentation generation

**Testing Requirements:**
- API compatibility testing
- Cross-platform testing
- Integration testing with common use cases
- Performance benchmarking

### 3. CLI Tool Context

**Additional Requirements:**
- Command structure and syntax
- Help documentation system
- Configuration file support
- Shell completion
- Cross-platform compatibility
- Error messaging and recovery

**CI/CD Requirements:**
- Binary distribution
- Installation methods (npm, homebrew, etc.)
- Auto-update mechanism
- Platform-specific builds

**Testing Requirements:**
- Command parsing testing
- Integration testing with shell environments
- Installation testing
- Upgrade path testing

### 4. Data Pipeline Context

**Additional Requirements:**
- Data source specifications
- Transformation requirements
- Data quality rules
- Schema evolution strategy
- Batch vs streaming requirements
- Error handling and recovery

**CI/CD Requirements:**
- Pipeline orchestration
- Data validation gates
- Environment data isolation
- Monitoring and alerting
- Data lineage tracking

**Testing Requirements:**
- Data quality testing
- Pipeline integration testing
- Performance testing with production-like data
- Failure scenario testing

### 5. Microservice Context

**Additional Requirements:**
- Service boundaries and responsibilities
- Inter-service communication
- Service discovery mechanism
- Circuit breaker patterns
- Event sourcing/CQRS (if applicable)
- API versioning strategy

**CI/CD Requirements:**
- Container orchestration
- Service mesh configuration
- Rolling deployment strategy
- Health check endpoints
- Distributed tracing
- Service-level monitoring

**Testing Requirements:**
- Contract testing
- Chaos engineering tests
- Load testing
- Service integration testing

### 6. Mobile Application Context

**Additional Requirements:**
- Platform targets (iOS/Android/both)
- Device compatibility matrix
- Offline functionality
- Push notification requirements
- App store requirements
- Deep linking support

**CI/CD Requirements:**
- App signing and certificates
- Beta distribution (TestFlight/Play Console)
- App store deployment
- Over-the-air updates
- Crash reporting

**Testing Requirements:**
- Device testing matrix
- UI automation testing
- Performance profiling
- Battery usage testing
- Network condition testing

## Usage Instructions

### 1. Project Type Selection
During the Discovery phase, identify the project type:
```
What type of project is this?
1. Web Application
2. Library/Package
3. CLI Tool
4. Data Pipeline
5. Microservice
6. Mobile Application
7. Other (specify)
```

### 2. Requirement Loading
Based on selection, load:
- Core requirements (always)
- Context-specific requirements
- Any custom requirements specified by user

### 3. Customization
Allow users to:
- Exclude irrelevant requirements
- Add project-specific requirements
- Modify requirement priorities

### 4. Validation
Ensure:
- No conflicting requirements
- All dependencies identified
- Feasibility confirmed

## Minimal Project Template

For projects that don't fit standard categories:

**Basic Requirements Only:**
- Core functionality definition
- Basic testing approach
- Minimal documentation
- Simple deployment method

**Optional Additions:**
- Selected requirements from other contexts
- Custom requirements as needed

## Context Switching

Projects may evolve from one type to another (e.g., CLI tool → Web service). When this happens:

1. Retain applicable requirements
2. Add new context requirements
3. Resolve any conflicts
4. Update project roadmap

## Best Practices

1. **Start Minimal**: Begin with core requirements, add context-specific ones only when confirmed needed
2. **Avoid Over-Specification**: Not every project needs every requirement
3. **Iterative Refinement**: Requirements can be added during later phases
4. **User Confirmation**: Always validate context selection with user
5. **Document Exclusions**: Explicitly note what's NOT in scope