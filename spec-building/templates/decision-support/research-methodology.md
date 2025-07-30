# Comprehensive Research Methodology

## Research Philosophy
Every architectural and technical decision must be grounded in evidence, not opinion. Research should be exhaustive enough to support confident decisions while time-boxed to prevent analysis paralysis.

## Research Domain Framework

### 1. Architecture Pattern Research

#### Research Objectives
- Identify proven patterns for our specific domain
- Understand failure modes and limitations
- Quantify performance characteristics
- Assess organizational fit

#### Research Sources
1. **Academic Sources**
   - IEEE/ACM digital libraries
   - Architecture conference proceedings
   - Peer-reviewed case studies

2. **Industry Sources**
   - High-scale engineering blogs (Netflix, Uber, Airbnb)
   - Cloud provider architecture centers
   - Open-source project architectures

3. **Vendor Resources**
   - Reference architectures
   - White papers (read critically)
   - Customer case studies

#### Research Deliverables
```markdown
## Architecture Option: [Pattern Name]

### Overview
- Pattern description
- Primary use cases
- Theoretical foundation

### Production Evidence
- Company A: Scale, duration, outcomes
- Company B: Scale, duration, outcomes
- Company C: Scale, duration, outcomes

### Performance Characteristics
- Latency: p50, p95, p99
- Throughput: requests/second
- Scalability: horizontal/vertical limits
- Resource efficiency: CPU/memory/network

### Failure Modes
1. Failure type → Impact → Recovery
2. Failure type → Impact → Recovery

### Implementation Complexity
- Team expertise required
- Development time estimate
- Operational overhead
- Maintenance burden

### Cost Model
- Development cost
- Infrastructure cost
- Operational cost
- Scaling cost curve

### Fitness Score
- Requirement alignment: X/10
- Team capability: X/10
- Risk level: X/10
- Future flexibility: X/10
```

### 2. Technology Stack Research

#### Evaluation Framework
For each technology component:

```yaml
technology_evaluation:
  metadata:
    name: 
    version:
    license:
    vendor:
  
  maturity:
    first_release:
    current_version:
    release_frequency:
    breaking_changes:
  
  adoption:
    github_stars:
    production_users:
    fortune_500_users:
    community_size:
  
  ecosystem:
    package_count:
    integration_availability:
    tooling_support:
    ide_support:
  
  performance:
    benchmarks:
      - source:
        results:
    real_world_numbers:
    scaling_characteristics:
  
  reliability:
    known_issues:
    stability_track_record:
    disaster_recovery:
  
  security:
    cve_history:
    security_model:
    audit_results:
    compliance_certs:
  
  cost:
    license_cost:
    support_cost:
    training_cost:
    migration_cost:
  
  risks:
    vendor_lock_in:
    skill_availability:
    long_term_viability:
    technical_debt:
```

#### Comparison Matrix
| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| Performance | 25% | Benchmark data | Benchmark data | Benchmark data |
| Reliability | 20% | Uptime stats | Uptime stats | Uptime stats |
| Ecosystem | 15% | Package count | Package count | Package count |
| Cost | 15% | TCO calculation | TCO calculation | TCO calculation |
| Team Fit | 15% | Skill assessment | Skill assessment | Skill assessment |
| Future Proof | 10% | Trend analysis | Trend analysis | Trend analysis |

### 3. Infrastructure Research

#### Cloud Provider Analysis
```markdown
## Provider Evaluation: [AWS/Azure/GCP/Other]

### Service Mapping
| Our Need | Provider Service | Limits | Costs |
|----------|-----------------|--------|-------|
| Compute | EC2/VM/GCE | vCPU, memory | $/hour |
| Storage | S3/Blob/GCS | Size, IOPS | $/GB/month |
| Database | RDS/CosmosDB/Cloud SQL | Connections, size | $/hour + storage |

### Regional Availability
- Primary region: Availability, latency to users
- DR region: Distance, replication costs
- Edge locations: CDN presence

### Compliance/Certification
- [ ] SOC2
- [ ] ISO 27001
- [ ] HIPAA
- [ ] PCI DSS
- [ ] Region-specific

### Cost Optimization
- Reserved instance savings: X%
- Spot instance availability: Use cases
- Volume discounts: Thresholds
- Free tier: What's included

### Migration Support
- Tools available
- Professional services
- Partner ecosystem
- Training resources
```

### 4. Tool Ecosystem Research

#### Development Tools
| Category | Options | Evaluation | Recommendation |
|----------|---------|------------|----------------|
| IDE | VS Code, IntelliJ, etc | Features, plugins | Team preference |
| Version Control | Git platforms | Features, limits | Integration needs |
| CI/CD | Jenkins, GH Actions, etc | Capabilities, cost | Workflow fit |
| Testing | Framework options | Coverage, speed | Language fit |
| Monitoring | APM solutions | Features, cost | Scale appropriate |

#### Operational Tools
- Logging: Centralized solutions
- Metrics: Time-series databases
- Tracing: Distributed tracing
- Alerting: Incident management
- Security: Scanning tools

### 5. Domain-Specific Research

#### Industry Standards
Research applicable standards:
- Data formats (HL7, FHIR, etc.)
- Protocols (OAuth, SAML, etc.)
- Compliance (GDPR, CCPA, etc.)
- Best practices (OWASP, etc.)

#### Competitor Analysis
```markdown
## Competitor: [Name]

### Technical Approach
- Architecture: [Microservices/Monolith/etc]
- Tech stack: [Languages, frameworks]
- Infrastructure: [Cloud/On-prem]

### Scale Metrics
- Users: X million
- Requests/day: Y million
- Data volume: Z TB

### Public Information
- Engineering blog posts
- Conference talks
- Open source contributions
- Job postings (tech requirements)

### Lessons Learned
- What works well
- Known pain points
- Migration stories
- Scaling challenges
```

## Research Execution Framework

### 1. Planning Phase
```yaml
research_plan:
  time_budget: X hours
  parallel_tracks:
    - track: Architecture
      owner: Agent A
      time: 2 hours
    - track: Technology
      owner: Agent B  
      time: 2 hours
    - track: Infrastructure
      owner: Agent C
      time: 1 hour
  
  success_criteria:
    min_options: 3 per category
    evidence_quality: High for top choice
    confidence_level: >80%
```

### 2. Execution Protocol

#### For Each Research Track:
1. **Define Questions**
   - What must we know?
   - What would be nice to know?
   - What can we defer?

2. **Source Priority**
   - Primary: Direct experience/benchmarks
   - Secondary: Case studies/documentation
   - Tertiary: Vendor claims/marketing

3. **Evidence Collection**
   ```markdown
   ## Finding: [Specific Claim]
   
   Source: [URL/Reference]
   Date: [When published]
   Credibility: [High/Medium/Low]
   
   Evidence:
   - Data point 1
   - Data point 2
   
   Caveats:
   - Limitation 1
   - Assumption 1
   ```

4. **Contradiction Resolution**
   When sources conflict:
   - Document both viewpoints
   - Seek third source
   - Apply critical thinking
   - Note uncertainty

### 3. Synthesis Phase

#### Pattern Recognition
Look for:
- Consistent themes across sources
- Common failure patterns
- Emerging trends
- Industry convergence

#### Decision Support Package
Create for each major decision:
1. Executive summary (1 page)
2. Detailed comparison matrix
3. Evidence appendix
4. Risk analysis
5. Recommendation with confidence level

## Research Quality Assurance

### Evidence Hierarchy
1. **Tier 1**: Our own benchmarks/tests
2. **Tier 2**: Published benchmarks with methodology
3. **Tier 3**: Production case studies with metrics
4. **Tier 4**: Documentation/specifications
5. **Tier 5**: Blog posts/opinions

### Bias Detection
Check for:
- Vendor bias in sources
- Selection bias in examples
- Survivorship bias in case studies
- Recency bias in technology
- Confirmation bias in search

### Research Validation
- [ ] Multiple independent sources agree
- [ ] Evidence covers success AND failure
- [ ] Methodology transparent
- [ ] Results reproducible
- [ ] Applies to our context

## Anti-Pattern Detection

### Research Anti-Patterns to Avoid
1. **Resume-Driven Development**: Choosing tech for career
2. **Hype-Driven Selection**: Latest != Best
3. **Big Company Cargo Cult**: Netflix scale != Our scale
4. **Analysis Paralysis**: Perfect information impossible
5. **Single Source Truth**: Vendor white papers

### Red Flags in Research
- Only positive case studies
- No failure modes discussed
- Vague performance claims
- Hidden costs/limitations
- Too good to be true

## Research Output Standards

### Documentation Requirements
Every research conclusion must include:
- Question answered
- Evidence summary
- Confidence level (%)
- Assumptions made
- Expiration date (when to re-research)

### Traceability
- Decision → Research → Evidence → Source
- Alternative considered → Why rejected
- Uncertainty → Mitigation plan

## Continuous Learning
- Document lessons learned
- Update research templates
- Build internal knowledge base
- Share findings across teams