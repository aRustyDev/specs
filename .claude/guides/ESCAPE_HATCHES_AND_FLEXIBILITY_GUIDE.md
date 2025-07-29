# Escape Hatches and Flexibility Guide

This guide explains how escape hatches and flexible implementations work with the document generation system, and how Claude Code should document them.

## Overview

The document generator provides **structured flexibility** while **escape hatches remain Claude Code's responsibility**. This separation ensures:

- Standard paths are clear and well-documented
- Edge cases are visible, not hidden
- Alternative approaches are consistently formatted
- Future developers understand both the ideal and the practical

## Division of Responsibilities

### Generator's Role (Structured Flexibility)

The generator handles:
- **Optional sections** - Include only when needed
- **Conditional content** - Show/hide based on config
- **Multiple alternatives** - Format arrays of options
- **Nested complexity** - Support arbitrary depth

### Claude Code's Role (Escape Hatch Decisions)

Claude Code handles:
- **Identifying** when standard approach won't work
- **Designing** appropriate workarounds
- **Documenting** escape hatches in config
- **Justifying** why they're necessary

## Patterns for Documenting Escape Hatches

### Pattern 1: Discovery Documentation

When Claude Code discovers unexpected requirements during implementation:

```json
{
  "work_breakdown": [{
    "section_number": "3.2",
    "title": "GraphQL Implementation",
    "tasks": [{
      "number": "3.2.1",
      "title": "Implement Subscription Support",
      "description": "Add real-time subscription capabilities using WebSockets",
      "special_considerations": [
        "DISCOVERED: Load balancer doesn't support WebSocket protocol",
        "ESCAPE HATCH: Implemented SSE (Server-Sent Events) as fallback",
        "JUSTIFICATION: SSE provides similar real-time capabilities without WebSocket requirement",
        "TRADEOFF: Client can't send messages back through same connection"
      ],
      "code_examples": [{
        "purpose": "SSE fallback implementation",
        "language": "rust",
        "code": "// When WebSocket upgrade fails, fallback to SSE\nif !supports_websocket(&request) {\n    return serve_sse_endpoint(request).await;\n}",
        "explanation": "Automatic fallback ensures real-time features work in all environments"
      }]
    }]
  }]
}
```

This generates clear documentation:

```markdown
#### Task 3.2.1: Implement Subscription Support

Add real-time subscription capabilities using WebSockets

**Special Considerations:**
- DISCOVERED: Load balancer doesn't support WebSocket protocol
- ESCAPE HATCH: Implemented SSE (Server-Sent Events) as fallback
- JUSTIFICATION: SSE provides similar real-time capabilities without WebSocket requirement
- TRADEOFF: Client can't send messages back through same connection

**SSE fallback implementation:**
```rust
// When WebSocket upgrade fails, fallback to SSE
if !supports_websocket(&request) {
    return serve_sse_endpoint(request).await;
}
```

*Automatic fallback ensures real-time features work in all environments*
```

### Pattern 2: Security Escape Hatches

For security requirements that need emergency overrides:

```json
{
  "security_requirements": {
    "categories": [{
      "name": "Data Sanitization",
      "requirements": [{
        "type": "MUST",
        "requirement": "Sanitize all user input before logging",
        "rationale": "Prevent log injection attacks"
      }],
      "escape_hatches": [{
        "scenario": "Production debugging of authentication failures",
        "trigger": "When auth success rate drops below 90%",
        "temporary_override": {
          "action": "Enable verbose auth logging with raw inputs",
          "safeguards": [
            "Requires security team approval via break-glass process",
            "Automatically disables after 4 hours",
            "Logs written to separate, encrypted file",
            "Must file incident report within 24 hours"
          ],
          "implementation_file": "src/security/emergency_auth_logging.rs"
        }
      }]
    }]
  }
}
```

### Pattern 3: Performance Trade-offs

When performance requirements conflict with other needs:

```json
{
  "performance_considerations": [{
    "area": "Query Performance",
    "primary_requirement": "All queries must complete in <100ms",
    "escape_hatches": [{
      "condition": "Complex authorization checks",
      "alternative": {
        "approach": "Cache authorization results for 5 minutes",
        "performance_impact": "Reduces auth queries by 95%",
        "security_tradeoff": "5-minute window where revoked permissions still work",
        "mitigation": "Critical operations always check fresh"
      }
    }, {
      "condition": "Full-text search on large datasets",
      "alternative": {
        "approach": "Asynchronous search with progress updates",
        "implementation": "Return job ID immediately, poll for results",
        "user_experience": "Shows progress bar instead of blocking"
      }
    }]
  }]
}
```

### Pattern 4: Alternative Implementation Paths

For features with multiple valid approaches:

```json
{
  "implementation_options": {
    "feature": "Rate Limiting",
    "approaches": [{
      "name": "Token Bucket (Recommended)",
      "when_to_use": "Standard case - predictable traffic",
      "pros": ["Simple", "Well-understood", "Good burst handling"],
      "cons": ["Memory per user", "Not distributed-friendly"],
      "implementation": "src/middleware/token_bucket.rs"
    }, {
      "name": "Sliding Window",
      "when_to_use": "Need precise rate enforcement",
      "pros": ["More accurate", "No burst issues"],
      "cons": ["Higher CPU usage", "Complex implementation"],
      "implementation": "src/middleware/sliding_window.rs"
    }, {
      "name": "Redis-backed Distributed",
      "when_to_use": "Multi-instance deployment",
      "pros": ["Scales horizontally", "Shared state"],
      "cons": ["Redis dependency", "Network latency"],
      "implementation": "src/middleware/redis_rate_limit.rs",
      "escape_hatch": {
        "scenario": "Redis unavailable",
        "fallback": "Local token bucket with 2x conservative limits"
      }
    }]
  }
}
```

## Best Practices for Escape Hatches

### 1. Document at Discovery Time

When Claude Code encounters an unexpected requirement:

```json
{
  "tasks": [{
    "title": "Standard implementation task",
    "discovered_issues": [{
      "timestamp": "2024-03-14",
      "issue": "Framework doesn't support required feature",
      "escape_hatch": "Custom implementation",
      "justification": "No alternative available",
      "review_status": "Approved by tech lead"
    }]
  }]
}
```

### 2. Make Trade-offs Explicit

Always document what you're giving up:

```json
{
  "escape_hatch": {
    "solution": "Skip validation for admin users",
    "tradeoffs": {
      "security": "Admins could accidentally corrupt data",
      "performance": "Saves 200ms per request",
      "maintenance": "Special case adds complexity"
    },
    "acceptance_criteria": "Product team approved this trade-off"
  }
}
```

### 3. Include Sunset Plans

Escape hatches should be temporary when possible:

```json
{
  "temporary_workarounds": [{
    "issue": "Database doesn't support JSON columns",
    "workaround": "Store JSON as text with manual parsing",
    "sunset_plan": {
      "trigger": "When we upgrade to PostgreSQL 12+",
      "target_date": "Q2 2025",
      "migration_script": "migrations/json_column_upgrade.sql"
    }
  }]
}
```

### 4. Group Related Escape Hatches

Keep similar workarounds together:

```json
{
  "legacy_system_adaptations": {
    "description": "Workarounds for legacy system integration",
    "escape_hatches": [{
      "component": "Authentication",
      "issue": "Legacy uses MD5 passwords",
      "solution": "Dual-hash with migration flag"
    }, {
      "component": "API Format",
      "issue": "Legacy expects XML",
      "solution": "XML adapter layer"
    }]
  }
}
```

## Common Escape Hatch Scenarios

### Infrastructure Limitations

```json
{
  "infrastructure_constraints": [{
    "constraint": "Kubernetes ingress doesn't support WebSockets",
    "escape_hatches": [{
      "name": "Direct node port",
      "description": "Bypass ingress for WebSocket connections",
      "configuration": "See k8s/websocket-nodeport.yaml"
    }, {
      "name": "Long polling fallback",
      "description": "Detect and fallback automatically",
      "implementation": "src/realtime/long_polling.rs"
    }]
  }]
}
```

### Third-Party API Limitations

```json
{
  "external_dependencies": [{
    "service": "Payment Provider API",
    "limitation": "Max 10 requests per second",
    "escape_hatches": [{
      "name": "Request batching",
      "description": "Batch up to 50 payments per request",
      "delay_impact": "Up to 5 second delay for single payments"
    }, {
      "name": "Queue with retry",
      "description": "Async processing with exponential backoff",
      "sla_impact": "Payment confirmation now async"
    }]
  }]
}
```

### Compliance Requirements

```json
{
  "compliance_adaptations": [{
    "regulation": "GDPR",
    "requirement": "Data deletion within 30 days",
    "standard_approach": "Hard delete from all systems",
    "escape_hatch": {
      "scenario": "Legal hold requirement conflicts",
      "solution": "Anonymize instead of delete",
      "approval": "Legal team memo 2024-03-14",
      "implementation": "src/gdpr/legal_hold_adapter.rs"
    }
  }]
}
```

## Anti-Patterns to Avoid

### 1. Hidden Escape Hatches

❌ **Bad**: Implementing workarounds without documentation
```rust
// Mysterious code with no explanation
if user.id == 12345 {
    skip_validation();  // Why?
}
```

✅ **Good**: Document in the plan config
```json
{
  "known_issues": [{
    "description": "User 12345 has legacy data that fails validation",
    "escape_hatch": "Skip validation for this specific user",
    "ticket": "LEGACY-4567",
    "sunset": "After data migration in Q3"
  }]
}
```

### 2. Permanent "Temporary" Solutions

❌ **Bad**: Escape hatches with no end plan
```json
{
  "workaround": "TODO: Fix this later"
}
```

✅ **Good**: Clear sunset criteria
```json
{
  "temporary_workaround": {
    "solution": "Manual cache invalidation",
    "sunset_trigger": "When distributed cache supports TTL",
    "tracking_issue": "INFRA-789"
  }
}
```

### 3. Undocumented Trade-offs

❌ **Bad**: Solution without consequences
```json
{
  "optimization": "Cache everything for 1 hour"
}
```

✅ **Good**: Explicit trade-offs
```json
{
  "optimization": {
    "approach": "Cache everything for 1 hour",
    "benefits": "99% cache hit rate, 10x performance",
    "risks": "Stale data visible for up to 1 hour",
    "mitigation": "Manual cache purge endpoint for critical updates"
  }
}
```

## Integration with Generator

The generator handles these patterns by:

1. **Recognizing escape hatch fields** in any section
2. **Formatting them prominently** with appropriate warnings
3. **Maintaining structure** even with complex alternatives
4. **Generating readable output** regardless of complexity

Example generator output for escape hatches:

```markdown
### Authentication Implementation

Standard OAuth2 flow with PKCE...

⚠️ **Infrastructure Limitation Detected**

**Issue**: Load balancer strips Authorization headers
**Escape Hatch**: Pass auth token in custom X-Auth-Token header
**Implementation**: See `src/auth/header_adapter.rs`
**Sunset Plan**: Remove when LB upgraded to v2.0 (Q4 2024)

This workaround is necessary because...
```

## Summary

The key to successful escape hatch documentation is:

1. **Claude Code identifies and documents** edge cases in the config
2. **Generator formats them consistently** and prominently
3. **Both paths are equally visible** in the final document
4. **Trade-offs are explicit** and justified
5. **Sunset plans exist** where possible

This approach ensures that:
- Nothing is hidden or surprising
- Future developers understand why
- Technical debt is tracked
- Standard and escape paths are both first-class citizens

Remember: The best escape hatch is one that's well-documented, justified, and temporary.