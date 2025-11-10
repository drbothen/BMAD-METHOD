# Error Handling Patterns for Obsidian MCP Integration

This document provides standardized error handling patterns for AI agents interacting with Obsidian vaults through MCP. It covers error detection, user-friendly messaging, remediation steps, and implementation examples.

## Error Handling Philosophy

### Core Principles

1. **Fail Gracefully:** Never crash or lose data; always provide actionable feedback
2. **User-Friendly Messages:** Translate technical errors into clear, helpful language
3. **Actionable Guidance:** Always suggest specific next steps
4. **Preserve Context:** Include enough detail for debugging without exposing sensitive data
5. **Retry Intelligently:** Distinguish transient errors (retry) from permanent failures (abort)

### Error Response Structure

All error responses should follow this standard format:

```javascript
{
  error: {
    code: "ERROR_TYPE",           // Machine-readable error code
    message: "User-friendly description",  // Human-readable message
    details: {
      // Context-specific details
      attemptedAction: "create_note",
      targetPath: "Projects/Note.md",
      reason: "File already exists"
    },
    remediation: [
      "Suggested action 1",
      "Suggested action 2"
    ],
    technical: {
      // Optional: Technical details for debugging
      httpStatus: 409,
      timestamp: "2025-01-15T10:30:00Z"
    }
  }
}
```

---

## Common Error Patterns

### 1. API Key Invalid

**Error Signature:**
- HTTP Status: `401 Unauthorized` or `403 Forbidden`
- Response body contains: "invalid api key", "unauthorized", "forbidden"
- REST API returns authentication failure

**Detection:**

```javascript
function detectApiKeyError(error) {
  const status = error.response?.status;
  const message = error.response?.body?.toLowerCase() || '';

  return (
    status === 401 ||
    status === 403 ||
    message.includes('invalid api key') ||
    message.includes('unauthorized') ||
    message.includes('authentication failed')
  );
}
```

**User-Facing Error Message:**

```
🔑 API Key Authentication Failed

I couldn't authenticate with your Obsidian vault because the API key is invalid or missing.

What happened:
The Obsidian Local REST API rejected the API key. This usually means:
• The API key has changed or been regenerated
• The API key wasn't properly copied (extra spaces, truncation)
• The environment variable isn't set correctly

How to fix:
1. Open Obsidian → Settings → Community Plugins → Local REST API
2. Copy the API key (click the copy button to avoid errors)
3. Update your API key:
   - In MCP Tools settings: paste the new key
   - Or in environment: export OBSIDIAN_API_KEY="your-key-here"
4. Restart Claude Desktop to apply changes
5. Try your request again

Need help? Check the troubleshooting guide:
docs/installation/mcp-server-setup.md#authentication-errors
```

**Remediation Steps:**

```javascript
async function remediateApiKeyError(agent) {
  agent.log("API key authentication failed");

  // Prompt user for new API key
  const newApiKey = await agent.ask(
    "Please copy your API key from Obsidian Settings → Local REST API"
  );

  // Validate format (basic check)
  if (!newApiKey || newApiKey.length < 10) {
    throw new Error("Invalid API key format");
  }

  // Update configuration
  agent.updateConfig({ apiKey: newApiKey });

  // Verify new key works
  const testResult = await agent.testConnection();

  if (testResult.success) {
    agent.log("✓ API key updated successfully");
    return true;
  } else {
    agent.error("New API key also failed authentication");
    return false;
  }
}
```

**Code Example (Agent Implementation):**

```javascript
async function executeObsidianOperation(operation) {
  try {
    return await callMcpTool(operation);
  } catch (error) {
    if (detectApiKeyError(error)) {
      throw new AgentError({
        code: "API_KEY_INVALID",
        message: "API key authentication failed. Please update your Obsidian API key.",
        userMessage: USER_MESSAGES.API_KEY_INVALID,
        remediation: await remediateApiKeyError(this),
        retryable: true
      });
    }
    throw error;
  }
}
```

---

### 2. REST API Unreachable (Obsidian Not Running)

**Error Signature:**
- Connection refused: `ECONNREFUSED`
- Timeout: `ETIMEDOUT`
- Network unreachable: `ENETUNREACH`
- No response from localhost:27123 or localhost:27124

**Detection:**

```javascript
function detectRestApiUnreachable(error) {
  const code = error.code;
  const errno = error.errno;

  return (
    code === 'ECONNREFUSED' ||
    code === 'ETIMEDOUT' ||
    code === 'ENETUNREACH' ||
    errno === -61 ||  // Connection refused (macOS)
    errno === -111    // Connection refused (Linux)
  );
}
```

**User-Facing Error Message:**

```
🔌 Cannot Connect to Obsidian

I couldn't reach your Obsidian vault because the Local REST API isn't responding.

What happened:
The connection to localhost:27123 failed. This usually means:
• Obsidian isn't running
• Local REST API plugin is disabled
• Obsidian is using a different port
• Firewall is blocking localhost connections (rare)

How to fix:
1. Open Obsidian (make sure it's running, not just minimized)
2. Go to Settings → Community Plugins
3. Verify "Local REST API" is enabled (green toggle)
4. Check the port number in Local REST API settings
5. Test connection: curl -H "Authorization: Bearer YOUR_KEY" http://localhost:27123/
6. Try your request again

Still not working?
• Restart Obsidian
• Disable and re-enable Local REST API plugin
• Check if another application is using port 27123

Need help? Check the troubleshooting guide:
docs/installation/obsidian-plugins.md#connection-refused-errors
```

**Remediation Steps:**

```javascript
async function remediateRestApiUnreachable(agent) {
  agent.log("Obsidian REST API unreachable");

  // Wait for user to start Obsidian
  await agent.ask(
    "Please ensure Obsidian is running and Local REST API plugin is enabled. " +
    "Press Enter when ready to retry..."
  );

  // Retry connection with timeout
  const maxRetries = 3;
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    agent.log(`Connection attempt ${attempt}/${maxRetries}...`);

    try {
      await agent.testConnection({ timeout: 5000 });
      agent.log("✓ Connected to Obsidian");
      return true;
    } catch (error) {
      if (attempt === maxRetries) {
        agent.error("Failed to connect after all retries");
        return false;
      }
      await sleep(2000);  // Wait 2 seconds between retries
    }
  }
}
```

**Code Example (With Backoff Retry):**

```javascript
async function executeWithRetry(operation, maxRetries = 3) {
  let lastError;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await callMcpTool(operation);
    } catch (error) {
      lastError = error;

      if (detectRestApiUnreachable(error)) {
        if (attempt === 1) {
          // First failure: prompt user
          await remediateRestApiUnreachable(this);
        } else {
          // Subsequent failures: exponential backoff
          const delay = Math.pow(2, attempt) * 1000;
          await sleep(delay);
        }
      } else {
        // Non-connection error: don't retry
        throw error;
      }
    }
  }

  throw new AgentError({
    code: "REST_API_UNREACHABLE",
    message: "Cannot connect to Obsidian after multiple retries",
    userMessage: USER_MESSAGES.REST_API_UNREACHABLE,
    originalError: lastError,
    retryable: false
  });
}
```

---

### 3. Note Not Found

**Error Signature:**
- HTTP Status: `404 Not Found`
- Response body contains: "file not found", "note does not exist"

**Detection:**

```javascript
function detectNoteNotFound(error) {
  const status = error.response?.status;
  const message = error.response?.body?.toLowerCase() || '';

  return (
    status === 404 ||
    message.includes('not found') ||
    message.includes('does not exist') ||
    message.includes('no such file')
  );
}
```

**User-Facing Error Message:**

```
📄 Note Not Found

I couldn't find the note you requested in your Obsidian vault.

What happened:
The note at path "{filePath}" doesn't exist.

Possible reasons:
• The note was moved, renamed, or deleted
• The file path has a typo
• The note is in a different folder than expected

How to fix:
1. Check if the note was moved or renamed
2. Search your vault for the note by title:
   "Search for notes containing '{title}'"
3. If the note should exist, try:
   • Check spelling of the file path
   • Use list_notes to browse the correct directory
   • Use semantic search to find similar notes

Would you like me to:
• Search for similar note names?
• List notes in the expected directory?
• Create a new note at this path?
```

**Remediation Steps:**

```javascript
async function remediateNoteNotFound(agent, filePath) {
  agent.log(`Note not found: ${filePath}`);

  // Extract note title from path
  const title = path.basename(filePath, '.md');

  // Offer search alternatives
  const response = await agent.ask({
    message: `Note "${title}" not found. What would you like to do?`,
    options: [
      { value: 'search_similar', label: 'Search for similar note names' },
      { value: 'list_directory', label: 'List notes in the directory' },
      { value: 'create_new', label: 'Create a new note at this path' },
      { value: 'abort', label: 'Cancel operation' }
    ]
  });

  switch (response) {
    case 'search_similar':
      return await agent.searchNotes({ query: title, limit: 10 });

    case 'list_directory':
      const dirPath = path.dirname(filePath);
      return await agent.listNotes({ dirPath });

    case 'create_new':
      return await agent.createNote({ filePath, content: "" });

    case 'abort':
      throw new Error("Operation cancelled by user");
  }
}
```

**Code Example (With Fuzzy Search Fallback):**

```javascript
async function readNoteWithFallback(filePath) {
  try {
    return await this.mcpTools.obsidian_read_note({ filePath });
  } catch (error) {
    if (detectNoteNotFound(error)) {
      this.log(`Note not found: ${filePath}`);

      // Try fuzzy search as fallback
      const title = path.basename(filePath, '.md');
      const searchResults = await this.mcpTools.obsidian_search_notes({
        query: title,
        caseSensitive: false,
        limit: 5
      });

      if (searchResults.results.length > 0) {
        this.log(`Found ${searchResults.results.length} similar notes`);

        // Present options to user
        const selectedPath = await this.ask({
          message: `Did you mean one of these notes?`,
          options: searchResults.results.map(r => ({
            value: r.filePath,
            label: path.basename(r.filePath)
          }))
        });

        // Read the selected note
        return await this.mcpTools.obsidian_read_note({ filePath: selectedPath });
      } else {
        throw new AgentError({
          code: "NOTE_NOT_FOUND",
          message: `Note not found: ${filePath}`,
          userMessage: USER_MESSAGES.NOTE_NOT_FOUND(filePath),
          remediation: await remediateNoteNotFound(this, filePath),
          retryable: false
        });
      }
    }
    throw error;
  }
}
```

---

### 4. Permission Denied

**Error Signature:**
- HTTP Status: `403 Forbidden`
- Response body contains: "permission denied", "access denied", "forbidden"
- File system error: `EACCES`, `EPERM`

**Detection:**

```javascript
function detectPermissionDenied(error) {
  const status = error.response?.status;
  const code = error.code;
  const message = error.response?.body?.toLowerCase() || '';

  return (
    status === 403 ||
    code === 'EACCES' ||
    code === 'EPERM' ||
    message.includes('permission denied') ||
    message.includes('access denied') ||
    message.includes('forbidden')
  );
}
```

**User-Facing Error Message:**

```
🚫 Permission Denied

I don't have permission to access the requested file or directory.

What happened:
The operation was blocked due to insufficient permissions on:
{filePath}

Possible reasons:
• File or directory is outside the vault
• File is locked by another application
• Insufficient file system permissions
• Security plugin is blocking access

How to fix:
1. Verify the file path is within your vault
2. Check if the file is open in another application (close it)
3. Check file system permissions:
   - macOS/Linux: ls -l "{filePath}"
   - Windows: Right-click → Properties → Security
4. If the file is outside the vault, move it inside
5. Restart Obsidian and try again

Security Note:
The MCP integration can only access files within your Obsidian vault for security reasons.
Paths like "../" or absolute paths outside the vault are blocked.
```

**Remediation Steps:**

```javascript
async function remediatePermissionDenied(agent, filePath) {
  agent.log(`Permission denied: ${filePath}`);

  // Check if path is outside vault
  if (isPathOutsideVault(filePath)) {
    agent.error("Attempted access outside vault (security violation)");
    throw new SecurityError("Path traversal attempt detected");
  }

  // Check if file exists but is locked
  const fileExists = await agent.checkFileExists(filePath);
  if (fileExists) {
    await agent.ask(
      "The file exists but is locked or in use. " +
      "Please close any applications that might be using it, then press Enter to retry..."
    );

    // Retry after user confirms
    return { retry: true };
  } else {
    agent.error("File doesn't exist or is inaccessible");
    return { retry: false };
  }
}
```

**Code Example (Path Validation):**

```javascript
function validatePath(filePath) {
  // Remove leading/trailing slashes
  filePath = filePath.trim().replace(/^\/+|\/+$/g, '');

  // Check for directory traversal
  if (filePath.includes('..') || filePath.startsWith('/')) {
    throw new SecurityError({
      code: "INVALID_PATH",
      message: "Path traversal is not allowed",
      userMessage: "Invalid path: Cannot access files outside the vault",
      details: { attemptedPath: filePath }
    });
  }

  // Check for absolute paths (OS-specific)
  if (path.isAbsolute(filePath)) {
    throw new SecurityError({
      code: "ABSOLUTE_PATH_NOT_ALLOWED",
      message: "Absolute paths are not allowed",
      userMessage: "Please use relative paths within your vault",
      details: { attemptedPath: filePath }
    });
  }

  return filePath;
}

async function executeWithPathValidation(operation) {
  try {
    // Validate path before operation
    if (operation.filePath) {
      operation.filePath = validatePath(operation.filePath);
    }

    return await callMcpTool(operation);
  } catch (error) {
    if (detectPermissionDenied(error)) {
      throw new AgentError({
        code: "PERMISSION_DENIED",
        message: "Permission denied for file operation",
        userMessage: USER_MESSAGES.PERMISSION_DENIED(operation.filePath),
        remediation: await remediatePermissionDenied(this, operation.filePath),
        retryable: true
      });
    }
    throw error;
  }
}
```

---

### 5. Invalid Path (Directory Traversal Attempt)

**Error Signature:**
- Path contains: `..`, `../`, `../../`
- Absolute path when relative expected
- Path escape characters or encoded traversal

**Detection:**

```javascript
function detectInvalidPath(filePath) {
  return (
    filePath.includes('..') ||
    path.isAbsolute(filePath) ||
    filePath.includes('%2e%2e') ||  // URL-encoded ..
    filePath.includes('%252e%252e') ||  // Double-encoded ..
    filePath.match(/[<>:"|?*]/)  // Invalid characters (Windows)
  );
}
```

**User-Facing Error Message:**

```
⚠️ Invalid File Path

The file path you provided contains invalid characters or patterns.

What happened:
The path "{filePath}" was rejected for security reasons.

Issues detected:
• Contains directory traversal sequences (.., ../)
• Uses absolute path instead of relative path
• Contains invalid characters for file names

How to fix:
1. Use relative paths from your vault root
   ✓ Good: "Projects/Website Redesign.md"
   ✗ Bad: "../../../etc/passwd"
   ✗ Bad: "/Users/name/Documents/note.md"

2. Avoid special characters in paths:
   ✗ Bad characters: < > : " | ? * ..

3. Use forward slashes (/) for directories:
   ✓ Good: "Projects/Subfolder/Note.md"
   ✗ Bad: "Projects\Subfolder\Note.md" (Windows-style)

Security Note:
Directory traversal is blocked to protect your system from unauthorized access.
```

**Remediation Steps:**

```javascript
function sanitizePath(filePath) {
  // Remove leading/trailing whitespace
  filePath = filePath.trim();

  // Remove leading slashes
  filePath = filePath.replace(/^\/+/, '');

  // Replace backslashes with forward slashes
  filePath = filePath.replace(/\\/g, '/');

  // Remove any directory traversal sequences
  filePath = filePath.replace(/\.\.\//g, '');
  filePath = filePath.replace(/\.\./g, '');

  // Normalize consecutive slashes
  filePath = filePath.replace(/\/+/g, '/');

  // Remove trailing slash
  filePath = filePath.replace(/\/$/, '');

  // Validate result
  if (detectInvalidPath(filePath)) {
    throw new SecurityError({
      code: "PATH_SANITIZATION_FAILED",
      message: "Path could not be sanitized",
      details: { originalPath: filePath }
    });
  }

  return filePath;
}
```

**Code Example (Automatic Sanitization):**

```javascript
async function executeWithSanitization(operation) {
  try {
    // Sanitize path if present
    if (operation.filePath) {
      const originalPath = operation.filePath;
      operation.filePath = sanitizePath(originalPath);

      if (originalPath !== operation.filePath) {
        this.log(`Path sanitized: "${originalPath}" → "${operation.filePath}"`);
      }
    }

    return await callMcpTool(operation);
  } catch (error) {
    if (error instanceof SecurityError) {
      throw new AgentError({
        code: "INVALID_PATH",
        message: "Invalid or unsafe file path",
        userMessage: USER_MESSAGES.INVALID_PATH(operation.filePath),
        originalError: error,
        retryable: false
      });
    }
    throw error;
  }
}
```

---

### 6. MCP Server Unavailable

**Error Signature:**
- MCP handshake fails
- Server process not running
- Binary not found or not executable

**Detection:**

```javascript
function detectMcpServerUnavailable(error) {
  const message = error.message?.toLowerCase() || '';

  return (
    message.includes('mcp server') ||
    message.includes('server unavailable') ||
    message.includes('handshake failed') ||
    message.includes('cannot find module') ||
    message.includes('ENOENT')  // Binary not found
  );
}
```

**User-Facing Error Message:**

```
🔧 MCP Server Not Available

The MCP server isn't running or couldn't be started.

What happened:
Claude Desktop couldn't communicate with the Obsidian MCP server.

Possible reasons:
• MCP server binary not installed
• Binary path in config is incorrect
• Binary doesn't have execute permissions
• Claude Desktop config is malformed

How to fix:
1. Open Obsidian → Settings → MCP Tools
2. Click "Install Server" to download the binary
3. Wait for installation to complete
4. Verify installation:
   - Check binary exists at configured path
   - macOS/Linux: chmod +x /path/to/mcp-server
5. Restart Claude Desktop completely (Quit, not just close window)
6. Try your request again

Manual verification:
1. Open claude_desktop_config.json
2. Verify "command" path is correct and absolute
3. Test binary: /path/to/mcp-server --version

Need help? Check the troubleshooting guide:
docs/installation/mcp-server-setup.md#mcp-server-not-appearing
```

**Remediation Steps:**

```javascript
async function remediateMcpServerUnavailable(agent) {
  agent.log("MCP server unavailable");

  // Guide user through verification
  await agent.ask(
    "Let's verify your MCP server installation.\n\n" +
    "1. Open Obsidian Settings → MCP Tools\n" +
    "2. Click 'Install Server' if not already installed\n" +
    "3. Wait for installation to complete\n\n" +
    "Press Enter when done..."
  );

  // Prompt to restart Claude Desktop
  await agent.ask(
    "Now please:\n\n" +
    "1. Completely quit Claude Desktop (Cmd+Q on Mac, not just close window)\n" +
    "2. Wait 5 seconds\n" +
    "3. Relaunch Claude Desktop\n\n" +
    "Press Enter after restarting..."
  );

  agent.log("User should restart agent session after Claude Desktop restart");
  return false;  // Requires manual restart
}
```

---

### 7. Vault Not Found

**Error Signature:**
- Vault directory doesn't exist
- Vault path misconfigured
- .obsidian folder missing

**Detection:**

```javascript
function detectVaultNotFound(error) {
  const message = error.message?.toLowerCase() || '';

  return (
    message.includes('vault not found') ||
    message.includes('vault directory') ||
    message.includes('.obsidian not found') ||
    (error.code === 'ENOENT' && message.includes('vault'))
  );
}
```

**User-Facing Error Message:**

```
📁 Obsidian Vault Not Found

I couldn't locate your Obsidian vault directory.

What happened:
The configured vault path doesn't exist or isn't accessible.

Possible reasons:
• Vault was moved or renamed
• Vault is on an external drive that's not mounted
• Vault path in config is incorrect
• .obsidian folder is missing (not a valid vault)

How to fix:
1. Verify vault location in Obsidian:
   Settings → About → Vault directory
2. Check if vault is on external drive (mount it if needed)
3. Update MCP server config if vault moved:
   - Edit claude_desktop_config.json
   - Update "command" path to point to correct vault
4. If vault is missing, restore from backup
5. Restart Claude Desktop after config changes

Creating a new vault?
Make sure to open it in Obsidian first so the .obsidian folder is created.
```

---

### 8. Rate Limit Exceeded

**Error Signature:**
- HTTP Status: `429 Too Many Requests`
- Response contains: "rate limit", "too many requests"

**Detection:**

```javascript
function detectRateLimitExceeded(error) {
  const status = error.response?.status;
  const message = error.response?.body?.toLowerCase() || '';

  return (
    status === 429 ||
    message.includes('rate limit') ||
    message.includes('too many requests')
  );
}
```

**User-Facing Error Message:**

```
⏱️ Rate Limit Exceeded

I'm sending requests too quickly to your Obsidian vault.

What happened:
The Local REST API is rate-limiting our requests to prevent overwhelming Obsidian.

How to fix:
• Wait a few seconds and try again
• I'll automatically slow down subsequent requests

This usually happens when:
• Processing many notes in a batch
• Rapid search or update operations
• Vault is under heavy load from sync

I'll implement exponential backoff to avoid this in the future.
```

**Code Example (Exponential Backoff):**

```javascript
async function executeWithBackoff(operation, maxRetries = 5) {
  let delay = 1000;  // Start with 1 second

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await callMcpTool(operation);
    } catch (error) {
      if (detectRateLimitExceeded(error)) {
        if (attempt === maxRetries) {
          throw new AgentError({
            code: "RATE_LIMIT_EXCEEDED",
            message: "Rate limit exceeded after retries",
            userMessage: USER_MESSAGES.RATE_LIMIT_EXCEEDED,
            retryable: false
          });
        }

        this.log(`Rate limited. Waiting ${delay}ms before retry ${attempt + 1}/${maxRetries}`);
        await sleep(delay);
        delay *= 2;  // Exponential backoff
      } else {
        throw error;  // Non-rate-limit error
      }
    }
  }
}
```

---

## Graceful Degradation Strategies

When errors occur, agents should degrade gracefully rather than fail completely.

### Strategy 1: Fallback to Alternative Methods

```javascript
async function readNoteWithFallbacks(filePath) {
  // Try primary method
  try {
    return await this.mcpTools.obsidian_read_note({ filePath });
  } catch (error) {
    this.log("Primary read failed, trying fallbacks...");

    // Fallback 1: Try with different path formats
    try {
      const normalizedPath = normalizePath(filePath);
      return await this.mcpTools.obsidian_read_note({ filePath: normalizedPath });
    } catch {}

    // Fallback 2: Search for note by title
    try {
      const title = path.basename(filePath, '.md');
      const searchResults = await this.mcpTools.obsidian_search_notes({
        query: title,
        limit: 1
      });

      if (searchResults.results.length > 0) {
        return await this.mcpTools.obsidian_read_note({
          filePath: searchResults.results[0].filePath
        });
      }
    } catch {}

    // All fallbacks failed
    throw new AgentError({
      code: "READ_NOTE_FAILED",
      message: `Could not read note: ${filePath}`,
      userMessage: USER_MESSAGES.NOTE_NOT_FOUND(filePath)
    });
  }
}
```

### Strategy 2: Partial Success Reporting

```javascript
async function processBatchOperations(operations) {
  const results = {
    successful: [],
    failed: [],
    total: operations.length
  };

  for (const op of operations) {
    try {
      const result = await executeOperation(op);
      results.successful.push({ operation: op, result });
    } catch (error) {
      results.failed.push({ operation: op, error: error.message });
    }
  }

  // Report partial success
  if (results.failed.length > 0) {
    this.log(`Batch completed with ${results.successful.length}/${results.total} successful`);
    this.log(`Failed operations: ${results.failed.length}`);

    // Continue with successful results instead of failing completely
    return results;
  }

  return results;
}
```

### Strategy 3: Cached Fallback Data

```javascript
class CachedMcpClient {
  constructor() {
    this.cache = new Map();
  }

  async readNoteWithCache(filePath) {
    try {
      const note = await this.mcpTools.obsidian_read_note({ filePath });

      // Cache successful reads
      this.cache.set(filePath, {
        data: note,
        timestamp: Date.now()
      });

      return note;
    } catch (error) {
      // If connection fails, use cached data if available
      if (detectRestApiUnreachable(error)) {
        const cached = this.cache.get(filePath);

        if (cached) {
          this.log(`Using cached data (${Math.round((Date.now() - cached.timestamp) / 1000)}s old)`);
          return {
            ...cached.data,
            _cached: true,
            _cacheAge: Date.now() - cached.timestamp
          };
        }
      }

      throw error;
    }
  }
}
```

---

## Error Logging Best Practices

### Structured Error Logging

```javascript
function logError(error, context = {}) {
  const errorLog = {
    timestamp: new Date().toISOString(),
    errorCode: error.code || 'UNKNOWN',
    message: error.message,
    context: {
      agent: context.agentName || 'unknown',
      operation: context.operation || 'unknown',
      filePath: context.filePath || null,
      ...context
    },
    stack: error.stack,
    // NEVER log sensitive data
    // ❌ apiKey: config.apiKey,  // NEVER DO THIS
    // ❌ authToken: token,       // NEVER DO THIS
  };

  console.error(JSON.stringify(errorLog));

  // Send to error tracking service (optional)
  if (config.errorTracking) {
    reportError(errorLog);
  }
}
```

### Sanitized Error Messages

```javascript
function sanitizeErrorForLogging(error) {
  const sanitized = { ...error };

  // Remove sensitive fields
  delete sanitized.apiKey;
  delete sanitized.authToken;
  delete sanitized.credentials;

  // Sanitize URLs (remove API keys from query params)
  if (sanitized.url) {
    sanitized.url = sanitized.url.replace(/api_key=[^&]+/, 'api_key=***');
  }

  // Sanitize file paths (remove username)
  if (sanitized.filePath) {
    sanitized.filePath = sanitized.filePath.replace(/\/Users\/[^\/]+/, '/Users/***');
  }

  return sanitized;
}
```

---

## Testing Error Scenarios

### Unit Test Examples

```javascript
describe('Error Handling', () => {
  it('should detect API key invalid error', () => {
    const error = {
      response: { status: 401, body: 'Invalid API key' }
    };
    expect(detectApiKeyError(error)).toBe(true);
  });

  it('should detect REST API unreachable error', () => {
    const error = { code: 'ECONNREFUSED' };
    expect(detectRestApiUnreachable(error)).toBe(true);
  });

  it('should sanitize path with directory traversal', () => {
    expect(() => validatePath('../../../etc/passwd')).toThrow(SecurityError);
  });

  it('should retry on transient errors', async () => {
    let attempts = 0;
    const mockOperation = async () => {
      attempts++;
      if (attempts < 3) {
        throw { code: 'ECONNREFUSED' };
      }
      return 'success';
    };

    const result = await executeWithRetry(mockOperation);
    expect(result).toBe('success');
    expect(attempts).toBe(3);
  });
});
```

---

## Summary Checklist

When implementing error handling in agents:

- [ ] Use standardized error response structure
- [ ] Provide user-friendly, actionable error messages
- [ ] Implement appropriate retry logic for transient errors
- [ ] Validate and sanitize all file paths
- [ ] Never log sensitive data (API keys, auth tokens)
- [ ] Implement graceful degradation strategies
- [ ] Cache data when appropriate for offline fallback
- [ ] Report partial success in batch operations
- [ ] Test all error scenarios with unit tests
- [ ] Document error codes and remediation steps

---

## Additional Resources

- [MCP Tools Reference](./mcp-tools-reference.md) - Error codes for each tool
- [MCP Server Setup Guide](./installation/mcp-server-setup.md) - Troubleshooting common setup issues
- [Obsidian Plugin Installation](./installation/obsidian-plugins.md) - Plugin-specific errors
- [Connection Testing Utilities](../tests/integration/README.md) - Test error scenarios

---

**Document Version:** 1.0
**Last Updated:** 2025-11-09
**Author:** BMAD Development Team
