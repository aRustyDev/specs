# Development Environment Setup Guide

## Overview
This guide helps you choose between Docker and Nix for your development environment and provides detailed templates for both. The choice impacts team collaboration, reproducibility, and development workflow.

## Decision Framework: Docker vs Nix

### Quick Decision Matrix

| Factor | Docker | Nix |
|--------|--------|-----|
| **Team Familiarity** | Most developers know it | Steeper learning curve |
| **OS Compatibility** | Works everywhere | Best on Linux/macOS |
| **Reproducibility** | Good | Excellent |
| **Build Speed** | Slower (layers) | Fast (cached) |
| **Dependency Precision** | Container-level | Package-level |
| **Dev/Prod Parity** | Excellent | Good |
| **Resource Usage** | Higher | Lower |
| **Debugging** | Can be challenging | Direct access |

### Choose Docker When:
1. **Team uses multiple operating systems** (Windows, macOS, Linux)
2. **Production runs in containers** (Kubernetes, ECS, etc.)
3. **Multiple services needed** (database, cache, queue)
4. **Team already familiar** with Docker
5. **Isolation is critical** (security, dependencies)
6. **Quick onboarding needed** for new developers

### Choose Nix When:
1. **Reproducibility is paramount** (research, critical systems)
2. **Complex dependency management** needed
3. **Team comfortable with functional paradigms**
4. **Development on Linux/macOS only**
5. **Need precise version control** of all tools
6. **Want to avoid container overhead**

## Docker Development Environment

### Basic Docker Setup

#### Step 1: Create Dockerfile.dev
```dockerfile
# Dockerfile.dev - Development container
# THINK: What base image provides the best foundation?

# For Node.js projects
FROM node:18-alpine AS base

# Install development tools
RUN apk add --no-cache \
    git \
    curl \
    bash \
    make \
    g++ \
    python3

WORKDIR /workspace

# For better caching, copy dependency files first
COPY package*.json ./
RUN npm ci

# Install dev dependencies
COPY package*.json ./
RUN npm ci --include=dev

# Copy source code
COPY . .

# Expose common development ports
EXPOSE 3000 4000 5000 8080

# Development command
CMD ["npm", "run", "dev"]
```

#### Step 2: Create docker-compose.yaml
```yaml
# docker-compose.yaml - Orchestrate development services
version: '3.8'

services:
  # Main application
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      # Mount source code for hot reloading
      - .:/workspace
      # Prevent node_modules from being overwritten
      - /workspace/node_modules
    ports:
      - "3000:3000"    # App port
      - "9229:9229"    # Debug port
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://user:pass@db:5432/devdb
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    # Keep container running
    stdin_open: true
    tty: true

  # PostgreSQL database
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: devdb
    volumes:
      # Persist database data
      - postgres_data:/var/lib/postgresql/data
      # Initialize scripts
      - ./scripts/db:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"

  # Redis cache
  cache:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  # Development tools container
  tools:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/workspace
    command: tail -f /dev/null
    profiles:
      - tools

volumes:
  postgres_data:
  redis_data:
```

#### Step 3: Create .dockerignore
```
# .dockerignore - Optimize build context
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.env.*
.vscode
.idea
coverage
.nyc_output
dist
build
*.log
.DS_Store
*.swp
*.swo
.claude/logs
```

#### Step 4: Development Scripts
Create `scripts/docker/dev.sh`:
```bash
#!/bin/bash
# Development helper script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Starting development environment...${NC}"

# Ensure docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Build images if needed
echo -e "${YELLOW}Building images...${NC}"
docker-compose build

# Start services
echo -e "${YELLOW}Starting services...${NC}"
docker-compose up -d

# Wait for database
echo -e "${YELLOW}Waiting for database...${NC}"
docker-compose exec -T db pg_isready --timeout=30

# Run migrations
echo -e "${YELLOW}Running migrations...${NC}"
docker-compose exec -T app npm run migrate

# Show status
echo -e "${GREEN}Environment ready!${NC}"
docker-compose ps

# Show logs
echo -e "${YELLOW}Following application logs (Ctrl+C to exit)...${NC}"
docker-compose logs -f app
```

### Advanced Docker Patterns

#### Multi-stage Production Build
```dockerfile
# Dockerfile - Production multi-stage build
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runtime
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY --from=build /app/package*.json ./
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

#### Development with Hot Reloading
```yaml
# docker-compose.override.yaml - Development overrides
version: '3.8'

services:
  app:
    volumes:
      # Mount source for hot reloading
      - ./src:/workspace/src
      - ./tests:/workspace/tests
      - ./configs:/workspace/configs
    environment:
      - CHOKIDAR_USEPOLLING=true  # For file watching
      - WATCHPACK_POLLING=true
    command: npm run dev:watch
```

## Nix Development Environment

### Basic Nix Setup

#### Step 1: Create flake.nix
```nix
{
  description = "Development environment for [project-name]";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        # Define Node.js version
        nodejs = pkgs.nodejs_18;
        
        # Custom packages
        projectPackages = with pkgs; [
          nodejs
          nodejs.pkgs.npm
          nodejs.pkgs.yarn
          nodejs.pkgs.pnpm
          
          # Development tools
          git
          gnumake
          jq
          ripgrep
          bat
          httpie
          
          # Database tools
          postgresql_15
          redis
          
          # Code quality
          pre-commit
          shellcheck
          hadolint
        ];
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = projectPackages;
          
          shellHook = ''
            echo "🚀 Development environment loaded!"
            echo "Node.js: $(node --version)"
            echo "npm: $(npm --version)"
            
            # Set up project-specific environment
            export PROJECT_ROOT=$PWD
            export NODE_ENV=development
            
            # Initialize git hooks
            if [ -f .pre-commit-config.yaml ]; then
              pre-commit install
            fi
            
            # Create local development directories
            mkdir -p .local/{db,redis,logs}
            
            # PostgreSQL setup
            export PGDATA=$PROJECT_ROOT/.local/db
            export PGHOST=$PROJECT_ROOT/.local
            export PGPORT=5432
            export DATABASE_URL="postgresql://localhost:$PGPORT/devdb"
            
            # Redis setup
            export REDIS_DIR=$PROJECT_ROOT/.local/redis
            export REDIS_PORT=6379
            export REDIS_URL="redis://localhost:$REDIS_PORT"
            
            # Start services function
            start_services() {
              echo "Starting PostgreSQL..."
              pg_ctl start -l .local/logs/postgres.log
              
              echo "Starting Redis..."
              redis-server --daemonize yes \
                --dir $REDIS_DIR \
                --port $REDIS_PORT \
                --logfile .local/logs/redis.log
            }
            
            # Stop services function
            stop_services() {
              echo "Stopping services..."
              pg_ctl stop 2>/dev/null || true
              redis-cli -p $REDIS_PORT shutdown 2>/dev/null || true
            }
            
            # Initialize database if needed
            if [ ! -d "$PGDATA" ]; then
              echo "Initializing PostgreSQL..."
              initdb --auth=trust --username=postgres
              start_services
              createdb -U postgres devdb
            fi
            
            echo ""
            echo "Available commands:"
            echo "  start_services - Start PostgreSQL and Redis"
            echo "  stop_services  - Stop all services"
            echo ""
          '';
        };
        
        # Additional development shells
        devShells.minimal = pkgs.mkShell {
          buildInputs = with pkgs; [
            nodejs
            git
          ];
        };
        
        devShells.full = pkgs.mkShell {
          buildInputs = projectPackages ++ (with pkgs; [
            # Additional tools for full environment
            docker
            docker-compose
            kubectl
            terraform
            awscli2
          ]);
        };
      });
}
```

#### Step 2: Create .envrc (for direnv)
```bash
# .envrc - Automatic environment loading
use flake

# Project-specific environment variables
export PROJECT_NAME="my-project"
export LOG_LEVEL="debug"

# Load local env file if exists
if [ -f .env.local ]; then
  source .env.local
fi

# Custom project functions
function project_status() {
  echo "Project: $PROJECT_NAME"
  echo "Node: $(node --version)"
  echo "Services:"
  pg_ctl status || echo "  PostgreSQL: stopped"
  redis-cli ping && echo "  Redis: running" || echo "  Redis: stopped"
}

# Auto-start services
if [ -z "$SKIP_SERVICE_START" ]; then
  start_services
fi
```

#### Step 3: Language-Specific Configurations

**For Python Projects**:
```nix
let
  python = pkgs.python311;
  pythonPackages = python.withPackages (ps: with ps; [
    pip
    setuptools
    wheel
    pytest
    black
    flake8
    mypy
    ipython
  ]);
in
{
  devShells.default = pkgs.mkShell {
    buildInputs = [ pythonPackages ] ++ projectPackages;
    
    shellHook = ''
      # Create virtual environment
      if [ ! -d .venv ]; then
        echo "Creating virtual environment..."
        python -m venv .venv
      fi
      source .venv/bin/activate
      
      # Install dependencies
      if [ -f requirements.txt ]; then
        pip install -r requirements.txt
      fi
      if [ -f requirements-dev.txt ]; then
        pip install -r requirements-dev.txt
      fi
    '';
  };
}
```

**For Go Projects**:
```nix
{
  devShells.default = pkgs.mkShell {
    buildInputs = with pkgs; [
      go_1_21
      gopls
      golangci-lint
      delve
      go-tools
    ] ++ projectPackages;
    
    shellHook = ''
      export GOPATH=$PROJECT_ROOT/.local/go
      export PATH=$GOPATH/bin:$PATH
      
      # Download dependencies
      if [ -f go.mod ]; then
        go mod download
      fi
    '';
  };
}
```

### Advanced Nix Patterns

#### Custom Derivations
```nix
let
  # Custom tool build
  myTool = pkgs.stdenv.mkDerivation {
    pname = "my-project-tool";
    version = "1.0.0";
    src = ./tools/my-tool;
    
    buildInputs = [ pkgs.python3 ];
    
    installPhase = ''
      mkdir -p $out/bin
      cp my-tool.py $out/bin/my-tool
      chmod +x $out/bin/my-tool
    '';
  };
in
{
  devShells.default = pkgs.mkShell {
    buildInputs = [ myTool ] ++ projectPackages;
  };
}
```

## Comparison Examples

### Database Setup

**Docker Approach**:
```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
```

**Nix Approach**:
```nix
shellHook = ''
  initdb --auth=trust
  pg_ctl start
  createdb myapp
  psql myapp < init.sql
'';
```

### Tool Installation

**Docker Approach**:
```dockerfile
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    vim
```

**Nix Approach**:
```nix
buildInputs = with pkgs; [
  gcc
  gnumake
  curl
  vim
];
```

## Best Practices

### For Docker

1. **Layer Caching**:
   ```dockerfile
   # Good - dependencies cached separately
   COPY package*.json ./
   RUN npm ci
   COPY . .
   
   # Bad - rebuilds on any change
   COPY . .
   RUN npm ci
   ```

2. **Security**:
   ```dockerfile
   # Run as non-root user
   RUN addgroup -g 1001 -S nodejs
   RUN adduser -S nodejs -u 1001
   USER nodejs
   ```

3. **Multi-stage Builds**:
   - Separate build and runtime
   - Minimize final image size
   - Don't include build tools in production

### For Nix

1. **Pinning**:
   ```nix
   inputs.nixpkgs.url = "github:NixOS/nixpkgs/abc123def456";
   ```

2. **Garbage Collection**:
   ```bash
   # Clean old generations
   nix-collect-garbage -d
   ```

3. **Sharing Environments**:
   ```bash
   # Generate lock file
   nix flake lock
   # Commit flake.lock to version control
   ```

## Troubleshooting

### Docker Issues

**Problem**: "Cannot connect to Docker daemon"
```bash
# Solution: Ensure Docker is running
sudo systemctl start docker  # Linux
open -a Docker  # macOS
```

**Problem**: "Port already in use"
```bash
# Find process using port
lsof -i :3000
# Or change port in docker-compose.yaml
```

**Problem**: "File changes not detected"
```yaml
# Enable polling for file systems that don't support inotify
environment:
  - CHOKIDAR_USEPOLLING=true
```

### Nix Issues

**Problem**: "Command not found after entering shell"
```nix
# Ensure package is in buildInputs
buildInputs = with pkgs; [
  # Add missing package here
];
```

**Problem**: "Flake commands not available"
```bash
# Enable flakes
mkdir -p ~/.config/nix
echo "experimental-features = nix-command flakes" >> ~/.config/nix/nix.conf
```

## Integration with IDEs

### VS Code with Docker
`.devcontainer/devcontainer.json`:
```json
{
  "name": "Project Dev Container",
  "dockerComposeFile": "../docker-compose.yaml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "extensions": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode"
  ]
}
```

### VS Code with Nix
`.vscode/settings.json`:
```json
{
  "nix.enableLanguageServer": true,
  "nix.serverPath": "nil",
  "terminal.integrated.profiles.linux": {
    "nix-shell": {
      "path": "nix-shell",
      "args": []
    }
  }
}
```

## Decision Documentation Template

Create `.claude/logs/setup/environment-decision.md`:
```markdown
# Development Environment Decision

## Decision: [Docker/Nix]

## Date: [YYYY-MM-DD]

## Factors Considered

### Team Factors
- Current expertise: 
- Learning capacity: 
- Time constraints: 

### Technical Factors
- OS diversity: 
- Production environment: 
- Dependency complexity: 

### Project Factors
- Expected lifetime: 
- Team size: 
- Deployment targets: 

## Rationale
[Detailed explanation of why this choice was made]

## Risks and Mitigations
1. Risk: [Description]
   Mitigation: [How to address]

## Review Date: [3 months from decision]
```

## Remember

**Think Long and Hard** about your choice. Consider:
- Who will maintain this?
- What are the team's skills?
- What does production look like?
- How complex are the dependencies?

**Ask Questions** if unclear about:
- Team preferences
- Production requirements
- Tooling constraints
- Performance needs

**Document Everything** about your setup:
- Why you chose this approach
- Any workarounds needed
- Lessons learned
- Pain points encountered

The right choice depends on your specific context. Both Docker and Nix are excellent tools when used appropriately.