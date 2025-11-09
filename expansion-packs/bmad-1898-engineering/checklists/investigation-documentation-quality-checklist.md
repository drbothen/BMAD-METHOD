# Investigation Documentation Quality Checklist

**Weight:** 5%
**Purpose:** Verify clear, professional, structured documentation that enables understanding and verification.

## Check Items

- [ ] **Logical Structure and Flow** - Investigation follows clear narrative (Alert → Context → Investigation → Evidence → Disposition → Next Actions), sections logically ordered
- [ ] **Professional Tone and Language** - Appropriate terminology, no slang or colloquialisms, technical precision maintained
- [ ] **Minimal Typos/Grammatical Errors** - Fewer than 5 errors in entire document (spell-check quality)
- [ ] **Key Findings Highlighted or Summarized** - Executive summary, key findings section, or highlights present for quick consumption
- [ ] **Evidence References Clear and Verifiable** - Log excerpts include timestamps, source systems, and context; references enable verification
- [ ] **Timestamps in Consistent Format** - All timestamps use same format (preferably UTC with timezone noted, e.g., "2024-11-09 14:32:15 UTC")

## Scoring

- **Total Items:** 6
- **Passed Items:** [count after review]
- **Score:** (Passed / 6) × 100 = ____%

## Guidance

### Logical Structure and Flow

**Recommended Investigation Document Structure:**

1. **Alert Summary** (What triggered the investigation?)
   - Alert source, rule ID, severity, timestamps
   - Source/destination IPs, protocol, port
   - Alert description

2. **Asset Context** (What assets are involved?)
   - Asset identification (hostnames, types, criticality)
   - Asset ownership and business function
   - Environmental context (prod vs. test, maintenance windows)

3. **Investigation Scope and Methodology** (How did you investigate?)
   - Hypothesis or investigative question
   - Data sources consulted
   - Investigation steps taken

4. **Evidence and Findings** (What did you find?)
   - Log excerpts, screenshots, data collected
   - Historical context, patterns observed
   - Negative findings (what was checked but not found)

5. **Analysis** (What does the evidence mean?)
   - Alternative explanations considered
   - Reasoning for disposition
   - Confidence level assessment

6. **Disposition and Recommendations** (What's the conclusion?)
   - Clear disposition (TP/FP/BTP)
   - Business impact and risk assessment
   - Escalation decision
   - Next actions (alert tuning, escalation, monitoring)

**Well-Structured Example:**
```
# SSH Connection Investigation - 2024-11-09

## Alert Summary
- Source: Claroty IDS
- Rule: SSH_Unusual_Destination_V2 (ID: 4782)
- Severity: High
- Detection: 2024-11-09 14:32:15 UTC
- Event: 10.50.1.100:54321 → 10.10.5.25:22 (SSH)

## Asset Context
[Asset details...]

## Investigation
[Steps and methodology...]

## Evidence
[Logs and data...]

## Analysis
[Interpretation and reasoning...]

## Disposition
**False Positive** (Confidence: High)
[Reasoning and next actions...]
```

**Poorly Structured Example:**
```
Alert from Claroty. SSH traffic. Checked some logs. Looks like backup. False positive. Close ticket.
```

### Professional Tone and Language

**Professional Examples:**

✓ "Investigation revealed authorized SSH connection for scheduled backup operations"
✓ "Evidence supports False Positive disposition with high confidence"
✓ "Recommend alert tuning to exclude authorized jump server connections during maintenance window"

**Unprofessional Examples:**

✗ "This alert is totally bogus, just some backup thing" (casual slang)
✗ "Obviously this is fine, don't waste time on this" (dismissive tone)
✗ "IDK what this is but probably nothing" (texting abbreviations)
✗ "This is a dumb alert" (unprofessional criticism)

**Technical Precision:**

✓ "SSH connection authenticated using RSA public key (fingerprint: aa:bb:cc:dd:ee:ff)"
✗ "SSH login with some key thing"

✓ "Historical analysis (90 days) reveals daily pattern at 02:00 UTC ±5 minutes"
✗ "This happens all the time at like 2am or something"

### Typos and Grammatical Errors

**Acceptable:** <5 errors per document
**Needs Improvement:** 5-10 errors
**Inadequate:** >10 errors

**Common Error Types:**

**Spelling Errors:**
- "Conektion" → "Connection"
- "Authentification" → "Authentication"
- "Occured" → "Occurred"

**Capitalization Errors:**
- "false Positive" → "False Positive" or "false positive" (be consistent)
- "ssh" → "SSH" (acronyms capitalized)

**Grammar Errors:**
- "Connection was occurred" → "Connection occurred"
- "Logs was reviewed" → "Logs were reviewed"
- "Disposition are False Positive" → "Disposition is False Positive"

**Technical Term Errors:**
- "IP adress" → "IP address"
- "Mac address" → "MAC address"
- "Firewall rule's" → "Firewall rules" (unnecessary apostrophe)

**Note:** Minor typos are acceptable (this is a 5% weight dimension), but excessive errors damage credibility.

### Key Findings Summary

**Why Summaries Matter:**
- Busy stakeholders (managers, IR team) need quick answers
- Enables rapid triage (is this critical or routine?)
- Improves searchability (can find key info without reading full investigation)

**Good Summary Examples:**

**Example 1: Executive Summary**
```
## Executive Summary

**Disposition:** False Positive (Confidence: High)

**Key Findings:**
- Alert detected authorized SSH connection from jump server to backup file server
- Connection occurs daily at 02:00 UTC as part of scheduled backup operation (87 occurrences in 90 days)
- SSH authentication used authorized IT Operations public key
- No indicators of compromise on source or destination systems

**Recommendation:** Tune alert to exclude authorized jump server → backup server connections during maintenance window (00:00-04:00 UTC)

**Business Impact:** None (authorized administrative activity)
```

**Example 2: Key Findings Highlights**
```
## Key Findings

✓ Source: Authorized jump server (10.50.1.100)
✓ Destination: Backup file server (10.10.5.25)
✓ Pattern: Daily at 02:00 UTC (87 occurrences in 90 days)
✓ Authentication: Authorized SSH key (IT Ops registry #129)
✗ No IOCs or suspicious activity detected
```

**Poor Summary (Missing):**
```
[No summary section - reader must read entire 5-page investigation to understand conclusion]
```

### Evidence References

**Well-Referenced Evidence:**

```
**Evidence 1: SSH Authentication Log (10.10.5.25)**

Source: /var/log/auth.log on file-server-backup.corp.local (10.10.5.25)
Timestamp: 2024-11-09 14:30:00 UTC
Entry:
```
Nov 09 14:30:00 file-server-backup sshd[12345]: Accepted publickey for backup_user from 10.50.1.100 port 54321 ssh2: RSA SHA256:aa:bb:cc:dd:ee:ff
```

**Interpretation:**
- Authentication method: Public key (RSA)
- User account: backup_user (authorized service account)
- Key fingerprint: SHA256:aa:bb:cc:dd:ee:ff (verified against IT Ops key registry entry #129)
```

**Poorly Referenced Evidence:**

```
Checked logs. SSH connection succeeded.
```
(Which logs? When? What did they say? How can this be verified?)

**Key Elements of Good References:**
- Source system clearly identified
- Timestamp in consistent format (UTC preferred)
- Actual log excerpt (verbatim, not paraphrased)
- Interpretation separated from raw data
- Verification method noted (e.g., "cross-referenced with asset DB")

### Timestamp Consistency

**Why Timestamp Consistency Matters:**
- Enables correlation across systems
- Prevents confusion (UTC vs. local time errors are common)
- Professional appearance
- Supports timeline reconstruction

**Recommended Format:** ISO 8601 with timezone
- `2024-11-09 14:32:15 UTC`
- `2024-11-09T14:32:15Z` (ISO 8601 with Z = UTC)

**Consistent Example:**
```
Alert Detection: 2024-11-09 14:32:15 UTC
Event Occurrence: 2024-11-09 14:30:00 UTC
Log Entry: 2024-11-09 14:30:00 UTC
Investigation Start: 2024-11-09 14:35:00 UTC
```

**Inconsistent Example (Problematic):**
```
Alert Detection: 11/9/2024 2:32 PM
Event Occurrence: Nov 09 14:30 (which timezone?)
Log Entry: 1699542600 (Unix timestamp - hard to read)
Investigation Start: 2024-11-09T14:35:00Z (different format)
```

**Timezone Handling:**
- **Preferred:** Use UTC for all timestamps (universal, no DST ambiguity)
- **Acceptable:** Use local time if clearly marked (e.g., "14:30:00 EST")
- **Problematic:** Mix UTC and local time without clear labels

**Consistency Check:**
- Pick ONE timestamp format and use it throughout the document
- Always include timezone (UTC, EST, PST, etc.)
- If converting timezones, show conversion (e.g., "14:30 UTC (9:30 AM EST)")

### Examples

#### Example 1: High Documentation Quality

```
# Security Alert Investigation - SSH Connection Analysis

**Investigation ID:** INV-2024-1109-001
**Date:** 2024-11-09
**Analyst:** Jane Smith
**Status:** Closed - False Positive

---

## Executive Summary

**Disposition:** False Positive (Confidence: High)

Alert detected SSH connection from authorized jump server (10.50.1.100) to backup file server (10.10.5.25). Investigation confirmed this is scheduled backup operation occurring daily at 02:00 UTC. No security concerns identified. Recommend alert tuning to reduce false positive noise.

---

## Alert Details

**Source:** Claroty IDS Platform
**Rule:** SSH_Unusual_Destination_V2 (Rule ID: 4782)
**Severity:** High
**Detection Time:** 2024-11-09 14:32:15 UTC
**Event Time:** 2024-11-09 14:30:00 UTC

**Network Activity:**
- Source: 10.50.1.100:54321 (jump-server-01.corp.local)
- Destination: 10.10.5.25:22 (file-server-backup.corp.local)
- Protocol: TCP/SSH
- Duration: 180 seconds

[... continues with well-structured sections ...]
```

**Quality Score:** 6/6 = 100%
- ✓ Logical structure (clear sections, flow)
- ✓ Professional tone ("Investigation confirmed" vs. "totally obvious")
- ✓ No significant typos
- ✓ Executive summary present
- ✓ Evidence clearly referenced with timestamps
- ✓ Consistent timestamp format (YYYY-MM-DD HH:MM:SS UTC)

---

#### Example 2: Poor Documentation Quality

```
SSH alert from clartoy

Source 10.50.1.1OO (typo in IP)
dest 10.10.5.25

Checked logs looks like backup stuff happens at like 2am everyday so its probly fine

searched siem no badness found

Dispositoin: FP

close ticket
```

**Quality Score:** 0/6 = 0%
- ✗ No logical structure (random fragments)
- ✗ Unprofessional tone ("probly fine", "badness")
- ✗ Multiple typos (clartoy, 1.1OO, Dispositoin, probly, its)
- ✗ No summary or highlights
- ✗ No evidence references (which logs? when? what exactly did they say?)
- ✗ No timestamps, inconsistent format ("2am" - which timezone?)

---

### Weighting Rationale

**Why 5% (Lowest Weight)?**

Documentation quality is important for communication and professionalism, but **substance matters more than style**. An investigation with perfect grammar but wrong conclusions is worse than one with typos but correct disposition.

**Prioritization:**
1. **Correctness** (Accuracy, Completeness, Disposition) → 65% combined weight
2. **Context** (Contextualization, Methodology) → 25% combined weight
3. **Communication** (Documentation Quality) → 5% weight
4. **Bias Detection** (Cognitive Bias) → 5% weight

**When Documentation Quality Becomes Critical:**
- External reporting (customers, regulators, executives)
- Incident response hand-off (IR team needs clear details)
- Compliance documentation (audit trail, regulatory requirements)
- Tuning justification (explain why alert should be modified)

**Quality Thresholds:**

**Excellent (6/6):** Professional, clear, well-structured documentation
**Good (4-5/6):** Readable with minor issues (few typos, mostly clear)
**Needs Improvement (3/6):** Unclear structure, multiple errors, missing summary
**Inadequate (<3/6):** Unprofessional, many errors, incomprehensible structure
