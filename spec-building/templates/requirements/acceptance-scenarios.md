# Acceptance Scenarios Template

## Instructions
For each user story or feature, create concrete scenarios that demonstrate the feature working correctly. Include happy paths, edge cases, and failure modes.

## Scenario Template

### Scenario ID: [SCAN-001]
**Feature**: [Feature name]
**User Story**: As a [user type], I want to [action] so that [outcome]

#### Preconditions
- [ ] [System state before scenario]
- [ ] [User state/permissions]
- [ ] [Data that must exist]

#### Steps
1. **Given**: [Initial context]
2. **When**: [User action]
3. **Then**: [Expected outcome]
4. **And**: [Additional outcomes]

### Real Example: SCAN-002 - Task Creation and Assignment
**Feature**: Task Management
**User Story**: As a project manager, I want to create and assign tasks quickly so that my team knows what to work on

#### Preconditions
- [x] User logged in with PM role
- [x] At least one project exists
- [x] Team members imported/invited

#### Steps
1. **Given**: User on project dashboard
2. **When**: User clicks "+" or presses "T" hotkey
3. **Then**: Quick task modal appears with cursor in title field
4. **When**: User types "Design new login screen"
5. **And**: Presses Tab and types "Create mockups for updated login with SSO option"
6. **And**: Types "@alex" in assignee field
7. **Then**: Alex Developer appears in dropdown
8. **When**: User selects Alex and sets due date to "Friday"
9. **Then**: System calculates actual date (2024-03-15)
10. **When**: User presses Enter or clicks "Create Task"
11. **Then**: Task created instantly
12. **And**: Alex receives notification in-app and via Slack
13. **And**: Task appears in dashboard with "New" badge

#### Test Data
```
Specific data needed:
- User: [Example user details]
- Input: [Example input values]
- Expected Output: [Exact expected results]
```

**TaskMaster Example Test Data:**
```json
{
  "task": {
    "title": "Design new login screen",
    "description": "Create mockups for updated login with SSO option",
    "assignee": "alex.dev@techcorp.com",
    "dueDate": "relative:friday",
    "priority": "medium",
    "labels": ["design", "frontend"]
  },
  "expectedResponse": {
    "status": 201,
    "responseTime": "<500ms",
    "notification": {
      "slack": true,
      "inApp": true,
      "email": false
    }
  }
}
```

#### Acceptance Criteria
- [ ] [Specific measurable criterion]
- [ ] [Performance requirement]
- [ ] [Quality requirement]

#### Edge Cases
- **Edge Case 1**: [Description]
  - Input: [Edge case input]
  - Expected: [How system should handle]
- **Edge Case 2**: [Description]
  - Input: [Edge case input]
  - Expected: [How system should handle]

#### Error Scenarios
- **Error 1**: [Invalid input type]
  - Input: [Bad input]
  - Expected: [Error message/behavior]
- **Error 2**: [System failure]
  - Condition: [Failure condition]
  - Expected: [Graceful handling]

---

## Core User Journey Scenarios

### Scenario: First-Time User Onboarding
**Feature**: User Registration and Setup
**User Story**: As a new user, I want to quickly set up my account so that I can start using the system

#### Preconditions
- [ ] User has valid email address
- [ ] System is operational
- [ ] No existing account with email

#### Happy Path Steps
1. **Given**: User arrives at registration page
2. **When**: User enters email "newuser@example.com"
3. **And**: User creates password meeting requirements
4. **And**: User completes profile information
5. **Then**: Account is created successfully
6. **And**: Verification email is sent within 30 seconds
7. **And**: User is logged in automatically
8. **And**: Welcome tutorial is displayed

#### Variations
- **Mobile Registration**: Steps adjusted for mobile UI
- **Social Login**: OAuth flow with Google/GitHub
- **Enterprise SSO**: SAML flow for corporate users

#### Performance Criteria
- Registration completes in <3 seconds
- Email sent within 30 seconds
- No timeout errors under 1000 concurrent registrations

### Scenario: Data Processing Workflow
**Feature**: Bulk Data Import
**User Story**: As a power user, I want to import large datasets so that I can analyze them in the system

#### Preconditions
- [ ] User has appropriate permissions
- [ ] CSV file is properly formatted
- [ ] System has available processing capacity

#### Steps
1. **Given**: User on import page with 50MB CSV file
2. **When**: User uploads file via drag-and-drop
3. **Then**: Upload progress is shown in real-time
4. **When**: Upload completes
5. **Then**: File validation begins automatically
6. **And**: Validation results shown within 10 seconds
7. **When**: User confirms import settings
8. **Then**: Background processing job is queued
9. **And**: User receives estimated completion time
10. **And**: User can track progress in dashboard

#### Data Limits
- Min file size: 1 KB
- Max file size: 500 MB
- Max rows: 1 million
- Max columns: 500

#### Error Handling
- **Malformed CSV**: Clear error with line numbers
- **Too Large**: Suggest splitting file
- **Invalid Data Types**: Highlight specific cells
- **Network Interruption**: Resume capability

### Scenario: Critical Business Operation
**Feature**: Payment Processing
**User Story**: As a customer, I want to complete purchases securely so that I receive my products

#### Preconditions
- [ ] Valid products in cart
- [ ] User logged in or guest checkout
- [ ] Payment gateway operational

#### Steps with Timing
1. **Given**: Cart with $150.00 in products [0s]
2. **When**: User proceeds to checkout [+1s]
3. **Then**: Shipping options loaded [+2s max]
4. **When**: User selects shipping [+3s]
5. **Then**: Tax calculated correctly [+3.5s max]
6. **When**: User enters payment details [+30s]
7. **Then**: Payment validated client-side [+31s]
8. **When**: User confirms order [+35s]
9. **Then**: Payment processed [+38s max]
10. **And**: Order confirmation shown [+39s]
11. **And**: Email sent [+45s max]
12. **And**: Inventory updated [+40s]

#### Security Requirements
- PCI compliance maintained
- No payment data in logs
- TLS 1.3 for all communications
- Tokenization of card details

#### Failure Recovery
- **Payment Timeout**: Automatic retry with idempotency
- **Partial Failure**: Rollback with user notification
- **Gateway Down**: Failover to backup processor

## Integration Scenarios

### Scenario: Third-Party API Integration
**Feature**: External Data Sync
**User Story**: As a system admin, I want automatic data sync so that information stays current

#### Preconditions
- [ ] API credentials configured
- [ ] Network connectivity
- [ ] Rate limits not exceeded

#### Sync Flow
1. **Given**: Scheduled sync at 2 AM
2. **When**: Cron job triggers
3. **Then**: System authenticates with API
4. **When**: Authentication successful
5. **Then**: Fetch changed records (delta sync)
6. **And**: Process in batches of 100
7. **When**: Conflicts detected
8. **Then**: Apply conflict resolution rules
9. **And**: Log conflicts for review
10. **When**: Sync completes
11. **Then**: Update sync timestamp
12. **And**: Send summary report

#### Monitoring
- Alert if sync fails 3 times
- Track sync duration trends
- Monitor data quality scores

## Performance Scenarios

### Scenario: High Load Operation
**Feature**: System Performance Under Load
**User Story**: As a user, I want consistent performance even during peak times

#### Load Profile
- Concurrent users: 10,000
- Requests/second: 5,000
- Data volume: 1TB active

#### Performance Requirements
| Operation | Target | Max | Degraded Mode |
|-----------|--------|-----|---------------|
| Page Load | 2s | 5s | Static cache |
| API Call | 200ms | 1s | Rate limit |
| Search | 500ms | 2s | Basic search only |
| Report Generation | 10s | 60s | Queue for async |

## Accessibility Scenarios

### Scenario: Screen Reader Navigation
**Feature**: Accessible UI
**User Story**: As a vision-impaired user, I want to navigate efficiently using screen reader

#### Requirements
- All interactive elements labeled
- Logical tab order
- ARIA landmarks present
- Skip navigation links
- Form validation announced

## Mobile Scenarios

### Scenario: Offline Mobile Usage
**Feature**: Offline Capability
**User Story**: As a mobile user, I want to work offline and sync when connected

#### Offline Flow
1. User works offline for 2 hours
2. Creates 5 new records
3. Edits 10 existing records
4. Deletes 2 records
5. Connection restored
6. Automatic sync begins
7. Conflicts resolved by timestamp
8. User notified of any issues

## Scenario Coverage Matrix

| Feature Area | Happy Path | Edge Cases | Error Cases | Performance | Security |
|--------------|------------|------------|-------------|-------------|----------|
| Registration | ✓ | ✓ | ✓ | ✓ | ✓ |
| Data Import | ✓ | ✓ | ✓ | ✓ | ✓ |
| Payments | ✓ | ✓ | ✓ | ✓ | ✓ |
| API Sync | ✓ | ✓ | ✓ | ✓ | ✓ |
| [Your Feature] | [ ] | [ ] | [ ] | [ ] | [ ] |

## Validation Checklist

Before finalizing scenarios:
- [ ] Every user story has at least one scenario
- [ ] Critical paths have multiple variations
- [ ] Edge cases identified for each feature
- [ ] Error handling specified
- [ ] Performance criteria defined
- [ ] Security considerations included
- [ ] Accessibility scenarios present
- [ ] Mobile scenarios included
- [ ] Integration points tested
- [ ] Data limits documented