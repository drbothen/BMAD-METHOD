# Integration Tests for Obsidian MCP Tools

This directory contains integration tests for verifying the connection and functionality of Obsidian MCP Tools with Claude Desktop.

## Test Files

### `obsidian-mcp-connection-test.js`

Comprehensive connection testing utility that verifies:

- Configuration validity (API key, host, port)
- Obsidian REST API reachability
- API key authentication
- Vault read permissions
- Claude Desktop configuration
- MCP server binary existence and permissions

## Prerequisites

Before running tests, ensure:

1. **Obsidian is running** with Local REST API plugin enabled
2. **MCP Tools plugin** is installed and configured
3. **Claude Desktop** is installed with MCP server configured
4. **API key** is available from Local REST API plugin settings
5. **Node.js** is installed (v16+ recommended)

## Running Tests

### Basic Usage

Run the connection test with environment variables:

```bash
export OBSIDIAN_API_KEY="your-api-key-here"
node tests/integration/obsidian-mcp-connection-test.js
```

### With Custom Configuration

Override default settings with environment variables:

```bash
export OBSIDIAN_API_KEY="your-api-key-here"
export OBSIDIAN_HOST="localhost"
export OBSIDIAN_PORT="27123"
export OBSIDIAN_PROTOCOL="http"
node tests/integration/obsidian-mcp-connection-test.js
```

### Using HTTPS

If your Local REST API is configured for HTTPS (port 27124):

```bash
export OBSIDIAN_API_KEY="your-api-key-here"
export OBSIDIAN_PORT="27124"
export OBSIDIAN_PROTOCOL="https"
node tests/integration/obsidian-mcp-connection-test.js
```

### Direct Execution (Unix/macOS/Linux)

Make the script executable and run directly:

```bash
chmod +x tests/integration/obsidian-mcp-connection-test.js
export OBSIDIAN_API_KEY="your-api-key-here"
./tests/integration/obsidian-mcp-connection-test.js
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OBSIDIAN_API_KEY` | API key from Local REST API plugin | none | ✅ Yes |
| `OBSIDIAN_HOST` | Hostname where Obsidian is running | `localhost` | No |
| `OBSIDIAN_PORT` | Port for REST API | `27123` | No |
| `OBSIDIAN_PROTOCOL` | Protocol (http or https) | `http` | No |

## Test Output

### Successful Test Run

```
╔════════════════════════════════════════════════════════════╗
║   Obsidian MCP Connection Test Utility v1.0               ║
║   Tests connectivity between Claude, MCP, and Obsidian    ║
╚════════════════════════════════════════════════════════════╝

═══ Configuration Validation ═══
✓ API key configured
ℹ API key length: 20 characters
ℹ Host: localhost
ℹ Port: 27123
ℹ Protocol: http

═══ Obsidian REST API Reachability ═══
✓ REST API server reachable
ℹ Server responded with status: 200

═══ API Key Validation ═══
✓ API key authentication

═══ Vault Read Permission ═══
✓ Vault read permission
ℹ Vault contains 150 files

═══ Claude Desktop Configuration ═══
ℹ Config path: ~/Library/Application Support/Claude/claude_desktop_config.json
✓ Claude Desktop config file exists
✓ Claude Desktop config valid JSON
✓ MCP servers section exists
✓ Obsidian MCP server configured
ℹ Found Obsidian servers: obsidian

═══ MCP Server Binary ═══
✓ MCP binary path configured (obsidian)
✓ MCP binary exists (obsidian)
✓ MCP binary executable (obsidian)

═══ Connection Health Summary ═══

Total Tests: 12
Passed: 12
Failed: 0
Success Rate: 100.0%

✓ All tests passed! MCP connection is properly configured.

Next steps:
ℹ 1. Test MCP operations with Phase 1 agents
ℹ 2. Review MCP Tools Reference documentation
ℹ 3. Explore Error Handling Patterns
```

### Failed Test Run

```
═══ Configuration Validation ═══
✗ API key configured: OBSIDIAN_API_KEY environment variable not set
⚠ Set API key: export OBSIDIAN_API_KEY="your-api-key-here"

═══ Obsidian REST API Reachability ═══
✗ REST API server reachable: connect ECONNREFUSED 127.0.0.1:27123
⚠ Troubleshooting:
⚠ 1. Ensure Obsidian is running
⚠ 2. Verify Local REST API plugin is enabled
⚠ 3. Check port 27123 is not blocked by firewall

...

═══ Connection Health Summary ═══

Total Tests: 10
Passed: 3
Failed: 7
Success Rate: 30.0%

✗ Some tests failed. Review errors above and apply troubleshooting steps.

Common issues:
⚠ • Obsidian not running → Start Obsidian
⚠ • Local REST API disabled → Enable in plugin settings
⚠ • Invalid API key → Copy from Local REST API settings
⚠ • MCP binary missing → Re-run "Install Server" in MCP Tools
⚠ • Claude config invalid → Validate JSON syntax
```

## Exit Codes

- **0** - All tests passed
- **1** - One or more tests failed

Use exit codes for CI/CD integration:

```bash
if node tests/integration/obsidian-mcp-connection-test.js; then
  echo "Connection tests passed"
else
  echo "Connection tests failed"
  exit 1
fi
```

## Troubleshooting

### API Key Not Set

**Error:**
```
✗ API key configured: OBSIDIAN_API_KEY environment variable not set
```

**Solution:**
1. Open Obsidian Settings → Local REST API
2. Copy the API key
3. Export environment variable:
   ```bash
   export OBSIDIAN_API_KEY="your-api-key-here"
   ```

### Connection Refused

**Error:**
```
✗ REST API server reachable: connect ECONNREFUSED
```

**Solution:**
1. Verify Obsidian is running
2. Check Local REST API plugin is enabled in Obsidian settings
3. Verify port number matches plugin settings (default: 27123)
4. Test REST API directly:
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:27123/
   ```

### Authentication Failed

**Error:**
```
✗ API key authentication: API key invalid or unauthorized
```

**Solution:**
1. Copy fresh API key from Local REST API plugin settings
2. Check for extra spaces before/after the API key
3. Regenerate API key if necessary
4. Verify environment variable is set correctly:
   ```bash
   echo $OBSIDIAN_API_KEY
   ```

### Claude Config Not Found

**Error:**
```
✗ Claude Desktop config file exists: File not found
```

**Solution:**
1. Verify Claude Desktop is installed
2. Run Claude Desktop at least once to create config file
3. Check OS-specific config path:
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux:** `~/.config/Claude/claude_desktop_config.json`

### MCP Binary Not Found

**Error:**
```
✗ MCP binary exists: Binary file not found
```

**Solution:**
1. Open Obsidian MCP Tools plugin settings
2. Click **"Install Server"** button
3. Wait for installation to complete
4. Restart test

### MCP Binary Not Executable

**Error:**
```
✗ MCP binary executable: Not executable
```

**Solution (macOS/Linux):**
```bash
chmod +x /path/to/vault/.obsidian/plugins/mcp-tools/bin/mcp-server
```

**Solution (Windows):**
- File permissions should be automatic; verify binary path ends with `.exe`

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Obsidian MCP Connection Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '16'

      - name: Run connection tests
        env:
          OBSIDIAN_API_KEY: ${{ secrets.OBSIDIAN_API_KEY }}
        run: |
          node expansion-packs/bmad-obsidian-2nd-brain/tests/integration/obsidian-mcp-connection-test.js
```

**Note:** CI/CD requires a running Obsidian instance, which may not be practical. These tests are primarily for local development.

## Next Steps

After connection tests pass:

1. **Run Phase 1 Operations Tests:** `phase1-mcp-operations-test.js` (see Story 015, Task 6)
2. **Test Individual Agents:** Test each Phase 1 agent's MCP tool usage
3. **Performance Testing:** Benchmark operation speeds with different vault sizes
4. **Review Documentation:**
   - [MCP Tools Reference](../../docs/mcp-tools-reference.md)
   - [Error Handling Patterns](../../docs/error-handling-patterns.md)
   - [MCP Server Setup Guide](../../docs/installation/mcp-server-setup.md)

## Future Tests

Planned integration tests (not yet implemented):

- `phase1-mcp-operations-test.js` - Test all Phase 1 agent MCP operations
- Performance benchmarks for different vault sizes (10, 100, 1000 notes)
- Concurrent operation tests (multiple agents)
- Error scenario tests (vault not found, permission denied, etc.)

## Contributing

When adding new integration tests:

1. Follow existing test structure and patterns
2. Include detailed error diagnostics
3. Provide troubleshooting guidance in output
4. Document usage in this README
5. Update checklist items as tests are added

## Support

For issues with tests or MCP integration:

1. Review [Troubleshooting](#troubleshooting) section above
2. Check [MCP Server Setup Guide](../../docs/installation/mcp-server-setup.md)
3. Consult [Error Handling Patterns](../../docs/error-handling-patterns.md)
4. Report issues to BMAD repository

---

**Last Updated:** 2025-11-09
**Version:** 1.0
