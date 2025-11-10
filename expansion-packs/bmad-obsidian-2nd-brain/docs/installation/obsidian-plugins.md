# Obsidian Plugin Installation Requirements

This document provides step-by-step installation and configuration instructions for the three essential Obsidian plugins required to enable AI agent interactions with your Obsidian vault through the Model Context Protocol (MCP).

## Prerequisites

Before installing the required plugins, ensure you have:

- **Obsidian:** Version 1.7.7 or higher
- **Claude Desktop:** Installed and configured (for MCP integration)
- **System Requirements:** Windows, macOS, or Linux with internet connection for plugin downloads

## Required Plugins

Three community plugins must be installed in the following order:

1. **Local REST API** - Provides HTTP REST API access to vault operations
2. **MCP Tools** - Bridges Local REST API to Model Context Protocol
3. **Smart Connections** - Enables semantic search using local embeddings

---

## Plugin 1: Local REST API

### Purpose

The Local REST API plugin provides a secure HTTPS interface (or HTTP for development) that allows external applications to interact with your Obsidian vault programmatically. It enables:

- Reading, creating, updating, and deleting notes
- Listing vault contents
- Creating periodic notes
- Executing Obsidian commands

### Installation Steps

1. Open Obsidian
2. Navigate to **Settings → Community Plugins**
3. Click **Browse** to open the Community Plugins browser
4. Search for **"Local REST API"**
5. Click **Install** on the plugin by coddingtonbear
6. After installation completes, click **Enable** to activate the plugin

### Configuration

#### Step 1: Generate API Key

1. In Obsidian Settings, scroll to **Plugin Options**
2. Click **Local REST API** in the sidebar
3. The plugin automatically generates an API key on first activation
4. **Copy the API key** - you'll need it for MCP Tools configuration
5. Store the API key securely (e.g., password manager)

#### Step 2: Configure Port Settings

The plugin uses these default ports:

- **HTTP Port:** 27123 (default for non-encrypted connections)
- **HTTPS Port:** 27124 (default for encrypted connections)

**Recommendation:** Use HTTPS (port 27124) for production; HTTP acceptable for local development.

To verify or change port settings:

1. In Local REST API settings, locate **Port Configuration**
2. Verify the **Non-encrypted (HTTP) Server Port** is set to **27123**
3. Verify the **HTTPS Server Port** is set to **27124** (if using HTTPS)
4. Leave ports at default unless you have port conflicts

#### Step 3: Advanced Settings (Optional)

For advanced users:

1. Enable **Show advanced settings**
2. Customize **Authorization Header** name (default: `Authorization`)
3. Configure **CORS settings** if accessing from web applications
4. Set **localhost binding** (127.0.0.1) to prevent external network access

#### Step 4: Verify Installation

To confirm the plugin is working:

1. Ensure the plugin is **Enabled** in Community Plugins
2. Open a web browser and navigate to:
   - HTTP: `http://localhost:27123/`
   - HTTPS: `https://localhost:27124/`
3. You should see an API response (may show "Unauthorized" without API key - this is expected)

### Security Notes

- **API Key Protection:** Never commit your API key to version control or share it publicly
- **Network Binding:** Ensure the API is bound to localhost (127.0.0.1) only, not 0.0.0.0
- **Firewall:** No firewall changes needed - the API is localhost-only
- **Key Rotation:** Regenerate your API key periodically or if compromised

### Troubleshooting

**Problem:** Plugin won't enable
- **Solution:** Update Obsidian to the latest version; restart Obsidian

**Problem:** Port conflict (port already in use)
- **Solution:** Change the HTTP/HTTPS port in plugin settings to an available port

**Problem:** Can't access API at localhost:27123
- **Solution:** Verify plugin is enabled; check if another application is using the port; restart Obsidian

**Problem:** API key not showing in settings
- **Solution:** Disable and re-enable the plugin; check plugin settings again

---

## Plugin 2: MCP Tools

### Purpose

The MCP Tools plugin bridges Obsidian's Local REST API to the Model Context Protocol (MCP), enabling AI assistants like Claude to interact with your vault using standardized MCP tools. It provides:

- **Vault Access:** AI assistants can read and reference your notes
- **Semantic Search:** Context-aware search beyond keyword matching
- **Template Integration:** Execute Obsidian templates through AI interactions

### Dependencies

**CRITICAL:** MCP Tools requires Local REST API to be installed and configured FIRST.

### Installation Steps

1. **Verify Local REST API is installed and enabled** (see Plugin 1 above)
2. Open Obsidian Settings → **Community Plugins**
3. Click **Browse**
4. Search for **"MCP Tools"**
5. Click **Install** on the plugin by jacksteamdev
6. After installation completes, click **Enable** to activate the plugin

### Configuration

#### Step 1: Open Plugin Settings

1. In Obsidian Settings, scroll to **Plugin Options**
2. Click **MCP Tools** in the sidebar

#### Step 2: Install MCP Server

1. In MCP Tools settings, click **"Install Server"** button
2. The plugin will automatically:
   - Download the appropriate MCP server binary for your OS (Windows/macOS/Linux)
   - Configure Claude Desktop integration
   - Set up necessary file paths and permissions
3. Wait for installation to complete (progress indicator will show status)
4. You should see a success message when complete

#### Step 3: Configure API Key

1. In MCP Tools settings, locate the **API Key** field
2. Paste the API key you copied from Local REST API plugin settings
3. Click **Save** to store the configuration

#### Step 4: Verify Claude Desktop Integration

The plugin automatically configures Claude Desktop. To verify:

1. Open Claude Desktop application
2. The MCP server should appear in available tools
3. You can test by asking Claude: "Can you read my Obsidian vault?"

### Optional: Templater Integration

If you use Obsidian's Templater plugin:

1. Install **Templater** from Community Plugins
2. MCP Tools will automatically detect and integrate with it
3. AI assistants can then execute templates dynamically

### Troubleshooting

**Problem:** Install Server button doesn't work
- **Solution:** Check internet connection; ensure you have write permissions to Obsidian config directory; try restarting Obsidian

**Problem:** MCP server not appearing in Claude Desktop
- **Solution:** Restart Claude Desktop; check that Claude Desktop is installed; verify MCP server installation completed successfully

**Problem:** API authentication errors
- **Solution:** Verify API key is correctly copied from Local REST API settings; ensure Local REST API plugin is enabled; regenerate API key if needed

**Problem:** "Local REST API not found" error
- **Solution:** Install and enable Local REST API plugin first; restart Obsidian; verify Local REST API is running on port 27123

---

## Plugin 3: Smart Connections

### Purpose

The Smart Connections plugin enables semantic search using local AI embeddings, allowing AI assistants to find related notes based on meaning and context rather than just keywords. It provides:

- **Semantic Search:** Find notes by conceptual similarity
- **Smart Links:** Discover related notes automatically
- **Privacy-First:** All processing happens locally using on-device embeddings

### Installation Steps

1. Open Obsidian Settings → **Community Plugins**
2. Click **Browse**
3. Search for **"Smart Connections"**
4. Click **Install** on the plugin by brianpetro
5. After installation completes, click **Enable** to activate the plugin

### Configuration

#### Step 1: Initial Setup

1. In Obsidian Settings, scroll to **Plugin Options**
2. Click **Smart Connections** in the sidebar
3. The plugin will prompt you to configure embedding settings

#### Step 2: Choose Embedding Model

**Default (Recommended):** BGE-micro-v2

The plugin defaults to **BGE-micro-v2** (also listed as TaylorAI/bge-micro-v2), which:

- Works out-of-the-box with zero setup
- Processes everything locally (no cloud, complete privacy)
- Lightweight: 512 tokens, 384 dimensions
- Suitable for most vaults up to several thousand notes

**Alternative Local Models:**

- **BGE-small** (512 tokens, 384 dim) - Better performance, slightly slower
- **Jina-v2-small-2K** (2,048 tokens, 512 dim) - Handles longer text sequences
- **Snowflake Arctic Embed** - Various sizes available

**Cloud Option:**

- **OpenAI Embeddings** - Requires API key, sends data to OpenAI (less private)

**Recommendation:** Use the default BGE-micro-v2 for privacy and simplicity.

#### Step 3: Index Your Vault

After selecting an embedding model:

1. Click **"Index Vault"** or **"Make Smart Connections"**
2. The plugin will process all notes in your vault
3. Progress bar shows: "Embedding progress: X / Y notes (Z tokens/sec)"
4. **First-time indexing may take several minutes** depending on vault size
5. Subsequent updates are incremental (only new/modified notes)

**Performance Estimates:**

- Small vault (10-100 notes): 1-5 minutes
- Medium vault (100-1,000 notes): 5-15 minutes
- Large vault (1,000-10,000 notes): 15-60 minutes

#### Step 4: Configure Indexing Settings

Optimize indexing behavior:

1. **Auto-Index:** Enable to automatically index new notes
2. **Excluded Folders:** Add folders to skip (e.g., `Templates/`, `Archive/`)
3. **File Extensions:** Choose which file types to index (default: `.md`)

#### Step 5: Verify Smart Connections

To test semantic search:

1. Open any note in your vault
2. Look for the **Smart Connections** pane (usually in right sidebar)
3. You should see a list of semantically related notes
4. Try searching: use the search box to find notes by meaning

### MCP Integration

Smart Connections integrates with MCP Tools to provide:

- `smart_connections.semantic_search` - Search vault by semantic meaning
- `smart_connections.get_similar_notes` - Find notes related to a specific note

These tools are automatically available to AI assistants when all three plugins are configured.

### Troubleshooting

**Problem:** Indexing stuck or very slow
- **Solution:** Check system resources (CPU/RAM); close other applications; try a smaller embedding model; exclude large folders

**Problem:** "Embedding progress: 0 / X" not moving
- **Solution:** Restart Obsidian; check if embedding model downloaded successfully; verify vault isn't empty

**Problem:** No related notes appearing in Smart Connections pane
- **Solution:** Ensure indexing completed; wait for index to rebuild; check that notes have sufficient content (very short notes may not link well)

**Problem:** MCP semantic search not working
- **Solution:** Verify Smart Connections is enabled and indexed; restart Claude Desktop; check MCP Tools plugin is configured

**Problem:** High CPU usage during indexing
- **Solution:** Normal behavior during first index; let it complete; subsequent updates are incremental

---

## Plugin Compatibility Matrix

| Plugin | Minimum Version | Tested Version | OS Compatibility |
|--------|----------------|----------------|------------------|
| Local REST API | Unknown | Latest | Windows, macOS, Linux |
| MCP Tools | Unknown | Latest | Windows, macOS, Linux |
| Smart Connections | Unknown | Latest | Windows, macOS, Linux |
| Obsidian | 1.7.7 | 1.7.7+ | Windows, macOS, Linux |

**Note:** "Unknown" minimum versions indicate the earliest compatible version has not been verified. Always use the latest plugin versions for best results.

---

## Complete Installation Checklist

Use this checklist to verify all plugins are correctly installed:

- [ ] Obsidian version 1.7.7 or higher installed
- [ ] Claude Desktop application installed
- [ ] Local REST API plugin installed and enabled
- [ ] Local REST API API key generated and saved securely
- [ ] Local REST API responding at `http://localhost:27123` or `https://localhost:27124`
- [ ] MCP Tools plugin installed and enabled
- [ ] MCP server binary downloaded via "Install Server" button
- [ ] API key configured in MCP Tools settings
- [ ] Claude Desktop recognizes MCP server
- [ ] Smart Connections plugin installed and enabled
- [ ] Embedding model selected (default: BGE-micro-v2)
- [ ] Vault indexing completed successfully
- [ ] Smart Connections pane showing related notes

---

## Security Best Practices

1. **API Key Storage**
   - Never commit API keys to git repositories
   - Store keys in secure password manager
   - Rotate keys periodically (e.g., every 90 days)

2. **Network Security**
   - Keep REST API bound to localhost (127.0.0.1) only
   - Do not expose ports 27123/27124 to external networks
   - Use HTTPS (port 27124) for production

3. **Vault Access**
   - Understand that MCP Tools has full read/write access to your vault
   - Regularly backup your vault before using automation
   - Monitor vault changes in git (if using version control)

4. **File System Permissions**
   - Restrict access to `claude_desktop_config.json` (chmod 600 on Unix)
   - Ensure only your user account can read Obsidian config files

5. **Privacy Considerations**
   - Smart Connections processes embeddings locally by default
   - Avoid cloud embedding models if privacy is critical
   - Be aware AI assistants can read entire vault when connected

---

## Next Steps

After completing plugin installation:

1. **Configure MCP Server:** See [MCP Server Setup Guide](./mcp-server-setup.md)
2. **Test Connection:** Run connection tests to verify all components work
3. **Explore MCP Tools:** Review available MCP tools and their parameters
4. **Enable Phase 1 Agents:** Start using AI agents for vault management

---

## Additional Resources

- **Local REST API Documentation:** https://github.com/coddingtonbear/obsidian-local-rest-api
- **MCP Tools Documentation:** https://github.com/jacksteamdev/obsidian-mcp-tools
- **Smart Connections Documentation:** https://github.com/brianpetro/obsidian-smart-connections
- **Model Context Protocol Specification:** https://modelcontextprotocol.io/
- **Obsidian Community Forum:** https://forum.obsidian.md/

---

**Document Version:** 1.0
**Last Updated:** 2025-11-09
**Author:** BMAD Development Team
