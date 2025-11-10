# Security Analyst Quick Reference Card
**Event Investigation Workflow**

---

## Command

```
*investigate-event {ticket-id}
```

**Duration:** 15-25 minutes | **Output:** Investigation report in JIRA

---

## 5-Stage Investigation Workflow

### 1. Alert Triage (2-3 min)
- [ ] Extract alert metadata (platform, rule ID, severity, timestamp)
- [ ] Document network identifiers (IPs, hostnames, protocols, ports)
- [ ] Identify affected assets and criticality
- [ ] Note alert frequency (first occurrence vs. recurring)

### 2. Evidence Collection (5-8 min)
- [ ] Gather logs from alert source (ICS/IDS/SIEM)
- [ ] Correlate with firewall/proxy logs
- [ ] Check for related alerts (same source/destination)
- [ ] Research historical patterns (past 7-30 days)
- [ ] Document asset communication baselines

### 3. Technical Analysis (4-6 min)
- [ ] Validate protocol behavior (expected vs. observed)
- [ ] Assess potential attack vectors
- [ ] Evaluate asset context (function, business impact)
- [ ] Consider ICS/SCADA implications (if applicable)
- [ ] Generate and test multiple hypotheses

### 4. Disposition Determination (2-3 min)
- [ ] Determine disposition: **TP / FP / BTP**
- [ ] Assign confidence level: **High / Medium / Low**
- [ ] Document reasoning with specific evidence
- [ ] Consider alternative explanations

### 5. Recommendations (2-3 min)
- [ ] Immediate actions (containment, escalation, tuning)
- [ ] Long-term improvements (detection tuning, process changes)
- [ ] Escalation requirements (SOC lead, IR team)

---

## Disposition Decision Tree

```
┌─────────────────────────────────┐
│ Did alert trigger correctly?    │
└─────────┬───────────────────────┘
          │
    ┌─────┴─────┐
   NO          YES
    │            │
    ▼            ▼
  FALSE      ┌────────────────────┐
POSITIVE     │ Is activity         │
  (FP)       │ malicious/          │
             │ unauthorized?       │
             └────┬───────────────┘
                  │
            ┌─────┴─────┐
           YES          NO
            │            │
            ▼            ▼
          TRUE      BENIGN TRUE
        POSITIVE    POSITIVE
          (TP)        (BTP)
```

---

## Disposition Definitions

| Disposition | Definition | Actions |
|-------------|------------|---------|
| **TP** (True Positive) | Malicious activity confirmed | Escalate to IR team, containment, preserve evidence |
| **FP** (False Positive) | Alert incorrect, no malicious activity | Document root cause, recommend tuning, no escalation |
| **BTP** (Benign True Positive) | Real activity, but authorized/expected | Create exception, document authorization, no containment |

---

## Confidence Levels

| Level | Criteria |
|-------|----------|
| **High** | Multiple corroborating evidence sources, clear attack pattern/authorization, no contradictory evidence |
| **Medium** | Some evidence gaps, partial corroboration, minor contradictions |
| **Low** | Limited evidence, significant gaps, conflicting data, requires escalation |

---

## Common Cognitive Biases

| Bias | Description | Mitigation |
|------|-------------|------------|
| **Automation Bias** | Over-trusting automated alerts | Verify alert logic, don't assume correctness |
| **Anchoring** | Fixating on first piece of evidence | Consider all evidence equally |
| **Confirmation** | Seeking evidence that confirms hypothesis | Actively seek contradictory evidence |
| **Availability** | Overweighting recent/memorable events | Use data-driven analysis, not recent memory |

---

## Platform-Specific Tips

### Claroty ICS Alerts
- **Focus on:** OT protocol validation, safety implications, asset function
- **Key Questions:** Does protocol behavior match expected operations? Is this change management-related?

### Snort IDS Alerts
- **Focus on:** Signature accuracy, PCAP analysis, protocol decoding
- **Key Questions:** Is payload actually malicious? Is server vulnerable to exploit?

### Splunk SIEM Alerts
- **Focus on:** Correlation across sources, user behavior, authentication patterns
- **Key Questions:** Is this consistent with user's normal behavior? Are there correlated events?

---

## Critical Questions Checklist

- [ ] What is the business function of the affected asset?
- [ ] What is the asset's criticality rating?
- [ ] Is this behavior consistent with the asset's normal operations?
- [ ] Are there any authorized changes (change tickets, maintenance windows)?
- [ ] Has this alert triggered before? What was the outcome?
- [ ] What is the potential impact if this is a true positive?
- [ ] What evidence would prove/disprove my hypothesis?

---

## Escalation Criteria

**Always escalate if:**
- True Positive (TP) determination (any severity)
- Critical/High severity alerts (regardless of disposition)
- Potential ICS/SCADA safety impact
- Confidence level is LOW (unclear disposition)
- Evidence suggests ongoing active compromise

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Rushing to disposition | Follow all 5 stages systematically |
| Ignoring business context | Always research asset function and criticality |
| Insufficient evidence | Collect from multiple sources before concluding |
| Confirmation bias | Generate and test alternative hypotheses |
| Poor documentation | Document reasoning with specific evidence references |

---

**Need Help?** See: `docs/troubleshooting-faq-best-practices.md`
**Deep Dive:** See: `docs/workflows/event-investigation-workflow-deep-dive.md`
**Training:** See: `docs/training/event-investigation-training.md`
