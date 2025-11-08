# Read JIRA Ticket Task

## Purpose

Read a JIRA security alert ticket via Atlassian MCP, extract CVE IDs and affected system metadata for vulnerability analysis.

## Prerequisites

- Atlassian MCP server configured and connected
- JIRA configuration in `config.yaml` with required fields
- Valid JIRA ticket ID to read

## Configuration Requirements

This task requires JIRA configuration in `expansion-packs/bmad-1898-engineering/config.yaml`:

```yaml
jira:
  cloud_id: 'YOUR_CLOUD_ID_HERE'
  project_key: 'YOUR_PROJECT_KEY'
  custom_fields:
    cve_id: 'customfield_XXXXX'
    affected_systems: 'customfield_XXXXX'
    asset_criticality_rating: 'customfield_XXXXX'
    system_exposure: 'customfield_XXXXX'
```

## Task Steps

### Step 1: Load and Validate Configuration

1. Read the config file at `expansion-packs/bmad-1898-engineering/config.yaml`
2. Verify the `jira` section exists
3. Validate required fields are present:
   - `jira.cloud_id` - JIRA Cloud instance ID
   - `jira.project_key` - Project key (e.g., "AOD")
   - `jira.custom_fields.cve_id` - Custom field ID for CVE tracking
   - `jira.custom_fields.affected_systems` - Custom field ID for affected systems
   - `jira.custom_fields.asset_criticality_rating` - Custom field ID for criticality
   - `jira.custom_fields.system_exposure` - Custom field ID for exposure level

**If validation fails:**

- Missing config file: "❌ Config file not found at expansion-packs/bmad-1898-engineering/config.yaml"
- Missing required field: "❌ Missing required field: jira.cloud_id" (or specific field name)
- HALT and request user to configure

### Step 2: Elicit Ticket ID from User

Ask the user: **"Please provide the JIRA ticket ID to read (e.g., AOD-1234):"**

Validate format: `{PROJECT_KEY}-{NUMBER}` (e.g., AOD-1234, SEC-567)

### Step 3: Read JIRA Ticket

Use the MCP tool to fetch the ticket:

```
mcp__atlassian__getJiraIssue
  issueKey: "{user_provided_ticket_id}"
  cloudId: "{from_config.jira.cloud_id}"
```

**Handle errors gracefully:**

- **Ticket not found:** "❌ Ticket {ticket_id} not found. Verify ticket ID and try again."
- **Authentication failure:** "❌ JIRA authentication failed. Check Atlassian MCP configuration."
- **Network error:** "❌ Cannot connect to JIRA. Check network connection and try again."
- **Rate limit (429):** "⚠️ JIRA rate limit reached. Waiting 60 seconds before retry..." (See Error Recovery section below for retry logic)
- **Other errors:** "❌ Error reading ticket: {error_type}. Please try again or contact support."

If error occurs, prompt user to retry or exit.

### Step 4: Extract CVE IDs

Search for CVE IDs using pattern: `CVE-\d{4}-\d{4,7}` (case-insensitive)

**Search locations (in order):**

1. Ticket summary field: `fields.summary`
2. Ticket description field: `fields.description`
3. Custom CVE ID field: `fields[config.jira.custom_fields.cve_id]`

**Extract ALL CVE IDs found:**

- Use regex with case-insensitive flag
- Collect all matches (may find multiple)
- Designate first CVE as "primary CVE"
- Store all CVEs for processing

**Example extraction:**

```
Summary: "Apache Struts 2 RCE (CVE-2024-1234) and Log4j (CVE-2024-5678)"
Result:
  - All CVEs: [CVE-2024-1234, CVE-2024-5678]
  - Primary CVE: CVE-2024-1234
```

**If no CVE IDs found:**

- Display: "⚠️ No CVE ID found in ticket {ticket_id}."
- Prompt: "Please provide CVE ID manually, or type 'skip' to proceed with generic vulnerability research:"
- If user provides CVE: Add to CVE list as primary
- If user types 'skip': Continue without CVE (set cve_ids to empty list)
- Log warning: "WARNING: No CVE ID available for ticket {ticket_id}"

### Step 5: Extract Affected Systems Metadata

Read custom fields from the ticket response (use primary CVE for ticket-level metadata):

1. **Affected Systems:** `fields[config.jira.custom_fields.affected_systems]`
   - May be string (single system) or array (multiple systems)
   - If string: Split by comma and trim whitespace from each value
   - If null/undefined/empty: Default to empty array `[]`
   - Examples:
     - `"server-01, server-02"` → `["server-01", "server-02"]`
     - `["server-01", "server-02"]` → `["server-01", "server-02"]`
     - `null` → `[]`

2. **Asset Criticality Rating:** `fields[config.jira.custom_fields.asset_criticality_rating]`
   - Expected values: Critical, High, Medium, Low
   - If null/undefined/empty: Default to `"Unknown"`

3. **System Exposure:** `fields[config.jira.custom_fields.system_exposure]`
   - Expected values: Internet-Facing, Internal, Isolated
   - If null/undefined/empty: Default to `"Unknown"`

4. **Additional metadata from standard fields:**
   - Components: `fields.components` (array of component objects)
   - Labels: `fields.labels` (array of strings)
   - Priority: `fields.priority.name`

### Step 6: Display Summary

Present extracted information to user:

```
✅ Successfully read JIRA ticket {ticket_id}

Summary: {ticket_summary}

CVE IDs Found:
  - Primary: {primary_cve}
  - All: {cve_list}

Affected Systems: {affected_systems}
Asset Criticality: {criticality_rating}
System Exposure: {exposure_level}
Priority: {jira_priority}

Components: {components}
Labels: {labels}
```

### Step 7: Return Structured Data

Return the following data structure for use by subsequent tasks:

```yaml
ticket_id: '{ticket_id}'
summary: '{ticket_summary}'
description: '{ticket_description}'
cve_ids:
  primary: '{primary_cve}'
  all: ['{cve_1}', '{cve_2}', ...]
affected_systems: ['{system_1}', '{system_2}', ...]
asset_criticality: '{criticality_rating}'
system_exposure: '{exposure_level}'
priority: '{jira_priority}'
components: ['{component_1}', '{component_2}', ...]
labels: ['{label_1}', '{label_2}', ...]
```

## Security Considerations

**DO NOT:**

- Log JIRA credentials or API tokens
- Display cloud_id in error messages
- Expose internal system names in public logs
- Include stack traces with file paths in user-facing errors

**DO:**

- CVE IDs are public - safe to log
- Sanitize error messages
- Cache ticket data to minimize API calls
- Implement exponential backoff for retries

## Error Recovery

**Rate Limiting:**

- Implement exponential backoff: 60s, 120s, 240s
- Max 3 retries before failing

**Authentication Failures:**

- Guide user to verify MCP configuration
- Check `~/.config/mcp/config.json` or equivalent

**Network Timeouts:**

- Retry once after 30 seconds
- Offer offline mode or alternative input

## Success Criteria

Task completes successfully when:

1. ✅ Config validated and loaded
2. ✅ Ticket read from JIRA via MCP
3. ✅ At least one CVE ID extracted (or user chose to skip)
4. ✅ Affected systems metadata extracted
5. ✅ Structured data returned for next task

## Next Steps

After this task completes, the extracted data will be used by:

- CVE research tasks (enrichment via NVD/CISA)
- Risk assessment workflows
- Remediation planning
- Documentation generation
