# Estimation Calibration System

## Overview
This system helps teams improve estimation accuracy over time by tracking actual vs. estimated effort and identifying patterns in estimation errors.

## Estimation Tracking Template

### Project Information
```markdown
Project: [Name]
Type: [Web App/Library/CLI/Service/Other]
Complexity: [Simple/Medium/Complex/Enterprise]
Team Size: [Number]
Start Date: [Date]
```

### Phase Estimation Tracking

| Phase | Original Estimate | Actual Effort | Variance | Complexity Factor | Notes |
|-------|------------------|---------------|----------|-------------------|-------|
| Spec Creation | 25 hours | 32 hours | +28% | Complex domain | Stakeholder availability issues |
| Quality Review | 10 hours | 8 hours | -20% | Standard | Well-prepared team |
| Roadmap | 8 hours | 12 hours | +50% | Many dependencies | Underestimated analysis |
| Phase 1 Planning | 4 hours | 4.5 hours | +12.5% | Standard | Good estimate |

### Work Unit Tracking

| Task | Estimated WU | Actual WU | Variance | Category | Lessons |
|------|--------------|-----------|----------|----------|---------|
| Dependency Analysis | 3 WU | 5 WU | +66% | Analysis | Need better tools |
| API Design | 5 WU | 4 WU | -20% | Design | Template helped |
| Test Writing | 8 WU | 10 WU | +25% | Development | Complex edge cases |

## Calibration Factors

### By Project Type

| Project Type | Historical Multiplier | Confidence | Sample Size |
|--------------|----------------------|------------|-------------|
| Web Application | 1.15x | High | 23 projects |
| Microservice | 1.05x | High | 18 projects |
| Library/Package | 0.95x | Medium | 12 projects |
| CLI Tool | 0.90x | Medium | 8 projects |
| Enterprise Integration | 1.45x | High | 15 projects |
| Greenfield | 1.20x | High | 20 projects |
| Brownfield/Legacy | 1.60x | High | 14 projects |

### By Complexity Factors

| Factor | Impact | When to Apply |
|--------|--------|---------------|
| New Technology | +30% | Team using tech for first time |
| Integration Heavy | +25% | >5 external systems |
| Regulatory Compliance | +40% | HIPAA, PCI, SOX required |
| Multi-team Coordination | +20% | >3 teams involved |
| Unclear Requirements | +35% | Spec score <75 |
| Performance Critical | +25% | Sub-second response required |
| High Availability | +20% | >99.9% uptime required |
| Data Migration | +30% | Existing data to migrate |

### By Team Experience

| Team Profile | Multiplier | Description |
|--------------|------------|-------------|
| Senior Team (>5 years avg) | 0.85x | Experienced with tech stack |
| Mixed Team | 1.00x | Balance of senior/junior |
| Junior Heavy | 1.30x | Majority <2 years experience |
| New Team | 1.25x | Haven't worked together |
| Domain Experts | 0.90x | Know the business domain |
| New Domain | 1.35x | Learning domain + building |

## Estimation Formula

```
Adjusted Estimate = Base Estimate 
                   × Project Type Multiplier 
                   × (1 + Sum of Complexity Factors) 
                   × Team Experience Multiplier
                   × Historical Accuracy Factor
```

### Example Calculation
```
Base Estimate: 100 hours
Project Type: Web Application (1.15x)
Complexity Factors: 
  - New Technology (+30%)
  - Integration Heavy (+25%)
  - Sum = 55% → 1.55
Team: Mixed Team (1.00x)
Historical Accuracy: Team typically underestimates by 10% (1.10x)

Adjusted = 100 × 1.15 × 1.55 × 1.00 × 1.10 = 196 hours
```

## Historical Patterns

### Common Underestimation Areas
1. **Integration Testing**: Typically 40% under
   - **Fix**: Always add integration test phase
   - **Buffer**: +2-3 days for complex integrations

2. **Documentation**: Typically 60% under
   - **Fix**: Include as explicit task
   - **Buffer**: 10% of development time minimum

3. **Code Reviews**: Often omitted entirely
   - **Fix**: Add 1 hour per 8 hours coding
   - **Buffer**: Include in each checkpoint

4. **Deployment/DevOps**: Typically 50% under
   - **Fix**: Separate DevOps planning session
   - **Buffer**: +20% for first deployment

5. **Stakeholder Communication**: Rarely estimated
   - **Fix**: Add 2-4 hours per week
   - **Buffer**: Include in PM allocation

### Common Overestimation Areas
1. **CRUD Operations**: Typically 20% over
   - **Reality**: Well-understood, good tools
   - **Adjust**: -20% for standard CRUD

2. **Report Generation**: Typically 30% over
   - **Reality**: Good libraries available
   - **Adjust**: -25% with template tools

## Continuous Improvement Process

### Monthly Calibration Review
1. **Collect Data**
   - All completed phases
   - Actual vs estimated
   - Identify outliers

2. **Analyze Patterns**
   ```markdown
   ## Monthly Analysis: [Month/Year]
   
   ### Accuracy Metrics
   - Overall Accuracy: XX% (Target: ±15%)
   - Underestimation Rate: XX%
   - Overestimation Rate: XX%
   
   ### Patterns Identified
   - [Pattern 1]: [Description]
   - [Pattern 2]: [Description]
   
   ### Calibration Adjustments
   - [Factor]: Changed from X to Y
   - [New Factor]: Added based on data
   ```

3. **Update Factors**
   - Adjust multipliers based on data
   - Add new factors if patterns emerge
   - Remove factors that don't correlate

4. **Communicate Changes**
   - Update this document
   - Team training on new factors
   - Update estimation tools

### Estimation Confidence Levels

| Confidence | Criteria | Buffer to Add |
|------------|----------|---------------|
| High (90%) | Done similar 5+ times | +10% |
| Medium (70%) | Done similar 2-3 times | +25% |
| Low (50%) | First time, but researched | +50% |
| Very Low (30%) | Unknown unknowns | +100% or T-shirt size |

## Quick Reference Card

### For New Estimates:
1. Start with base estimate (hours or WU)
2. Identify project type → apply multiplier
3. Check each complexity factor → add percentages
4. Assess team experience → apply multiplier
5. Check team's historical accuracy → final adjustment
6. Add confidence-based buffer
7. Round up to nearest half-day

### Red Flags Requiring Re-estimation:
- Requirements change >20%
- New integration discovered
- Team composition changes significantly
- Technology choice changes
- Compliance requirements added

## Tools and Automation

### Estimation Spreadsheet Template
```
[Available at: /tools/estimation-calculator.xlsx]
- Enter base estimates
- Check applicable factors
- Automatic calculation
- Historical data tracking
```

### Tracking Script
```python
# Simple tracking example
def track_estimation(phase, estimated, actual):
    variance = (actual - estimated) / estimated * 100
    
    # Log to CSV
    with open('estimation_history.csv', 'a') as f:
        f.write(f"{date},{phase},{estimated},{actual},{variance}\n")
    
    # Alert if variance > 25%
    if abs(variance) > 25:
        alert_team(f"Large variance in {phase}: {variance}%")
```

## Key Takeaways

1. **Track Everything**: Can't improve what you don't measure
2. **Adjust Regularly**: Monthly calibration minimum
3. **Be Honest**: Accurate data more important than looking good
4. **Buffer Appropriately**: Confidence level should drive buffer size
5. **Learn from Patterns**: Same mistakes = process problem

Remember: Perfect estimates are impossible, but we can get consistently closer with good data and regular calibration.