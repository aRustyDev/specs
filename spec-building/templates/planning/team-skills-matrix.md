# Team Skills Matrix Template

## Overview
This matrix helps assess team capabilities against project requirements, identify gaps, and plan for training or hiring needs.

## Instructions
1. List all required skills for the project
2. Rate each team member's proficiency (0-5 scale)
3. Identify critical gaps
4. Plan mitigation strategies

## Proficiency Scale
- **0**: No experience
- **1**: Aware (has read about it)
- **2**: Novice (tutorial/training completed)
- **3**: Intermediate (1-2 projects)
- **4**: Advanced (3+ projects, can mentor)
- **5**: Expert (recognized expertise, can architect)

## Skills Matrix

### Technical Skills

| Skill Area | Required Level | Team Member 1 | Team Member 2 | Team Member 3 | Team Member 4 | Gap Analysis |
|------------|---------------|---------------|---------------|---------------|---------------|--------------|
| **Frontend** |
| React | 4 | 5 | 3 | 4 | 0 | ✅ Covered |
| TypeScript | 3 | 4 | 2 | 3 | 3 | ✅ Covered |
| Redux | 3 | 3 | 1 | 4 | 2 | ✅ Covered |
| CSS/Responsive | 3 | 2 | 4 | 3 | 3 | ✅ Covered |
| Testing (Jest/RTL) | 3 | 3 | 2 | 2 | 1 | ⚠️ Weak |
| **Backend** |
| Node.js | 4 | 2 | 5 | 3 | 4 | ✅ Covered |
| Express/REST | 4 | 2 | 5 | 3 | 4 | ✅ Covered |
| PostgreSQL | 3 | 1 | 4 | 2 | 3 | ✅ Covered |
| Redis | 2 | 0 | 3 | 1 | 2 | ✅ Covered |
| WebSockets | 3 | 0 | 2 | 1 | 2 | ❌ Gap |
| **DevOps** |
| Docker | 3 | 2 | 3 | 4 | 2 | ✅ Covered |
| AWS/Cloud | 3 | 1 | 2 | 4 | 1 | ⚠️ Weak |
| CI/CD | 3 | 2 | 3 | 4 | 2 | ✅ Covered |
| Monitoring | 2 | 1 | 2 | 3 | 1 | ✅ Covered |
| **Security** |
| Auth/OAuth | 3 | 2 | 3 | 2 | 2 | ⚠️ Weak |
| OWASP | 2 | 1 | 2 | 2 | 1 | ⚠️ Weak |
| Encryption | 2 | 1 | 2 | 1 | 1 | ❌ Gap |

### Domain Skills

| Skill Area | Required Level | TM 1 | TM 2 | TM 3 | TM 4 | Gap Analysis |
|------------|---------------|------|------|------|------|--------------|
| Project Domain | 3 | 2 | 1 | 3 | 4 | ✅ Covered |
| Industry Regulations | 2 | 1 | 0 | 2 | 3 | ✅ Covered |
| Business Process | 3 | 3 | 1 | 2 | 4 | ✅ Covered |
| Customer Perspective | 3 | 4 | 2 | 3 | 3 | ✅ Covered |

### Soft Skills

| Skill Area | Required Level | TM 1 | TM 2 | TM 3 | TM 4 | Gap Analysis |
|------------|---------------|------|------|------|------|--------------|
| Communication | 4 | 4 | 3 | 5 | 3 | ✅ Covered |
| Problem Solving | 4 | 4 | 5 | 4 | 3 | ✅ Covered |
| Team Collaboration | 4 | 5 | 4 | 4 | 3 | ✅ Covered |
| Time Management | 3 | 3 | 4 | 3 | 2 | ✅ Covered |
| Mentoring | 2 | 4 | 2 | 3 | 1 | ✅ Covered |

## Gap Analysis Summary

### Critical Gaps (Required level - Max team level ≥ 2)
1. **WebSockets**: Required: 3, Best: 2
   - Impact: Real-time features at risk
   - Mitigation: Training or contractor

2. **Encryption**: Required: 2, Best: 2 (but weak)
   - Impact: Security implementation risk
   - Mitigation: Security consultant review

### Weak Areas (Barely meeting requirements)
1. **Frontend Testing**: Low proficiency across team
   - Mitigation: Team training workshop
   
2. **Cloud/AWS**: Dependent on one person
   - Mitigation: Knowledge transfer sessions

3. **Security**: Generally weak
   - Mitigation: Security training + code reviews

## Mitigation Strategies

### Immediate Actions (Before project start)
1. **WebSockets Training**
   - Who: TM2 and TM4 (backend strong)
   - What: 2-day intensive course
   - When: Week -2
   - Cost: $3,000

2. **Security Workshop**
   - Who: Entire team
   - What: 1-day OWASP training
   - When: Week -1
   - Cost: $2,000

### During Project
1. **Pair Programming**
   - Pair WebSocket features: TM2 + External expert
   - Pair security features: TM3 + Security consultant

2. **Code Review Focus**
   - All WebSocket code: External review
   - All auth/encryption: Security review
   - Testing: Mandatory pair review

3. **Knowledge Transfer**
   - Weekly tech talks
   - Document all decisions
   - Record architecture sessions

### Hiring/Contracting Needs
1. **WebSocket Expert** (Contractor)
   - Duration: 2 weeks during Phase 2
   - Role: Implementation + mentoring
   - Budget: $15,000

2. **Security Consultant** (Part-time)
   - Duration: 2 days/month
   - Role: Review + guidance
   - Budget: $3,000/month

## Team Development Plan

### Individual Development Goals

**Team Member 1**
- Strength: Frontend expert, good communicator
- Growth: Backend and cloud skills
- Plan: Shadow TM2 on backend tasks

**Team Member 2**
- Strength: Full-stack, problem solver
- Growth: Frontend testing, security
- Plan: Lead testing practice improvement

**Team Member 3**
- Strength: DevOps, cloud expert
- Growth: Frontend, domain knowledge
- Plan: Cross-training on React

**Team Member 4**
- Strength: Backend, domain expert
- Growth: Modern frontend, testing
- Plan: React course, testing workshop

## Risk Assessment

### High Risk Areas
1. **Real-time Features** (WebSockets)
   - Mitigation: External expert + aggressive timeline
   
2. **Security Implementation**
   - Mitigation: Consultant + extra review cycles

3. **Cloud Architecture** (Bus factor: 1)
   - Mitigation: Document everything, pair deploy

### Medium Risk Areas
1. **Testing Coverage**
   - Mitigation: Mandate TDD, automated checks

2. **Performance Optimization**
   - Mitigation: Early load testing, profiling

## Success Metrics

### Team Capability Metrics
- [ ] All critical skills covered (level 3+)
- [ ] No single points of failure
- [ ] 80% of team at level 3+ for core skills
- [ ] Knowledge transfer sessions completed

### Project Impact Metrics
- [ ] No features blocked by skill gaps
- [ ] Security review passes first time
- [ ] Performance targets met
- [ ] Team satisfaction maintained

## Review Schedule

- **Week -2**: Initial assessment
- **Week 0**: Post-training reassessment
- **Week 4**: First sprint retrospective
- **Week 8**: Mid-project adjustment
- **Project End**: Final assessment + lessons learned

## Example: TaskMaster Project Team

| Skill | Required | Alex (Sr Dev) | Sara (PM/Dev) | Mike (Jr Dev) | Lisa (DevOps) | Gap |
|-------|----------|---------------|---------------|---------------|---------------|-----|
| React | 4 | 5 | 2 | 3 | 1 | ✅ |
| Node.js | 4 | 4 | 2 | 2 | 3 | ✅ |
| PostgreSQL | 3 | 4 | 1 | 2 | 3 | ✅ |
| WebSockets | 3 | 2 | 0 | 1 | 2 | ❌ |
| AWS | 3 | 2 | 1 | 1 | 5 | ✅ |
| Testing | 4 | 4 | 3 | 2 | 3 | ✅ |
| Project Mgmt | 3 | 2 | 5 | 1 | 2 | ✅ |

**Gap Mitigation**: 
- WebSockets: Alex to take Udemy course + bring in contractor for implementation
- Sara to shadow Alex on technical tasks while managing project

---

Remember: Skills can be developed, but timeline and budget must account for learning curves!