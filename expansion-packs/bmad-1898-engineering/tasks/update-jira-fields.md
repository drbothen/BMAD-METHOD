# Update JIRA Fields Task

## Purpose

Update JIRA security alert custom fields with enrichment data (CVSS, EPSS, KEV status, Priority) via Atlassian MCP.

## Prerequisites

- Atlassian MCP server configured and connected
- JIRA configuration in `config.yaml` with custom field mappings
- Valid JIRA ticket ID to update
- Enrichment data from previous research tasks

## Configuration Requirements

This task requires JIRA configuration in `expansion-packs/bmad-1898-engineering/config.yaml`:

```yaml
jira:
  cloud_id: 'YOUR_CLOUD_ID_HERE'
  project_key: 'YOUR_PROJECT_KEY'

  custom_fields:
    cve_id:
      field_id: 'customfield_10001'
      field_type: 'text'
      label: 'CVE ID'
      validation: "^CVE-\\d{4}-\\d{4,7}$"

    cvss_score:
      field_id: 'customfield_10010'
      field_type: 'number'
      label: 'CVSS Base Score'
      min: 0.0
      max: 10.0
      decimals: 1

    epss_score:
      field_id: 'customfield_10011'
      field_type: 'number'
      label: 'EPSS Score'
      min: 0.0
      max: 1.0
      decimals: 2

    kev_status:
      field_id: 'customfield_10012'
      field_type: 'select'
      label: 'CISA KEV Status'
      options: ['Listed', 'Not Listed']

    exploit_status:
      field_id: 'customfield_10013'
      field_type: 'select'
      label: 'Exploit Availability'
      options: ['None', 'PoC', 'Public Exploit', 'Active Exploitation']

  priority_mapping:
    P1: 'Critical'
    P2: 'High'
    P3: 'Medium'
    P4: 'Low'
    P5: 'Trivial'
```

## Task Steps

### Step 1: Load and Validate Configuration

1. Read the config file at `expansion-packs/bmad-1898-engineering/config.yaml`
2. Verify the `jira` section exists
3. Validate required fields are present:
   - `jira.cloud_id` - JIRA Cloud instance ID
   - `jira.project_key` - Project key (e.g., "AOD")
   - `jira.custom_fields` - Custom field mappings section

**Validate each custom field configuration:**

- Each field must have `field_id` property
- Number fields must have `min`, `max`, and `decimals` properties
- Select fields must have `options` array
- Text fields must have `validation` regex (optional)

**If validation fails:**

- Missing config file: "❌ Config file not found at expansion-packs/bmad-1898-engineering/config.yaml"
- Missing required field: "❌ Missing required configuration: {field_path}"
- Invalid field config: "❌ Custom field '{field_name}' missing required property: {property}"
- HALT and request user to configure

### Step 2: Accept Enrichment Data Input

Accept enrichment data structure from previous tasks:

```yaml
ticket_id: 'AOD-1234'
cve_id: 'CVE-2024-1234'
cvss:
  score: 9.8
  vector: 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H'
  severity: 'Critical'
epss:
  score: 0.85432
  percentile: 0.95123
kev:
  status: 'Listed'
  date_added: '2024-01-15'
exploit_status: 'Active Exploitation'
priority_assessment: 'P1'
```

**If enrichment data is missing or incomplete:**

- Display: "⚠️ Warning: Enrichment data is incomplete. Some fields may not be updated."
- Continue with available data (partial update is acceptable)
- Log which fields are being skipped due to missing data

### Step 3: Validate and Prepare Field Values

For each field, validate and format the value:

**CVE ID (Text Field):**

- Read from: `enrichment.cve_id`
- Validation: Must match pattern `CVE-\d{4}-\d{4,7}`
- If invalid: Skip field, log warning "⚠️ Invalid CVE ID format: {value}"
- Format: Use value as-is (e.g., "CVE-2024-1234")

**CVSS Score (Number Field):**

- Read from: `enrichment.cvss.score`
- Validation: Must be between 0.0 and 10.0
- Format: Round to 1 decimal place
- If invalid: Skip field, log error "❌ Cannot update CVSS score: {value} is out of range (0.0-10.0)"
- Additional: Store CVSS vector string for comment/description

**EPSS Score (Number Field):**

- Read from: `enrichment.epss.score`
- Validation: Must be between 0.0 and 1.0
- Format: Round to 2 decimal places
- If invalid: Skip field, log error "❌ Cannot update EPSS score: {value} is out of range (0.0-1.0)"
- Additional: Store EPSS percentile for comment

**KEV Status (Select/Dropdown Field):**

- Read from: `enrichment.kev.status`
- Validation: Must be "Listed" or "Not Listed"
- Format: Dropdown object format `{ value: "Listed" }` or `{ value: "Not Listed" }`
- If invalid: Skip field, log error "❌ Invalid KEV status: {value}. Must be 'Listed' or 'Not Listed'"
- Additional: If Listed, store KEV date_added for comment

**Exploit Status (Select/Dropdown Field):**

- Read from: `enrichment.exploit_status`
- Validation: Must be one of: "None", "PoC", "Public Exploit", "Active Exploitation"
- Format: Dropdown object format `{ value: "{status}" }`
- If invalid: Skip field, log error "❌ Invalid exploit status: {value}"

**Priority (Standard JIRA Field):**

- Read from: `enrichment.priority_assessment`
- Validation: Must be P1, P2, P3, P4, or P5
- Mapping: Use `jira.priority_mapping` from config
  - P1 → "Critical"
  - P2 → "High"
  - P3 → "Medium"
  - P4 → "Low"
  - P5 → "Trivial"
- Format: Standard field format `{ name: "{priority_name}" }`
- If invalid: Skip field, log error "❌ Invalid priority: {value}. Must be P1-P5"

**Validation Summary:**

- Track how many fields passed validation
- Track how many fields failed validation
- Display summary: "✅ {n} fields validated successfully, ⚠️ {m} fields skipped due to invalid data"

### Step 4: Build Field Update Payload

Create the `fields` object for the MCP tool call:

```yaml
fields:
  customfield_10001: 'CVE-2024-1234' # CVE ID (text)
  customfield_10010: 9.8 # CVSS score (number)
  customfield_10011: 0.85 # EPSS score (number, rounded)
  customfield_10012: { value: 'Listed' } # KEV status (select)
  customfield_10013: { value: 'Active Exploitation' } # Exploit status (select)
  priority: { name: 'Critical' } # Priority (standard field)
```

**Important formatting rules:**

- Text/Number fields: Direct value assignment
- Select/Dropdown fields: Object format with `value` property
- Standard JIRA fields (priority): Object format with `name` property
- Only include fields that have valid data (skip fields with validation failures)

**Payload validation:**

- Verify at least one field is being updated
- If no fields to update: Display "⚠️ No valid fields to update. Skipping JIRA field update."
- HALT gracefully without making API call

### Step 5: Execute JIRA Field Update

Use the MCP tool to update the ticket:

```
mcp__atlassian__updateJiraIssue
  issueKey: "{ticket_id}"
  cloudId: "{config.jira.cloud_id}"
  fields: {prepared_fields_object}
```

**Handle MCP errors gracefully:**

**Field Does Not Exist (400 - Invalid field ID):**

```
❌ Custom field '{field_id}' does not exist in JIRA project {project_key}
Action: Skip field update, continue with other fields
Help: Verify field ID in JIRA admin panel (Settings → Issues → Custom Fields)
```

**Permission Denied (403 - Forbidden):**

```
❌ Cannot update fields in {ticket_id}. Edit permission denied.
Action: Skip all field updates, return failure status
Help: Check JIRA user permissions for editing tickets
```

**Invalid Field Value (400 - Validation error):**

```
❌ Field '{field_label}' rejected value: {error_message}
Action: Skip field, log error, continue with other fields
```

**Ticket Not Found (404 - Issue not found):**

```
❌ Ticket {ticket_id} not found. Verify ticket ID and try again.
Action: HALT task execution, return error
```

**Rate Limit (429 - Too many requests):**

```
⚠️ JIRA rate limit reached. Waiting 60 seconds before retry...
Action: Implement exponential backoff (60s, 120s, 240s)
Max retries: 3 attempts
```

**Network/Connection Errors:**

```
❌ Cannot connect to JIRA. Check network connection and try again.
Action: Retry once after 30 seconds, then fail gracefully
```

**Other Errors:**

```
❌ Error updating JIRA fields: {error_type}
Action: Log error details, return failure status
```

### Step 6: Verify and Report Results

**On Success (all fields updated):**

```
✅ Successfully updated {n} fields in ticket {ticket_id}

Updated Fields:
  - CVE ID: CVE-2024-1234
  - CVSS Score: 9.8 (Critical)
  - EPSS Score: 0.85 (95th percentile)
  - KEV Status: Listed (added 2024-01-15)
  - Exploit Status: Active Exploitation
  - Priority: Critical
```

**On Partial Success (some fields updated):**

```
⚠️ Partial update completed for ticket {ticket_id}

Successfully Updated ({n} fields):
  - CVE ID: CVE-2024-1234
  - CVSS Score: 9.8

Failed/Skipped ({m} fields):
  - EPSS Score: Invalid value (1.5 out of range)
  - KEV Status: Field does not exist (customfield_10012)
```

**On Complete Failure (no fields updated):**

```
❌ Failed to update any fields in ticket {ticket_id}

Errors:
  - Permission denied: User lacks edit permissions
  - Contact JIRA admin to grant required permissions
```

**Audit Log Entry:**

- Log all field updates for audit trail
- Include timestamp, ticket ID, fields updated, user/agent
- Format: "{timestamp} - Ticket {ticket_id} - Updated {n} fields: {field_list}"

### Step 7: Store Additional Context in Comment (Optional)

If additional context data exists (CVSS vector, EPSS percentile, KEV date), consider adding a comment with this enrichment metadata. This is optional and depends on workflow requirements.

**Example enrichment context:**

```
Security Enrichment Details:
- CVSS Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
- EPSS Percentile: 95.1%
- KEV Date Added: 2024-01-15
```

## Security Considerations

**DO NOT:**

- Log JIRA credentials or API tokens
- Display cloud_id in user-facing error messages
- Expose internal system details in public logs
- Include stack traces with file paths in error messages

**DO:**

- Sanitize all error messages before displaying
- CVE IDs are public - safe to log
- Cache config data to minimize file reads
- Validate all input data before API calls
- Implement rate limiting and exponential backoff

## Error Recovery

**Rate Limiting:**

- Implement exponential backoff: 60s, 120s, 240s
- Max 3 retries before failing
- Display countdown timer to user

**Field Configuration Errors:**

- Guide user to JIRA admin panel
- Provide example field configuration
- Check `expansion-packs/bmad-1898-engineering/config.yaml`

**Authentication Failures:**

- Guide user to verify MCP configuration
- Check `~/.config/mcp/config.json` or equivalent

**Network Timeouts:**

- Retry once after 30 seconds
- If still failing, offer to skip field updates and continue workflow

## Success Criteria

Task completes successfully when:

1. ✅ Config validated and loaded
2. ✅ Enrichment data validated
3. ✅ At least one field value prepared successfully
4. ✅ JIRA field update executed via MCP
5. ✅ Update results verified and reported

**Acceptable partial success:**

- Some fields updated, some skipped due to validation errors
- Task returns success status with warnings

**Complete failure:**

- No fields updated due to permissions, network, or config errors
- Task returns failure status with error details

## Next Steps

After this task completes:

- Field updates are immediately visible in JIRA
- JIRA automation rules can trigger based on field values
- JQL queries can filter/search using custom field data
- Security dashboards can display enrichment metrics
- Priority-based workflows can route tickets appropriately

## Usage Example

**Input (Enrichment Data):**

```yaml
ticket_id: 'AOD-1234'
cve_id: 'CVE-2024-1234'
cvss:
  score: 9.8
  vector: 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H'
epss:
  score: 0.85432
  percentile: 0.95123
kev:
  status: 'Listed'
  date_added: '2024-01-15'
exploit_status: 'Active Exploitation'
priority_assessment: 'P1'
```

**Output (Success):**

```
✅ Successfully updated 6 fields in ticket AOD-1234

Updated Fields:
  - CVE ID: CVE-2024-1234
  - CVSS Score: 9.8 (Critical)
  - EPSS Score: 0.85 (95th percentile)
  - KEV Status: Listed (added 2024-01-15)
  - Exploit Status: Active Exploitation
  - Priority: Critical

Audit Log: 2024-11-08T10:30:00Z - AOD-1234 - Updated 6 fields via Security Analyst agent
```
