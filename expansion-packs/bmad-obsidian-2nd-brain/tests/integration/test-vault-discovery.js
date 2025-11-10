
/**
 * Vault Discovery Integration Tests
 *
 * Tests vault discovery, structure detection, and configuration validation.
 *
 * Prerequisites:
 * - Node.js v16+
 * - Obsidian installed (optional - uses mocks if not available)
 *
 * Usage:
 *   node test-vault-discovery.js
 *   npm run test:vault-discovery
 *
 * Tests:
 * - Vault discovery from Obsidian config
 * - OS-specific config path detection
 * - Path validation and security
 * - Vault accessibility checking
 * - Structure detection (PARA, Zettelkasten, LYT, Johnny Decimal, Custom)
 * - Key location detection
 * - Configuration generation
 * - Error handling (invalid paths, missing vaults, etc.)
 *
 * Exit Codes:
 *   0 - All tests passed
 *   1 - One or more tests failed
 */

const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

// Import modules to test
const vaultDiscovery = require('../../tools/vault-discovery.js');
const vaultAnalyzer = require('../../tools/vault-analyzer.js');

// ANSI color codes for terminal output
const COLORS = {
  reset: '\u001B[0m',
  bright: '\u001B[1m',
  red: '\u001B[31m',
  green: '\u001B[32m',
  yellow: '\u001B[33m',
  blue: '\u001B[34m',
  cyan: '\u001B[36m',
  magenta: '\u001B[35m',
};

// Test results tracking
const results = {
  passed: 0,
  failed: 0,
  skipped: 0,
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

function logSkipped(message) {
  log(`⊘ ${message}`, COLORS.cyan);
}

function logSection(message) {
  log(`\n${COLORS.bright}${COLORS.cyan}═══ ${message} ═══${COLORS.reset}`);
}

/**
 * Record test result
 */
function recordTest(name, passed, error = null, skipped = false) {
  results.tests.push({ name, passed, error, skipped });
  if (skipped) {
    results.skipped++;
    logSkipped(`${name} (skipped)`);
  } else if (passed) {
    results.passed++;
    logSuccess(name);
  } else {
    results.failed++;
    logError(`${name}: ${error}`);
  }
}

/**
 * Create temporary test vault
 */
function createTestVault(name, folders = []) {
  const tmpDir = os.tmpdir();
  const vaultPath = path.join(tmpDir, `test-vault-${name}-${Date.now()}`);

  // Create vault directory
  fs.mkdirSync(vaultPath, { recursive: true });

  // Create .obsidian directory (required for valid vault)
  const obsidianDir = path.join(vaultPath, '.obsidian');
  fs.mkdirSync(obsidianDir, { recursive: true });

  // Create test folders
  for (const folder of folders) {
    const folderPath = path.join(vaultPath, folder);
    fs.mkdirSync(folderPath, { recursive: true });
  }

  return vaultPath;
}

/**
 * Clean up test vault
 */
function cleanupTestVault(vaultPath) {
  try {
    if (fs.existsSync(vaultPath)) {
      fs.rmSync(vaultPath, { recursive: true, force: true });
    }
  } catch (error) {
    logWarning(`Failed to cleanup test vault: ${error.message}`);
  }
}

/**
 * Create mock Obsidian config
 */
function createMockObsidianConfig(vaults) {
  const tmpDir = os.tmpdir();
  const configDir = path.join(tmpDir, `obsidian-config-${Date.now()}`);
  fs.mkdirSync(configDir, { recursive: true });

  const configPath = path.join(configDir, 'obsidian.json');
  const config = {
    vaults: {}
  };

  for (const vault of vaults) {
    config.vaults[vault.id] = {
      path: vault.path,
      ts: vault.ts || Date.now(),
      open: vault.open || false,
      type: vault.type || 'file-system'
    };
  }

  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));

  return configDir;
}

/**
 * Tests
 */

async function testObsidianConfigPathDetection() {
  logSection('Obsidian Config Path Detection');

  try {
    const configPath = vaultDiscovery.getObsidianConfigPath();
    recordTest('Get Obsidian config path for current OS', !!configPath);

    const platform = os.platform();
    const homeDir = os.homedir();

    switch (platform) {
    case 'darwin': {
      const expected = path.join(homeDir, 'Library', 'Application Support', 'obsidian');
      recordTest('macOS config path is correct', configPath === expected);
    
    break;
    }
    case 'win32': {
      const expected = path.join(process.env.APPDATA || path.join(homeDir, 'AppData', 'Roaming'), 'obsidian');
      recordTest('Windows config path is correct', configPath === expected);
    
    break;
    }
    case 'linux': {
      const expected = path.join(process.env.XDG_CONFIG_HOME || path.join(homeDir, '.config'), 'obsidian');
      recordTest('Linux config path is correct', configPath === expected);
    
    break;
    }
    // No default
    }

  } catch (error) {
    recordTest('Get Obsidian config path', false, error.message);
  }
}

async function testPathValidation() {
  logSection('Path Validation and Security');

  try {
    // Test valid absolute path
    const validPath = path.resolve('/tmp');
    const validated = vaultDiscovery.validatePath(validPath);
    recordTest('Validate absolute path', !!validated);

    // Test path traversal rejection
    let pathTraversalBlocked = false;
    try {
      const dangerousPath = '../../../etc/passwd';
      vaultDiscovery.validatePath(dangerousPath);
      pathTraversalBlocked = false; // Should have thrown
    } catch {
      pathTraversalBlocked = true; // Any error is good - path was blocked
    }
    recordTest('Reject path traversal attempts', pathTraversalBlocked);

    // Test invalid path (null)
    let nullPathBlocked = false;
    try {
      vaultDiscovery.validatePath(null);
    } catch (error) {
      nullPathBlocked = error.message.includes('Invalid path');
    }
    recordTest('Reject null path', nullPathBlocked);

    // Test invalid path (empty string)
    let emptyPathBlocked = false;
    try {
      vaultDiscovery.validatePath('');
    } catch (error) {
      emptyPathBlocked = error.message.includes('Invalid path');
    }
    recordTest('Reject empty path', emptyPathBlocked);

  } catch (error) {
    recordTest('Path validation tests', false, error.message);
  }
}

async function testVaultAccessibility() {
  logSection('Vault Accessibility Checking');

  const testVault = createTestVault('accessibility', ['Projects', 'Areas']);

  try {
    // Test existing, accessible vault
    const accessibility = vaultDiscovery.checkVaultAccessibility(testVault);
    recordTest('Check accessible vault exists', accessibility.exists);
    recordTest('Check accessible vault is readable', accessibility.readable);
    recordTest('Check accessible vault is writable', accessibility.writable);
    recordTest('No accessibility errors for valid vault', !accessibility.error);

    // Test non-existent vault
    const nonExistent = vaultDiscovery.checkVaultAccessibility('/nonexistent/vault/path');
    recordTest('Detect non-existent vault', !nonExistent.exists);
    recordTest('Report error for non-existent vault', !!nonExistent.error);

  } catch (error) {
    recordTest('Vault accessibility tests', false, error.message);
  } finally {
    cleanupTestVault(testVault);
  }
}

async function testValidVaultDetection() {
  logSection('Valid Vault Detection');

  const validVault = createTestVault('valid', ['Projects']);
  const invalidVault = path.join(os.tmpdir(), `invalid-vault-${Date.now()}`);
  fs.mkdirSync(invalidVault, { recursive: true });

  try {
    // Test valid vault (has .obsidian directory)
    const isValid = vaultDiscovery.isValidVault(validVault);
    recordTest('Detect valid Obsidian vault', isValid);

    // Test invalid vault (missing .obsidian directory)
    const isInvalid = vaultDiscovery.isValidVault(invalidVault);
    recordTest('Reject invalid vault (no .obsidian)', !isInvalid);

  } catch (error) {
    recordTest('Valid vault detection', false, error.message);
  } finally {
    cleanupTestVault(validVault);
    cleanupTestVault(invalidVault);
  }
}

async function testOrganizationMethodDetection() {
  logSection('Organization Method Detection');

  // Test PARA detection
  const paraVault = createTestVault('para', [
    '10 Projects',
    '20 Areas',
    '30 Resources',
    '40 Archive',
    '00 Inbox'
  ]);

  try {
    const paraAnalysis = vaultAnalyzer.analyzeVault(paraVault);
    recordTest('Detect PARA organization', paraAnalysis.organizationMethod === 'para');
    recordTest('PARA detection confidence > 50%', paraAnalysis.confidence > 0.5);
  } catch (error) {
    recordTest('PARA detection', false, error.message);
  } finally {
    cleanupTestVault(paraVault);
  }

  // Test Zettelkasten detection
  const zettelVault = createTestVault('zettel', [
    'Fleeting',
    'Permanent',
    'Literature',
    'Reference'
  ]);

  try {
    const zettelAnalysis = vaultAnalyzer.analyzeVault(zettelVault);
    recordTest('Detect Zettelkasten organization', zettelAnalysis.organizationMethod === 'zettelkasten');
    recordTest('Zettelkasten detection confidence > 50%', zettelAnalysis.confidence > 0.5);
  } catch (error) {
    recordTest('Zettelkasten detection', false, error.message);
  } finally {
    cleanupTestVault(zettelVault);
  }

  // Test LYT detection
  const lytVault = createTestVault('lyt', [
    '100 MOCs',
    '200 Notes',
    '300 Projects',
    '000 Inbox'
  ]);

  try {
    const lytAnalysis = vaultAnalyzer.analyzeVault(lytVault);
    recordTest('Detect LYT organization', lytAnalysis.organizationMethod === 'lyt');
  } catch (error) {
    recordTest('LYT detection', false, error.message);
  } finally {
    cleanupTestVault(lytVault);
  }

  // Test Johnny Decimal detection
  const jdVault = createTestVault('johnny', [
    '00-09 System',
    '10-19 Projects',
    '20-29 Areas',
    '30-39 Resources',
    '90-99 Archive'
  ]);

  try {
    const jdAnalysis = vaultAnalyzer.analyzeVault(jdVault);
    const isJD = jdAnalysis.organizationMethod === 'johnnyDecimal';
    recordTest('Detect Johnny Decimal organization', isJD, isJD ? null : `Got: ${jdAnalysis.organizationMethod}`);
    recordTest('Johnny Decimal detection confidence > 50%', jdAnalysis.confidence > 0.5);
  } catch (error) {
    recordTest('Johnny Decimal detection', false, error.message);
    recordTest('Johnny Decimal detection confidence > 50%', false, error.message);
  } finally {
    cleanupTestVault(jdVault);
  }

  // Test Custom (no clear pattern)
  const customVault = createTestVault('custom', [
    'MyStuff',
    'RandomFolder',
    'Things'
  ]);

  try {
    const customAnalysis = vaultAnalyzer.analyzeVault(customVault);
    const isCustom = customAnalysis.organizationMethod === 'custom';
    recordTest('Detect Custom organization (fallback)', isCustom, isCustom ? null : `Got: ${customAnalysis.organizationMethod}`);
  } catch (error) {
    recordTest('Custom detection', false, error.message);
  } finally {
    cleanupTestVault(customVault);
  }
}

async function testKeyLocationDetection() {
  logSection('Key Location Detection');

  const testVault = createTestVault('locations', [
    '00 Inbox',
    '10 Projects',
    '20 Areas',
    '30 Resources',
    '40 Archive',
    '50 Permanent Notes',
    '60 MOCs',
    'Templates',
    'AI Generated'
  ]);

  try {
    const analysis = vaultAnalyzer.analyzeVault(testVault);
    const locations = analysis.keyLocations;

    recordTest('Detect inbox location', !!locations.inbox);
    recordTest('Detect projects location', !!locations.projects);
    recordTest('Detect areas location', !!locations.areas);
    recordTest('Detect resources location', !!locations.resources);
    recordTest('Detect archive location', !!locations.archive);
    recordTest('Detect atomic notes location', !!locations.atomicNotes);
    recordTest('Detect MOCs location', !!locations.mocs);
    recordTest('Detect templates location', !!locations.templates);
    recordTest('Detect agent output location', !!locations.agentOutput);

  } catch (error) {
    recordTest('Key location detection', false, error.message);
  } finally {
    cleanupTestVault(testVault);
  }
}

async function testStructureValidation() {
  logSection('Structure Validation');

  const goodVault = createTestVault('good', [
    'Inbox',
    'Projects',
    'Areas',
    'Resources'
  ]);

  const deepVault = createTestVault('deep', [
    'Level1/Level2/Level3/Level4/Level5/Level6'
  ]);

  try {
    // Test well-structured vault
    const goodAnalysis = vaultAnalyzer.analyzeVault(goodVault);
    recordTest('Validate good vault structure', goodAnalysis.validation && goodAnalysis.validation.isValid);

    // Test deep structure (should generate warning)
    const deepAnalysis = vaultAnalyzer.analyzeVault(deepVault);
    const isDeep = deepAnalysis.structureDepth > 3;
    recordTest('Detect deep structure', isDeep, isDeep ? null : `Depth: ${deepAnalysis.structureDepth}`);

  } catch (error) {
    recordTest('Structure validation', false, error.message);
    recordTest('Detect deep structure', false, error.message);
  } finally {
    cleanupTestVault(goodVault);
    cleanupTestVault(deepVault);
  }
}

async function testConfigurationGeneration() {
  logSection('Configuration Generation');

  const testVault = createTestVault('config', [
    '10 Projects',
    '20 Areas',
    '30 Resources',
    '00 Inbox'
  ]);

  try {
    const analysis = vaultAnalyzer.analyzeVault(testVault);
    const config = vaultAnalyzer.generateConfigSuggestion(analysis);

    recordTest('Generate configuration suggestion', !!config);
    recordTest('Config has required id field', !!config.id);
    recordTest('Config has required name field', !!config.name);
    recordTest('Config has required path field', !!config.path);
    recordTest('Config has required enabled field', typeof config.enabled === 'boolean');
    recordTest('Config has organizationMethod field', !!config.organizationMethod);
    recordTest('Config has keyLocations object', !!config.keyLocations && typeof config.keyLocations === 'object');
    recordTest('Config has agentsEnabled array', Array.isArray(config.agentsEnabled));

  } catch (error) {
    recordTest('Configuration generation', false, error.message);
  } finally {
    cleanupTestVault(testVault);
  }
}

async function testErrorHandling() {
  logSection('Error Handling');

  try {
    // Test non-existent vault path
    const nonExistentAnalysis = vaultAnalyzer.analyzeVault('/nonexistent/vault/path');
    recordTest('Handle non-existent vault gracefully', !!nonExistentAnalysis.error);

    // Test invalid vault (no .obsidian)
    const invalidVault = path.join(os.tmpdir(), `invalid-${Date.now()}`);
    fs.mkdirSync(invalidVault, { recursive: true });
    const invalidAnalysis = vaultAnalyzer.analyzeVault(invalidVault);
    recordTest('Handle invalid vault gracefully', !!invalidAnalysis.error);
    cleanupTestVault(invalidVault);

  } catch (error) {
    recordTest('Error handling tests', false, error.message);
  }
}

async function testRealVaultDiscovery() {
  logSection('Real Vault Discovery (Optional)');

  try {
    const configPath = vaultDiscovery.getObsidianConfigPath();
    const obsidianJsonPath = path.join(configPath, 'obsidian.json');

    if (!fs.existsSync(obsidianJsonPath)) {
      recordTest('Discover real Obsidian vaults', false, null, true);
      logInfo('Skipping real vault discovery - Obsidian not installed or not configured');
      return;
    }

    const summary = vaultDiscovery.getVaultSummary();

    if (summary.error) {
      recordTest('Discover real vaults', false, summary.error);
      return;
    }

    recordTest('Discover real Obsidian vaults', summary.total >= 0);
    logInfo(`Found ${summary.total} vault(s), ${summary.accessible} accessible, ${summary.valid} valid`);

    if (summary.accessible > 0) {
      const vaults = vaultDiscovery.discoverVaults();
      recordTest('Parse discovered vaults', vaults.length > 0);

      if (vaults.length > 0) {
        const firstVault = vaults[0];
        recordTest('Discovered vault has path', !!firstVault.path);
        recordTest('Discovered vault is validated', firstVault.validated);

        // Try to analyze the first discovered vault
        try {
          const analysis = vaultAnalyzer.analyzeVault(firstVault.path);
          recordTest('Analyze discovered vault', !analysis.error);
          if (!analysis.error) {
            logInfo(`Detected organization: ${analysis.organizationMethod} (${(analysis.confidence * 100).toFixed(0)}% confidence)`);
          }
        } catch (error) {
          recordTest('Analyze discovered vault', false, error.message);
        }
      }
    }

  } catch (error) {
    recordTest('Real vault discovery', false, error.message);
  }
}

/**
 * Main test runner
 */
async function runTests() {
  log(`${COLORS.bright}${COLORS.magenta}
╔═══════════════════════════════════════════════════════════╗
║  BMAD 2nd Brain - Vault Discovery Integration Tests      ║
╚═══════════════════════════════════════════════════════════╝
${COLORS.reset}`);

  logInfo(`Platform: ${os.platform()}`);
  logInfo(`Node.js: ${process.version}`);
  logInfo(`Test started: ${new Date().toISOString()}\n`);

  // Run all test suites
  await testObsidianConfigPathDetection();
  await testPathValidation();
  await testVaultAccessibility();
  await testValidVaultDetection();
  await testOrganizationMethodDetection();
  await testKeyLocationDetection();
  await testStructureValidation();
  await testConfigurationGeneration();
  await testErrorHandling();
  await testRealVaultDiscovery();

  // Print summary
  logSection('Test Summary');

  log(`${COLORS.bright}Total Tests: ${results.passed + results.failed + results.skipped}${COLORS.reset}`);
  logSuccess(`Passed: ${results.passed}`);

  if (results.failed > 0) {
    logError(`Failed: ${results.failed}`);
  }

  if (results.skipped > 0) {
    logInfo(`Skipped: ${results.skipped}`);
  }

  const passRate = ((results.passed / (results.passed + results.failed)) * 100).toFixed(1);
  log(`${COLORS.bright}Pass Rate: ${passRate}%${COLORS.reset}\n`);

  // List failed tests
  if (results.failed > 0) {
    logSection('Failed Tests');
    for (const test of results.tests) {
      if (!test.passed && !test.skipped) {
        logError(`${test.name}: ${test.error}`);
      }
    }
  }

  // Exit with appropriate code
  const exitCode = results.failed > 0 ? 1 : 0;
  process.exit(exitCode);
}

// Run tests
runTests().catch(error => {
  logError(`Fatal error: ${error.message}`);
  console.error(error);
  process.exit(1);
});
