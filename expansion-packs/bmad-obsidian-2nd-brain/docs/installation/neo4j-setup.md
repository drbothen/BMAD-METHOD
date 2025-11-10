# Neo4j Installation Guide

This document provides detailed instructions for installing and configuring Neo4j to support temporal knowledge tracking in the Obsidian 2nd Brain system.

## Important: Optional Feature

**Neo4j integration is completely optional.** The Obsidian 2nd Brain system works perfectly without Neo4j by operating in Obsidian-only mode. Install Neo4j only if you want:

- Temporal knowledge tracking (when notes were captured/edited)
- Graph-based relationship queries with confidence scores
- Time-based knowledge retrieval ("notes from last week")
- Advanced graph analytics and visualization

## Prerequisites

Before installing Neo4j, ensure you have:

- ✅ **4GB RAM minimum** (8GB recommended for production use)
- ✅ **10GB free disk space** for database storage
- ✅ **Docker Desktop or Docker Engine** (for recommended Docker installation)
- ✅ **OpenAI API key** (required for Graphiti MCP integration)
- ✅ Completed STORY-015 (Obsidian MCP integration)

## Installation Options Comparison

Choose the installation method that best fits your needs:

| Feature | Docker (Recommended) | Neo4j Desktop | Aura Cloud |
|---------|---------------------|---------------|------------|
| **Setup Time** | 5 minutes | 10 minutes | 5 minutes |
| **Difficulty** | Easy | Medium | Easy |
| **Cost** | Free | Free | Paid ($) |
| **Resource Usage** | Medium | Medium | Low (remote) |
| **Best For** | Developers, automation | Visual exploration, learning | Production, teams |
| **Network Required** | No | No | Yes (always) |
| **Data Location** | Local | Local | Cloud |
| **Multi-Platform** | ✅ macOS/Linux/Windows | ✅ macOS/Linux/Windows | ✅ Any platform |
| **Backup Control** | Full | Full | Managed |
| **Version Control** | Specific versions | Latest stable | Managed versions |

## Method 1: Docker Installation (Recommended)

Docker provides the easiest and most reproducible Neo4j setup.

### Why Docker?

- **Consistent environment** across all platforms
- **Easy upgrades** - just pull new image
- **Isolated setup** - no conflicts with system packages
- **Simple backup** - volume-based data persistence
- **Quick cleanup** - remove container when done

### Step 1: Verify Docker Installation

```bash
# Check Docker is installed and running
docker --version
docker compose version

# Expected output (versions may vary):
# Docker version 24.0.0+
# Docker Compose version v2.20.0+
```

If Docker is not installed:
- **macOS**: Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
- **Windows**: Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop) (requires WSL2)
- **Linux**: Install Docker Engine via package manager

### Step 2: Create Docker Compose Configuration

The `docker-compose.neo4j.yml` file is created in Task 2 of this story. If not yet created, see [Task 2 implementation](#task-2-reference).

### Step 3: Configure Environment Variables

Create a `.env` file in the expansion pack root:

```bash
# Navigate to expansion pack directory
cd expansion-packs/bmad-obsidian-2nd-brain

# Copy environment template
cp .env.example .env

# Edit with your preferred editor
nano .env  # or vim, code, etc.
```

**CRITICAL: Set a strong Neo4j password in `.env`:**

```env
# Neo4j Authentication
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_strong_password_here_NOT_default

# NEVER use default passwords like 'password', 'neo4j', or 'demodemo'
# Generate strong password: openssl rand -base64 32
```

### Step 4: Start Neo4j

```bash
# Start Neo4j in detached mode
docker compose -f docker-compose.neo4j.yml up -d

# Check container status
docker compose -f docker-compose.neo4j.yml ps

# View logs (optional)
docker compose -f docker-compose.neo4j.yml logs -f neo4j
```

### Step 5: Verify Installation

**Access Neo4j Browser:**
1. Open browser: http://localhost:7474
2. Connect with credentials:
   - Username: `neo4j`
   - Password: (from your `.env` file)
   - Connect URL: `neo4j://localhost:7687`

**Run test query:**
```cypher
// In Neo4j Browser, run this query:
RETURN "Neo4j is running!" AS message
```

Expected result: Single row with message "Neo4j is running!"

### Step 6: Verify APOC Plugin

```cypher
// Check APOC is installed
CALL apoc.help("apoc") YIELD name
RETURN count(name) AS apoc_procedures
```

Expected result: 100+ procedures available

### Docker Management Commands

```bash
# Stop Neo4j
docker compose -f docker-compose.neo4j.yml down

# Stop and remove data (CAUTION: deletes all data)
docker compose -f docker-compose.neo4j.yml down -v

# Restart Neo4j
docker compose -f docker-compose.neo4j.yml restart

# View resource usage
docker stats neo4j

# Backup database (while running)
docker exec neo4j neo4j-admin database dump neo4j --to-path=/backups

# Copy backup to host
docker cp neo4j:/backups/neo4j.dump ./backups/
```

---

## Method 2: Neo4j Desktop Installation

Neo4j Desktop provides a GUI for managing databases and is ideal for visual exploration.

### Why Neo4j Desktop?

- **Visual interface** for database management
- **Built-in graph visualization** tools
- **Multiple database** management
- **One-click APOC installation**
- **Good for learning** and experimentation

### Step 1: Download Neo4j Desktop

1. Visit: https://neo4j.com/download/
2. Click **"Download Neo4j Desktop"**
3. Create free Neo4j account (required for activation key)
4. Download installer for your platform:
   - **macOS**: `Neo4j Desktop-{version}.dmg`
   - **Windows**: `Neo4j Desktop Setup {version}.exe`
   - **Linux**: `neo4j-desktop-{version}.AppImage`

### Step 2: Install and Activate

**macOS:**
```bash
# Open DMG and drag to Applications
# Launch from Applications folder
# Enter activation key from download email
```

**Windows:**
```bash
# Run installer executable
# Follow installation wizard
# Enter activation key from download email
```

**Linux:**
```bash
# Make AppImage executable
chmod +x neo4j-desktop-*.AppImage

# Run AppImage
./neo4j-desktop-*.AppImage

# Enter activation key from download email
```

### Step 3: Create Database

1. Click **"New"** → **"Create Project"**
2. Name project: "Obsidian 2nd Brain"
3. Click **"Add Database"** → **"Create Local Database"**
4. Configure database:
   - **Name**: `obsidian-temporal`
   - **Password**: (set strong password)
   - **Version**: 5.x (latest stable)
5. Click **"Create"**

### Step 4: Install APOC Plugin

1. Select your database
2. Click **"Plugins"** tab
3. Find **"APOC"** in list
4. Click **"Install"**
5. Wait for installation to complete

### Step 5: Start Database

1. Click **"Start"** button on database
2. Wait for status to show **"Active"**
3. Click **"Open with Neo4j Browser"**

### Step 6: Verify Installation

In Neo4j Browser, run:

```cypher
// Verify connection
RETURN "Neo4j Desktop is running!" AS message;

// Verify APOC
CALL apoc.help("apoc") YIELD name
RETURN count(name) AS apoc_procedures;
```

### Neo4j Desktop Configuration for MCP

**Important:** Note these connection details for Graphiti MCP setup:

- **Bolt URL**: `bolt://localhost:7687` (default)
- **Username**: `neo4j` (default)
- **Password**: (your set password)

---

## Method 3: Neo4j Aura Cloud Installation

Neo4j Aura is a fully managed cloud service (paid).

### Why Aura Cloud?

- **No local resources** required
- **Automatic backups** and updates
- **Team collaboration** features
- **Production-ready** with high availability
- **Pay-as-you-go** pricing

### Step 1: Create Aura Account

1. Visit: https://neo4j.com/cloud/aura/
2. Click **"Start Free"** or **"Sign Up"**
3. Create account with email
4. Verify email address

### Step 2: Create Free Tier Instance

1. Login to Aura Console
2. Click **"New Instance"**
3. Select **"AuraDB Free"** (includes free tier)
4. Configure:
   - **Instance Name**: `obsidian-2nd-brain`
   - **Region**: (closest to your location)
5. Click **"Create Instance"**

### Step 3: Save Connection Details

**CRITICAL:** Aura shows connection details only once at creation.

Save these immediately:
- **Connection URI**: `neo4j+s://<instance-id>.databases.neo4j.io`
- **Username**: `neo4j`
- **Password**: (auto-generated, copy carefully)

Download credentials file and store securely.

### Step 4: Configure Firewall (Optional)

By default, Aura accepts connections from any IP. To restrict:

1. Go to **"Settings"** → **"Security"**
2. Click **"IP Whitelist"**
3. Add your IP address(es)
4. Click **"Save"**

### Step 5: Verify Connection

1. Click **"Open with Neo4j Browser"**
2. Login with saved credentials
3. Run test query:

```cypher
RETURN "Aura Cloud is running!" AS message
```

### Aura Configuration for MCP

Use these connection details for Graphiti MCP:

- **Bolt URL**: `neo4j+s://<your-instance-id>.databases.neo4j.io`
- **Username**: `neo4j`
- **Password**: (your saved password)

**Note:** Use `neo4j+s://` protocol (with `s` for secure) for Aura.

---

## Security Best Practices

### Password Security

**DO:**
- ✅ Use strong passwords (16+ characters, mixed case, numbers, symbols)
- ✅ Generate passwords with: `openssl rand -base64 32`
- ✅ Store passwords in password manager (1Password, Bitwarden, etc.)
- ✅ Use different passwords for each environment (dev/staging/prod)
- ✅ Rotate passwords every 90 days

**DON'T:**
- ❌ Use default passwords (`neo4j`, `password`, `demodemo`)
- ❌ Commit passwords to git (use `.env` files with `.gitignore`)
- ❌ Share passwords in chat/email (use secure sharing tools)
- ❌ Reuse passwords across services

### Network Security

**Docker/Desktop installations:**
- ✅ Bind to `localhost` only (not `0.0.0.0`)
- ✅ Never expose port 7687 to external network
- ✅ Use firewall to block external connections
- ✅ Use VPN for remote access

**Aura Cloud:**
- ✅ Use IP whitelisting to restrict access
- ✅ Enable two-factor authentication on Aura account
- ✅ Use secure connections (`neo4j+s://` protocol)

### Environment Variable Security

```bash
# Add to .gitignore (CRITICAL)
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
echo ".env.*.local" >> .gitignore

# Set strict file permissions
chmod 600 .env
chmod 600 docker-compose.neo4j.yml

# Verify not tracked by git
git status --ignored | grep .env
```

### API Key Security

For OpenAI API key (required by Graphiti):

- ✅ Store in password manager
- ✅ Use environment variables, not hardcoded in configs
- ✅ Set usage limits in OpenAI dashboard
- ✅ Monitor API usage regularly
- ✅ Rotate keys every 90 days
- ❌ Never commit API keys to git
- ❌ Never share API keys in chat/email

---

## Resource Requirements

### Minimum Requirements (Development)

- **CPU**: 2 cores
- **RAM**: 4GB
- **Disk**: 10GB free space
- **Network**: None (Docker/Desktop) or Stable internet (Aura)

### Recommended Requirements (Production)

- **CPU**: 4+ cores
- **RAM**: 8GB+ allocated to Neo4j
- **Disk**: 50GB+ free space (SSD preferred)
- **Network**: Low-latency connection (Aura only)

### Docker Resource Allocation

Edit `docker-compose.neo4j.yml` to adjust:

```yaml
services:
  neo4j:
    deploy:
      resources:
        limits:
          memory: 4G    # Adjust based on your system
        reservations:
          memory: 2G
```

---

## Platform-Specific Notes

### macOS

**Intel Macs:**
- All methods work without issues
- Docker performance: Excellent

**Apple Silicon (M1/M2/M3):**
- All methods work without issues
- Docker uses native ARM images
- Rosetta not required
- Docker performance: Excellent

**Installation Notes:**
- Docker Desktop requires macOS 11.0+
- Neo4j Desktop requires macOS 10.14+

### Linux

**Ubuntu/Debian:**
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login for group change to take effect
```

**Fedora/RHEL:**
```bash
# Install Docker Engine
sudo dnf install docker
sudo systemctl start docker
sudo systemctl enable docker
```

### Windows

**Requirements:**
- Windows 10 version 2004+ or Windows 11
- WSL2 installed and enabled
- Virtualization enabled in BIOS

**Docker Desktop Setup:**
1. Download Docker Desktop for Windows
2. Install with WSL2 backend (recommended)
3. Restart computer
4. Verify WSL2 integration enabled in Docker Desktop settings

**Neo4j Desktop:**
- Works natively on Windows
- No WSL2 required for Neo4j Desktop

---

## Troubleshooting

### Docker Issues

**"Cannot connect to Docker daemon"**
```bash
# macOS/Linux: Start Docker Desktop or Docker service
# macOS: Open Docker Desktop application
# Linux: sudo systemctl start docker
```

**"Port 7474 or 7687 already in use"**
```bash
# Check what's using the port
sudo lsof -i :7474
sudo lsof -i :7687

# Kill process or change Neo4j ports in docker-compose.neo4j.yml
```

**"Container fails to start"**
```bash
# Check logs for error messages
docker compose -f docker-compose.neo4j.yml logs neo4j

# Common issues:
# - Insufficient memory allocated to Docker
# - Data volume permission issues
# - Corrupt data from hard shutdown
```

### Neo4j Desktop Issues

**"Database won't start"**
1. Check logs: Settings → Logs
2. Common causes:
   - Insufficient RAM available
   - Corrupted database files
   - Port conflicts

**Solution:** Stop other databases, restart Neo4j Desktop

**"APOC procedures not available"**
1. Stop database
2. Reinstall APOC plugin
3. Restart database
4. Verify with `CALL apoc.help("apoc")`

### Aura Cloud Issues

**"Connection refused"**
- ✅ Check internet connection
- ✅ Verify connection URI is correct (includes `neo4j+s://`)
- ✅ Check IP whitelist settings
- ✅ Verify credentials not expired

**"Performance is slow"**
- ✅ Choose region closer to your location
- ✅ Upgrade instance size
- ✅ Optimize queries (create indexes)

### Connection Test Failures

If connection tests fail (Task 5), check:

1. **Neo4j is running**: `docker compose -f docker-compose.neo4j.yml ps`
2. **Ports are open**: `telnet localhost 7687`
3. **Credentials are correct**: Try Neo4j Browser login
4. **Firewall not blocking**: Disable temporarily to test

---

## Advanced: Custom Configuration with docker-compose.override.yml

**Problem**: You want to customize Neo4j settings without modifying the tracked `docker-compose.neo4j.yml` file.

**Solution**: Use Docker Compose override pattern

### Why Use Override Files?

- ✅ Keep custom settings separate from version-controlled config
- ✅ Different developers can have different local settings
- ✅ Easier to update when pulling new changes
- ✅ Git-ignored by default (added to `.gitignore`)

### How to Create Override File

Create `docker-compose.override.yml` in the expansion pack root:

```yaml
# docker-compose.override.yml
# Custom Neo4j configuration (git-ignored)
# This file automatically merges with docker-compose.neo4j.yml

version: '3.8'

services:
  neo4j:
    # Example: Increase memory limits for production use
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G

    # Example: Add custom environment variables
    environment:
      NEO4J_dbms_memory_heap_max__size: 2G
      NEO4J_dbms_memory_pagecache_size: 1G
      NEO4J_server_logs_debug_level: DEBUG

    # Example: Mount custom plugins directory
    volumes:
      - ./my-custom-plugins:/plugins

    # Example: Add additional ports
    ports:
      - "127.0.0.1:7473:7473"  # HTTPS port
```

### Usage

Once created, Docker Compose **automatically merges** override file:

```bash
# Standard command (automatically uses override)
docker compose -f docker-compose.neo4j.yml up -d

# Explicit override (same result)
docker compose -f docker-compose.neo4j.yml -f docker-compose.override.yml up -d

# Ignore override file (use base config only)
docker compose -f docker-compose.neo4j.yml --no-deps up -d
```

### Common Customizations

**Development Mode: More Logging**
```yaml
services:
  neo4j:
    environment:
      NEO4J_server_logs_debug_level: DEBUG
      NEO4J_dbms_logs_query_enabled: INFO
```

**Production Mode: More Resources**
```yaml
services:
  neo4j:
    deploy:
      resources:
        limits:
          memory: 8G
          cpus: '4'
    environment:
      NEO4J_dbms_memory_heap_max__size: 4G
      NEO4J_dbms_memory_pagecache_size: 3G
```

**Testing Mode: Reset Data on Restart**
```yaml
services:
  neo4j:
    volumes:
      # Use temporary volume instead of named volume
      - type: tmpfs
        target: /data
```

**Multi-Database Setup**
```yaml
services:
  neo4j:
    environment:
      NEO4J_server_databases_default__to__read__only: "false"
      NEO4J_server_databases_seed__from__uri__on__request__enabled: "true"
```

### Git Ignore Pattern

The `.gitignore` already includes:

```gitignore
docker-compose.override.yml
```

This ensures your custom settings stay local and don't get committed to version control.

### Troubleshooting Override Files

**Issue**: Changes not taking effect

**Solution**:
```bash
# Recreate containers with new config
docker compose -f docker-compose.neo4j.yml down
docker compose -f docker-compose.neo4j.yml up -d --force-recreate
```

**Issue**: Want to see merged configuration

**Solution**:
```bash
# View final configuration after merge
docker compose -f docker-compose.neo4j.yml config
```

**Issue**: Override file has syntax errors

**Solution**:
```bash
# Validate YAML syntax
docker compose -f docker-compose.neo4j.yml -f docker-compose.override.yml config
# If valid, shows merged config. If invalid, shows error.
```

---

## Next Steps

After installing Neo4j, proceed to:

1. ✅ **Task 3**: [Graphiti MCP Installation](./graphiti-mcp-setup.md)
2. ✅ **Task 4**: [MCP Server Configuration](./mcp-server-setup.md#graphiti-section)
3. ✅ **Task 5**: Run connection tests
4. ✅ **Task 6**: Review temporal schema design

---

## Additional Resources

- **Neo4j Documentation**: https://neo4j.com/docs/
- **Docker Documentation**: https://docs.docker.com/
- **Neo4j Community Forum**: https://community.neo4j.com/
- **Graphiti GitHub**: https://github.com/getzep/graphiti
- **APOC Documentation**: https://neo4j.com/labs/apoc/

---

## Support

For issues specific to this integration:
- Open issue in BMAD-METHOD repository
- Tag with `obsidian-2nd-brain` and `neo4j`
- Include relevant logs and error messages

For Neo4j-specific issues:
- Neo4j Community Forum
- Neo4j Support (Enterprise customers)
