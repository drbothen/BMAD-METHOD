# Priority-Based Review Triggering Reference

## Overview

The priority-based review triggering system automatically determines which security enrichments require review based on priority level (P1-P5), optimizing reviewer workload while maintaining comprehensive quality coverage for high-priority vulnerabilities.

**Key Features:**

- **Mandatory Review:** 100% review coverage for critical and high priority vulnerabilities (P1/P2)
- **Statistical Sampling:** Random sampling for medium/low/trivial priority vulnerabilities (P3-P5)
- **Smart Assignment:** Least-loaded assignment for senior reviewers, round-robin for general pool
- **Multi-Channel Notifications:** JIRA, email, and Slack integration
- **Audit Trail:** Complete review decision logging with sampling statistics

## Review Triggering Decision Tree

```
Enrichment Complete
    ↓
Determine Priority (P1-P5)
    ↓
P1 → Review Required: YES (100%), Blocking: YES, Reviewer: Senior (least-loaded)
P2 → Review Required: YES (100%), Blocking: YES, Reviewer: Senior (least-loaded)
P3 → Review Required: 25% Sample, Blocking: NO, Reviewer: Any (round-robin)
P4 → Review Required: 10% Sample, Blocking: NO, Reviewer: Junior (round-robin)
P5 → Review Required: 5% Sample, Blocking: NO, Reviewer: Junior (round-robin)
    ↓
If Review Required or Sampled:
    - Assign Reviewer (per assignment rules)
    - Transition JIRA to "In Review"
    - Send Notifications
    - Log Review Decision
    ↓
If Review Not Sampled:
    - Transition JIRA to "Remediation Planning"
    - Log Review Decision (not_required)
```

---

## Review Triggering Rules by Priority

### P1 (Critical) Review Triggering

**Configuration:**

```yaml
review_triggers:
  P1:
    review_required: true
    sampling_rate: 100
    blocking: true
    assignment: 'senior-reviewer'
```

**Triggering Rules:**

- **Review Required:** YES (mandatory)
- **Sampling Rate:** 100% (all P1 enrichments reviewed)
- **Blocking:** YES (remediation waits for review approval)
- **Reviewer Assignment:** Senior reviewer pool, least-loaded method

**Rationale:**

- Critical severity (CVSS ≥ 9.0 typically)
- Short SLA (24 hours)
- High business impact
- Active exploitation likely
- Error in priority or remediation guidance = critical risk
- 100% review coverage essential for P1 quality assurance

**Statistical Note:** No sampling - full population review

**Example:** CVE-2024-1234 Apache Struts RCE, CVSS 9.8, KEV: Yes, Internet-exposed → 100% reviewed

---

### P2 (High) Review Triggering

**Configuration:**

```yaml
review_triggers:
  P2:
    review_required: true
    sampling_rate: 100
    blocking: true
    assignment: 'senior-reviewer'
```

**Triggering Rules:**

- **Review Required:** YES (mandatory)
- **Sampling Rate:** 100%
- **Blocking:** YES
- **Reviewer Assignment:** Senior reviewer pool, least-loaded method

**Rationale:**

- High severity (CVSS ≥ 7.0 typically)
- Short SLA (7 days)
- Moderate to high business impact
- Potential for exploitation
- Errors can lead to significant security gaps
- 100% review ensures quality before 7-day SLA countdown

**Statistical Note:** No sampling - full population review

**Example:** CVE-2024-5678 PostgreSQL Privilege Escalation, CVSS 8.1, High ACR database → 100% reviewed

---

### P3 (Medium) Review Triggering

**Configuration:**

```yaml
review_triggers:
  P3:
    review_required: false
    sampling_rate: 25
    blocking: false
    assignment: 'any-reviewer'
```

**Triggering Rules:**

- **Review Required:** NO (sampling-based)
- **Sampling Rate:** 25% (1 in 4 enrichments reviewed)
- **Blocking:** NO (remediation proceeds in parallel with review)
- **Reviewer Assignment:** All reviewers (senior + junior), round-robin method

**Rationale:**

- Medium severity (CVSS 4.0-6.9 or CVSS 7.0-8.9 with Low ACR)
- Longer SLA (30 days)
- Moderate business impact
- Lower exploitation probability
- 25% sampling provides statistical confidence in quality trends
- Balances quality assurance with reviewer capacity

**Statistical Basis:**

- **Confidence Level:** 95%
- **Margin of Error:** ±10%
- **Population:** All P3 enrichments per month (e.g., 100 P3/month)
- **Sample Size:** 25 enrichments (25%)
- **Statistical Power:** Sufficient to detect systemic quality issues
- **Rationale:** If 25% sample shows quality issues, entire population likely affected

**Sampling Method:** Random selection using `random.random() < 0.25` (Python)

**Example:** CVE-2024-9012 Nginx Path Traversal, CVSS 5.3, Internal system → 25% chance of review

**Sampling Statistics:**

- If 100 P3 enrichments per month, approximately 25 reviewed
- Quality trends detected from 25-sample analysis
- If sample quality drops below 75% average, flag for increased sampling or training

---

### P4 (Low) Review Triggering

**Configuration:**

```yaml
review_triggers:
  P4:
    review_required: false
    sampling_rate: 10
    blocking: false
    assignment: 'any-reviewer'
```

**Triggering Rules:**

- **Review Required:** NO (sampling-based)
- **Sampling Rate:** 10% (1 in 10 enrichments reviewed)
- **Blocking:** NO
- **Reviewer Assignment:** Junior reviewers or all reviewers, round-robin

**Rationale:**

- Low severity (CVSS < 4.0 or isolated systems)
- Long SLA (90 days)
- Low business impact
- Minimal exploitation risk
- 10% sampling sufficient for systemic issue detection
- Minimal reviewer burden

**Statistical Basis:**

- 10% sample for quality spot-checking
- Detects major systemic issues (e.g., analysts consistently skipping sections)
- Not intended for comprehensive quality assurance

**Sampling Method:** Random selection using `random.random() < 0.10`

**Example:** CVE-2024-7654 Information Disclosure, CVSS 3.1, isolated dev server → 10% chance of review

---

### P5 (Trivial) Review Triggering

**Configuration:**

```yaml
review_triggers:
  P5:
    review_required: false
    sampling_rate: 5
    blocking: false
    assignment: 'any-reviewer'
```

**Triggering Rules:**

- **Review Required:** NO (sampling-based)
- **Sampling Rate:** 5% (1 in 20 enrichments reviewed)
- **Blocking:** NO
- **Reviewer Assignment:** Junior reviewers, round-robin

**Rationale:**

- Trivial severity (CVSS < 4.0, Low ACR, Isolated, No patch available)
- No SLA (best effort)
- Minimal business impact
- No exploitation expected
- 5% minimal sampling for process improvement feedback only
- Training opportunity for junior reviewers

**Statistical Basis:**

- 5% sample for minimal quality monitoring
- Primary purpose: Analyst training feedback, not comprehensive QA

**Sampling Method:** Random selection using `random.random() < 0.05`

**Example:** CVE-2024-1111 Deprecated library info disclosure, CVSS 2.1, no patch → 5% chance of review

---

## Reviewer Assignment Logic

### 1. Least-Loaded Method (P1/P2)

**Purpose:** Distribute high-priority reviews to senior reviewers based on current workload

**Algorithm:**

```python
def assign_least_loaded(priority, reviewer_pool):
    # Query active reviews per reviewer in pool
    active_reviews = {
        'Alex': count_active_reviews('Alex'),
        'Jordan': count_active_reviews('Jordan')
    }

    # Filter pool for reviewers with capacity
    available = {r: active_reviews[r] for r in reviewer_pool
                 if active_reviews[r] < reviewer_config[r]['max_concurrent']}

    if not available:
        # All reviewers at capacity
        # Assign to minimum (over-capacity allowed for P1/P2)
        reviewer = min(active_reviews, key=active_reviews.get)
        escalate_capacity_warning(reviewer)
    else:
        # Assign to reviewer with minimum active reviews
        reviewer = min(available, key=available.get)

    return reviewer
```

**Example:**

- P1 enrichment completed
- Alex: 2 active reviews
- Jordan: 4 active reviews
- **Assignment:** Alex (least-loaded)

**Tie-Breaker:** If equal active reviews, assign to reviewer with most recent completion (fresher availability)

---

### 2. Round-Robin Method (P3/P4/P5)

**Purpose:** Distribute medium/low priority reviews evenly across all reviewers

**Algorithm:**

```python
# Global counter (persisted in state file or database)
round_robin_counter = {
    'P3': 0,
    'P4': 0,
    'P5': 0
}

def assign_round_robin(priority, reviewer_pool):
    # Get current counter for priority
    counter = round_robin_counter[priority]

    # Assign to reviewer at counter position
    reviewer = reviewer_pool[counter % len(reviewer_pool)]

    # Increment counter for next assignment
    round_robin_counter[priority] = (counter + 1) % len(reviewer_pool)

    return reviewer
```

**Example:**

- P3 pool: [Alex, Jordan, Taylor]
- Counter: 0
- **1st P3 Review:** Alex (counter → 1)
- **2nd P3 Review:** Jordan (counter → 2)
- **3rd P3 Review:** Taylor (counter → 3 = 0 after modulo)
- **4th P3 Review:** Alex (counter → 1)

**Benefits:**

- Even distribution over time
- Predictable assignment
- No reviewer overloading

---

### 3. Skill-Based Method (Optional Enhancement)

**Purpose:** Match reviewer specialization to vulnerability type for complex P1/P2

**Configuration:**

```yaml
reviewer_assignment:
  reviewers:
    - name: 'Alex'
      specializations: ['web-vulnerabilities', 'infrastructure']
    - name: 'Jordan'
      specializations: ['application-security', 'cryptography']
    - name: 'Taylor'
      specializations: ['network-security']
```

**Algorithm:**

```python
def assign_skill_based(priority, cve_type, reviewer_pool):
    # Extract vulnerability type from CVE research
    # e.g., "RCE", "SQLi", "XSS", "Cryptography", "Network"

    # Match to reviewer specializations
    specialists = []
    for reviewer in reviewer_pool:
        if cve_type_matches_specialization(cve_type, reviewer['specializations']):
            specialists.append(reviewer)

    if specialists:
        # Assign to specialist using least-loaded
        return assign_least_loaded(priority, specialists)
    else:
        # No specialist available - fallback to standard assignment
        return assign_least_loaded(priority, reviewer_pool)
```

**Example:**

- CVE: Cryptography vulnerability (weak cipher)
- Alex specializations: web, infra (no crypto)
- Jordan specializations: app-sec, **crypto** (match!)
- **Assignment:** Jordan (specialist)

**Fallback:** If no specialist available, use least-loaded (P1/P2) or round-robin (P3-P5)

---

## Reviewer Configuration

### Reviewer Attributes

```yaml
reviewer_assignment:
  reviewers:
    - name: 'Alex'
      role: 'senior-reviewer'
      specializations: ['web-vulnerabilities', 'infrastructure']
      max_concurrent: 5
      priorities: ['P1', 'P2', 'P3', 'P4', 'P5']

    - name: 'Jordan'
      role: 'senior-reviewer'
      specializations: ['application-security', 'cryptography']
      max_concurrent: 5
      priorities: ['P1', 'P2', 'P3', 'P4', 'P5']

    - name: 'Taylor'
      role: 'reviewer'
      specializations: ['network-security']
      max_concurrent: 8
      priorities: ['P3', 'P4', 'P5'] # Not eligible for P1/P2
```

**Attribute Definitions:**

- **name:** Reviewer identifier (matches JIRA username for assignment)
- **role:** senior-reviewer (P1/P2 eligible) or reviewer (P3-P5 only)
- **specializations:** List of expertise areas for skill-based assignment
  - Common: web-vulnerabilities, application-security, infrastructure, network-security, cryptography, database-security, cloud-security
- **max_concurrent:** Maximum active reviews before capacity warning
  - Senior reviewers: 5 typical
  - Junior reviewers: 8 typical (less complex reviews)
- **priorities:** List of priorities reviewer is eligible to review
  - Senior: P1-P5 (all)
  - Junior: P3-P5 (not P1/P2)

### Reviewer Pools

```yaml
reviewer_assignment:
  assignment_rules:
    P1:
      pool: ['Alex', 'Jordan'] # Senior reviewers only
      method: 'least-loaded'
    P2:
      pool: ['Alex', 'Jordan'] # Senior reviewers only
      method: 'least-loaded'
    P3:
      pool: ['Alex', 'Jordan', 'Taylor'] # All reviewers
      method: 'round-robin'
    P4:
      pool: ['Taylor'] # Junior reviewers (or all if needed)
      method: 'round-robin'
    P5:
      pool: ['Taylor'] # Junior reviewers
      method: 'round-robin'
```

### Capacity Management

- **Capacity Warning:** Triggered when reviewer at or over `max_concurrent`
- **Over-Capacity Handling (P1/P2):** Assign anyway, escalate to manager
- **Over-Capacity Handling (P3-P5):** Delay assignment until capacity available, or assign to next available

### Scaling Reviewer Pools

| Team Size     | P1/P2 Pool | P3-P5 Pool    | Sampling Rates                                   |
| ------------- | ---------- | ------------- | ------------------------------------------------ |
| 1 reviewer    | 1 senior   | 1 senior      | P1:100%, P2:100%, P3:10%, P4:5%, P5:2%           |
| 2 reviewers   | 2 senior   | 2 reviewers   | P1:100%, P2:100%, P3:25%, P4:10%, P5:5%          |
| 3-4 reviewers | 2-3 senior | 3-4 reviewers | P1:100%, P2:100%, P3:25-50%, P4:10-25%, P5:5-10% |
| 5+ reviewers  | 3+ senior  | 5+ reviewers  | P1:100%, P2:100%, P3:50%, P4:25%, P5:10%         |

---

## Notification System

### Primary Notification: JIRA Assignment

- **Trigger:** Reviewer assigned to JIRA ticket
- **Method:** Automatic JIRA notification (built-in)
- **Content:** Standard JIRA assignment notification
- **Delivery:** Email (if reviewer has email notifications enabled in JIRA), JIRA inbox
- **Reliability:** High (JIRA native feature)

### Optional Notification: Email

**Configuration:**

```yaml
notification:
  email:
    enabled: true
    smtp_server: 'smtp.company.com'
    smtp_port: 587
    smtp_username: 'security-notifications@company.com'
    smtp_password: '${SMTP_PASSWORD}' # Environment variable
    from_address: 'security-notifications@company.com'
    subject_template: 'Security Review Required: {ticket_id} - {cve_id} ({priority})'
    body_template: |
      A security enrichment requires your review:

      Ticket: {ticket_id}
      CVE: {cve_id}
      Priority: {priority}
      Analyst: {analyst_name}
      SLA Deadline: {sla_deadline}

      Please review at: {jira_url}

      ---
      Automated notification from bmad-1898-engineering
```

**Email Trigger:** After JIRA assignment
**Delivery:** SMTP server
**Error Handling:** If email fails, log error, continue (JIRA assignment is primary)

### Optional Notification: Slack

**Configuration:**

```yaml
notification:
  slack:
    enabled: true
    webhook_url: '${SLACK_WEBHOOK_URL}' # Environment variable
    channel: '#security-reviews'
    message_template: |
      :mag: *Security Review Required*
      *Ticket:* <{jira_url}|{ticket_id}>
      *CVE:* {cve_id}
      *Priority:* {priority}
      *Analyst:* {analyst_name}
      *Reviewer:* @{reviewer_name}
      *SLA Deadline:* {sla_deadline}
```

**Slack Trigger:** After JIRA assignment
**Delivery:** Slack incoming webhook
**Mentions:** @reviewer_name (requires Slack username mapping)
**Error Handling:** If Slack webhook fails, log error, continue

### Notification Content Variables

- `ticket_id`: JIRA ticket ID (e.g., AOD-1234)
- `cve_id`: CVE identifier (e.g., CVE-2024-1234)
- `priority`: Priority level (P1-P5)
- `analyst_name`: Analyst who performed enrichment
- `reviewer_name`: Assigned reviewer
- `sla_deadline`: SLA deadline timestamp
- `jira_url`: Direct link to JIRA ticket

### Error Handling

```yaml
notification:
  error_handling:
    fallback_to_jira_only: true
    retry_count: 2
    retry_delay_seconds: 30
    log_failures: true
    log_file: 'logs/notification-errors.log'
```

---

## Review Decision Logging

### Log File Format

**Log File:** `metrics/review-decisions.csv`

**Purpose:**

- Audit trail of all review decisions (required/not_required)
- Sampling statistics (actual vs. configured rates)
- Reviewer assignment tracking
- Process improvement insights

**CSV Format:**

```csv
ticket_id,cve_id,priority,decision,sampling_rate,sampled,reason,reviewer_assigned,decision_timestamp
AOD-1234,CVE-2024-1234,P1,required,100,yes,mandatory_p1,Alex,2025-11-08T08:43:00Z
AOD-1235,CVE-2024-5678,P2,required,100,yes,mandatory_p2,Jordan,2025-11-08T09:15:00Z
AOD-1236,CVE-2024-9012,P3,not_required,25,no,sampling_skip,null,2025-11-08T10:30:00Z
AOD-1237,CVE-2024-7654,P3,required,25,yes,sampling_selected,Taylor,2025-11-08T11:00:00Z
```

**Columns:**

- **ticket_id:** JIRA ticket ID
- **cve_id:** CVE identifier
- **priority:** P1-P5
- **decision:** required (review triggered) / not_required (skipped)
- **sampling_rate:** Configured sampling percentage (e.g., 25 for P3)
- **sampled:** yes (selected for review) / no (skipped)
- **reason:** Explanation code
  - mandatory_p1, mandatory_p2 (100% review)
  - sampling_selected (random selection for P3-P5)
  - sampling_skip (not selected in random sampling)
- **reviewer_assigned:** Reviewer name (null if not_required)
- **decision_timestamp:** When decision made

### Sampling Statistics Analysis

**Script:** `scripts/generate_sampling_report.py`

```python
import pandas as pd

# Load review decisions
df = pd.read_csv('metrics/review-decisions.csv')

# Calculate actual sampling rates by priority
sampling_stats = df.groupby('priority').agg({
    'decision': 'count',
    'sampled': lambda x: (x == 'yes').sum()
}).rename(columns={'decision': 'total_enrichments', 'sampled': 'reviews_triggered'})

sampling_stats['actual_sampling_rate'] = (
    sampling_stats['reviews_triggered'] / sampling_stats['total_enrichments'] * 100
)

print("Sampling Statistics Report")
print("="*50)
print(sampling_stats)

# Compare actual vs. configured
configured_rates = {'P1': 100, 'P2': 100, 'P3': 25, 'P4': 10, 'P5': 5}
for priority in sampling_stats.index:
    actual = sampling_stats.loc[priority, 'actual_sampling_rate']
    configured = configured_rates.get(priority, 0)
    variance = actual - configured
    print(f"{priority}: Configured {configured}%, Actual {actual:.1f}%, Variance {variance:+.1f}%")
```

**Output Example:**

```
Sampling Statistics Report
==================================================
          total_enrichments  reviews_triggered  actual_sampling_rate
priority
P1                       15                 15                100.0
P2                       42                 42                100.0
P3                      128                 31                 24.2
P4                       67                  7                 10.4
P5                       23                  1                  4.3

P1: Configured 100%, Actual 100.0%, Variance +0.0%
P2: Configured 100%, Actual 100.0%, Variance +0.0%
P3: Configured 25%, Actual 24.2%, Variance -0.8%
P4: Configured 10%, Actual 10.4%, Variance +0.4%
P5: Configured 5%, Actual 4.3%, Variance -0.7%
```

**Insights from Sampling Statistics:**

- P1/P2: 100% coverage confirmed (no variance expected)
- P3-P5: Actual rates within ±1% of configured (random sampling working correctly)
- Large variances indicate sampling logic issue or configuration drift

---

## Configuration Customization Guide

### Scenario 1: Small Team (1-2 Reviewers)

**Challenge:** Limited reviewer capacity, need to reduce sampling to avoid overload

**Recommended Configuration:**

```yaml
review_triggers:
  P1: { review_required: true, sampling_rate: 100, blocking: true }
  P2: { review_required: true, sampling_rate: 100, blocking: true }
  P3: { review_required: false, sampling_rate: 10, blocking: false } # Reduced from 25%
  P4: { review_required: false, sampling_rate: 5, blocking: false } # Reduced from 10%
  P5: { review_required: false, sampling_rate: 2, blocking: false } # Reduced from 5%

reviewer_assignment:
  reviewers:
    - name: 'Alex'
      role: 'senior-reviewer'
      max_concurrent: 8 # Increased capacity
      priorities: ['P1', 'P2', 'P3', 'P4', 'P5']
```

**Trade-off:** Lower P3-P5 quality coverage, but prevents reviewer burnout

---

### Scenario 2: Large Team (5+ Reviewers)

**Challenge:** Abundant reviewer capacity, can increase sampling for better quality coverage

**Recommended Configuration:**

```yaml
review_triggers:
  P1: { review_required: true, sampling_rate: 100, blocking: true }
  P2: { review_required: true, sampling_rate: 100, blocking: true }
  P3: { review_required: false, sampling_rate: 50, blocking: false } # Increased from 25%
  P4: { review_required: false, sampling_rate: 25, blocking: false } # Increased from 10%
  P5: { review_required: false, sampling_rate: 10, blocking: false } # Increased from 5%
```

**Benefit:** Higher quality coverage, more training opportunities, better systemic issue detection

---

### Scenario 3: High-Quality Focus

**Challenge:** Recent quality issues, need comprehensive review coverage

**Recommended Configuration:**

```yaml
review_triggers:
  P1: { review_required: true, sampling_rate: 100, blocking: true }
  P2: { review_required: true, sampling_rate: 100, blocking: true }
  P3: { review_required: true, sampling_rate: 100, blocking: true } # Mandatory for P3
  P4: { review_required: false, sampling_rate: 50, blocking: false }
  P5: { review_required: false, sampling_rate: 25, blocking: false }
```

**Duration:** Temporary (1-2 months), revert to standard after quality improves
**Reviewer Capacity:** Requires 3+ reviewers to sustain

---

### Scenario 4: Efficiency Focus

**Challenge:** High enrichment volume, need to optimize reviewer time

**Recommended Configuration:**

```yaml
review_triggers:
  P1: { review_required: true, sampling_rate: 100, blocking: true } # Always 100%
  P2: { review_required: false, sampling_rate: 50, blocking: false } # Sample P2!
  P3: { review_required: false, sampling_rate: 25, blocking: false }
  P4: { review_required: false, sampling_rate: 10, blocking: false }
  P5: { review_required: false, sampling_rate: 5, blocking: false }
```

**Trade-off:** P2 sampling risky (short SLA), only use if analyst quality consistently high (>90%)
**Recommendation:** Monitor P2 sampling quality closely, revert to 100% if issues arise

---

### Scenario 5: Custom Blocking Rules

**Challenge:** Want P3 reviews to be advisory (non-blocking) but still complete before remediation

**Configuration:**

```yaml
review_triggers:
  P3:
    review_required: false
    sampling_rate: 25
    blocking: false # Remediation proceeds
    notify_on_completion: true # Notify DevOps when review complete
    sla_target_hours: 48 # Target 48-hour review completion
```

**Workflow Adjustment:** DevOps proceeds with remediation, but review feedback provided for future enrichments
**Benefit:** No remediation delays, but quality feedback loop maintained

---

## Related Documentation

- **[Security Reviewer Agent Usage Guide](security-reviewer-agent.md)** - How to perform reviews
- **[Security Analysis Review Workflow Deep Dive](review-workflow-deep-dive.md)** - Complete review workflow
- **[Complete Vulnerability Lifecycle Guide](../stories/5.6.complete-vulnerability-lifecycle-guide.md)** - Full lifecycle Stage 3
- **[Configuration Reference & Customization Guide](configuration-reference.md)** - Complete config.yaml reference
- **[Installation & Initial Setup Guide](../stories/5.1.installation-initial-setup-guide.md)** - Initial configuration

---

## Implementation Reference

**Workflow Script:** `expansion-packs/bmad-1898-engineering/workflows/review_trigger.py`
**Configuration:** `expansion-packs/bmad-1898-engineering/config.yaml`
**Sections:** `review_triggers`, `reviewer_assignment`, `notification`

---

**Document Version:** 1.0
**Last Updated:** 2025-11-08
**Epic:** Epic 5 - User Documentation & Usage Guide
**Story:** 5.7 - Priority-Based Review Triggering Reference
