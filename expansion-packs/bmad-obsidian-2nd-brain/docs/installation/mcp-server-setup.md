# MCP Server Configuration Guide

This document provides detailed instructions for configuring the Model Context Protocol (MCP) server to connect Claude Desktop with your Obsidian vault through the MCP Tools plugin.

## Prerequisites

Before configuring the MCP server, ensure you have completed:

- ✅ Installed and configured the **Local REST API** plugin (see [obsidian-plugins.md](./obsidian-plugins.md))
- ✅ Copied your **API key** from Local REST API plugin settings
- ✅ Installed and enabled the **MCP Tools** plugin in Obsidian
- ✅ Installed **Claude Desktop** application

## Overview

The MCP server acts as a bridge between Claude Desktop and your Obsidian vault. The configuration involves:

1. Installing the MCP server binary (automated by MCP Tools plugin)
2. Configuring Claude Desktop to recognize the server
3. Setting environment variables for authentication
4. Verifying the connection

## Configuration Methods

The MCP Tools plugin offers **two configuration methods**:

### Method 1: Automatic Configuration (Recommended)

The MCP Tools plugin automatically configures Claude Desktop when you click "Install Server".

**Advantages:**
- Zero manual configuration
- Automatic binary download and setup
- Correct permissions set automatically
- Platform-specific configuration handled

**Use this method unless:** You need custom configuration or are troubleshooting connection issues.

### Method 2: Manual Configuration

Manual configuration gives you full control over the setup and is useful for:
- Troubleshooting connection issues
- Using custom binary paths
- Advanced environment variable configuration
- Managing multiple Obsidian vaults

**This guide covers both methods.**

---

## Method 1: Automatic Configuration

### Step 1: Open MCP Tools Plugin Settings

1. Open Obsidian
2. Navigate to **Settings → Community Plugins**
3. Find **MCP Tools** in the installed plugins list
4. Click the **gear icon** to open plugin settings

### Step 2: Install MCP Server Binary

1. In MCP Tools settings, locate the **"Install Server"** button
2. Click **"Install Server"**
3. The plugin will:
   - Detect your operating system (Windows/macOS/Linux)
   - Download the appropriate MCP server binary
   - Configure Claude Desktop automatically
   - Set file permissions
4. Wait for the progress indicator to complete
5. You should see a **"Installation Complete"** message

### Step 3: Configure API Key

1. In MCP Tools settings, locate the **"API Key"** field
2. Paste the API key you copied from Local REST API plugin settings
3. Click **"Save"** to store the configuration

### Step 4: Restart Claude Desktop

1. **Completely quit** Claude Desktop (not just close the window)
   - **macOS:** `Cmd+Q` or Claude Desktop → Quit
   - **Windows:** Right-click taskbar icon → Exit
   - **Linux:** Close the application completely
2. Wait 5 seconds
3. **Relaunch** Claude Desktop

### Step 5: Verify Connection

1. Open Claude Desktop
2. Start a new conversation
3. Ask Claude: **"Can you access my Obsidian vault?"**
4. Claude should respond confirming MCP server access
5. Test functionality: **"List the notes in my Obsidian vault"**

✅ **If successful, you're done!** Skip to [Testing MCP Connection](#testing-mcp-connection) section.

⚠️ **If unsuccessful, proceed to Method 2** for manual configuration.

---

## Method 2: Manual Configuration

### Step 1: Locate Claude Desktop Configuration File

The configuration file is located at different paths depending on your operating system:

#### macOS
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

To open in Finder:
1. Open Finder
2. Press `Cmd+Shift+G` (Go to Folder)
3. Paste: `~/Library/Application Support/Claude/`
4. Open `claude_desktop_config.json` in a text editor

#### Windows
```
%APPDATA%\Claude\claude_desktop_config.json
```

To open in Explorer:
1. Press `Win+R` (Run dialog)
2. Type: `%APPDATA%\Claude\`
3. Press Enter
4. Open `claude_desktop_config.json` in a text editor

#### Linux
```
~/.config/Claude/claude_desktop_config.json
```

To open in terminal:
```bash
nano ~/.config/Claude/claude_desktop_config.json
```

### Step 2: Determine MCP Server Binary Location

The MCP Tools plugin installs the server binary in your Obsidian vault's plugin directory. The exact path depends on where Obsidian stores plugins.

**Common paths:**

#### macOS
```
~/Documents/<VaultName>/.obsidian/plugins/mcp-tools/bin/mcp-server
```
or
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/<VaultName>/.obsidian/plugins/mcp-tools/bin/mcp-server
```

#### Windows
```
C:\Users\<Username>\Documents\<VaultName>\.obsidian\plugins\mcp-tools\bin\mcp-server.exe
```

#### Linux
```
~/Documents/<VaultName>/.obsidian/plugins/mcp-tools/bin/mcp-server
```

**To find your vault's plugin directory:**

1. Open Obsidian
2. Open Settings → About
3. Note the **"Vault directory"** path
4. Append `/.obsidian/plugins/mcp-tools/bin/mcp-server` (or `.exe` on Windows)

### Step 3: Create or Edit Configuration File

Open `claude_desktop_config.json` and add the MCP server configuration.

**If the file is empty or doesn't exist, create this structure:**

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "/absolute/path/to/vault/.obsidian/plugins/mcp-tools/bin/mcp-server",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "your-api-key-here",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27123"
      }
    }
  }
}
```

**If the file already has MCP servers, add the "obsidian" entry:**

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "...",
      "args": []
    },
    "obsidian": {
      "command": "/absolute/path/to/vault/.obsidian/plugins/mcp-tools/bin/mcp-server",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "your-api-key-here",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27123"
      }
    }
  }
}
```

### Step 4: Configure Environment Variables

In the `env` section, configure the following variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `OBSIDIAN_API_KEY` | `<your-api-key>` | API key from Local REST API plugin settings |
| `OBSIDIAN_HOST` | `localhost` | Hostname where Obsidian REST API is running (always localhost) |
| `OBSIDIAN_PORT` | `27123` | Port for HTTP connections (default: 27123; use 27124 for HTTPS) |

**Example with actual values:**

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "/Users/john/Documents/MyVault/.obsidian/plugins/mcp-tools/bin/mcp-server",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "a1b2c3d4e5f6g7h8i9j0",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27123"
      }
    }
  }
}
```

### Step 5: Verify JSON Syntax

**CRITICAL:** Invalid JSON will prevent Claude Desktop from starting.

**Common JSON mistakes:**
- Missing commas between entries
- Trailing commas after last entry
- Unescaped backslashes in Windows paths (use `\\` or `/`)
- Mismatched braces or brackets

**Validate your JSON:**
- Use a JSON validator: https://jsonlint.com/
- Or use `jq` command (macOS/Linux): `jq . claude_desktop_config.json`

### Step 6: Save and Restart Claude Desktop

1. **Save** the configuration file
2. **Completely quit** Claude Desktop
3. **Wait 5 seconds**
4. **Relaunch** Claude Desktop

### Step 7: Verify Connection

See [Testing MCP Connection](#testing-mcp-connection) below.

---

## Configuration Templates

### Basic Configuration (HTTP)

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "/path/to/vault/.obsidian/plugins/mcp-tools/bin/mcp-server",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "your-api-key-here",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27123"
      }
    }
  }
}
```

### Secure Configuration (HTTPS)

If you configured Local REST API to use HTTPS (port 27124):

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "/path/to/vault/.obsidian/plugins/mcp-tools/bin/mcp-server",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "your-api-key-here",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27124"
      }
    }
  }
}
```

### Multiple Vaults Configuration

To manage multiple Obsidian vaults, create separate server entries:

```json
{
  "mcpServers": {
    "obsidian-work": {
      "command": "/Users/john/Documents/WorkVault/.obsidian/plugins/mcp-tools/bin/mcp-server",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "work-vault-api-key",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27123"
      }
    },
    "obsidian-personal": {
      "command": "/Users/john/Documents/PersonalVault/.obsidian/plugins/mcp-tools/bin/mcp-server",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "personal-vault-api-key",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27125"
      }
    }
  }
}
```

**Note:** Each vault must use a different port in Local REST API plugin settings.

### Windows Path Example

Use forward slashes or escaped backslashes:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "C:/Users/John/Documents/MyVault/.obsidian/plugins/mcp-tools/bin/mcp-server.exe",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "your-api-key-here",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27123"
      }
    }
  }
}
```

Or with escaped backslashes:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "C:\\Users\\John\\Documents\\MyVault\\.obsidian\\plugins\\mcp-tools\\bin\\mcp-server.exe",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "your-api-key-here",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27123"
      }
    }
  }
}
```

---

## Testing MCP Connection

### Basic Connection Test

1. Open Claude Desktop
2. Start a new conversation
3. Type: **"What MCP servers are available?"**
4. Claude should list "obsidian" (or your custom name) in the response

### Vault Access Test

Ask Claude to perform vault operations:

**Test 1: List Notes**
```
List all notes in my Obsidian vault
```

**Test 2: Read a Note**
```
Read the contents of [note name]
```

**Test 3: Search Notes**
```
Search my vault for notes about [topic]
```

**Test 4: Semantic Search (if Smart Connections is configured)**
```
Find notes semantically related to [concept]
```

### Expected Responses

✅ **Success:** Claude responds with actual vault data (note lists, contents, search results)

❌ **Failure:** Claude responds with:
- "I don't have access to your Obsidian vault"
- "The MCP server is not available"
- "Connection refused"

### Troubleshooting Failed Tests

If tests fail, see [Troubleshooting](#troubleshooting) section below.

---

## Security Considerations

### API Key Security

**DO:**
- ✅ Store API keys securely in password manager
- ✅ Use file system permissions to protect `claude_desktop_config.json`
  - macOS/Linux: `chmod 600 ~/.config/Claude/claude_desktop_config.json`
- ✅ Rotate API keys periodically (every 90 days recommended)
- ✅ Generate new API key if compromised

**DON'T:**
- ❌ Commit `claude_desktop_config.json` to version control
- ❌ Share API keys in screenshots or documentation
- ❌ Use the same API key across multiple systems

### Network Security

**Local Binding:**
- The Local REST API should bind to `localhost` (127.0.0.1) only
- Verify in Local REST API plugin settings: "Host" should be `localhost`
- **Never** bind to `0.0.0.0` (all interfaces) - this exposes your vault to the network

**Firewall:**
- No firewall configuration needed - localhost traffic is internal
- Do not create firewall rules to allow external access to ports 27123/27124

**HTTPS Recommendation:**
- Use HTTPS (port 27124) for encrypted communication
- Certificates are self-signed; this is acceptable for localhost

### File System Permissions

**MCP Server Binary:**
- Should be executable only by your user account
- Verify permissions: `ls -l /path/to/mcp-server` should show `-rwx------`

**Configuration File:**
- Should be readable/writable only by your user account
- Set permissions: `chmod 600 ~/.config/Claude/claude_desktop_config.json`

**Vault Directory:**
- Protect vault directory with appropriate permissions
- Backup vault regularly (git, cloud sync, or local backup)

### Threat Scenarios

| Threat | Risk Level | Mitigation |
|--------|-----------|------------|
| Attacker gains access to `claude_desktop_config.json` | **High** | API key grants full vault access; rotate key immediately |
| API key leaked in screenshot | **High** | Regenerate API key; review where screenshot was shared |
| Malicious prompt injection | **Medium** | MCP has full vault access; trust boundary is at LLM level |
| Local REST API exposed to network | **Critical** | Verify `localhost` binding; never bind to `0.0.0.0` |
| Compromised MCP server binary | **Medium** | Plugin uses signed binaries with SLSA provenance; verify signatures |

---

## Troubleshooting

### MCP Server Not Appearing in Claude Desktop

**Symptoms:**
- Claude responds: "I don't have access to MCP servers"
- Asking "What MCP servers are available?" returns empty list

**Solutions:**
1. **Verify configuration file location is correct** for your OS
2. **Check JSON syntax** using https://jsonlint.com/
3. **Completely quit and restart** Claude Desktop (not just close window)
4. **Check binary path** is absolute and points to actual file
5. **Verify binary permissions** (should be executable)

**Verify binary path:**
```bash
# macOS/Linux
ls -l /path/to/mcp-server
# Should show: -rwxr-xr-x ... mcp-server

# Windows
dir C:\path\to\mcp-server.exe
```

### Connection Refused Errors

**Symptoms:**
- Claude responds: "Connection refused"
- Or: "Cannot connect to Obsidian"

**Solutions:**
1. **Verify Obsidian is running** - MCP requires Obsidian to be open
2. **Check Local REST API plugin is enabled** in Obsidian settings
3. **Verify port number** matches Local REST API settings (default: 27123)
4. **Test REST API directly:**
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:27123/
   ```
   Should return API response (not error)

### Authentication Errors

**Symptoms:**
- Claude responds: "API key invalid"
- Or: "Authentication failed"

**Solutions:**
1. **Verify API key is correct** - copy directly from Local REST API settings
2. **Check for extra spaces** in API key (before/after)
3. **Regenerate API key** in Local REST API settings and update config
4. **Verify environment variable name** is `OBSIDIAN_API_KEY` (not `OBSIDIAN_REST_API_KEY`)

### MCP Server Binary Not Found

**Symptoms:**
- Claude Desktop shows error on startup
- Or: "Cannot execute command"

**Solutions:**
1. **Re-run "Install Server"** in MCP Tools plugin settings
2. **Manually verify binary exists** at the configured path
3. **Check binary permissions** (should be executable)
4. **Use absolute path**, not relative path (e.g., `/Users/john/...` not `~/...`)

### Claude Desktop Won't Start After Config Change

**Symptoms:**
- Claude Desktop crashes on launch
- Or: Shows error dialog

**Solutions:**
1. **Invalid JSON syntax** - validate with https://jsonlint.com/
2. **Restore backup** of `claude_desktop_config.json` if you have one
3. **Delete config file** to reset (Claude will recreate it):
   ```bash
   # macOS/Linux
   mv ~/.config/Claude/claude_desktop_config.json ~/.config/Claude/claude_desktop_config.json.backup
   ```
4. **Start fresh** with basic configuration template

### Smart Connections Semantic Search Not Working

**Symptoms:**
- Basic vault access works
- Semantic search returns no results or errors

**Solutions:**
1. **Verify Smart Connections plugin is enabled** in Obsidian
2. **Ensure vault is indexed** - check Smart Connections settings for indexing progress
3. **Wait for indexing to complete** - can take 5-60 minutes depending on vault size
4. **Check Smart Connections MCP integration** - may require separate configuration

### Multiple Vaults Not Working

**Symptoms:**
- Can only access one vault at a time
- Claude confuses vaults

**Solutions:**
1. **Use unique server names** (e.g., `obsidian-work`, `obsidian-personal`)
2. **Configure different ports** for each vault's Local REST API
3. **Use separate API keys** for each vault
4. **Specify which vault** when asking Claude (e.g., "In my work vault, ...")

---

## Verification Checklist

Use this checklist to verify your MCP server configuration:

- [ ] `claude_desktop_config.json` file exists at correct OS-specific location
- [ ] JSON syntax is valid (verified with jsonlint or jq)
- [ ] MCP server entry exists under `mcpServers` key
- [ ] `command` path is absolute and points to actual binary file
- [ ] Binary file has executable permissions
- [ ] `OBSIDIAN_API_KEY` environment variable is set with correct API key
- [ ] `OBSIDIAN_HOST` is set to `localhost`
- [ ] `OBSIDIAN_PORT` matches Local REST API plugin settings (default: 27123)
- [ ] Claude Desktop was completely quit and restarted after config changes
- [ ] Obsidian is running with Local REST API plugin enabled
- [ ] Claude Desktop recognizes MCP server (test: "What MCP servers are available?")
- [ ] Vault access test passes (test: "List notes in my Obsidian vault")

---

## Advanced Configuration

### Using Environment Variables from Shell

Instead of hardcoding the API key in JSON, you can reference shell environment variables:

**Set environment variable:**
```bash
# macOS/Linux - add to ~/.bashrc or ~/.zshrc
export OBSIDIAN_API_KEY="your-api-key-here"

# Windows - use System Environment Variables UI
setx OBSIDIAN_API_KEY "your-api-key-here"
```

**Reference in config:**
```json
{
  "mcpServers": {
    "obsidian": {
      "command": "/path/to/mcp-server",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "${OBSIDIAN_API_KEY}",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27123"
      }
    }
  }
}
```

**Note:** Variable substitution may not work in all MCP client implementations. Test thoroughly.

### Custom Server Arguments

The MCP Tools server binary accepts optional arguments:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "/path/to/mcp-server",
      "args": [
        "--log-level", "debug",
        "--timeout", "30"
      ],
      "env": {
        "OBSIDIAN_API_KEY": "your-api-key-here",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27123"
      }
    }
  }
}
```

**Note:** Available arguments depend on MCP server version. Check plugin documentation.

### Logging and Debugging

To enable verbose logging:

1. **Enable debug mode in MCP Tools plugin settings** (if available)
2. **Check Claude Desktop logs:**
   - **macOS:** `~/Library/Logs/Claude/`
   - **Windows:** `%LOCALAPPDATA%\Claude\logs\`
   - **Linux:** `~/.local/share/Claude/logs/`
3. **Check Obsidian Developer Console:** `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Option+I` (macOS)

---

## Next Steps

After successfully configuring the MCP server:

1. **Test Connection:** Run [connection tests](../tests/integration/obsidian-mcp-connection-test.js)
2. **Explore MCP Tools:** Review [MCP Tools Reference](../mcp-tools-reference.md)
3. **Enable Phase 1 Agents:** Start using AI agents for vault management
4. **Review Error Handling:** See [Error Handling Patterns](../error-handling-patterns.md)

---

## Additional Resources

- **Model Context Protocol Documentation:** https://modelcontextprotocol.io/
- **MCP Tools Plugin GitHub:** https://github.com/jacksteamdev/obsidian-mcp-tools
- **Local REST API Plugin GitHub:** https://github.com/coddingtonbear/obsidian-local-rest-api
- **Claude Desktop Documentation:** https://support.claude.com/
- **JSON Validator:** https://jsonlint.com/

---

**Document Version:** 1.0
**Last Updated:** 2025-11-09
**Author:** BMAD Development Team
