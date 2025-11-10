#!/usr/bin/env node

/**
 * Neo4j Connection Test Utility
 *
 * Tests the connection to Neo4j database for temporal knowledge tracking.
 *
 * Prerequisites:
 * - Neo4j must be running (Docker, Desktop, or Aura)
 * - neo4j-driver npm package installed globally or locally
 *
 * Usage:
 *   node test-neo4j-connection.js
 *
 * Environment Variables:
 *   NEO4J_URI - Bolt connection URI (default: bolt://localhost:7687)
 *   NEO4J_USER - Database username (default: neo4j)
 *   NEO4J_PASSWORD - Database password (required)
 *
 * Exit Codes:
 *   0 - All tests passed
 *   1 - One or more tests failed
 */

const http = require('node:http');
const https = require('node:https');

// Configuration from environment variables
const CONFIG = {
  uri: process.env.NEO4J_URI || 'bolt://localhost:7687',
  user: process.env.NEO4J_USER || 'neo4j',
  password: process.env.NEO4J_PASSWORD || '',
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
 * Make HTTP request to Neo4j Browser (HTTP API)
 */
function makeHttpRequest(port, path = '/') {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: port,
      path: path,
      method: 'GET',
      timeout: 5000,
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => resolve({ status: res.statusCode, data }));
    });

    req.on('error', (error) => reject(error));
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });

    req.end();
  });
}

/**
 * Test Neo4j driver availability
 */
async function testDriverAvailability() {
  try {
    // Try to require neo4j-driver
    require.resolve('neo4j-driver');
    return { success: true };
  } catch (error) {
    return {
      success: false,
      error: 'neo4j-driver not installed. Install with: npm install neo4j-driver',
    };
  }
}

/**
 * Test Neo4j Bolt connection
 */
async function testBoltConnection() {
  let neo4j;
  try {
    neo4j = require('neo4j-driver');
  } catch (error) {
    return {
      success: false,
      error: 'neo4j-driver not available',
    };
  }

  const driver = neo4j.driver(CONFIG.uri, neo4j.auth.basic(CONFIG.user, CONFIG.password), {
    maxConnectionLifetime: 3 * 60 * 1000,
    maxConnectionPoolSize: 50,
    connectionAcquisitionTimeout: 5000,
  });

  try {
    await driver.verifyConnectivity();
    await driver.close();
    return { success: true };
  } catch (error) {
    await driver.close();
    return { success: false, error: error.message };
  }
}

/**
 * Test database authentication
 */
async function testAuthentication() {
  let neo4j;
  try {
    neo4j = require('neo4j-driver');
  } catch (error) {
    return {
      success: false,
      error: 'neo4j-driver not available',
    };
  }

  const driver = neo4j.driver(CONFIG.uri, neo4j.auth.basic(CONFIG.user, CONFIG.password));
  const session = driver.session();

  try {
    const result = await session.run('RETURN 1 AS test');
    const value = result.records[0].get('test').toNumber();
    await session.close();
    await driver.close();

    if (value === 1) {
      return { success: true };
    } else {
      return { success: false, error: 'Unexpected query result' };
    }
  } catch (error) {
    await session.close();
    await driver.close();
    return { success: false, error: error.message };
  }
}

/**
 * Test APOC plugin availability
 */
async function testApocPlugin() {
  let neo4j;
  try {
    neo4j = require('neo4j-driver');
  } catch (error) {
    return {
      success: false,
      error: 'neo4j-driver not available',
    };
  }

  const driver = neo4j.driver(CONFIG.uri, neo4j.auth.basic(CONFIG.user, CONFIG.password));
  const session = driver.session();

  try {
    const result = await session.run("CALL apoc.help('apoc') YIELD name RETURN count(name) AS apoc_count");
    const count = result.records[0].get('apoc_count').toNumber();
    await session.close();
    await driver.close();

    if (count > 0) {
      return { success: true, procedureCount: count };
    } else {
      return { success: false, error: 'APOC plugin not installed or no procedures available' };
    }
  } catch (error) {
    await session.close();
    await driver.close();
    return { success: false, error: error.message };
  }
}

/**
 * Test database write permissions
 */
async function testWritePermissions() {
  let neo4j;
  try {
    neo4j = require('neo4j-driver');
  } catch (error) {
    return {
      success: false,
      error: 'neo4j-driver not available',
    };
  }

  const driver = neo4j.driver(CONFIG.uri, neo4j.auth.basic(CONFIG.user, CONFIG.password));
  const session = driver.session();

  try {
    // Create test node
    await session.run('CREATE (n:TestNode {id: $id, timestamp: datetime()}) RETURN n', {
      id: 'test-' + Date.now(),
    });

    // Clean up test node
    await session.run('MATCH (n:TestNode) WHERE n.id STARTS WITH "test-" DELETE n');

    await session.close();
    await driver.close();
    return { success: true };
  } catch (error) {
    await session.close();
    await driver.close();
    return { success: false, error: error.message };
  }
}

/**
 * Test Neo4j Browser HTTP endpoint
 */
async function testNeo4jBrowser() {
  try {
    const response = await makeHttpRequest(7474, '/');
    if (response.status === 200) {
      return { success: true };
    } else {
      return { success: false, error: `HTTP ${response.status}` };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Get Neo4j version
 */
async function getNeo4jVersion() {
  let neo4j;
  try {
    neo4j = require('neo4j-driver');
  } catch (error) {
    return { success: false, error: 'neo4j-driver not available' };
  }

  const driver = neo4j.driver(CONFIG.uri, neo4j.auth.basic(CONFIG.user, CONFIG.password));
  const session = driver.session();

  try {
    const result = await session.run('CALL dbms.components() YIELD name, versions RETURN name, versions[0] AS version');
    const record = result.records.find((r) => r.get('name') === 'Neo4j Kernel');
    const version = record ? record.get('version') : 'Unknown';
    await session.close();
    await driver.close();
    return { success: true, version };
  } catch (error) {
    await session.close();
    await driver.close();
    return { success: false, error: error.message };
  }
}

/**
 * Test database schema creation
 */
async function testSchemaCreation() {
  let neo4j;
  try {
    neo4j = require('neo4j-driver');
  } catch (error) {
    return {
      success: false,
      error: 'neo4j-driver not available',
    };
  }

  const driver = neo4j.driver(CONFIG.uri, neo4j.auth.basic(CONFIG.user, CONFIG.password));
  const session = driver.session();

  try {
    // Create test constraint (if not exists)
    await session.run(
      'CREATE CONSTRAINT test_node_id IF NOT EXISTS FOR (n:TestNode) REQUIRE n.id IS UNIQUE'
    );

    // Create test index (if not exists)
    await session.run(
      'CREATE INDEX test_node_timestamp IF NOT EXISTS FOR (n:TestNode) ON (n.timestamp)'
    );

    // Clean up test schema
    await session.run('DROP CONSTRAINT test_node_id IF EXISTS');
    await session.run('DROP INDEX test_node_timestamp IF EXISTS');

    await session.close();
    await driver.close();
    return { success: true };
  } catch (error) {
    await session.close();
    await driver.close();
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
  logSection('Neo4j Connection Test Utility');
  logInfo(`URI: ${CONFIG.uri}`);
  logInfo(`User: ${CONFIG.user}`);
  logInfo(`Password: ${CONFIG.password ? '***' + CONFIG.password.slice(-4) : '(not set)'}\n`);

  // Prerequisites check
  logSection('Prerequisites Check');

  if (!CONFIG.password) {
    logError('NEO4J_PASSWORD environment variable not set');
    logInfo('Set with: export NEO4J_PASSWORD="your-password"');
    process.exit(1);
  }

  // Test 1: Check driver availability
  logSection('Test 1: Neo4j Driver Availability');
  const driverTest = await testDriverAvailability();
  recordTest('Neo4j driver installed', driverTest.success, driverTest.error);

  if (!driverTest.success) {
    logWarning('\nSkipping remaining tests - neo4j-driver not available');
    logInfo('Install with: npm install neo4j-driver');
    logInfo('Or globally: npm install -g neo4j-driver');
    printSummary();
    process.exit(1);
  }

  // Test 2: Check Neo4j Browser HTTP endpoint
  logSection('Test 2: Neo4j Browser HTTP Endpoint');
  const browserTest = await testNeo4jBrowser();
  recordTest('Neo4j Browser accessible (http://localhost:7474)', browserTest.success, browserTest.error);

  // Test 3: Bolt connection
  logSection('Test 3: Bolt Protocol Connection');
  const boltTest = await testBoltConnection();
  recordTest('Bolt connection established', boltTest.success, boltTest.error);

  if (!boltTest.success) {
    logWarning('\nSkipping remaining tests - cannot connect to Neo4j');
    logInfo('Verify Neo4j is running:');
    logInfo('  Docker: docker compose -f docker-compose.neo4j.yml ps');
    logInfo('  Desktop: Check Neo4j Desktop application');
    printSummary();
    process.exit(1);
  }

  // Test 4: Authentication
  logSection('Test 4: Database Authentication');
  const authTest = await testAuthentication();
  recordTest('Authentication successful', authTest.success, authTest.error);

  if (!authTest.success) {
    logWarning('\nAuthentication failed - check credentials');
    printSummary();
    process.exit(1);
  }

  // Test 5: Get Neo4j version
  logSection('Test 5: Database Version');
  const versionTest = await getNeo4jVersion();
  if (versionTest.success) {
    recordTest(`Neo4j version detected: ${versionTest.version}`, true);
  } else {
    recordTest('Get Neo4j version', false, versionTest.error);
  }

  // Test 6: APOC plugin
  logSection('Test 6: APOC Plugin Availability');
  const apocTest = await testApocPlugin();
  if (apocTest.success) {
    recordTest(`APOC plugin available (${apocTest.procedureCount} procedures)`, true);
  } else {
    recordTest('APOC plugin available', false, apocTest.error);
    logWarning('APOC is required for temporal knowledge tracking');
    logInfo('Install APOC: See docs/installation/neo4j-setup.md');
  }

  // Test 7: Write permissions
  logSection('Test 7: Database Write Permissions');
  const writeTest = await testWritePermissions();
  recordTest('Write operations permitted', writeTest.success, writeTest.error);

  // Test 8: Schema creation
  logSection('Test 8: Schema Management');
  const schemaTest = await testSchemaCreation();
  recordTest('Constraints and indexes can be created', schemaTest.success, schemaTest.error);

  // Print summary
  printSummary();

  // Exit with appropriate code
  process.exit(results.failed > 0 ? 1 : 0);
}

// Run tests
runTests().catch((error) => {
  logError(`Unexpected error: ${error.message}`);
  console.error(error);
  process.exit(1);
});
