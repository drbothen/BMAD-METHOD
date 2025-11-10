#!/usr/bin/env node

/**
 * Graphiti MCP Connection Test Utility
 *
 * Tests the connection to Graphiti MCP server for temporal knowledge tracking.
 *
 * Prerequisites:
 * - Neo4j must be running and accessible
 * - Graphiti MCP server must be running (Docker or local)
 * - OpenAI API key configured (for entity extraction)
 *
 * Usage:
 *   node test-graphiti-mcp-connection.js
 *
 * Environment Variables:
 *   GRAPHITI_MCP_HOST - MCP server hostname (default: localhost)
 *   GRAPHITI_MCP_PORT - MCP server port (default: 8000)
 *   NEO4J_URI - Bolt connection URI (default: bolt://localhost:7687)
 *   NEO4J_USER - Database username (default: neo4j)
 *   NEO4J_PASSWORD - Database password (required)
 *   OPENAI_API_KEY - OpenAI API key (required for Graphiti)
 *
 * Exit Codes:
 *   0 - All tests passed
 *   1 - One or more tests failed
 */

const http = require('node:http');
const https = require('node:https');

// Configuration from environment variables
const CONFIG = {
  host: process.env.GRAPHITI_MCP_HOST || 'localhost',
  port: process.env.GRAPHITI_MCP_PORT || '8000',
  neo4jUri: process.env.NEO4J_URI || 'bolt://localhost:7687',
  neo4jUser: process.env.NEO4J_USER || 'neo4j',
  neo4jPassword: process.env.NEO4J_PASSWORD || '',
  openaiKey: process.env.OPENAI_API_KEY || '',
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
 * Make HTTP request
 */
function makeRequest(options, postData = null) {
  return new Promise((resolve, reject) => {
    const protocol = options.protocol === 'https:' ? https : http;

    const req = protocol.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          const parsed = data ? JSON.parse(data) : null;
          resolve({ status: res.statusCode, data: parsed, headers: res.headers });
        } catch (error) {
          resolve({ status: res.statusCode, data, headers: res.headers });
        }
      });
    });

    req.on('error', (error) => reject(error));
    req.on('timeout', () => {
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
 * Test Graphiti MCP server health endpoint
 */
async function testHealthEndpoint() {
  try {
    const options = {
      hostname: CONFIG.host,
      port: CONFIG.port,
      path: '/health',
      method: 'GET',
      timeout: 5000,
    };

    const response = await makeRequest(options);

    if (response.status === 200) {
      if (response.data && response.data.status === 'healthy') {
        return { success: true, data: response.data };
      } else {
        return { success: false, error: 'Health check returned unhealthy status' };
      }
    } else {
      return { success: false, error: `HTTP ${response.status}` };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Test Neo4j connection via Graphiti health endpoint
 */
async function testNeo4jConnection() {
  try {
    const options = {
      hostname: CONFIG.host,
      port: CONFIG.port,
      path: '/health',
      method: 'GET',
      timeout: 5000,
    };

    const response = await makeRequest(options);

    if (response.status === 200 && response.data) {
      if (response.data.neo4j === 'connected') {
        return { success: true };
      } else {
        return { success: false, error: `Neo4j status: ${response.data.neo4j || 'unknown'}` };
      }
    } else {
      return { success: false, error: `HTTP ${response.status}` };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Test MCP tools endpoint (list available tools)
 */
async function testMcpTools() {
  try {
    const options = {
      hostname: CONFIG.host,
      port: CONFIG.port,
      path: '/mcp/tools',
      method: 'GET',
      timeout: 5000,
    };

    const response = await makeRequest(options);

    if (response.status === 200) {
      if (response.data && Array.isArray(response.data.tools)) {
        return { success: true, tools: response.data.tools };
      } else {
        return { success: false, error: 'Unexpected response format' };
      }
    } else if (response.status === 404) {
      // Try alternate endpoint format
      return { success: false, error: 'MCP tools endpoint not found (may vary by Graphiti version)' };
    } else {
      return { success: false, error: `HTTP ${response.status}` };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Test specific MCP operations (simulated, without actual MCP client)
 */
async function testMcpOperationAvailability() {
  const requiredOperations = ['add_episode', 'get_episodes', 'add_entity', 'add_relation'];

  try {
    const options = {
      hostname: CONFIG.host,
      port: CONFIG.port,
      path: '/mcp/tools',
      method: 'GET',
      timeout: 5000,
    };

    const response = await makeRequest(options);

    if (response.status === 404) {
      // If /mcp/tools not available, assume operations exist (cannot verify without MCP client)
      return {
        success: true,
        message: 'Cannot verify operations without MCP client (endpoint not available)',
        partial: true,
      };
    }

    if (response.status === 200 && response.data && Array.isArray(response.data.tools)) {
      const availableTools = response.data.tools.map((t) => t.name || t);
      const missingTools = requiredOperations.filter((op) => !availableTools.includes(op));

      if (missingTools.length === 0) {
        return { success: true, tools: availableTools };
      } else {
        return {
          success: false,
          error: `Missing operations: ${missingTools.join(', ')}`,
        };
      }
    } else {
      return { success: false, error: 'Unexpected response format' };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Test Graphiti Docker container (if using Docker)
 */
async function testDockerContainer() {
  const { exec } = require('child_process');
  const { promisify } = require('util');
  const execPromise = promisify(exec);

  try {
    const { stdout } = await execPromise('docker ps --filter "name=graphiti" --format "{{.Names}}"');
    const containers = stdout.trim().split('\n').filter(Boolean);

    if (containers.length > 0) {
      return { success: true, containers };
    } else {
      return { success: false, error: 'No Graphiti containers running' };
    }
  } catch (error) {
    // Docker not available or no containers found
    return { success: false, error: 'Docker not available or no Graphiti containers' };
  }
}

/**
 * Test OpenAI API key configuration
 */
async function testOpenAiConfig() {
  if (!CONFIG.openaiKey) {
    return { success: false, error: 'OPENAI_API_KEY not set' };
  }

  if (!CONFIG.openaiKey.startsWith('sk-')) {
    return { success: false, error: 'Invalid API key format (should start with sk-)' };
  }

  // Basic format validation
  if (CONFIG.openaiKey.length < 20) {
    return { success: false, error: 'API key too short (invalid format)' };
  }

  return { success: true, keyLength: CONFIG.openaiKey.length };
}

/**
 * Test connectivity to Graphiti server (basic ping)
 */
async function testServerReachability() {
  try {
    const options = {
      hostname: CONFIG.host,
      port: CONFIG.port,
      path: '/',
      method: 'GET',
      timeout: 5000,
    };

    const response = await makeRequest(options);

    // Any response (even 404) means server is reachable
    if (response.status >= 200 && response.status < 600) {
      return { success: true, status: response.status };
    } else {
      return { success: false, error: `Unexpected status: ${response.status}` };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Print test summary
 */
function printSummary() {
  logSection('Test Summary');
  log(`Total tests: ${results.tests.length}`);
  logSuccess(`Passed: ${results.passed}`);
  if (results.failed > 0) {
    logError(`Failed: ${results.failed}`);
  } else {
    log(`Failed: ${results.failed}`);
  }

  if (results.failed > 0) {
    log('\nFailed tests:', COLORS.red);
    results.tests
      .filter((t) => !t.passed)
      .forEach((t) => {
        logError(`  - ${t.name}: ${t.error}`);
      });
  }
}

/**
 * Main test runner
 */
async function runTests() {
  logSection('Graphiti MCP Connection Test Utility');
  logInfo(`Graphiti MCP: http://${CONFIG.host}:${CONFIG.port}`);
  logInfo(`Neo4j URI: ${CONFIG.neo4jUri}`);
  logInfo(`Neo4j User: ${CONFIG.neo4jUser}`);
  logInfo(`Neo4j Password: ${CONFIG.neo4jPassword ? '***' + CONFIG.neo4jPassword.slice(-4) : '(not set)'}`);
  logInfo(`OpenAI Key: ${CONFIG.openaiKey ? 'sk-***' + CONFIG.openaiKey.slice(-4) : '(not set)'}\n`);

  // Prerequisites check
  logSection('Prerequisites Check');

  if (!CONFIG.neo4jPassword) {
    logWarning('NEO4J_PASSWORD not set');
    logInfo('Set with: export NEO4J_PASSWORD="your-password"');
  }

  if (!CONFIG.openaiKey) {
    logWarning('OPENAI_API_KEY not set');
    logInfo('Set with: export OPENAI_API_KEY="sk-your-key"');
  }

  // Test 1: Server reachability
  logSection('Test 1: Graphiti MCP Server Reachability');
  const reachTest = await testServerReachability();
  recordTest('Graphiti MCP server reachable', reachTest.success, reachTest.error);

  if (!reachTest.success) {
    logWarning('\nCannot reach Graphiti MCP server');
    logInfo('Verify Graphiti is running:');
    logInfo('  Docker: docker compose ps');
    logInfo('  Local: Check uv/graphiti-server process');
    printSummary();
    process.exit(1);
  }

  // Test 2: Health endpoint
  logSection('Test 2: Health Endpoint');
  const healthTest = await testHealthEndpoint();
  recordTest('Health endpoint returns healthy status', healthTest.success, healthTest.error);

  if (healthTest.success && healthTest.data) {
    logInfo(`Health data: ${JSON.stringify(healthTest.data)}`);
  }

  // Test 3: Neo4j connection via Graphiti
  logSection('Test 3: Neo4j Connection (via Graphiti)');
  const neo4jTest = await testNeo4jConnection();
  recordTest('Neo4j connection verified through Graphiti', neo4jTest.success, neo4jTest.error);

  if (!neo4jTest.success) {
    logWarning('Graphiti cannot connect to Neo4j');
    logInfo('Check Neo4j is running: docker compose -f docker-compose.neo4j.yml ps');
    logInfo('Verify Graphiti .env configuration');
  }

  // Test 4: MCP tools availability
  logSection('Test 4: MCP Tools Endpoint');
  const toolsTest = await testMcpTools();
  if (toolsTest.success) {
    recordTest(`MCP tools endpoint accessible (${toolsTest.tools.length} tools available)`, true);
    logInfo(`Available tools: ${toolsTest.tools.map((t) => t.name || t).join(', ')}`);
  } else {
    recordTest('MCP tools endpoint accessible', false, toolsTest.error);
    logInfo('This may be expected depending on Graphiti version/configuration');
  }

  // Test 5: Required MCP operations
  logSection('Test 5: Required MCP Operations');
  const opsTest = await testMcpOperationAvailability();
  if (opsTest.partial) {
    recordTest(opsTest.message, true);
    logInfo('Full verification requires MCP client integration');
  } else if (opsTest.success) {
    recordTest('All required operations available', true);
    logInfo('Operations: add_episode, get_episodes, add_entity, add_relation');
  } else {
    recordTest('All required operations available', false, opsTest.error);
  }

  // Test 6: OpenAI API key configuration
  logSection('Test 6: OpenAI API Key Configuration');
  const openaiTest = await testOpenAiConfig();
  recordTest('OpenAI API key configured', openaiTest.success, openaiTest.error);

  if (!openaiTest.success) {
    logWarning('Graphiti requires OpenAI API key for entity extraction');
    logInfo('Set with: export OPENAI_API_KEY="sk-your-key"');
  }

  // Test 7: Docker container check (optional)
  logSection('Test 7: Docker Container Status (Optional)');
  const dockerTest = await testDockerContainer();
  if (dockerTest.success) {
    recordTest(`Graphiti Docker containers running: ${dockerTest.containers.join(', ')}`, true);
  } else {
    logInfo('Docker check skipped or no containers found (may be using local installation)');
    recordTest('Docker containers detected', false, dockerTest.error);
  }

  // Print summary
  printSummary();

  // Additional recommendations
  if (results.failed > 0) {
    logSection('Troubleshooting Tips');
    logInfo('1. Check Graphiti logs: docker compose logs graphiti-mcp');
    logInfo('2. Verify Neo4j is running: docker compose -f docker-compose.neo4j.yml ps');
    logInfo('3. Test Neo4j separately: node test-neo4j-connection.js');
    logInfo('4. Review Graphiti .env configuration');
    logInfo('5. See docs/installation/graphiti-mcp-setup.md for setup details');
  } else {
    logSection('Next Steps');
    logInfo('✓ Graphiti MCP server is operational');
    logInfo('Configure Claude Desktop:');
    logInfo('  - See docs/installation/mcp-server-setup.md (Graphiti section)');
    logInfo('  - Add Graphiti to claude_desktop_config.json');
    logInfo('  - Restart Claude Desktop');
    logInfo('Test in Claude Desktop: "What Graphiti tools are available?"');
  }

  // Exit with appropriate code
  process.exit(results.failed > 0 ? 1 : 0);
}

// Run tests
runTests().catch((error) => {
  logError(`Unexpected error: ${error.message}`);
  console.error(error);
  process.exit(1);
});
