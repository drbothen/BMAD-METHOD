# Graphiti MCP Server Installation Guide

This document provides detailed instructions for installing and configuring the Graphiti MCP server to enable temporal knowledge tracking with Neo4j.

## Overview

Graphiti is an open-source temporal knowledge graph system that provides MCP (Model Context Protocol) integration for Claude Desktop. It enables AI agents to:

- Store episodic memories with timestamps (capture events)
- Create and link entities (notes) with semantic relationships
- Query knowledge by time range ("notes from last week")
- Track knowledge evolution over time

**Repository:** https://github.com/getzep/graphiti

## Prerequisites

Before installing Graphiti MCP, ensure you have:

- ✅ **Neo4j installed and running** (see [neo4j-setup.md](./neo4j-setup.md))
- ✅ **Git** installed (`git --version`)
- ✅ **Docker and Docker Compose** installed (`docker compose version`)
- ✅ **OpenAI API key** with available credits
- ✅ **Python 3.11+** (if running without Docker)
- ✅ **uv** Python package manager (recommended for non-Docker setup)

## Installation Methods

There are two ways to run Graphiti MCP:

1. **Docker Compose** (Recommended) - Easiest, most reliable
2. **Local Python** - For development, requires more setup

This guide covers both methods.

---

## Method 1: Docker Compose Installation (Recommended)

This is the recommended method for most users.

### Step 1: Clone Graphiti Repository

```bash
# Navigate to your preferred installation directory
# (NOT inside the bmad-obsidian-2nd-brain expansion pack)
cd ~/Development  # or your preferred location

# Clone the Graphiti repository
git clone https://github.com/getzep/graphiti.git

# Navigate into the repository
cd graphiti

# Check latest stable release (optional but recommended)
git tag -l | grep -E '^v[0-9]' | sort -V | tail -1

# Checkout latest stable version (replace v0.3.0 with actual version)
# git checkout v0.3.0

# Or stay on main branch for latest features
git checkout main
```

### Step 2: Configure Environment Variables

Graphiti uses a `.env` file for configuration.

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your credentials
nano .env  # or vim, code, etc.
```

**Required environment variables:**

```env
# Neo4j Connection
# If using docker-compose.neo4j.yml from Task 2:
NEO4J_URI=bolt://host.docker.internal:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password_from_earlier

# If Neo4j is running locally (not in Docker), use:
# NEO4J_URI=bolt://localhost:7687

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
MODEL_NAME=gpt-4o-mini

# Alternative: Anthropic (if not using OpenAI)
# ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
# MODEL_NAME=claude-3-5-sonnet-20241022

# Server Configuration
MCP_PORT=8000
LOG_LEVEL=INFO

# Optional: Custom embeddings model
# EMBEDDING_MODEL=text-embedding-3-small
```

**Important notes:**

- **`host.docker.internal`**: Use this hostname when Graphiti container needs to connect to Neo4j running on host machine
- **`localhost`**: Use this if Graphiti is NOT running in Docker or both are in same Docker network
- **Never commit `.env`** to git - it should already be in `.gitignore`

### Step 3: Verify Docker Compose Configuration

Check that the Graphiti `docker-compose.yml` includes the MCP server:

```bash
# View the docker-compose.yml file
cat docker-compose.yml | grep -A 10 mcp
```

Expected configuration should include a service for the Graphiti MCP server.

### Step 4: Start Graphiti MCP Server

```bash
# Start Graphiti services (in detached mode)
docker compose up -d

# Check that services are running
docker compose ps

# View logs to verify startup
docker compose logs -f graphiti-mcp
```

**Expected output:**
```
graphiti-mcp | INFO: Starting MCP server on port 8000
graphiti-mcp | INFO: Connected to Neo4j at bolt://host.docker.internal:7687
graphiti-mcp | INFO: MCP server ready
```

### Step 5: Verify Installation

**Test 1: Check HTTP endpoint**
```bash
# Test that the server is responding
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "neo4j": "connected"}
```

**Test 2: List available MCP tools**
```bash
# This requires an MCP client, will be tested in Task 5
# For now, just verify the server is running
docker compose ps | grep graphiti-mcp | grep "Up"
```

### Docker Management Commands

```bash
# View Graphiti logs
docker compose logs -f graphiti-mcp

# Restart Graphiti
docker compose restart graphiti-mcp

# Stop Graphiti
docker compose down

# Stop and remove volumes (CAUTION: deletes data)
docker compose down -v

# Check resource usage
docker stats graphiti-mcp

# Access container shell for debugging
docker compose exec graphiti-mcp bash
```

---

## Method 2: Local Python Installation

For development or when Docker is not available.

### Step 1: Install Prerequisites

**Install uv (Python package manager):**

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew
brew install uv

# Verify installation
uv --version
```

**Install Python 3.11+:**

```bash
# macOS (via Homebrew)
brew install python@3.11

# Ubuntu/Debian
sudo apt install python3.11 python3.11-venv

# Fedora/RHEL
sudo dnf install python3.11

# Verify
python3.11 --version
```

### Step 2: Clone Repository

```bash
# Clone Graphiti (if not already done)
cd ~/Development
git clone https://github.com/getzep/graphiti.git
cd graphiti
```

### Step 3: Install Dependencies

```bash
# Create virtual environment with uv
uv venv --python 3.11

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install Graphiti with MCP support
uv pip install -e ".[mcp]"

# Verify installation
graphiti-server --version
```

### Step 4: Configure Environment

```bash
# Copy and edit .env file
cp .env.example .env
nano .env

# Use localhost for local Neo4j connection
# NEO4J_URI=bolt://localhost:7687
```

### Step 5: Start Graphiti MCP Server

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Start the MCP server
graphiti-server --port 8000

# Or run as background process
nohup graphiti-server --port 8000 > graphiti.log 2>&1 &
```

### Step 6: Verify Installation

```bash
# Test health endpoint
curl http://localhost:8000/health

# Check logs
tail -f graphiti.log
```

---

## Claude Desktop Configuration

After installing Graphiti MCP, you need to configure Claude Desktop to use it.

### For Docker Installation

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "graphiti": {
      "command": "docker",
      "args": [
        "compose",
        "-f",
        "/Users/<your-username>/Development/graphiti/docker-compose.yml",
        "exec",
        "-T",
        "graphiti-mcp",
        "graphiti-mcp-client"
      ],
      "env": {}
    }
  }
}
```

**Note:** This is a preliminary configuration. See [mcp-server-setup.md](./mcp-server-setup.md#graphiti-configuration) for complete multi-server setup.

### For Local Installation

```json
{
  "mcpServers": {
    "graphiti": {
      "command": "/Users/<your-username>/.local/bin/uv",
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

**Security note:** Use environment variable substitution (`${VAR_NAME}`) instead of hardcoding sensitive values.

---

## Verification Steps

### 1. Check Neo4j Connection

```bash
# From Graphiti directory
docker compose exec graphiti-mcp python -c "
from neo4j import GraphDatabase
driver = GraphDatabase.driver(
    'bolt://host.docker.internal:7687',
    auth=('neo4j', 'your_password')
)
driver.verify_connectivity()
print('✅ Neo4j connection successful')
"
```

### 2. Verify MCP Tools Available

Will be tested in Task 5 using connection test utilities.

### 3. Check Claude Desktop Integration

1. Restart Claude Desktop
2. Open Claude Desktop
3. Start new conversation
4. Type: "List available MCP tools"
5. Look for Graphiti tools:
   - `graphiti.add_episode`
   - `graphiti.get_episodes`
   - `graphiti.add_entity`
   - `graphiti.add_relation`

---

## Troubleshooting

### Issue: "Cannot connect to Neo4j"

**Symptoms:**
```
ERROR: Failed to connect to Neo4j at bolt://host.docker.internal:7687
```

**Solutions:**

1. **Verify Neo4j is running:**
   ```bash
   docker compose -f ../bmad-obsidian-2nd-brain/docker-compose.neo4j.yml ps
   ```

2. **Check Neo4j credentials:**
   - Ensure `.env` has correct NEO4J_PASSWORD
   - Test login via Neo4j Browser (http://localhost:7474)

3. **Fix hostname resolution:**
   ```bash
   # If host.docker.internal doesn't work, try:
   # Option 1: Use host IP address
   NEO4J_URI=bolt://192.168.1.x:7687

   # Option 2: Use Docker network
   # Add Graphiti to same network as Neo4j in docker-compose.yml
   ```

4. **Check firewall:**
   ```bash
   # Verify port 7687 is accessible
   telnet localhost 7687
   ```

### Issue: "OpenAI API key invalid"

**Symptoms:**
```
ERROR: Invalid OpenAI API key
```

**Solutions:**

1. **Verify API key:**
   - Login to https://platform.openai.com/api-keys
   - Check key is active and not revoked
   - Check usage limits not exceeded

2. **Test API key:**
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

3. **Regenerate key:**
   - Create new key in OpenAI dashboard
   - Update `.env` file
   - Restart Graphiti: `docker compose restart`

### Issue: "MCP server not found in Claude Desktop"

**Symptoms:**
- Claude Desktop doesn't show Graphiti tools
- Error: "Failed to start MCP server"

**Solutions:**

1. **Verify configuration path:**
   ```bash
   # macOS
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

   # Windows
   type %APPDATA%\Claude\claude_desktop_config.json

   # Linux
   cat ~/.config/Claude/claude_desktop_config.json
   ```

2. **Check JSON syntax:**
   ```bash
   # Validate JSON
   cat claude_desktop_config.json | python -m json.tool
   ```

3. **Verify command path:**
   ```bash
   # For local installation, verify uv path
   which uv

   # For Docker installation, verify docker compose works
   docker compose version
   ```

4. **Check Claude Desktop logs:**
   ```bash
   # macOS
   tail -f ~/Library/Logs/Claude/mcp*.log
   ```

5. **Restart Claude Desktop:**
   - Fully quit Claude Desktop (Cmd+Q on macOS)
   - Relaunch application

### Issue: "Port 8000 already in use"

**Symptoms:**
```
ERROR: bind: address already in use
```

**Solutions:**

1. **Find process using port:**
   ```bash
   lsof -i :8000
   ```

2. **Kill process or change port:**
   ```bash
   # Option 1: Kill process
   kill -9 <PID>

   # Option 2: Change Graphiti port in .env
   MCP_PORT=8001
   ```

### Issue: "Docker container crashes immediately"

**Symptoms:**
- Container status shows "Exited (1)"
- `docker compose ps` shows container not running

**Solutions:**

1. **Check container logs:**
   ```bash
   docker compose logs graphiti-mcp
   ```

2. **Common causes:**
   - Missing `.env` file → Create from `.env.example`
   - Invalid environment variables → Verify all required vars set
   - Neo4j not accessible → Check NEO4J_URI
   - Insufficient memory → Increase Docker memory limit

3. **Rebuild container:**
   ```bash
   docker compose down
   docker compose build --no-cache
   docker compose up -d
   ```

### Issue: "graphiti-server command not found"

**Symptoms:**
```
bash: graphiti-server: command not found
```

**Solutions:**

1. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

2. **Reinstall Graphiti:**
   ```bash
   uv pip install -e ".[mcp]"
   ```

3. **Check installation:**
   ```bash
   which graphiti-server
   uv pip list | grep graphiti
   ```

---

## Performance Tuning

### Optimize OpenAI API Usage

```env
# Use faster, cheaper model for development
MODEL_NAME=gpt-4o-mini

# Use more accurate model for production
# MODEL_NAME=gpt-4o
```

### Optimize Neo4j Connection

```env
# Increase connection pool size for high throughput
NEO4J_MAX_CONNECTION_POOL_SIZE=50

# Adjust query timeout
NEO4J_QUERY_TIMEOUT=30
```

### Optimize Docker Resources

Edit `docker-compose.yml`:

```yaml
services:
  graphiti-mcp:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
```

---

## Security Best Practices

### API Key Management

- ✅ Store API keys in `.env`, never in code
- ✅ Use environment variable substitution in configs
- ✅ Set usage limits in OpenAI dashboard
- ✅ Rotate keys every 90 days
- ✅ Monitor API usage for anomalies
- ❌ Never commit `.env` to git
- ❌ Never share API keys in chat/email

### Network Security

- ✅ Bind to `localhost` only (not `0.0.0.0`)
- ✅ Use firewall to block external access
- ✅ Keep Graphiti and Neo4j on same private network
- ❌ Don't expose Graphiti MCP port to internet

### Updates and Patches

```bash
# Update Graphiti regularly
cd ~/Development/graphiti
git pull origin main
docker compose build --no-cache
docker compose up -d

# Or for local installation
source .venv/bin/activate
uv pip install --upgrade graphiti-core
```

---

## Backup and Recovery

### Backup Graphiti Configuration

```bash
# Backup .env and docker-compose.yml
cp .env .env.backup
cp docker-compose.yml docker-compose.yml.backup

# Or create tarball
tar -czf graphiti-config-backup.tar.gz .env docker-compose.yml
```

### Backup Neo4j Data

Neo4j data backup is covered in [neo4j-setup.md](./neo4j-setup.md#backup-restore).

---

## Uninstallation

### Docker Installation

```bash
# Stop and remove containers
docker compose down

# Remove volumes (deletes all data)
docker compose down -v

# Remove repository
cd ..
rm -rf graphiti
```

### Local Installation

```bash
# Deactivate virtual environment
deactivate

# Remove repository
cd ..
rm -rf graphiti

# Uninstall uv (optional)
rm -rf ~/.local/bin/uv
```

---

## Next Steps

After installing Graphiti MCP:

1. ✅ **Task 4**: [Configure Claude Desktop for multi-MCP setup](./mcp-server-setup.md)
2. ✅ **Task 5**: Run connection tests to verify integration
3. ✅ **Task 6**: Review temporal schema design
4. ✅ **Task 8**: Test Phase 1 MCP operations

---

## Additional Resources

- **Graphiti Documentation**: https://github.com/getzep/graphiti#readme
- **Graphiti Issues**: https://github.com/getzep/graphiti/issues
- **MCP Protocol Specification**: https://spec.modelcontextprotocol.io/
- **Neo4j Drivers**: https://neo4j.com/docs/drivers-apis/
- **OpenAI API Documentation**: https://platform.openai.com/docs/

---

## Support

**For Graphiti-specific issues:**
- GitHub Issues: https://github.com/getzep/graphiti/issues
- Zep Community: https://discord.gg/zep

**For integration issues:**
- Open issue in BMAD-METHOD repository
- Tag with `obsidian-2nd-brain` and `graphiti-mcp`
- Include logs and error messages
