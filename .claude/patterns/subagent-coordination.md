# Subagent Coordination Patterns

## Why Subagents Are Essential

Complex projects naturally decompose into parallel workstreams. Without proper coordination patterns, AI assistants become bottlenecks, processing tasks sequentially when they could be handled concurrently. Subagent coordination transforms linear workflows into efficient, parallel operations.

### The Coordination Challenge

Consider implementing a new feature that requires:
- Frontend components
- Backend API endpoints  
- Database migrations
- Documentation updates
- Test coverage

Without subagents, these tasks execute sequentially. With proper coordination, they progress in parallel, dramatically reducing time-to-completion.

## Principles of Effective Task Decomposition

### 1. Independence First

Tasks should be maximally independent:

```yaml
# GOOD - Independent tasks
tasks:
  - id: create-user-model
    description: "Create User database model"
    dependencies: []
    
  - id: create-auth-utilities
    description: "Create JWT token utilities"
    dependencies: []
    
  - id: design-login-ui
    description: "Design login form mockup"
    dependencies: []

# BAD - Tightly coupled tasks
tasks:
  - id: implement-complete-auth
    description: "Implement entire authentication system"
    dependencies: ["everything"]
```

### 2. Clear Interfaces

Define explicit contracts between components:

```yaml
interface_definitions:
  user_api:
    endpoints:
      - POST /api/users
      - GET /api/users/:id
      - PUT /api/users/:id
    
    request_schemas:
      create_user:
        type: object
        properties:
          email: string
          password: string
          name: string
        required: [email, password]
    
    response_schemas:
      user:
        type: object
        properties:
          id: string
          email: string
          name: string
          createdAt: datetime
```

### 3. Granular Scope

Break work into 30-90 minute chunks:

```yaml
# GOOD - Granular tasks
frontend_tasks:
  - "Create LoginForm component with validation"
  - "Create UserProfile component"
  - "Add forgot password flow"
  - "Implement remember me functionality"

# BAD - Monolithic task
frontend_tasks:
  - "Implement entire authentication UI"
```

## Patterns for Parallel Workflow Design

### Pattern 1: Feature Slice Decomposition

Split features vertically through the stack:

```yaml
feature: user_authentication
slices:
  - name: registration_flow
    agents:
      - frontend_agent:
          tasks:
            - Create registration form component
            - Add client-side validation
            - Implement email verification UI
      
      - backend_agent:
          tasks:
            - Create /api/auth/register endpoint
            - Implement email verification service
            - Add rate limiting middleware
      
      - database_agent:
          tasks:
            - Create users table migration
            - Add email_verifications table
            - Create indexes for performance
```

### Pattern 2: Layer-Based Parallelization

Organize work by architectural layers:

```yaml
project: e_commerce_platform
layers:
  presentation:
    agent: ui_specialist
    tasks:
      - Design component library
      - Create product catalog UI
      - Implement shopping cart interface
      - Build checkout flow
  
  business_logic:
    agent: backend_specialist
    tasks:
      - Implement pricing engine
      - Create inventory management
      - Build order processing pipeline
      - Add payment integration
  
  data:
    agent: database_specialist
    tasks:
      - Design schema for products
      - Create order tables
      - Implement audit logging
      - Set up read replicas
  
  infrastructure:
    agent: devops_specialist
    tasks:
      - Configure CDN for assets
      - Set up container orchestration
      - Implement monitoring
      - Create CI/CD pipelines
```

### Pattern 3: Domain-Driven Decomposition

Align subagents with business domains:

```yaml
domains:
  user_management:
    bounded_context: "Users and Authentication"
    agent: auth_specialist
    responsibilities:
      - User registration/login
      - Profile management
      - Permission system
      - Session handling
  
  product_catalog:
    bounded_context: "Product Information"
    agent: catalog_specialist
    responsibilities:
      - Product CRUD operations
      - Category management
      - Search functionality
      - Inventory tracking
  
  order_processing:
    bounded_context: "Order Lifecycle"
    agent: order_specialist
    responsibilities:
      - Cart management
      - Checkout process
      - Payment processing
      - Order fulfillment
```

### Pattern 4: Pipeline Coordination

Create processing pipelines with specialized agents:

```yaml
data_processing_pipeline:
  stages:
    - name: ingestion
      agent: data_ingestion_agent
      inputs: ["raw_data_sources"]
      outputs: ["normalized_data"]
      tasks:
        - Parse CSV files
        - Validate data format
        - Handle missing values
        - Generate ingestion report
    
    - name: transformation
      agent: etl_agent
      inputs: ["normalized_data"]
      outputs: ["transformed_data"]
      tasks:
        - Apply business rules
        - Aggregate metrics
        - Join related datasets
        - Create derived fields
    
    - name: quality_check
      agent: quality_agent
      inputs: ["transformed_data"]
      outputs: ["validated_data", "quality_report"]
      tasks:
        - Run integrity checks
        - Validate constraints
        - Check for anomalies
        - Generate quality metrics
    
    - name: loading
      agent: warehouse_agent
      inputs: ["validated_data"]
      outputs: ["warehouse_confirmation"]
      tasks:
        - Create/update tables
        - Load data efficiently
        - Update indexes
        - Refresh materialized views
```

## Communication Protocols Between Agents

### Message-Based Communication

```yaml
message_protocol:
  format: structured_json
  required_fields:
    - agent_id: string
    - task_id: string
    - message_type: enum[request, response, notification, error]
    - timestamp: datetime
    - payload: object
  
  message_types:
    task_request:
      payload:
        task_description: string
        priority: enum[low, medium, high, critical]
        deadline: datetime
        dependencies: array[task_id]
        context: object
    
    progress_update:
      payload:
        completion_percentage: number
        current_step: string
        estimated_remaining: duration
        blockers: array[string]
    
    completion_notification:
      payload:
        outputs: object
        metrics: object
        next_steps: array[string]
        artifacts: array[url]
```

### Shared State Management

```yaml
shared_state:
  type: distributed_key_value_store
  
  namespaces:
    project_config:
      access: read_all_agents
      data:
        - api_endpoints
        - database_schemas
        - design_tokens
        - dependency_versions
    
    task_status:
      access: read_write_all_agents
      data:
        - task_states
        - completion_flags
        - blocking_issues
        - progress_metrics
    
    agent_coordination:
      access: read_write_coordinating_agent
      data:
        - agent_assignments
        - resource_locks
        - priority_queue
        - conflict_resolution
```

### Event-Driven Coordination

```yaml
event_system:
  broker: "project_event_bus"
  
  events:
    - name: task_completed
      emitted_by: any_agent
      consumed_by: [coordinator, dependent_agents]
      payload:
        task_id: string
        outputs: object
        duration: number
    
    - name: blocker_encountered
      emitted_by: any_agent
      consumed_by: [coordinator, relevant_agents]
      payload:
        task_id: string
        blocker_type: string
        required_action: string
        severity: enum[low, medium, high, critical]
    
    - name: api_contract_changed
      emitted_by: backend_agents
      consumed_by: [frontend_agents, test_agents]
      payload:
        endpoint: string
        changes: object
        migration_guide: string
    
    - name: schema_migration_ready
      emitted_by: database_agent
      consumed_by: [backend_agents, data_agents]
      payload:
        migration_id: string
        affected_tables: array[string]
        rollback_plan: string
```

## Task Dependency Management

### Dependency Graph Specification

```yaml
task_graph:
  tasks:
    - id: create_user_model
      agent: database_agent
      estimated_duration: 45m
      outputs: ["user_schema.sql", "migration_001.sql"]
    
    - id: create_user_api
      agent: backend_agent
      dependencies: [create_user_model]
      estimated_duration: 90m
      outputs: ["user_controller.py", "user_service.py"]
    
    - id: create_auth_middleware
      agent: backend_agent
      dependencies: [create_user_model]
      estimated_duration: 60m
      outputs: ["auth_middleware.py", "jwt_utils.py"]
    
    - id: create_user_ui
      agent: frontend_agent
      dependencies: [create_user_api]
      estimated_duration: 120m
      outputs: ["UserForm.tsx", "UserList.tsx"]
    
    - id: create_api_tests
      agent: test_agent
      dependencies: [create_user_api, create_auth_middleware]
      estimated_duration: 60m
      outputs: ["test_user_api.py", "test_auth.py"]
```

### Dynamic Dependency Resolution

```python
# Coordinator logic for dependency management
class TaskCoordinator:
    def __init__(self):
        self.task_graph = {}
        self.agent_pool = {}
        self.completed_tasks = set()
        self.in_progress = {}
    
    def assign_ready_tasks(self):
        """Assign tasks that have all dependencies satisfied"""
        ready_tasks = []
        
        for task_id, task in self.task_graph.items():
            if task_id in self.completed_tasks:
                continue
            if task_id in self.in_progress:
                continue
            
            # Check if all dependencies are completed
            deps_satisfied = all(
                dep in self.completed_tasks 
                for dep in task.dependencies
            )
            
            if deps_satisfied:
                ready_tasks.append(task_id)
        
        # Assign to available agents
        for task_id in ready_tasks:
            task = self.task_graph[task_id]
            agent = self.find_available_agent(task.agent_type)
            
            if agent:
                self.assign_task(agent, task)
                self.in_progress[task_id] = agent
    
    def handle_task_completion(self, task_id, outputs):
        """Handle when a task completes"""
        self.completed_tasks.add(task_id)
        del self.in_progress[task_id]
        
        # Store outputs for dependent tasks
        self.store_outputs(task_id, outputs)
        
        # Check for newly ready tasks
        self.assign_ready_tasks()
        
        # Notify dependent agents
        self.notify_dependents(task_id)
```

### Circular Dependency Detection

```yaml
dependency_validator:
  rules:
    - name: no_circular_dependencies
      implementation: |
        def detect_cycles(graph):
            visited = set()
            rec_stack = set()
            
            def has_cycle(node):
                visited.add(node)
                rec_stack.add(node)
                
                for neighbor in graph.get(node, []):
                    if neighbor not in visited:
                        if has_cycle(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        return True
                
                rec_stack.remove(node)
                return False
            
            for node in graph:
                if node not in visited:
                    if has_cycle(node):
                        return True
            return False
    
    - name: maximum_dependency_depth
      max_depth: 5
      implementation: |
        def check_depth(graph, max_depth):
            def get_depth(node, visited=None):
                if visited is None:
                    visited = set()
                
                if node in visited:
                    return 0
                
                visited.add(node)
                
                if node not in graph or not graph[node]:
                    return 1
                
                return 1 + max(
                    get_depth(dep, visited.copy()) 
                    for dep in graph[node]
                )
            
            for node in graph:
                if get_depth(node) > max_depth:
                    return False
            return True
```

## State Synchronization Strategies

### Optimistic Concurrency Control

```yaml
optimistic_sync:
  strategy: version_based
  
  implementation:
    shared_resource:
      version: integer
      data: object
      last_modified_by: agent_id
      last_modified_at: timestamp
    
    update_protocol:
      1. read_with_version: "Agent reads resource and version"
      2. modify_locally: "Agent modifies data locally"
      3. compare_and_swap: "Agent attempts update with version check"
      4. retry_on_conflict: "If version changed, retry with merge"
  
  conflict_resolution:
    strategies:
      - last_write_wins: "Simple overwrite"
      - merge: "Attempt automatic merge"
      - manual: "Flag for human intervention"
```

### Event Sourcing Pattern

```yaml
event_sourcing:
  event_store:
    - event_id: uuid
      timestamp: datetime
      agent_id: string
      event_type: string
      payload: object
      metadata: object
  
  state_reconstruction:
    process:
      1. load_all_events: "Get all events for entity"
      2. sort_by_timestamp: "Order chronologically"
      3. apply_events: "Fold events into current state"
      4. cache_snapshot: "Store computed state"
  
  example_events:
    - type: task_created
      payload:
        task_id: string
        description: string
        assigned_to: agent_id
    
    - type: task_updated
      payload:
        task_id: string
        changes: object
        reason: string
    
    - type: dependency_added
      payload:
        task_id: string
        depends_on: task_id
        added_by: agent_id
```

### Distributed Lock Management

```yaml
locking_strategy:
  lock_types:
    exclusive:
      description: "Only one agent can hold lock"
      use_cases:
        - "Modifying shared configuration"
        - "Deploying to production"
        - "Running database migrations"
    
    shared:
      description: "Multiple agents can read"
      use_cases:
        - "Reading configuration"
        - "Accessing reference data"
        - "Viewing task status"
    
    hierarchical:
      description: "Locks on parent lock children"
      use_cases:
        - "Locking entire feature area"
        - "Preventing conflicting changes"
        - "Coordinating related updates"
  
  implementation:
    acquire_lock:
      timeout: 30s
      retry_strategy: exponential_backoff
      deadlock_detection: true
    
    lock_info:
      holder: agent_id
      acquired_at: timestamp
      expires_at: timestamp
      purpose: string
```

## Error Handling and Recovery

### Failure Detection

```yaml
health_monitoring:
  agent_health:
    heartbeat_interval: 30s
    timeout_threshold: 90s
    
    health_checks:
      - name: responsive
        check: "Agent responds to ping"
      - name: productive
        check: "Agent completing tasks"
      - name: not_stuck
        check: "Task progress increasing"
  
  task_health:
    stuck_detection:
      no_progress_threshold: 30m
      repeated_error_threshold: 3
      escalation_path:
        - retry_with_same_agent
        - reassign_to_different_agent
        - escalate_to_coordinator
        - request_human_intervention
```

### Recovery Strategies

```yaml
recovery_patterns:
  retry_with_backoff:
    initial_delay: 1s
    max_delay: 5m
    multiplier: 2
    max_attempts: 5
    
    applicable_errors:
      - temporary_resource_unavailable
      - network_timeout
      - rate_limit_exceeded
  
  checkpoint_restart:
    checkpoint_frequency: 10m
    checkpoint_data:
      - task_progress
      - intermediate_outputs
      - agent_state
    
    restart_process:
      1. load_last_checkpoint
      2. verify_checkpoint_validity
      3. resume_from_checkpoint
      4. mark_redundant_work
  
  compensating_transaction:
    when: "Partial failure in multi-step process"
    steps:
      1. identify_completed_steps
      2. determine_compensation_needed
      3. execute_rollback_operations
      4. verify_clean_state
      5. retry_entire_operation
  
  circuit_breaker:
    failure_threshold: 5
    timeout: 30s
    half_open_requests: 3
    
    states:
      closed: "Normal operation"
      open: "Failing fast"
      half_open: "Testing recovery"
```

### Cascading Failure Prevention

```yaml
isolation_strategies:
  resource_pools:
    description: "Separate resources per agent type"
    implementation:
      frontend_pool:
        max_concurrent: 10
        queue_size: 50
        timeout: 5m
      
      backend_pool:
        max_concurrent: 20
        queue_size: 100
        timeout: 10m
      
      database_pool:
        max_concurrent: 5
        queue_size: 20
        timeout: 15m
  
  bulkheads:
    description: "Isolate failures to prevent spread"
    patterns:
      - separate_queues_per_priority
      - independent_retry_mechanisms
      - isolated_failure_domains
  
  rate_limiting:
    description: "Prevent resource exhaustion"
    limits:
      per_agent:
        requests_per_minute: 100
        concurrent_tasks: 5
      
      global:
        total_active_tasks: 50
        api_calls_per_minute: 1000
```

## Progress Tracking Across Subagents

### Unified Progress Dashboard

```yaml
progress_tracking:
  dashboard_schema:
    overall_progress:
      total_tasks: integer
      completed_tasks: integer
      in_progress_tasks: integer
      blocked_tasks: integer
      failed_tasks: integer
      
      completion_percentage: float
      estimated_completion: timestamp
      current_velocity: tasks_per_hour
    
    per_agent_metrics:
      agent_id: string
      assigned_tasks: integer
      completed_tasks: integer
      average_task_duration: duration
      current_task: string
      idle_time: duration
    
    critical_path:
      tasks: array[task_id]
      total_duration: duration
      current_position: task_id
      estimated_delay: duration
```

### Real-time Progress Updates

```python
# Progress aggregation service
class ProgressAggregator:
    def __init__(self):
        self.task_progress = {}
        self.agent_metrics = {}
        self.subscribers = []
    
    def update_task_progress(self, task_id, progress):
        """Update individual task progress"""
        self.task_progress[task_id] = {
            'percentage': progress.percentage,
            'current_step': progress.current_step,
            'updated_at': datetime.now(),
            'agent_id': progress.agent_id
        }
        
        # Recalculate overall progress
        overall = self.calculate_overall_progress()
        
        # Notify subscribers
        self.notify_subscribers({
            'type': 'progress_update',
            'task_id': task_id,
            'task_progress': progress,
            'overall_progress': overall
        })
    
    def calculate_overall_progress(self):
        """Calculate weighted progress across all tasks"""
        if not self.task_progress:
            return 0.0
        
        total_weight = sum(
            task.get('weight', 1.0) 
            for task in self.task_progress.values()
        )
        
        weighted_progress = sum(
            task.get('percentage', 0) * task.get('weight', 1.0)
            for task in self.task_progress.values()
        )
        
        return weighted_progress / total_weight if total_weight > 0 else 0.0
    
    def get_critical_path_status(self):
        """Identify and report critical path status"""
        critical_tasks = self.identify_critical_path()
        
        return {
            'critical_tasks': critical_tasks,
            'completion_estimate': self.estimate_completion(critical_tasks),
            'potential_delays': self.identify_delays(critical_tasks),
            'mitigation_options': self.suggest_mitigations()
        }
```

### Progress Visualization

```yaml
visualization_patterns:
  gantt_chart:
    shows:
      - task_timeline
      - dependencies
      - agent_assignments
      - progress_bars
      - critical_path_highlight
    
    updates: real_time
    interaction: 
      - hover_for_details
      - click_to_expand
      - drag_to_reschedule
  
  burndown_chart:
    shows:
      - remaining_work
      - completion_velocity
      - projected_completion
      - scope_changes
    
    time_periods:
      - hourly
      - daily
      - sprint
  
  agent_utilization:
    shows:
      - agent_workload
      - idle_time
      - task_distribution
      - performance_metrics
    
    alerts:
      - overloaded_agent
      - idle_agent
      - degraded_performance
```

## Examples of Well-Designed Subagent Tasks

### Example 1: E-commerce Platform Feature

```yaml
feature: product_recommendations
total_time_estimate: 2_days

subagent_tasks:
  ml_agent:
    tasks:
      - name: "Design recommendation algorithm"
        duration: 3h
        outputs:
          - algorithm_spec.md
          - data_requirements.yaml
      
      - name: "Implement collaborative filtering"
        duration: 4h
        dependencies: ["Design recommendation algorithm"]
        outputs:
          - recommendation_engine.py
          - model_training.py
      
      - name: "Create model evaluation pipeline"
        duration: 2h
        outputs:
          - evaluation_metrics.py
          - ab_test_framework.py
  
  backend_agent:
    tasks:
      - name: "Create recommendations API"
        duration: 3h
        dependencies: ["Design recommendation algorithm"]
        outputs:
          - recommendations_controller.py
          - recommendations_service.py
          - api_schema.yaml
      
      - name: "Implement caching layer"
        duration: 2h
        outputs:
          - redis_cache.py
          - cache_warmup.py
  
  frontend_agent:
    tasks:
      - name: "Design recommendation UI component"
        duration: 2h
        outputs:
          - RecommendationCard.tsx
          - RecommendationList.tsx
      
      - name: "Implement personalization settings"
        duration: 2h
        outputs:
          - PersonalizationSettings.tsx
          - preferences_api.ts
  
  data_agent:
    tasks:
      - name: "Create ETL for training data"
        duration: 3h
        outputs:
          - user_behavior_etl.py
          - product_features_etl.py
      
      - name: "Set up real-time event streaming"
        duration: 3h
        outputs:
          - kafka_producers.py
          - event_schemas.avro
```

### Example 2: Mobile App Development

```yaml
project: fitness_tracker_app
platforms: [ios, android]

subagent_allocation:
  ios_agent:
    parallel_with: [android_agent, backend_agent]
    tasks:
      - "Set up iOS project structure"
      - "Implement HealthKit integration"
      - "Create workout tracking UI"
      - "Add push notification handling"
      - "Implement data synchronization"
  
  android_agent:
    parallel_with: [ios_agent, backend_agent]
    tasks:
      - "Set up Android project structure"
      - "Implement Google Fit integration"
      - "Create workout tracking UI"
      - "Add push notification handling"
      - "Implement data synchronization"
  
  backend_agent:
    parallel_with: [ios_agent, android_agent]
    tasks:
      - "Design API endpoints"
      - "Implement user authentication"
      - "Create workout data models"
      - "Set up push notification service"
      - "Implement data aggregation"
  
  ui_design_agent:
    completes_before: [ios_agent, android_agent]
    tasks:
      - "Create design system"
      - "Design workout screens"
      - "Create animation specifications"
      - "Design onboarding flow"
      - "Create app icon and assets"
```

### Example 3: Microservices Migration

```yaml
migration: monolith_to_microservices
approach: strangler_fig_pattern

phase_1_agents:
  analysis_agent:
    tasks:
      - "Identify service boundaries"
      - "Map data dependencies"
      - "Create migration roadmap"
      - "Design service contracts"
    duration: 1_day
  
  user_service_agent:
    tasks:
      - "Extract user management code"
      - "Create user service API"
      - "Implement service tests"
      - "Set up service deployment"
    duration: 2_days
    can_start_after: ["Identify service boundaries"]
  
  auth_service_agent:
    tasks:
      - "Extract authentication logic"
      - "Create auth service API"
      - "Implement JWT handling"
      - "Set up service deployment"
    duration: 2_days
    can_start_after: ["Identify service boundaries"]
  
  api_gateway_agent:
    tasks:
      - "Set up API gateway"
      - "Configure routing rules"
      - "Implement rate limiting"
      - "Add request authentication"
    duration: 1_day
    can_start_after: ["Design service contracts"]
  
  migration_testing_agent:
    tasks:
      - "Create integration test suite"
      - "Set up contract testing"
      - "Implement smoke tests"
      - "Create rollback procedures"
    duration: continuous
    runs_parallel_with: all_other_agents
```

## Anti-Patterns to Avoid

### 1. Over-Coordination

```yaml
# BAD - Too much coordination overhead
anti_pattern:
  name: "Chatty Agents"
  problem: "Agents communicate for every small decision"
  symptoms:
    - More time coordinating than working
    - Circular communication loops
    - Decision paralysis
    - Message queue overflow
  
  example:
    frontend_agent: "Should button be blue or green?"
    design_agent: "What's the context?"
    frontend_agent: "User profile page"
    design_agent: "What other colors are there?"
    frontend_agent: "White background, black text"
    # ... 20 more messages
  
  solution: "Define clear design tokens upfront"
```

### 2. Tight Coupling

```yaml
# BAD - Agents can't work independently
anti_pattern:
  name: "Synchronized Swimmers"
  problem: "All agents must move in lockstep"
  symptoms:
    - No agent can progress alone
    - Constant waiting for others
    - Single point of failure
    - Cascading delays
  
  example:
    task_1: "Frontend waits for exact API implementation"
    task_2: "API waits for exact database schema"
    task_3: "Database waits for exact frontend needs"
    result: "Circular dependency - nothing progresses"
  
  solution: "Define interfaces first, implement independently"
```

### 3. Resource Contention

```yaml
# BAD - Agents fight over shared resources
anti_pattern:
  name: "Resource Warriors"
  problem: "Multiple agents modifying same files"
  symptoms:
    - Merge conflicts
    - Overwritten changes
    - Inconsistent state
    - Lost work
  
  example:
    agent_1: "Modifies config.yaml at 10:00"
    agent_2: "Modifies config.yaml at 10:01"
    agent_3: "Modifies config.yaml at 10:02"
    result: "Only agent_3's changes survive"
  
  solution: "Assign clear ownership of files/modules"
```

### 4. Unclear Responsibilities

```yaml
# BAD - Overlap in agent responsibilities
anti_pattern:
  name: "Everyone's Job, No One's Job"
  problem: "Multiple agents think they own same task"
  symptoms:
    - Duplicate implementations
    - Conflicting approaches
    - Wasted effort
    - Finger pointing
  
  example:
    frontend_agent: "I'll add input validation"
    backend_agent: "I'll add input validation"
    result: "Two different validation systems"
  
  solution: "Clear RACI matrix for all tasks"
```

### 5. Premature Optimization

```yaml
# BAD - Over-engineering the coordination
anti_pattern:
  name: "NASA Mission Control"
  problem: "Complex coordination for simple tasks"
  symptoms:
    - 10-step process for 1-hour task
    - More documentation than code
    - Analysis paralysis
    - Slow progress
  
  example:
    simple_task: "Add login button"
    process:
      - Architecture review meeting
      - Design committee approval
      - Security assessment
      - Performance impact analysis
      - 5 levels of sign-off
  
  solution: "Match coordination complexity to task complexity"
```

## Integration with Project Planning

### Milestone-Based Coordination

```yaml
project_milestones:
  milestone_1:
    name: "MVP Release"
    date: "2024-03-01"
    required_features:
      - user_authentication
      - basic_crud_operations
      - minimal_ui
    
    agent_assignments:
      critical_path:
        - auth_agent: "Complete by 2024-02-15"
        - backend_agent: "Complete by 2024-02-20"
        - frontend_agent: "Complete by 2024-02-25"
      
      parallel_work:
        - docs_agent: "Throughout milestone"
        - test_agent: "Throughout milestone"
        - devops_agent: "Complete by 2024-02-20"
```

### Sprint-Based Allocation

```yaml
sprint_planning:
  sprint_23:
    duration: 2_weeks
    velocity: 50_story_points
    
    agent_capacity:
      frontend_agent: 15_points
      backend_agent: 20_points
      database_agent: 10_points
      test_agent: 5_points
    
    story_allocation:
      - story: "User can reset password"
        points: 8
        agents:
          frontend_agent: 3_points
          backend_agent: 5_points
      
      - story: "Add product search"
        points: 13
        agents:
          frontend_agent: 5_points
          backend_agent: 5_points
          database_agent: 3_points
```

### Risk-Based Prioritization

```yaml
risk_management:
  high_risk_areas:
    - area: "Payment Processing"
      mitigation: "Assign most experienced agents"
      parallel_agents:
        - payment_specialist
        - security_agent
        - compliance_agent
    
    - area: "Data Migration"
      mitigation: "Extra validation and rollback plans"
      sequential_phases:
        - analysis_agent: "Map all data"
        - migration_agent: "Execute with checkpoints"
        - validation_agent: "Verify integrity"
```

## Metrics and Monitoring

### Coordination Efficiency Metrics

```yaml
metrics:
  coordination_overhead:
    definition: "Time spent coordinating vs working"
    target: "< 20%"
    measurement: |
      coordination_time / (coordination_time + work_time)
  
  parallel_efficiency:
    definition: "Speedup from parallelization"
    target: "> 0.7 * num_agents"
    measurement: |
      time_sequential / time_parallel
  
  blocking_frequency:
    definition: "How often agents wait for others"
    target: "< 10%"
    measurement: |
      blocked_time / total_time
  
  rework_rate:
    definition: "Work discarded due to conflicts"
    target: "< 5%"
    measurement: |
      discarded_work / total_work
```

### Agent Performance Metrics

```yaml
agent_metrics:
  throughput:
    - tasks_completed_per_hour
    - story_points_per_sprint
    - lines_of_code_per_day
  
  quality:
    - defects_per_task
    - rework_required
    - peer_review_scores
  
  collaboration:
    - response_time_to_requests
    - helpful_interactions
    - knowledge_sharing_contributions
```

## Conclusion

Effective subagent coordination transforms sequential workflows into parallel powerhouses. Key principles:

1. **Design for Independence**: Minimize dependencies between agents
2. **Communicate Through Contracts**: Define clear interfaces upfront
3. **Fail Gracefully**: Build resilience into the system
4. **Monitor Constantly**: Track both progress and coordination overhead
5. **Iterate and Improve**: Refine patterns based on actual performance

The goal is not maximum parallelization, but optimal parallelization - where coordination overhead doesn't exceed efficiency gains. Start simple, measure constantly, and scale complexity only when proven necessary.