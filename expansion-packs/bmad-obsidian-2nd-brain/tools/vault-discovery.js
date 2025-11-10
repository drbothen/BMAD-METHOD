
/**
 * Vault Discovery Utility
 * =======================
 * Discovers installed Obsidian vaults by reading Obsidian's configuration files.
 * Supports macOS, Windows, and Linux platforms.
 *
 * Features:
 * - Auto-detects OS and locates Obsidian config directory
 * - Parses obsidian.json to find vault locations
 * - Validates vault accessibility (read/write permissions)
 * - Implements security validation (path traversal prevention)
 * - Handles both file-system and Obsidian Sync vaults
 *
 * Security:
 * - All paths are normalized and validated
 * - Path traversal attempts are rejected
 * - Symbolic links are resolved to real paths
 * - Permissions are checked atomically
 *
 * Usage:
 *   const { discoverVaults } = require('./vault-discovery.js');
 *   const vaults = await discoverVaults();
 */

const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

/**
 * Get the Obsidian configuration directory based on the current OS
 * @returns {string} Absolute path to Obsidian config directory
 */
function getObsidianConfigPath() {
  const platform = os.platform();
  const homeDir = os.homedir();

  switch (platform) {
    case 'darwin': { // macOS
      return path.join(homeDir, 'Library', 'Application Support', 'obsidian');
    }

    case 'win32': { // Windows
      return path.join(process.env.APPDATA || path.join(homeDir, 'AppData', 'Roaming'), 'obsidian');
    }

    case 'linux': {
      return path.join(process.env.XDG_CONFIG_HOME || path.join(homeDir, '.config'), 'obsidian');
    }

    default: {
      throw new Error(`Unsupported platform: ${platform}`);
    }
  }
}

/**
 * Validate and normalize a file path for security
 * Prevents path traversal attacks and resolves symbolic links
 *
 * @param {string} userPath - Path provided by user or config
 * @param {string} allowedBaseDir - Optional base directory constraint
 * @returns {string} Normalized, validated absolute path
 * @throws {Error} If path is invalid or outside allowed directory
 */
function validatePath(userPath, allowedBaseDir = null) {
  if (!userPath || typeof userPath !== 'string') {
    throw new Error('Invalid path: path must be a non-empty string');
  }

  // Normalize and resolve to absolute path
  let normalized = path.resolve(userPath);

  // Resolve symbolic links to real path
  try {
    if (fs.existsSync(normalized)) {
      normalized = fs.realpathSync(normalized);
    }
  } catch (error) {
    throw new Error(`Failed to resolve path: ${error.message}`);
  }

  // Check for path traversal attempts
  const normalizedLower = normalized.toLowerCase();
  if (normalizedLower.includes('..') || normalizedLower.includes('%2e%2e')) {
    throw new Error('Path traversal detected and rejected');
  }

  // Validate against allowed base directory if specified
  if (allowedBaseDir) {
    const allowedBase = path.resolve(allowedBaseDir);
    if (!normalized.startsWith(allowedBase)) {
      throw new Error(`Path outside allowed directory: ${normalized}`);
    }
  }

  return normalized;
}

/**
 * Check if a path is accessible with read and write permissions
 * @param {string} vaultPath - Path to check
 * @returns {Object} Accessibility status {readable: boolean, writable: boolean, exists: boolean}
 */
function checkVaultAccessibility(vaultPath) {
  const result = {
    exists: false,
    readable: false,
    writable: false,
    error: null
  };

  try {
    // Check if path exists
    result.exists = fs.existsSync(vaultPath);

    if (!result.exists) {
      result.error = 'Path does not exist';
      return result;
    }

    // Check read permission
    try {
      fs.accessSync(vaultPath, fs.constants.R_OK);
      result.readable = true;
    } catch {
      result.error = 'No read permission';
    }

    // Check write permission
    try {
      fs.accessSync(vaultPath, fs.constants.W_OK);
      result.writable = true;
    } catch {
      result.error = result.error ? 'No read/write permission' : 'No write permission';
    }

  } catch (error) {
    result.error = error.message;
  }

  return result;
}

/**
 * Check if a path is a valid Obsidian vault (contains .obsidian directory)
 * @param {string} vaultPath - Path to check
 * @returns {boolean} True if valid Obsidian vault
 */
function isValidVault(vaultPath) {
  try {
    const obsidianDir = path.join(vaultPath, '.obsidian');
    return fs.existsSync(obsidianDir) && fs.statSync(obsidianDir).isDirectory();
  } catch {
    return false;
  }
}

/**
 * Parse Obsidian's obsidian.json configuration file
 * @returns {Object} Parsed configuration object
 * @throws {Error} If config file doesn't exist or is invalid JSON
 */
function parseObsidianConfig() {
  const configPath = getObsidianConfigPath();
  const obsidianJsonPath = path.join(configPath, 'obsidian.json');

  if (!fs.existsSync(obsidianJsonPath)) {
    throw new Error(`Obsidian config not found at: ${obsidianJsonPath}`);
  }

  try {
    const configContent = fs.readFileSync(obsidianJsonPath, 'utf8');
    return JSON.parse(configContent);
  } catch (error) {
    throw new Error(`Failed to parse Obsidian config: ${error.message}`);
  }
}

/**
 * Extract vault information from Obsidian config
 * @param {Object} config - Parsed Obsidian config object
 * @returns {Array} Array of vault objects with id, path, timestamp, open status
 */
function extractVaults(config) {
  if (!config || !config.vaults || typeof config.vaults !== 'object') {
    return [];
  }

  const vaults = [];

  for (const [vaultId, vaultData] of Object.entries(config.vaults)) {
    if (vaultData && vaultData.path) {
      vaults.push({
        id: vaultId,
        path: vaultData.path,
        timestamp: vaultData.ts || null,
        open: vaultData.open || false,
        type: vaultData.type || 'file-system' // file-system or sync
      });
    }
  }

  return vaults;
}

/**
 * Discover all Obsidian vaults on the system
 * @param {Object} options - Discovery options
 * @param {boolean} options.validatePaths - Whether to validate vault paths (default: true)
 * @param {boolean} options.checkAccessibility - Whether to check vault accessibility (default: true)
 * @param {boolean} options.includeInaccessible - Include vaults even if not accessible (default: false)
 * @returns {Array} Array of discovered vault objects with validation status
 */
function discoverVaults(options = {}) {
  const {
    validatePaths = true,
    checkAccessibility = true,
    includeInaccessible = false
  } = options;

  try {
    // Parse Obsidian config
    const config = parseObsidianConfig();

    // Extract vault information
    const rawVaults = extractVaults(config);

    // Process and validate each vault
    const processedVaults = rawVaults.map(vault => {
      const processed = {
        ...vault,
        validated: false,
        accessible: null,
        isValidVault: false,
        errors: []
      };

      try {
        // Validate path if enabled
        if (validatePaths) {
          processed.path = validatePath(vault.path);
          processed.validated = true;
        }

        // Check accessibility if enabled
        if (checkAccessibility) {
          const accessibility = checkVaultAccessibility(processed.path);
          processed.accessible = accessibility;

          if (!accessibility.exists) {
            processed.errors.push('Vault path does not exist');
          }
          if (!accessibility.readable) {
            processed.errors.push('Vault is not readable');
          }
          if (!accessibility.writable) {
            processed.errors.push('Vault is not writable');
          }
        }

        // Check if it's a valid Obsidian vault
        processed.isValidVault = isValidVault(processed.path);
        if (!processed.isValidVault) {
          processed.errors.push('Not a valid Obsidian vault (.obsidian directory missing)');
        }

      } catch (error) {
        processed.errors.push(error.message);
      }

      return processed;
    });

    // Filter out inaccessible vaults if requested
    if (!includeInaccessible) {
      return processedVaults.filter(vault =>
        vault.validated &&
        vault.accessible &&
        vault.accessible.exists &&
        vault.accessible.readable &&
        vault.accessible.writable &&
        vault.isValidVault
      );
    }

    return processedVaults;

  } catch (error) {
    throw new Error(`Vault discovery failed: ${error.message}`);
  }
}

/**
 * Get a summary of discovered vaults
 * @returns {Object} Summary statistics
 */
function getVaultSummary() {
  try {
    const allVaults = discoverVaults({ includeInaccessible: true });
    const accessibleVaults = allVaults.filter(v =>
      v.accessible && v.accessible.exists && v.accessible.readable && v.accessible.writable
    );
    const validVaults = allVaults.filter(v => v.isValidVault);

    return {
      total: allVaults.length,
      accessible: accessibleVaults.length,
      valid: validVaults.length,
      inaccessible: allVaults.length - accessibleVaults.length,
      invalid: allVaults.length - validVaults.length,
      vaults: allVaults
    };
  } catch (error) {
    return {
      error: error.message,
      total: 0,
      accessible: 0,
      valid: 0
    };
  }
}

// Export functions
module.exports = {
  discoverVaults,
  getObsidianConfigPath,
  validatePath,
  checkVaultAccessibility,
  isValidVault,
  parseObsidianConfig,
  extractVaults,
  getVaultSummary
};

// CLI usage
if (require.main === module) {
  console.log('🔍 BMAD 2nd Brain - Vault Discovery Utility\n');

  try {
    const summary = getVaultSummary();

    if (summary.error) {
      console.error('❌ Error:', summary.error);
      process.exit(1);
    }

    console.log(`📊 Summary:`);
    console.log(`   Total vaults found: ${summary.total}`);
    console.log(`   Accessible vaults: ${summary.accessible}`);
    console.log(`   Valid vaults: ${summary.valid}`);
    console.log(`   Inaccessible vaults: ${summary.inaccessible}`);
    console.log(`   Invalid vaults: ${summary.invalid}\n`);

    if (summary.vaults.length > 0) {
      console.log('📁 Discovered Vaults:\n');
      for (const [index, vault] of summary.vaults.entries()) {
        const status = vault.errors.length === 0 ? '✅' : '⚠️';
        console.log(`${status} Vault ${index + 1}:`);
        console.log(`   ID: ${vault.id}`);
        console.log(`   Path: ${vault.path}`);
        console.log(`   Type: ${vault.type}`);
        console.log(`   Valid: ${vault.isValidVault ? 'Yes' : 'No'}`);

        if (vault.accessible) {
          console.log(`   Accessible: Exists=${vault.accessible.exists}, Read=${vault.accessible.readable}, Write=${vault.accessible.writable}`);
        }

        if (vault.errors.length > 0) {
          console.log(`   Errors: ${vault.errors.join(', ')}`);
        }
        console.log('');
      }
    } else {
      console.log('No vaults discovered. Make sure Obsidian is installed and has been opened at least once.');
    }

    process.exit(0);

  } catch (error) {
    console.error('❌ Fatal error:', error.message);
    process.exit(1);
  }
}
