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

## Graphiti MCP Server Configuration (Optional)

This section covers configuring **Graphiti MCP** alongside the Obsidian MCP server for temporal knowledge tracking with Neo4j.

### What is Graphiti MCP?

Graphiti provides temporal knowledge graph capabilities:
- Store episodic memories with timestamps (capture events)
- Track knowledge evolution over time
- Query by time range ("notes from last week")
- Create semantic relationships with confidence scores

**Prerequisites:**
- ✅ Neo4j installed and running (see [neo4j-setup.md](./neo4j-setup.md))
- ✅ Graphiti MCP server installed (see [graphiti-mcp-setup.md](./graphiti-mcp-setup.md))
- ✅ Obsidian MCP configured (previous sections)

**Important:** Graphiti is completely optional. The system works without it in Obsidian-only mode.

---

### Multi-Server Configuration Overview

Claude Desktop supports multiple MCP servers running simultaneously. You'll configure:

1. **Obsidian MCP** - Vault access and management
2. **Graphiti MCP** - Temporal knowledge tracking

Both servers coexist in the same `claude_desktop_config.json` file.

---

### Configuration Template (macOS)

**File:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "/Users/<username>/Documents/<VaultName>/.obsidian/plugins/mcp-tools/bin/mcp-server",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "your-obsidian-api-key-here",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27123"
      }
    },
    "graphiti": {
      "command": "/Users/<username>/.local/bin/uv",
      "args": [
        "run",
        "--with", "graphiti-core",
        "--with", "mcp",
        "graphiti-server"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "${NEO4J_PASSWORD}",
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "MODEL_NAME": "gpt-4o-mini"
      }
    }
  }
}
```

**Replace placeholders:**
- `<username>` - Your macOS username
- `<VaultName>` - Your Obsidian vault name
- `your-obsidian-api-key-here` - Actual Obsidian REST API key
- `${NEO4J_PASSWORD}` - Neo4j password from `.env` file
- `${OPENAI_API_KEY}` - OpenAI API key

---

### Configuration Template (Windows)

**File:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "C:/Users/<Username>/Documents/<VaultName>/.obsidian/plugins/mcp-tools/bin/mcp-server.exe",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "your-obsidian-api-key-here",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27123"
      }
    },
    "graphiti": {
      "command": "C:/Users/<Username>/.local/bin/uv.exe",
      "args": [
        "run",
        "--with", "graphiti-core",
        "--with", "mcp",
        "graphiti-server"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "${NEO4J_PASSWORD}",
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "MODEL_NAME": "gpt-4o-mini"
      }
    }
  }
}
```

**Note:** Use forward slashes (`/`) or escaped backslashes (`\\`) in Windows paths.

---

### Configuration Template (Linux)

**File:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "/home/<username>/Documents/<VaultName>/.obsidian/plugins/mcp-tools/bin/mcp-server",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "your-obsidian-api-key-here",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27123"
      }
    },
    "graphiti": {
      "command": "/home/<username>/.local/bin/uv",
      "args": [
        "run",
        "--with", "graphiti-core",
        "--with", "mcp",
        "graphiti-server"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "${NEO4J_PASSWORD}",
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "MODEL_NAME": "gpt-4o-mini"
      }
    }
  }
}
```

---

### Environment Variable Configuration

For security, use environment variable substitution instead of hardcoding sensitive values.

#### macOS/Linux Setup

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Obsidian MCP
export OBSIDIAN_API_KEY="your-obsidian-api-key"

# Graphiti MCP
export NEO4J_PASSWORD="your-neo4j-password"
export OPENAI_API_KEY="sk-your-openai-key"
```

Reload shell configuration:
```bash
source ~/.bashrc  # or ~/.zshrc
```

Verify variables are set:
```bash
echo $OBSIDIAN_API_KEY
echo $NEO4J_PASSWORD
echo $OPENAI_API_KEY
```

#### Windows Setup

1. Open **System Properties → Environment Variables**
2. Click **New** under "User variables"
3. Add variables:
   - `OBSIDIAN_API_KEY` = your-obsidian-api-key
   - `NEO4J_PASSWORD` = your-neo4j-password
   - `OPENAI_API_KEY` = sk-your-openai-key
4. Click **OK** to save
5. Restart Claude Desktop

Verify variables (PowerShell):
```powershell
echo $env:OBSIDIAN_API_KEY
echo $env:NEO4J_PASSWORD
echo $env:OPENAI_API_KEY
```

---

### Alternative: Hardcoded Configuration (Not Recommended)

If environment variable substitution doesn't work, hardcode values (**security risk**):

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "/path/to/mcp-server",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "a1b2c3d4e5f6g7h8",
        "OBSIDIAN_HOST": "localhost",
        "OBSIDIAN_PORT": "27123"
      }
    },
    "graphiti": {
      "command": "/path/to/uv",
      "args": ["run", "--with", "graphiti-core", "--with", "mcp", "graphiti-server"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "actual-password-here",
        "OPENAI_API_KEY": "sk-actual-key-here",
        "MODEL_NAME": "gpt-4o-mini"
      }
    }
  }
}
```

**Security warnings:**
- ⚠️ File contains plaintext credentials
- ⚠️ Set file permissions: `chmod 600 claude_desktop_config.json`
- ⚠️ Never commit to version control
- ⚠️ Rotate credentials if file is compromised

---

### Verifying Multi-Server Configuration

#### Step 1: Validate JSON Syntax

```bash
# macOS/Linux
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool

# Windows PowerShell
Get-Content $env:APPDATA\Claude\claude_desktop_config.json | python -m json.tool

# Or use online validator
# https://jsonlint.com/
```

#### Step 2: Verify Prerequisites

Check that all required services are running:

```bash
# Check Neo4j (should return "Up")
docker compose -f docker-compose.neo4j.yml ps

# Check Graphiti (if using Docker)
docker compose -f ~/Development/graphiti/docker-compose.yml ps

# Test Neo4j connection
curl http://localhost:7474
# Expected: Neo4j Browser page

# Test Graphiti health endpoint
curl http://localhost:8000/health
# Expected: {"status": "healthy", "neo4j": "connected"}
```

#### Step 3: Restart Claude Desktop

```bash
# macOS
osascript -e 'quit app "Claude"'
sleep 5
open -a Claude

# Windows
# Use Task Manager to end "Claude.exe"
# Then relaunch from Start Menu

# Linux
pkill -f claude
sleep 5
claude &
```

#### Step 4: Test Both MCP Servers

Open Claude Desktop and test:

**Test 1: List MCP servers**
```
What MCP servers are available?
```

Expected response should list both:
- `obsidian`
- `graphiti`

**Test 2: Test Obsidian MCP**
```
List notes in my Obsidian vault
```

Expected: List of actual notes from your vault

**Test 3: Test Graphiti MCP**
```
What Graphiti tools are available?
```

Expected: List including `add_episode`, `get_episodes`, `add_entity`, `add_relation`

**Test 4: Combined Operation**
```
Create a capture event for today with note "Testing Graphiti integration"
```

Expected: Confirmation of event creation in Neo4j

---

### Troubleshooting Multi-Server Setup

#### Issue: Only Obsidian MCP Works, Not Graphiti

**Symptoms:**
- Obsidian commands work
- Graphiti commands fail or are unavailable

**Solutions:**

1. **Check Graphiti command path:**
   ```bash
   which uv
   # Should return: /Users/<username>/.local/bin/uv
   ```

2. **Verify Neo4j is running:**
   ```bash
   docker compose -f docker-compose.neo4j.yml ps
   # Should show "Up"
   ```

3. **Test Graphiti manually:**
   ```bash
   uv run --with graphiti-core --with mcp graphiti-server
   # Should start without errors
   ```

4. **Check Claude Desktop logs:**
   ```bash
   # macOS
   tail -f ~/Library/Logs/Claude/mcp-graphiti.log
   ```

#### Issue: Environment Variables Not Resolved

**Symptoms:**
- Error: "Invalid Neo4j password"
- Or: "OpenAI API key not set"

**Solutions:**

1. **Verify variables are exported:**
   ```bash
   echo $NEO4J_PASSWORD
   echo $OPENAI_API_KEY
   ```

2. **If empty, export manually:**
   ```bash
   export NEO4J_PASSWORD="your-password"
   export OPENAI_API_KEY="sk-your-key"
   ```

3. **Restart Claude Desktop from terminal:**
   ```bash
   # macOS - launch from terminal to inherit env vars
   /Applications/Claude.app/Contents/MacOS/Claude &
   ```

4. **Alternative: Use hardcoded values** (see Alternative configuration above)

#### Issue: JSON Syntax Error

**Symptoms:**
- Claude Desktop won't start
- Error: "Failed to parse configuration"

**Solutions:**

1. **Common JSON mistakes:**
   - Missing comma between server entries
   - Trailing comma after last entry
   - Unmatched braces `{}` or brackets `[]`
   - Unescaped backslashes in paths (Windows)

2. **Validate JSON:**
   ```bash
   python3 -m json.tool < claude_desktop_config.json
   ```

3. **Fix and retry:**
   - Save corrected file
   - Restart Claude Desktop

#### Issue: Both Servers Not Working

**Symptoms:**
- Claude reports no MCP servers available
- Both Obsidian and Graphiti fail

**Solutions:**

1. **Verify configuration file location:**
   ```bash
   # macOS
   ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json

   # Windows
   dir %APPDATA%\Claude\claude_desktop_config.json

   # Linux
   ls -la ~/.config/Claude/claude_desktop_config.json
   ```

2. **Check file permissions:**
   ```bash
   chmod 600 ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

3. **Restore from backup:**
   ```bash
   cp claude_desktop_config.json.backup claude_desktop_config.json
   ```

4. **Start with minimal config:**
   - Remove Graphiti entry
   - Test Obsidian-only
   - Add Graphiti back incrementally

---

### Testing Temporal Knowledge Tracking

After configuring both MCP servers, test the complete integration:

#### Test 1: Create Capture Event

```
Using Graphiti, create a capture event for today with the note "Testing temporal tracking"
```

**Expected:** Confirmation that event was created in Neo4j

#### Test 2: Query Recent Events

```
Using Graphiti, retrieve capture events from the last 7 days
```

**Expected:** List including the event just created

#### Test 3: Link Notes

```
Create a relationship between note "Project Ideas" and note "Implementation Plan" with confidence 0.8
```

**Expected:** Confirmation of relationship creation

#### Test 4: Verify in Neo4j Browser

1. Open Neo4j Browser: http://localhost:7474
2. Run Cypher query:
   ```cypher
   MATCH (e:CaptureEvent)
   WHERE e.timestamp > datetime() - duration('P7D')
   RETURN e.timestamp, e.note
   ORDER BY e.timestamp DESC
   LIMIT 10
   ```
3. Should see created events

---

### Performance Considerations

#### OpenAI API Usage

Graphiti calls OpenAI for entity extraction. To optimize costs:

```json
{
  "mcpServers": {
    "graphiti": {
      "env": {
        "MODEL_NAME": "gpt-4o-mini",
        ...
      }
    }
  }
}
```

**Model options:**
- `gpt-4o-mini` - Fast, cost-effective (recommended)
- `gpt-4o` - More accurate, higher cost
- `gpt-4-turbo` - Balanced

#### Neo4j Connection Pooling

For high-throughput scenarios, adjust Neo4j connection settings in Graphiti `.env`:

```env
NEO4J_MAX_CONNECTION_POOL_SIZE=50
NEO4J_QUERY_TIMEOUT=30
```

---

### Security Best Practices (Multi-Server)

#### Credential Isolation

- ✅ Use separate API keys for Obsidian and OpenAI
- ✅ Store credentials in password manager
- ✅ Rotate all credentials every 90 days
- ✅ Set usage limits on OpenAI dashboard
- ❌ Don't reuse credentials across systems

#### File Permissions

```bash
# Secure configuration file
chmod 600 ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Verify permissions
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json
# Should show: -rw------- (600)
```

#### Network Security

- ✅ Neo4j bound to localhost only
- ✅ Graphiti MCP bound to localhost only
- ✅ No firewall rules exposing services
- ❌ Never bind to 0.0.0.0 (all interfaces)

#### Monitoring

Set up monitoring for security events:

1. **Monitor OpenAI API usage** - Check dashboard daily for anomalies
2. **Monitor Neo4j connections** - Review logs for unauthorized access
3. **Rotate credentials** on schedule (90 days)
4. **Audit MCP server access** - Review Claude Desktop logs

---

### Disabling Graphiti (Graceful Degradation)

To disable Graphiti temporarily without removing configuration:

#### Option 1: Stop Neo4j

```bash
docker compose -f docker-compose.neo4j.yml down
```

Agents will detect Neo4j unavailable and operate in Obsidian-only mode.

#### Option 2: Comment Out Graphiti in Config

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "obsidian": {
      ...
    }
    // Temporarily disabled Graphiti
    // "graphiti": {
    //   ...
    // }
  }
}
```

Restart Claude Desktop.

#### Option 3: Remove Graphiti Entry

Delete the entire `"graphiti": {...}` block from config, restart Claude Desktop.

---

### Re-enabling Graphiti

1. Restore Graphiti entry in `claude_desktop_config.json`
2. Start Neo4j: `docker compose -f docker-compose.neo4j.yml up -d`
3. Verify Neo4j health: `curl http://localhost:7474`
4. Restart Claude Desktop
5. Test: "What Graphiti tools are available?"

---

## Next Steps

After successfully configuring the MCP server(s):

1. **Test Connection:** Run [connection tests](../tests/integration/obsidian-mcp-connection-test.js)
2. **Explore MCP Tools:** Review [MCP Tools Reference](../mcp-tools-reference.md)
3. **Enable Phase 1 Agents:** Start using AI agents for vault management
4. **Review Error Handling:** See [Error Handling Patterns](../error-handling-patterns.md)
5. **Test Temporal Features:** If Graphiti configured, test temporal queries
6. **Review Temporal Schema:** See [Temporal Schema Documentation](../temporal-schema.md)

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
