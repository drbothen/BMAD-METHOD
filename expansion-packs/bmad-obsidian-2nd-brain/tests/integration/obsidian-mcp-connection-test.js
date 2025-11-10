
/**
 * Obsidian MCP Connection Test Utility
 *
 * Tests the connection between Claude Desktop, MCP server, and Obsidian Local REST API.
 *
 * Prerequisites:
 * - Obsidian must be running with Local REST API plugin enabled
 * - MCP Tools plugin must be installed and configured
 * - Claude Desktop must be configured with MCP server
 *
 * Usage:
 *   node obsidian-mcp-connection-test.js
 *
 * Environment Variables:
 *   OBSIDIAN_API_KEY - API key from Local REST API plugin (required)
 *   OBSIDIAN_HOST - Hostname (default: localhost)
 *   OBSIDIAN_PORT - Port number (default: 27123)
 *   OBSIDIAN_PROTOCOL - Protocol (default: http)
 *
 * Exit Codes:
 *   0 - All tests passed
 *   1 - One or more tests failed
 */

const http = require('node:http');
const https = require('node:https');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

// Configuration from environment variables
const CONFIG = {
  apiKey: process.env.OBSIDIAN_API_KEY || '',
  host: process.env.OBSIDIAN_HOST || 'localhost',
  port: process.env.OBSIDIAN_PORT || '27123',
  protocol: process.env.OBSIDIAN_PROTOCOL || 'http',
};

// ANSI color codes for terminal output
const COLORS = {
  reset: '\u001B[0m',
  bright: '\u001B[1m',
  red: '\u001B[31m',
  green: '\u001B[32m',
  yellow: '\u001B[33m',
  blue: '\u001B[34m',
  cyan: '\u001B[36m',
};

// Test results tracking
const results = {
  passed: 0,
  failed: 0,
  tests: [],
};

/**
 * Logging utilities
 */
function log(message, color = COLORS.reset) {
  console.log(`${color}${message}${COLORS.reset}`);
}

function logSuccess(message) {
  log(`✓ ${message}`, COLORS.green);
}

function logError(message) {
  log(`✗ ${message}`, COLORS.red);
}

function logInfo(message) {
  log(`ℹ ${message}`, COLORS.blue);
}

function logWarning(message) {
  log(`⚠ ${message}`, COLORS.yellow);
}

function logSection(message) {
  log(`\n${COLORS.bright}${COLORS.cyan}═══ ${message} ═══${COLORS.reset}`);
}

/**
 * Record test result
 */
function recordTest(name, passed, error = null) {
  results.tests.push({ name, passed, error });
  if (passed) {
    results.passed++;
    logSuccess(name);
  } else {
    results.failed++;
    logError(`${name}: ${error}`);
  }
}

/**
 * Make HTTP/HTTPS request
 */
function makeRequest(options, postData = null) {
  return new Promise((resolve, reject) => {
    const protocol = options.protocol === 'https:' ? https : http;

    const req = protocol.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          headers: res.headers,
          body: data,
        });
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    req.setTimeout(5000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });

    if (postData) {
      req.write(postData);
    }

    req.end();
  });
}

/**
 * Test 1: Configuration Validation
 */
async function testConfigValidation() {
  logSection('Configuration Validation');

  // Check API key
  if (CONFIG.apiKey) {
    recordTest('API key configured', true);
    logInfo(`API key length: ${CONFIG.apiKey.length} characters`);
  } else {
    recordTest('API key configured', false, 'OBSIDIAN_API_KEY environment variable not set');
    logWarning('Set API key: export OBSIDIAN_API_KEY="your-api-key-here"');
    return false;
  }

  // Check configuration values
  logInfo(`Host: ${CONFIG.host}`);
  logInfo(`Port: ${CONFIG.port}`);
  logInfo(`Protocol: ${CONFIG.protocol}`);

  return true;
}

/**
 * Test 2: Obsidian REST API Reachability
 */
async function testRestApiReachability() {
  logSection('Obsidian REST API Reachability');

  try {
    const response = await makeRequest({
      hostname: CONFIG.host,
      port: CONFIG.port,
      path: '/',
      method: 'GET',
      protocol: `${CONFIG.protocol}:`,
      headers: {
        'Authorization': `Bearer ${CONFIG.apiKey}`,
      },
    });

    if (response.statusCode === 200 || response.statusCode === 401 || response.statusCode === 403) {
      recordTest('REST API server reachable', true);
      logInfo(`Server responded with status: ${response.statusCode}`);
      return true;
    } else {
      recordTest('REST API server reachable', false, `Unexpected status code: ${response.statusCode}`);
      return false;
    }
  } catch (error) {
    recordTest('REST API server reachable', false, error.message);
    logWarning('Troubleshooting:');
    logWarning('1. Ensure Obsidian is running');
    logWarning('2. Verify Local REST API plugin is enabled');
    logWarning(`3. Check port ${CONFIG.port} is not blocked by firewall`);
    return false;
  }
}

/**
 * Test 3: API Key Validation
 */
async function testApiKeyValidation() {
  logSection('API Key Validation');

  try {
    const response = await makeRequest({
      hostname: CONFIG.host,
      port: CONFIG.port,
      path: '/',
      method: 'GET',
      protocol: `${CONFIG.protocol}:`,
      headers: {
        'Authorization': `Bearer ${CONFIG.apiKey}`,
      },
    });

    if (response.statusCode === 200) {
      recordTest('API key authentication', true);
      return true;
    } else if (response.statusCode === 401 || response.statusCode === 403) {
      recordTest('API key authentication', false, 'API key invalid or unauthorized');
      logWarning('Troubleshooting:');
      logWarning('1. Copy API key from Obsidian Settings → Local REST API');
      logWarning('2. Regenerate API key if necessary');
      logWarning('3. Verify no extra spaces in API key');
      return false;
    } else {
      recordTest('API key authentication', false, `Unexpected status code: ${response.statusCode}`);
      return false;
    }
  } catch (error) {
    recordTest('API key authentication', false, error.message);
    return false;
  }
}

/**
 * Test 4: Vault Read Permission
 */
async function testVaultReadPermission() {
  logSection('Vault Read Permission');

  try {
    // Try to list vault contents
    const response = await makeRequest({
      hostname: CONFIG.host,
      port: CONFIG.port,
      path: '/vault/',
      method: 'GET',
      protocol: `${CONFIG.protocol}:`,
      headers: {
        'Authorization': `Bearer ${CONFIG.apiKey}`,
      },
    });

    if (response.statusCode === 200) {
      recordTest('Vault read permission', true);

      try {
        const data = JSON.parse(response.body);
        if (data.files && Array.isArray(data.files)) {
          logInfo(`Vault contains ${data.files.length} files`);
        }
      } catch {
        logInfo('Vault data received (could not parse JSON)');
      }

      return true;
    } else {
      recordTest('Vault read permission', false, `Status code: ${response.statusCode}`);
      return false;
    }
  } catch (error) {
    recordTest('Vault read permission', false, error.message);
    return false;
  }
}

/**
 * Test 5: Claude Desktop Configuration
 */
async function testClaudeDesktopConfig() {
  logSection('Claude Desktop Configuration');

  // Determine config file path based on OS
  let configPath;
  switch (os.platform()) {
    case 'darwin': { // macOS
      configPath = path.join(os.homedir(), 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json');
      break;
    }
    case 'win32': { // Windows
      configPath = path.join(process.env.APPDATA || '', 'Claude', 'claude_desktop_config.json');
      break;
    }
    default: { // Linux
      configPath = path.join(os.homedir(), '.config', 'Claude', 'claude_desktop_config.json');
    }
  }

  logInfo(`Config path: ${configPath}`);

  // Check if config file exists
  if (!fs.existsSync(configPath)) {
    recordTest('Claude Desktop config file exists', false, 'File not found');
    logWarning('Claude Desktop may not be installed or configured');
    return false;
  }

  recordTest('Claude Desktop config file exists', true);

  // Read and parse config
  try {
    const configContent = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(configContent);

    recordTest('Claude Desktop config valid JSON', true);

    // Check for MCP servers
    if (!config.mcpServers) {
      recordTest('MCP servers configured', false, 'No mcpServers section found');
      logWarning('Add MCP server configuration to claude_desktop_config.json');
      return false;
    }

    recordTest('MCP servers section exists', true);

    // Look for Obsidian MCP server
    const obsidianServers = Object.keys(config.mcpServers).filter(key =>
      key.toLowerCase().includes('obsidian')
    );

    if (obsidianServers.length === 0) {
      recordTest('Obsidian MCP server configured', false, 'No Obsidian server found in config');
      logWarning('Configure Obsidian MCP server in claude_desktop_config.json');
      return false;
    }

    recordTest('Obsidian MCP server configured', true);
    logInfo(`Found Obsidian servers: ${obsidianServers.join(', ')}`);

    // Verify server configuration
    for (const serverName of obsidianServers) {
      const serverConfig = config.mcpServers[serverName];
      logInfo(`\nServer: ${serverName}`);
      logInfo(`  Command: ${serverConfig.command || 'NOT SET'}`);
      logInfo(`  Args: ${JSON.stringify(serverConfig.args || [])}`);

      if (serverConfig.env) {
        logInfo(`  Environment variables:`);
        for (const key of Object.keys(serverConfig.env)) {
          const value = serverConfig.env[key];
          // Mask API keys in output
          const maskedValue = key.includes('KEY') || key.includes('TOKEN')
            ? value.slice(0, 4) + '...' + value.slice(Math.max(0, value.length - 4))
            : value;
          logInfo(`    ${key}: ${maskedValue}`);
        }
      }
    }

    return true;
  } catch (error) {
    if (error instanceof SyntaxError) {
      recordTest('Claude Desktop config valid JSON', false, 'Invalid JSON syntax');
      logWarning('Validate JSON at https://jsonlint.com/');
    } else {
      recordTest('Claude Desktop config readable', false, error.message);
    }
    return false;
  }
}

/**
 * Test 6: MCP Server Binary Exists
 */
async function testMcpServerBinary() {
  logSection('MCP Server Binary');

  // Read Claude config to find binary path
  let configPath;
  switch (os.platform()) {
    case 'darwin': {
      configPath = path.join(os.homedir(), 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json');
      break;
    }
    case 'win32': {
      configPath = path.join(process.env.APPDATA || '', 'Claude', 'claude_desktop_config.json');
      break;
    }
    default: {
      configPath = path.join(os.homedir(), '.config', 'Claude', 'claude_desktop_config.json');
    }
  }

  if (!fs.existsSync(configPath)) {
    recordTest('MCP server binary check', false, 'Claude config not found');
    return false;
  }

  try {
    const configContent = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(configContent);

    if (!config.mcpServers) {
      recordTest('MCP server binary check', false, 'No MCP servers configured');
      return false;
    }

    const obsidianServers = Object.keys(config.mcpServers).filter(key =>
      key.toLowerCase().includes('obsidian')
    );

    if (obsidianServers.length === 0) {
      recordTest('MCP server binary check', false, 'No Obsidian server configured');
      return false;
    }

    let allBinariesExist = true;

    for (const serverName of obsidianServers) {
      const serverConfig = config.mcpServers[serverName];
      const binaryPath = serverConfig.command;

      if (!binaryPath) {
        recordTest(`MCP binary path configured (${serverName})`, false, 'No command specified');
        allBinariesExist = false;
        continue;
      }

      recordTest(`MCP binary path configured (${serverName})`, true);
      logInfo(`Binary path: ${binaryPath}`);

      // Check if binary exists
      if (fs.existsSync(binaryPath)) {
        recordTest(`MCP binary exists (${serverName})`, true);

        // Check if executable (Unix-like systems)
        if (os.platform() !== 'win32') {
          try {
            fs.accessSync(binaryPath, fs.constants.X_OK);
            recordTest(`MCP binary executable (${serverName})`, true);
          } catch {
            recordTest(`MCP binary executable (${serverName})`, false, 'Not executable');
            logWarning(`Make executable: chmod +x ${binaryPath}`);
            allBinariesExist = false;
          }
        }
      } else {
        recordTest(`MCP binary exists (${serverName})`, false, 'Binary file not found');
        logWarning('Re-run "Install Server" in MCP Tools plugin settings');
        allBinariesExist = false;
      }
    }

    return allBinariesExist;
  } catch (error) {
    recordTest('MCP server binary check', false, error.message);
    return false;
  }
}

/**
 * Test 7: Health Check Summary
 */
function testHealthCheckSummary() {
  logSection('Connection Health Summary');

  const totalTests = results.passed + results.failed;
  const successRate = totalTests > 0 ? ((results.passed / totalTests) * 100).toFixed(1) : 0;

  log(`\nTotal Tests: ${totalTests}`);
  logSuccess(`Passed: ${results.passed}`);

  if (results.failed > 0) {
    logError(`Failed: ${results.failed}`);
  } else {
    logSuccess(`Failed: ${results.failed}`);
  }

  log(`Success Rate: ${successRate}%\n`);

  if (results.failed === 0) {
    logSuccess('✓ All tests passed! MCP connection is properly configured.');
    log('\nNext steps:');
    logInfo('1. Test MCP operations with Phase 1 agents');
    logInfo('2. Review MCP Tools Reference documentation');
    logInfo('3. Explore Error Handling Patterns');
  } else {
    logError('✗ Some tests failed. Review errors above and apply troubleshooting steps.');
    log('\nCommon issues:');
    logWarning('• Obsidian not running → Start Obsidian');
    logWarning('• Local REST API disabled → Enable in plugin settings');
    logWarning('• Invalid API key → Copy from Local REST API settings');
    logWarning('• MCP binary missing → Re-run "Install Server" in MCP Tools');
    logWarning('• Claude config invalid → Validate JSON syntax');
  }
}

/**
 * Main test runner
 */
async function runTests() {
  log(`${COLORS.bright}${COLORS.cyan}`);
  log('╔════════════════════════════════════════════════════════════╗');
  log('║   Obsidian MCP Connection Test Utility v1.0               ║');
  log('║   Tests connectivity between Claude, MCP, and Obsidian    ║');
  log('╚════════════════════════════════════════════════════════════╝');
  log(COLORS.reset);

  // Run tests sequentially
  const configValid = await testConfigValidation();

  if (configValid) {
    await testRestApiReachability();
    await testApiKeyValidation();
    await testVaultReadPermission();
  }

  await testClaudeDesktopConfig();
  await testMcpServerBinary();

  testHealthCheckSummary();

  // Exit with appropriate code
  process.exit(results.failed > 0 ? 1 : 0);
}

/**
 * Entry point
 */
if (require.main === module) {
  runTests().catch(error => {
    logError(`Fatal error: ${error.message}`);
    console.error(error);
    process.exit(1);
  });
}

module.exports = {
  runTests,
  makeRequest,
  CONFIG,
};
