# Phase 5: Observability & Monitoring - Work Plan

## Prerequisites

Before implementing observability, ensure the foundation is solid and ready for instrumentation:
- **Completed Phases**: 1-4 - Server foundation with health checks, database layer with connection pooling, GraphQL API with resolvers, and authorization with SpiceDB integration
- **Required Knowledge**:
    - **Metrics and Time Series Data**: Understanding of Prometheus metrics types (counters, gauges, histograms), cardinality implications, and aggregation patterns (*Essential*)
    - **Distributed Tracing Concepts**: Familiarity with spans, trace context propagation, sampling strategies, and OpenTelemetry standards (*Essential*)
    - **Structured Logging**: Experience with JSON logging, log levels, contextual fields, and security considerations for log data (*Essential*)
    - **Performance Profiling**: Basic understanding of profiling tools, overhead measurement, and optimization techniques (*Recommended*)

## Quick Reference - Essential Resources

All resources are organized to support both implementation and learning:

### Example Files
All example files are located in `../../.spec/examples/tdd-test-structure.rs/../`:
- **[tdd-test-structure.rs](../../.spec/examples/tdd-test-structure.rs)** - Comprehensive test examples following TDD methodology - Provides the testing patterns that should be followed throughout this phase
- **[metrics-patterns.rs](../../.spec/examples/metrics-patterns.rs)** - Prometheus metrics implementation patterns with cardinality control - Shows proper metric design to avoid cardinality explosion
- **[tracing-patterns.rs](../../.spec/examples/tracing-patterns.rs)** - OpenTelemetry tracing examples with context propagation - Demonstrates span creation and trace context management
- **[log-sanitization.rs](../../.spec/examples/log-sanitization.rs)** - Security-focused log sanitization patterns - Critical for preventing sensitive data leakage in logs

### Specification Documents
Key specifications for this phase:
- **[metrics.md](../../.spec/metrics.md)** - Complete metrics specification with cardinality guidelines
    - Key sections: Metric Types, Naming Conventions, Cardinality Limits, Dashboard Requirements
- **[logging.md](../../.spec/logging.md)** - Logging standards and sanitization requirements
    - Key sections: Log Levels, Structured Format, Security Rules, Retention Policies
- **[tracing.md](../../.spec/tracing.md)** - Distributed tracing requirements and patterns
    - Key sections: Span Attributes, Sampling Configuration, Context Propagation, Performance Budgets

### Junior Developer Resources
Additional learning resources organized by when you'll need them:
- **[Observability Tutorial](../../junior-dev-helper/observability-tutorial.md)** - Introduction to the three pillars of observability
    - *When to read*: Before starting any implementation
- **[Prometheus Metrics Guide](../../junior-dev-helper/prometheus-metrics-guide.md)** - Deep dive into metric types, labels, and best practices
    - *When to read*: Before implementing Section 5.1
- **[Cardinality Control Guide](../../junior-dev-helper/cardinality-control-guide.md)** - Critical guide on preventing metric explosion
    - *When to read*: Before adding ANY metric labels
- **[Structured Logging Guide](../../junior-dev-helper/structured-logging-guide.md)** - JSON logging patterns and security considerations
    - *When to read*: Before implementing Section 5.2
- **[OpenTelemetry Tracing Guide](../../junior-dev-helper/opentelemetry-tracing-guide.md)** - Distributed tracing concepts and implementation
    - *When to read*: Before implementing Section 5.3
- **[Common Observability Errors](../../junior-dev-helper/observability-common-errors.md)** - Troubleshooting guide for metrics, logs, and traces
    - *When to read*: When encountering issues

### Quick Links
- **Verification Script**: `scripts/verify-phase-5.sh` - Validates all observability components are working
- **Metrics Dashboard**: `just metrics-up && just grafana-up` - Starts local Prometheus and Grafana for testing
- **Trace Viewer**: `just jaeger-up` - Starts Jaeger UI for viewing distributed traces

## Overview

This work plan implements comprehensive observability across the PCF API in four carefully sequenced checkpoints. Each checkpoint builds upon the previous one, starting with metrics collection, then structured logging, followed by distributed tracing, and concluding with dashboard creation and performance validation. The plan emphasizes security (no sensitive data in telemetry), reliability (cardinality control), and performance (minimal overhead).

**Checkpoint Strategy**: Four checkpoints divide the work at natural boundaries: after metrics setup, after logging implementation, after tracing integration, and after dashboard/alerting setup. Each checkpoint includes specific verification steps and deliverables.

**Time Estimate**: 3-4 weeks for an experienced developer, 5-6 weeks for someone new to observability. Add 1 week if creating custom dashboards or complex alerting rules.

## Build and Test Commands

This project uses `just` as the command runner to ensure consistency across environments. All commands include proper configuration and dependencies:
- `just test` - Run all tests including observability-specific test suites (After any code changes to verify nothing is broken)
- `just test-metrics` - Run only metrics-related tests (When working on Section 5.1)
- `just test-logging` - Run only logging-related tests (When working on Section 5.2)
- `just test-tracing` - Run only tracing-related tests (When working on Section 5.3)
- `just metrics-up` - Start local Prometheus with pre-configured scraping (To verify metrics are being collected correctly)
- `just grafana-up` - Start Grafana with provisioned dashboards (To visualize metrics and test dashboards)
- `just jaeger-up` - Start Jaeger for trace visualization (To verify distributed tracing is working)

## IMPORTANT: Review Process

**This plan includes 4 mandatory review checkpoints where work MUST stop for external review. These checkpoints prevent cascading issues and ensure each observability layer is properly implemented before building the next. Observability code is particularly prone to production issues (cardinality explosion, performance degradation) if not reviewed carefully.**

At each of the 4 checkpoints:
1. **STOP all work and commit your code with a descriptive message**
2. **Request external review** by:
   - Run all tests for the completed section
   - Verify deliverables match the checkpoint requirements
   - Document any deviations or blockers encountered
   - Prepare specific questions if you need clarification
   - Create checkpoint documentation in .claude/.reviews/
3. **DO NOT PROCEED to the next section until you receive explicit approval. Use wait time to review upcoming sections or study relevant guides.**

## Development Methodology: Test-Driven Development (TDD)

**IMPORTANT**: TDD is especially critical for observability because telemetry code must work reliably even when the system is failing. Writing tests first ensures we verify the observability data we expect to see before implementing the instrumentation.

1. **Write tests FIRST** - Before implementing any metric, log, or span, write a test that verifies the expected output
     - *Observability code is hard to test after implementation; tests ensure we're measuring what we think we're measuring*
2. **Run tests to see them FAIL** - Confirm the test actually detects the missing telemetry
     - *A test that passes before implementation is testing the wrong thing*
3. **Write minimal code to make tests PASS** - Implement just enough instrumentation to satisfy the test
     - *Prevents over-instrumentation which can impact performance*
4. **REFACTOR for clarity and performance** - Optimize hot paths and ensure telemetry code is maintainable
     - *Observability code runs frequently and must have minimal overhead*
5. **Document telemetry semantics** - Add clear documentation about what each metric/log/span represents
     - *Future developers need to understand the meaning of telemetry data*

## Done Criteria Checklist

Phase 5 is complete when all observability pillars are operational and verified:
- [ ] /metrics endpoint returns valid Prometheus format
    - *Verification*: curl localhost:8080/metrics | promtool check metrics
- [ ] User-facing operations emit structured logs with trace IDs
    - *Verification*: Make API calls and verify JSON logs contain trace_id field
- [ ] Infrastructure operations have basic logging
    - *Verification*: Check logs for startup, shutdown, and health check events
- [ ] Distributed tracing spans for significant operations
    - *Verification*: View traces in Jaeger UI, verify parent-child relationships
- [ ] No sensitive data in any telemetry output
    - *Verification*: Run security scan script: just scan-telemetry-security
- [ ] Monitoring dashboards created and functional
    - *Verification*: Access Grafana dashboards, verify data is populating
- [ ] Cardinality limits enforced
    - *Verification*: Run cardinality test: just test-metrics-cardinality
- [ ] Performance impact <5% overhead
    - *Verification*: Run benchmarks with/without telemetry: just bench-overhead
- [ ] All code has corresponding tests written first
    - *Verification*: Review git history to confirm test-first approach

## Work Breakdown with Review Checkpoints

### 5.1 Metrics Implementation (~800 lines, 6-7 files)

**Work Unit Context:**
- **Complexity**: Medium - Cardinality control and performance optimization require careful design
- **Scope**: ~800 lines across 6-7 files
- **Key Components**:
  - Prometheus recorder setup (~150) - Configure PrometheusBuilder with cardinality limits and buckets
  - Core metrics implementation (~300) - HTTP, GraphQL, database, and system metrics
  - Cardinality limiter (~200) - Prevent metric explosion through label limiting
  - Metrics endpoint (~100) - Expose /metrics with proper security
  - Performance sampling (~50) - Reduce overhead for high-frequency operations
- **Patterns**: Builder pattern for recorder, Lazy static initialization, Label sanitization
- **Required Algorithms**: Exponential histogram buckets, Reservoir sampling for high-cardinality data

#### Task 5.1.1: Write Metrics Registry Tests First

💡 **Junior Dev Tip**: Start with the Prometheus Metrics Guide to understand metric types before writing tests
   See: [../../junior-dev-helper/prometheus-metrics-guide.md](../../junior-dev-helper/prometheus-metrics-guide.md)

⚠️ **Warning Tip**: CRITICAL: Read the Cardinality Control Guide before adding any labels to metrics
   See: [../../junior-dev-helper/cardinality-control-guide.md](../../junior-dev-helper/cardinality-control-guide.md)

Following TDD, start by writing comprehensive tests for the metrics registry. These tests will verify metric registration, label validation, and cardinality limits. The tests should fail initially, driving the implementation of the registry.

**TDD Approach**: Create tests that verify: metric names follow conventions, labels are properly sanitized, cardinality limits are enforced, and metrics can be retrieved. Use the pattern from tdd-test-structure.rs.

**Test structure for metrics registry:**
```rust
#[cfg(test)]
mod metrics_registry_tests {
    use super::*;
    use prometheus::{Counter, Histogram};

    #[test]
    fn test_metric_registration_with_cardinality_limit() {
        // Arrange
        let registry = MetricsRegistry::new()
            .with_cardinality_limit(1000)
            .build();
        
        // Act
        let result = registry.register_counter(
            "api_requests_total",
            "Total API requests",
            &["method", "endpoint", "status"]
        );
        
        // Assert
        assert!(result.is_ok());
        let counter = result.unwrap();
        
        // Verify cardinality limits
        for i in 0..1001 {
            let labels = vec![
                ("method", "GET"),
                ("endpoint", &format!("/test/{}", i)),
                ("status", "200")
            ];
            
            if i < 1000 {
                assert!(counter.record_with_labels(&labels).is_ok());
            } else {
                // Should reject after limit
                assert!(counter.record_with_labels(&labels).is_err());
            }
        }
    }
}
```

*This test verifies that our metrics registry enforces cardinality limits. It attempts to create more label combinations than allowed and verifies the registry correctly rejects them after the limit.*

**Special Considerations:**
- Metrics must follow Prometheus naming conventions (snake_case, descriptive suffixes)
- Consider using metric families to group related metrics
- Plan for both application and infrastructure metrics

#### Task 5.1.2: Implement Prometheus Recorder with Cardinality Control

⚡ **Performance Tip**: Use lazy_static or OnceCell for metric initialization to avoid runtime overhead

🔒 **Security Tip**: Never include user IDs, emails, or other PII as metric labels

Now implement the Prometheus recorder to make the tests pass. Focus on setting up the PrometheusBuilder with appropriate configuration, implementing cardinality limiting, and ensuring thread-safe access to metrics.

**TDD Approach**: Implement only enough code to make the registry tests pass. Start with basic registration, then add cardinality limiting.

**Prometheus recorder setup with cardinality limits:**
```rust
use prometheus::{Registry, Encoder, TextEncoder};
use std::sync::Arc;
use parking_lot::RwLock;

pub struct MetricsRecorder {
    registry: Registry,
    cardinality_limiter: Arc<RwLock<CardinalityLimiter>>,
}

impl MetricsRecorder {
    pub fn new() -> Result<Self, MetricsError> {
        let registry = Registry::new();
        
        // Register default metrics
        let process_collector = prometheus::process_collector::ProcessCollector::for_self();
        registry.register(Box::new(process_collector))?;
        
        let limiter = Arc::new(RwLock::new(
            CardinalityLimiter::new(1000) // Default limit
        ));
        
        Ok(Self {
            registry,
            cardinality_limiter: limiter,
        })
    }
    
    pub fn register_counter(
        &self,
        name: &str,
        help: &str,
        labels: &[&str],
    ) -> Result<CardinalityLimitedCounter, MetricsError> {
        let counter = CounterVec::new(
            Opts::new(name, help),
            labels
        )?;
        
        self.registry.register(Box::new(counter.clone()))?;
        
        Ok(CardinalityLimitedCounter {
            inner: counter,
            limiter: self.cardinality_limiter.clone(),
        })
    }
}
```

*This implementation provides a thread-safe metrics recorder with built-in cardinality limiting. The CardinalityLimiter is shared across all metrics to enforce global limits.*

#### Task 5.1.3: Add Core Application Metrics

💡 **Junior Dev Tip**: Use the metrics-patterns.rs example file for standard metric implementations
   See: [../../.spec/examples/metrics-patterns.rs](../../.spec/examples/metrics-patterns.rs)

Implement the essential metrics for monitoring application health: HTTP request metrics (duration, status, method), GraphQL operation metrics (type, complexity, errors), Database query metrics (duration, pool stats), and System resource metrics (CPU, memory, connections).

**TDD Approach**: Write tests for each metric type first, verifying correct labels and appropriate bucket boundaries for histograms.

**HTTP request duration histogram:**
```rust
lazy_static! {
    static ref HTTP_REQUEST_DURATION: HistogramVec = register_histogram_vec!(
        "http_request_duration_seconds",
        "HTTP request latencies in seconds",
        &["method", "endpoint", "status_group"],
        // Buckets optimized for web API latencies
        vec![0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
    ).unwrap();
}

// Middleware to record metrics
pub async fn metrics_middleware<B>(
    req: Request<B>,
    next: Next<B>,
) -> Result<Response, Error> {
    let start = Instant::now();
    let method = req.method().to_string();
    let path = normalize_path(req.uri().path()); // Normalize to prevent explosion
    
    let response = next.run(req).await;
    let elapsed = start.elapsed().as_secs_f64();
    
    let status_group = match response.status().as_u16() {
        200..=299 => "2xx",
        300..=399 => "3xx",
        400..=499 => "4xx",
        500..=599 => "5xx",
        _ => "other",
    };
    
    HTTP_REQUEST_DURATION
        .with_label_values(&[&method, &path, status_group])
        .observe(elapsed);
    
    Ok(response)
}
```

*This middleware records HTTP request durations with normalized paths to prevent cardinality explosion. Status codes are grouped to reduce label combinations.*

---

### 🛑 CHECKPOINT 1: Metrics Implementation Review - STOP and request review before proceeding

**Deliverables:**
- Prometheus recorder with cardinality limiting
- Core application metrics (HTTP, GraphQL, Database)
- Metrics endpoint at /metrics
- All metrics tests passing
- Cardinality verification script results

**Verification Steps:**
1. Run `just test-metrics` - all tests should pass
2. Start server and access http://localhost:8080/metrics
3. Verify Prometheus format with `curl localhost:8080/metrics | promtool check metrics`
4. Run cardinality check: `just check-metrics-cardinality`
5. Ensure no PII in metric labels

**Common Issues:**
- **Issue**: Metrics endpoint returns 404
  **Solution**: Ensure metrics route is registered in router configuration
- **Issue**: Cardinality limit exceeded errors
  **Solution**: Review label combinations, use label normalization, group similar values
- **Issue**: High memory usage from metrics
  **Solution**: Reduce histogram buckets, implement metric expiry for unused series

**DO NOT PROCEED** until review is complete and approved.

---

### 5.2 Structured Logging Implementation (~600 lines, 5-6 files)

**Work Unit Context:**
- **Complexity**: Medium - Security-critical sanitization and performance-sensitive hot paths
- **Scope**: ~600 lines across 5-6 files
- **Key Components**:
  - Tracing subscriber setup (~100) - Configure structured JSON logging with appropriate layers
  - Log sanitization layer (~200) - Remove sensitive data before output
  - Context injection (~150) - Add trace IDs and request context to all logs
  - Performance logging (~100) - Efficient logging for hot paths
  - Log sampling (~50) - Reduce volume while maintaining visibility
- **Patterns**: Layer composition, Visitor pattern for sanitization, Context propagation
- **Required Algorithms**: Regex-based sanitization, Dynamic sampling based on log level

#### Task 5.2.1: Write Log Sanitization Tests First

🔒 **Security Tip**: Review the log-sanitization.rs example for comprehensive patterns
   See: [../../.spec/examples/log-sanitization.rs](../../.spec/examples/log-sanitization.rs)

⚠️ **Warning Tip**: Sanitization must work even if the regex engine fails - always fail closed

Create comprehensive tests for log sanitization that verify sensitive data is properly removed or masked. Tests should cover various data types including passwords, tokens, API keys, emails, credit card numbers, and social security numbers.

**TDD Approach**: Write tests that attempt to log sensitive data and verify it's properly sanitized in the output. Include edge cases like nested JSON and URL parameters.

**Log sanitization test cases:**
```rust
#[cfg(test)]
mod log_sanitization_tests {
    use super::*;
    use tracing_test::traced_test;
    
    #[traced_test]
    #[test]
    fn test_password_sanitization() {
        // Arrange
        let sensitive_data = json!({
            "user": "john@example.com",
            "password": "super-secret-123",
            "api_key": "sk_live_abcd1234",
            "credit_card": "4111-1111-1111-1111"
        });
        
        // Act
        tracing::info!(data = ?sensitive_data, "User login attempt");
        
        // Assert
        let logs = logs_contain("User login attempt");
        assert!(logs.len() > 0);
        
        let log_output = &logs[0];
        assert!(!log_output.contains("super-secret-123"));
        assert!(!log_output.contains("sk_live_abcd1234"));
        assert!(!log_output.contains("4111-1111-1111-1111"));
        
        // Should contain sanitized versions
        assert!(log_output.contains("password\":\"[REDACTED]"));
        assert!(log_output.contains("api_key\":\"sk_live_[REDACTED]"));
        assert!(log_output.contains("credit_card\":\"****-****-****-1111"));
    }
}
```

*This test verifies that sensitive data is properly sanitized before being written to logs. Different data types require different sanitization strategies.*

#### Task 5.2.2: Implement Structured Logging with Tracing

💡 **Junior Dev Tip**: Study the Structured Logging Guide for JSON formatting patterns
   See: [../../junior-dev-helper/structured-logging-guide.md](../../junior-dev-helper/structured-logging-guide.md)

⚡ **Performance Tip**: Use tracing's span fields instead of formatting strings in hot paths

Set up the tracing subscriber with JSON formatting, implement the sanitization layer to make tests pass, and configure appropriate log levels for different components. Ensure all logs include trace context for correlation with distributed traces.

**TDD Approach**: Focus on making the sanitization tests pass first, then add context injection and performance optimizations.

**Tracing subscriber with sanitization layer:**
```rust
use tracing_subscriber::{
    layer::SubscriberExt,
    util::SubscriberInitExt,
    EnvFilter, Registry,
};

pub fn init_tracing(config: &ObservabilityConfig) -> Result<(), TracingError> {
    let env_filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));
    
    // JSON formatting layer
    let json_layer = tracing_subscriber::fmt::layer()
        .json()
        .with_current_span(true)
        .with_span_list(true)
        .with_target(true)
        .with_thread_ids(true)
        .with_thread_names(true);
    
    // Sanitization layer
    let sanitize_layer = SanitizationLayer::new()
        .add_pattern(SensitivePattern::Password)
        .add_pattern(SensitivePattern::ApiKey)
        .add_pattern(SensitivePattern::CreditCard)
        .add_pattern(SensitivePattern::Email)
        .add_pattern(SensitivePattern::IpAddress);
    
    // Context injection layer
    let context_layer = ContextInjectionLayer::new();
    
    // Compose layers
    Registry::default()
        .with(env_filter)
        .with(context_layer)
        .with(sanitize_layer)
        .with(json_layer)
        .init();
    
    Ok(())
}

// Sanitization layer implementation
pub struct SanitizationLayer {
    patterns: Vec<SensitivePattern>,
}

impl<S> Layer<S> for SanitizationLayer
where
    S: Subscriber,
{
    type Subscriber = SanitizingSubscriber<S>;
    
    fn layer(&self, inner: S) -> Self::Subscriber {
        SanitizingSubscriber {
            inner,
            patterns: self.patterns.clone(),
        }
    }
}
```

*This sets up a layered tracing subscriber with JSON output, sanitization, and context injection. Layers are composable and process events in order.*

#### Task 5.2.3: Add Request Context and Trace Correlation

💡 **Junior Dev Tip**: Trace context propagation is complex - review the tracing guide carefully
   See: [../../junior-dev-helper/opentelemetry-tracing-guide.md](../../junior-dev-helper/opentelemetry-tracing-guide.md)

Implement automatic injection of request context (trace ID, span ID, user ID, request ID) into all logs. Ensure logs can be correlated with distributed traces by including OpenTelemetry trace context.

**TDD Approach**: Write tests that verify trace IDs appear in logs and match the distributed trace context.

**Context injection middleware:**
```rust
use opentelemetry::trace::TraceContextExt;
use tracing_opentelemetry::OpenTelemetrySpanExt;

pub async fn context_injection_middleware<B>(
    req: Request<B>,
    next: Next<B>,
) -> Result<Response, Error> {
    // Extract or create trace context
    let trace_id = extract_trace_id(&req)
        .unwrap_or_else(|| generate_trace_id());
    
    let request_id = Uuid::new_v4().to_string();
    
    // Create root span with context
    let span = tracing::info_span!(
        "http_request",
        trace_id = %trace_id,
        request_id = %request_id,
        method = %req.method(),
        path = %req.uri().path(),
        // These will be added after auth
        user_id = tracing::field::Empty,
        tenant_id = tracing::field::Empty,
    );
    
    // Set OpenTelemetry context
    let cx = opentelemetry::Context::current();
    span.set_parent(cx);
    
    // Process request within span
    async move {
        let response = next.run(req).await;
        
        // Record response info
        tracing::Span::current().record(
            "status", 
            &response.status().as_u16()
        );
        
        response
    }
    .instrument(span)
    .await
}
```

*This middleware creates a root span for each request and ensures all logs within that request include trace context. The trace ID enables correlation between logs and distributed traces.*

---

### 🛑 CHECKPOINT 2: Structured Logging Review - STOP and request review before proceeding

**Deliverables:**
- JSON structured logging configuration
- Log sanitization for all sensitive data types
- Request context injection with trace IDs
- Performance-optimized logging for hot paths
- All logging tests passing

**Verification Steps:**
1. Run `just test-logging` - all tests should pass
2. Make API requests and verify JSON logs contain trace_id
3. Attempt to log sensitive data and verify sanitization
4. Check log performance with `just bench-logging`
5. Verify no sensitive data in sample logs

**Common Issues:**
- **Issue**: Logs missing trace_id field
  **Solution**: Ensure context injection middleware runs before other middleware
- **Issue**: Sensitive data appearing in logs
  **Solution**: Add missing patterns to sanitization layer, check for custom Debug impls
- **Issue**: High CPU usage from logging
  **Solution**: Reduce log verbosity in hot paths, use sampling for debug logs

**DO NOT PROCEED** until review is complete and approved.

---

### 5.3 Distributed Tracing Implementation (~700 lines, 6-7 files)

**Work Unit Context:**
- **Complexity**: High - Complex context propagation across async boundaries and service calls
- **Scope**: ~700 lines across 6-7 files
- **Key Components**:
  - OpenTelemetry setup (~150) - Configure OTLP exporter and trace pipeline
  - Span instrumentation (~250) - Add spans to key operations
  - Context propagation (~150) - Ensure trace context flows through async operations
  - Sampling configuration (~100) - Implement adaptive sampling for cost control
  - Trace attributes (~50) - Add semantic conventions and custom attributes
- **Patterns**: Context propagation, Async tracing, Sampling strategies
- **Required Algorithms**: Adaptive sampling, Trace ID generation, Context extraction

#### Task 5.3.1: Write Distributed Tracing Tests First

💡 **Junior Dev Tip**: Start with the OpenTelemetry Tracing Guide to understand concepts
   See: [../../junior-dev-helper/opentelemetry-tracing-guide.md](../../junior-dev-helper/opentelemetry-tracing-guide.md)

⚠️ **Warning Tip**: Context propagation across async boundaries is tricky - test thoroughly

Create tests that verify trace context propagation across service boundaries, span parent-child relationships, and proper attribute attachment. Tests should cover HTTP headers, async task spawning, and database queries.

**TDD Approach**: Write integration tests that create traces and verify the span hierarchy. Use the OpenTelemetry test exporter to capture spans.

**Test for trace context propagation:**
```rust
#[cfg(test)]
mod tracing_tests {
    use opentelemetry::testing::TestExporter;
    use opentelemetry::trace::{Tracer, TracerProvider};
    
    #[tokio::test]
    async fn test_trace_context_propagation() {
        // Arrange
        let exporter = TestExporter::new();
        let provider = init_test_tracer(exporter.clone());
        let tracer = provider.tracer("test");
        
        // Act - simulate request flow
        let root_span = tracer.start("http_request");
        let root_context = Context::current_with_span(root_span);
        
        // Simulate GraphQL resolver
        let graphql_span = tracer.start_with_context(
            "graphql_resolver",
            &root_context
        );
        let graphql_context = root_context.with_span(graphql_span);
        
        // Simulate database query
        let db_span = tracer.start_with_context(
            "database_query",
            &graphql_context
        );
        
        // Close spans
        db_span.end();
        graphql_context.span().end();
        root_context.span().end();
        
        // Assert - verify span hierarchy
        let spans = exporter.get_finished_spans();
        assert_eq!(spans.len(), 3);
        
        let db_span = spans.iter()
            .find(|s| s.name == "database_query")
            .unwrap();
        let graphql_span = spans.iter()
            .find(|s| s.name == "graphql_resolver")
            .unwrap();
        let root_span = spans.iter()
            .find(|s| s.name == "http_request")
            .unwrap();
        
        // Verify parent-child relationships
        assert_eq!(
            db_span.parent_span_id,
            graphql_span.span_context.span_id()
        );
        assert_eq!(
            graphql_span.parent_span_id,
            root_span.span_context.span_id()
        );
    }
}
```

*This test verifies that trace context properly propagates through multiple service layers, maintaining parent-child relationships between spans.*

#### Task 5.3.2: Implement OpenTelemetry Integration

⚡ **Performance Tip**: Use sampling to control costs - not every request needs to be traced

💡 **Junior Dev Tip**: The tracing-patterns.rs file has examples of proper span usage
   See: [../../.spec/examples/tracing-patterns.rs](../../.spec/examples/tracing-patterns.rs)

Set up OpenTelemetry with OTLP exporter, configure the trace pipeline with appropriate sampling, and integrate with the existing tracing subscriber. Ensure traces include both automatic instrumentation and custom spans.

**TDD Approach**: Implement the tracer setup to make propagation tests pass, then add span creation to key operations.

**OpenTelemetry setup with OTLP exporter:**
```rust
use opentelemetry::{global, KeyValue, runtime::TokioCurrentThread};
use opentelemetry_otlp::{OtlpExporterPipeline, WithExportConfig};
use opentelemetry_sdk::{
    trace::{self, RandomIdGenerator, Sampler},
    Resource,
};

pub fn init_tracer(config: &TracingConfig) -> Result<(), TraceError> {
    // Configure resource attributes
    let resource = Resource::new(vec![
        KeyValue::new("service.name", "pcf-api"),
        KeyValue::new("service.version", env!("CARGO_PKG_VERSION")),
        KeyValue::new("deployment.environment", &config.environment),
    ]);
    
    // Configure OTLP exporter
    let exporter = opentelemetry_otlp::new_exporter()
        .tonic()
        .with_endpoint(&config.otlp_endpoint)
        .with_timeout(Duration::from_secs(3));
    
    // Configure trace pipeline
    let trace_config = trace::config()
        .with_sampler(get_sampler(&config.sampling))
        .with_id_generator(RandomIdGenerator::default())
        .with_resource(resource);
    
    let tracer = opentelemetry_otlp::new_pipeline()
        .tracing()
        .with_exporter(exporter)
        .with_trace_config(trace_config)
        .install_batch(TokioCurrentThread)?;
    
    // Set global tracer
    global::set_tracer_provider(tracer.provider().unwrap());
    
    // Configure tracing subscriber with OpenTelemetry layer
    let telemetry_layer = tracing_opentelemetry::layer()
        .with_tracer(tracer);
    
    Registry::default()
        .with(telemetry_layer)
        .with(existing_layers) // JSON, sanitization, etc.
        .init();
    
    Ok(())
}

fn get_sampler(config: &SamplingConfig) -> Sampler {
    match config.strategy {
        SamplingStrategy::AlwaysOn => Sampler::AlwaysOn,
        SamplingStrategy::AlwaysOff => Sampler::AlwaysOff,
        SamplingStrategy::Probability(rate) => {
            Sampler::TraceIdRatioBased(rate)
        },
        SamplingStrategy::Adaptive => {
            // Custom sampler that adjusts based on load
            AdaptiveSampler::new(
                config.base_rate,
                config.peak_rate,
            )
        },
    }
}
```

*This configuration sets up OpenTelemetry with OTLP export, configurable sampling, and integration with the existing tracing infrastructure. The adaptive sampler helps control costs while maintaining visibility.*

#### Task 5.3.3: Instrument Key Operations with Spans

🔒 **Security Tip**: Never include sensitive data in span attributes - apply same sanitization as logs

⚡ **Performance Tip**: Be selective with spans in hot paths - tracing has overhead

Add detailed span instrumentation to critical paths: GraphQL resolvers (including field-level tracing), Database queries (with SQL sanitization), External API calls, Cache operations, and Authorization checks. Ensure all spans include appropriate attributes following OpenTelemetry semantic conventions.

**TDD Approach**: For each operation type, write tests first that verify span creation and attribute attachment.

**GraphQL resolver instrumentation:**
```rust
use async_graphql::{Context, Object, Result};
use opentelemetry::trace::{FutureExt, StatusCode, TraceContextExt};

#[Object]
impl UserQuery {
    #[tracing::instrument(
        name = "graphql.resolve_user",
        skip(self, ctx),
        fields(
            graphql.operation = "query",
            graphql.field = "user",
            user.id = %id,
            otel.kind = "server"
        )
    )]
    async fn user(
        &self,
        ctx: &Context<'_>,
        id: ID,
    ) -> Result<User> {
        let span = tracing::Span::current();
        
        // Add GraphQL-specific attributes
        span.record("graphql.document", &ctx.query_env.document);
        span.record("graphql.operation_name", &ctx.query_env.operation_name);
        
        // Authorization check with span
        let auth_result = async {
            check_user_permission(&ctx, &id).await
        }
        .instrument(tracing::info_span!("authorization.check"))
        .await?;
        
        // Database query with span
        let user = async {
            let pool = ctx.data::<DbPool>()?;
            
            let span = tracing::info_span!(
                "db.query",
                db.system = "surrealdb",
                db.operation = "select",
                db.statement = "SELECT * FROM user WHERE id = $id",
                otel.kind = "client"
            );
            
            sqlx::query_as!(User, 
                "SELECT * FROM user WHERE id = $1",
                id.as_str()
            )
            .fetch_one(pool)
            .instrument(span)
            .await
        }
        .await
        .map_err(|e| {
            span.record_error(&e);
            span.set_status(StatusCode::Error, "Database query failed");
            e
        })?;
        
        span.add_event(
            "user.loaded",
            vec![
                KeyValue::new("user.type", user.user_type.to_string()),
                KeyValue::new("user.active", user.is_active),
            ],
        );
        
        Ok(user)
    }
}
```

*This example shows comprehensive instrumentation of a GraphQL resolver with nested spans for authorization and database queries. Each span includes semantic attributes and proper error handling.*

---

### 🛑 CHECKPOINT 3: Distributed Tracing Review - STOP and request review before proceeding

**Deliverables:**
- OpenTelemetry integration with OTLP export
- Span instrumentation for all key operations
- Context propagation across async boundaries
- Sampling configuration with adaptive strategy
- All tracing tests passing

**Verification Steps:**
1. Run `just test-tracing` - all tests should pass
2. Start Jaeger UI with `just jaeger-up`
3. Make API requests and view traces in Jaeger
4. Verify parent-child span relationships
5. Check sampling is working (not all requests traced)

**Common Issues:**
- **Issue**: Spans not appearing in Jaeger
  **Solution**: Check OTLP endpoint configuration, verify Jaeger is running
- **Issue**: Broken trace context (orphan spans)
  **Solution**: Ensure context propagation in async spawns, use .instrument()
- **Issue**: High overhead from tracing
  **Solution**: Reduce sampling rate, remove spans from tight loops

**DO NOT PROCEED** until review is complete and approved.

---

### 5.4 Dashboards and Alerting (~400 lines, 8-10 files (mostly JSON/YAML))

**Work Unit Context:**
- **Complexity**: Low - Mostly configuration with some custom PromQL queries
- **Scope**: ~400 lines across 8-10 files (mostly JSON/YAML)
- **Key Components**:
  - Grafana dashboards (~200) - Visualize metrics with useful layouts
  - Prometheus alerts (~100) - Define alerting rules for critical conditions
  - Performance validation (~100) - Verify observability overhead is acceptable
- **Patterns**: PromQL queries, Dashboard as code, Alert routing
- **Required Algorithms**: Rate calculations, Percentile aggregations

#### Task 5.4.1: Create Grafana Dashboards

💡 **Junior Dev Tip**: Start with Grafana's dashboard templates and customize
   See: [https://grafana.com/grafana/dashboards](https://grafana.com/grafana/dashboards)

⚠️ **Warning Tip**: Avoid too many panels - focus on actionable metrics

Design and implement Grafana dashboards that provide actionable insights. Create an Overview Dashboard (Golden signals: latency, traffic, errors, saturation), Service Dashboard (GraphQL operations, database performance, cache hit rates), and Infrastructure Dashboard (Resource usage, connection pools, garbage collection).

**TDD Approach**: While dashboards aren't typically tested with TDD, create smoke tests that verify dashboard JSON is valid and queries are syntactically correct.

**Overview dashboard configuration:**
```json
{
  "dashboard": {
    "title": "PCF API Overview",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [{
          "expr": "sum(rate(http_requests_total[5m])) by (method)",
          "legendFormat": "{{method}}"
        }],
        "type": "graph",
        "yaxes": [{"format": "reqps"}]
      },
      {
        "title": "Error Rate",
        "targets": [{
          "expr": "sum(rate(http_requests_total{status_group=~\"4xx|5xx\"}[5m])) / sum(rate(http_requests_total[5m]))",
          "legendFormat": "Error %"
        }],
        "type": "singlestat",
        "format": "percentunit",
        "thresholds": "0.01,0.05",
        "colors": ["green", "yellow", "red"]
      },
      {
        "title": "P95 Latency",
        "targets": [{
          "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))",
          "legendFormat": "{{endpoint}}"
        }],
        "type": "graph",
        "yaxes": [{"format": "s"}],
        "alert": {
          "conditions": [{
            "evaluator": {"params": [1], "type": "gt"},
            "query": {"params": ["A", "5m", "now"]},
            "reducer": {"params": [], "type": "avg"}
          }],
          "name": "High P95 Latency"
        }
      }
    ]
  }
}
```

*This dashboard provides the 'golden signals' for monitoring service health. The error rate panel uses color coding for quick visual assessment, and the latency panel includes alerting configuration.*

#### Task 5.4.2: Configure Prometheus Alerting Rules

⚠️ **Warning Tip**: Avoid alert fatigue - only alert on actionable issues

💡 **Junior Dev Tip**: Test alerts in staging before production to tune thresholds

Define Prometheus alerting rules for critical conditions that require human intervention. Create alerts for: High error rates (>5% for 5 minutes), High latency (P95 > 1s), Resource exhaustion (memory > 90%, connection pool > 80%), Service degradation (circuit breaker open, database unavailable).

**TDD Approach**: Create unit tests that verify alert expressions are valid PromQL and produce expected results with test data.

**Critical alerting rules:**
```yaml
groups:
  - name: pcf_api_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status_group=~"4xx|5xx"}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) > 0.05
        for: 5m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} for the last 5 minutes"
          runbook_url: "https://docs.pcf.io/runbooks/high-error-rate"
      
      - alert: HighP95Latency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 1.0
        for: 5m
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "P95 latency exceeds 1 second"
          description: "95th percentile latency is {{ $value | humanizeDuration }}"
      
      - alert: DatabaseConnectionPoolExhaustion
        expr: |
          (
            db_connection_pool_used / db_connection_pool_size
          ) > 0.8
        for: 2m
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "Database connection pool near exhaustion"
          description: "Connection pool is {{ $value | humanizePercentage }} full"
          
      - alert: CircuitBreakerOpen
        expr: circuit_breaker_state{state="open"} == 1
        for: 1m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "Circuit breaker {{ $labels.name }} is open"
          description: "Service {{ $labels.service }} is experiencing failures"
```

*These alerting rules cover the most critical failure scenarios. Each alert includes metadata for routing and runbook links for incident response.*

#### Task 5.4.3: Validate Performance Impact

⚡ **Performance Tip**: Use sampling and batching to reduce overhead in production

⚠️ **Warning Tip**: Some overhead is acceptable for the visibility gained - find the right balance

Measure and document the performance overhead of observability instrumentation. Run benchmarks with and without telemetry enabled, measure memory overhead from metrics, assess CPU impact of logging and tracing, and optimize hot paths if overhead exceeds 5%.

**TDD Approach**: Write benchmarks that compare performance with telemetry on/off. Tests should fail if overhead exceeds acceptable thresholds.

**Performance overhead benchmark:**
```rust
#[cfg(test)]
mod performance_tests {
    use criterion::{black_box, criterion_group, criterion_main, Criterion};
    
    fn benchmark_with_telemetry(c: &mut Criterion) {
        let runtime = tokio::runtime::Runtime::new().unwrap();
        
        c.bench_function("api_request_with_telemetry", |b| {
            b.to_async(&runtime).iter(|| async {
                // Simulate API request with all telemetry enabled
                let response = client
                    .post("/graphql")
                    .json(&json!({
                        "query": "{ user(id: 1) { name email } }"
                    }))
                    .send()
                    .await
                    .unwrap();
                    
                black_box(response);
            });
        });
    }
    
    fn benchmark_without_telemetry(c: &mut Criterion) {
        // Disable all telemetry
        std::env::set_var("TELEMETRY_DISABLED", "true");
        let runtime = tokio::runtime::Runtime::new().unwrap();
        
        c.bench_function("api_request_without_telemetry", |b| {
            b.to_async(&runtime).iter(|| async {
                // Same request without telemetry
                let response = client
                    .post("/graphql")
                    .json(&json!({
                        "query": "{ user(id: 1) { name email } }"
                    }))
                    .send()
                    .await
                    .unwrap();
                    
                black_box(response);
            });
        });
    }
    
    criterion_group!(
        benches,
        benchmark_with_telemetry,
        benchmark_without_telemetry
    );
    criterion_main!(benches);
}

// Overhead calculation script
#[test]
fn verify_overhead_acceptable() {
    let with_telemetry = run_benchmark("api_request_with_telemetry");
    let without_telemetry = run_benchmark("api_request_without_telemetry");
    
    let overhead_percent = 
        ((with_telemetry - without_telemetry) / without_telemetry) * 100.0;
    
    println!("Telemetry overhead: {:.2}%", overhead_percent);
    
    assert!(
        overhead_percent < 5.0,
        "Telemetry overhead {:.2}% exceeds 5% limit",
        overhead_percent
    );
}
```

*These benchmarks measure the real performance impact of observability. The test ensures overhead stays within acceptable limits, failing the build if it exceeds 5%.*

---

### 🛑 CHECKPOINT 4: Complete Observability Review - STOP and request final review

**Deliverables:**
- Grafana dashboards provisioned and functional
- Prometheus alerting rules configured
- Performance overhead verified <5%
- All observability tests passing
- Documentation for dashboard usage and alert response

**Verification Steps:**
1. Access Grafana dashboards and verify data is populating
2. Trigger test alerts and verify they fire correctly
3. Run performance benchmarks: `just bench-overhead`
4. Execute security scan: `just scan-telemetry-security`
5. Review sample of logs/metrics/traces for sensitive data

**Common Issues:**
- **Issue**: Dashboards show 'No Data'
  **Solution**: Verify Prometheus is scraping metrics endpoint, check metric names match queries
- **Issue**: Alerts not firing when expected
  **Solution**: Check alert expressions with promtool, verify 'for' duration isn't too long
- **Issue**: Performance overhead too high
  **Solution**: Increase sampling rates, reduce cardinality, optimize hot path instrumentation

**DO NOT PROCEED** until review is complete and approved.

---

## Troubleshooting

Observability implementation can surface unique challenges. This section covers the most common issues and their solutions:

### Metrics Issues
- **Symptom**: Prometheus returns 'out of memory' errors
    - **Cause**: Cardinality explosion from unbounded labels
    - **Solution**: Review metric labels, implement cardinality limiting, use label normalization
- **Symptom**: Metrics endpoint response time increasing
    - **Cause**: Too many metric series being tracked
    - **Solution**: Implement metric expiry, reduce histogram buckets, aggregate before exposing

### Logging Issues
- **Symptom**: Logs missing important context
    - **Cause**: Span not properly propagated
    - **Solution**: Ensure .instrument() is used for async operations, check middleware ordering
- **Symptom**: Log volume overwhelming storage
    - **Cause**: Debug logging enabled in production
    - **Solution**: Implement dynamic log levels, use sampling for verbose components

### Tracing Issues
- **Symptom**: Traces show orphaned spans
    - **Cause**: Context lost across async boundaries
    - **Solution**: Use opentelemetry::Context::current_with_span() when spawning tasks
- **Symptom**: Trace export failing intermittently
    - **Cause**: OTLP endpoint unreachable or timing out
    - **Solution**: Implement retry logic, use batch processor, increase timeout

### Escalation Path
If blocked for more than 2 hours on any observability issue
**Documentation Requirements:**
- Document the specific error messages or symptoms
- Include relevant configuration and code snippets
- Provide metrics/logs/traces showing the issue
- List troubleshooting steps already attempted

## Security Requirements

**Observability systems have access to all data flowing through the application, making them a critical security concern. A single misconfiguration can leak sensitive data to logs or metrics that are often stored for long periods.**

### Data Sanitization
- **MUST NOT**: Log passwords, tokens, API keys, or authentication headers
    - *Rationale*: Authentication credentials in logs can lead to account compromise
- **MUST NOT**: Include PII (emails, SSNs, credit cards) in metrics labels
    - *Rationale*: Metrics are often retained indefinitely and difficult to purge
- **MUST**: Sanitize SQL queries in traces before recording
    - *Rationale*: SQL queries may contain sensitive data in WHERE clauses
- **SHOULD**: Hash user IDs in metrics labels
    - *Rationale*: Allows correlation while maintaining privacy

**Implementation**: Use the sanitization layer for all telemetry output. When in doubt, redact rather than expose. Test sanitization with real-world data patterns.
**Testing**: Create test cases with known sensitive patterns and verify they're sanitized in all telemetry outputs

### Access Control
- **MUST**: Protect /metrics endpoint with authentication in production
    - *Rationale*: Metrics can reveal system architecture and usage patterns
- **MUST**: Use TLS for OTLP trace export
    - *Rationale*: Traces contain detailed application behavior
- **SHOULD**: Implement RBAC for dashboard access
    - *Rationale*: Different roles need different levels of visibility

**Implementation**: Use existing authentication middleware for metrics endpoint. Configure OTLP exporter with TLS certificates.
**Testing**: Verify endpoints require authentication, test TLS configuration with openssl

### Data Retention
- **MUST**: Configure retention policies for all telemetry data
    - *Rationale*: Compliance requirements and storage costs
- **SHOULD**: Implement shorter retention for high-cardinality data
    - *Rationale*: Reduces both cost and privacy risk

**Implementation**: Configure Prometheus retention, implement log rotation, set trace sampling to control volume
**Testing**: Verify retention policies are applied, test data is purged after retention period

## Junior Developer Learning Path

**Target Audience**: Developers new to observability or the specific tools used

Observability can be overwhelming with its three pillars and numerous tools. Follow this structured path to build understanding progressively:

### Step 1: Observability Fundamentals
- **Resources**: Observability Tutorial, Three Pillars Overview
- **Time**: 2 hours
- **Practice**: Set up local Prometheus and Grafana, explore existing dashboards

### Step 2: Metrics Deep Dive
- **Resources**: Prometheus Metrics Guide, Cardinality Control Guide
- **Time**: 4 hours
- **Practice**: Implement a custom metric with proper labels and test cardinality limits

### Step 3: Structured Logging
- **Resources**: Structured Logging Guide, Log Sanitization Patterns
- **Time**: 3 hours
- **Practice**: Add structured logging to a sample application with sanitization

### Step 4: Distributed Tracing
- **Resources**: OpenTelemetry Tracing Guide, Context Propagation
- **Time**: 4 hours
- **Practice**: Trace a request through multiple services, view in Jaeger

### Step 5: Production Practices
- **Resources**: Performance Optimization, Security Considerations
- **Time**: 2 hours
- **Practice**: Measure overhead, implement sampling, secure endpoints

### Remember:
- ⚠️ Cardinality explosion can crash Prometheus - always limit labels
- ⚠️ Sensitive data in logs is a compliance violation - sanitize everything
- ⚠️ Observability has overhead - measure impact and optimize hot paths
- ⚠️ Broken traces are worse than no traces - test context propagation thoroughly

## Next Phase Preview

### Phase 6: Performance Optimization

With comprehensive observability in place, Phase 6 focuses on using the telemetry data to optimize performance. This includes implementing DataLoader for N+1 query prevention, response caching strategies, connection pool tuning, and load testing to identify bottlenecks.

**Key Features:**
- DataLoader pattern for batching database queries
- Multi-layer caching with Redis
- Connection pool optimization based on metrics
- Load testing with realistic scenarios
- Performance regression detection

---

*Generated on 2025-07-28 by Phase Plan Generator v2*