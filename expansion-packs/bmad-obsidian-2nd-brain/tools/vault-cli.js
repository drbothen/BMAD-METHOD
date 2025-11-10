
/**
 * Vault Management CLI
 * ====================
 * Command-line interface for managing Obsidian vault configurations.
 *
 * Commands:
 * - configure               Interactive setup wizard
 * - detect-vaults           Discover Obsidian vaults
 * - vault:add <path>        Add a vault to configuration
 * - vault:remove <id>       Remove a vault from configuration
 * - vault:list              List all configured vaults
 * - vault:enable <id>       Enable a vault
 * - vault:disable <id>      Disable a vault
 * - set-organization <id> <method>  Set organization method for vault
 *
 * Usage:
 *   node vault-cli.js <command> [options]
 */

const fs = require('node:fs');
const path = require('node:path');
const yaml = require('js-yaml');
const inquirer = require('inquirer');
const chalk = require('chalk');

const vaultDiscovery = require('./vault-discovery.js');
const vaultAnalyzer = require('./vault-analyzer.js');

// Configuration file path
const CONFIG_PATH = path.join(__dirname, '../config/vault-mappings.yaml');

/**
 * Load vault configuration from YAML file
 * @returns {Object} Configuration object
 */
function loadConfig() {
  try {
    if (!fs.existsSync(CONFIG_PATH)) {
      return {
        vaults: [],
        globalDefaults: {
          autoProcessing: { enabled: false, schedule: 'manual', time: '09:00' },
          excludedFolders: ['.trash', '.obsidian', '.git'],
          agentsEnabled: [
            'inbox-triage-agent',
            'atomic-note-creator',
            'semantic-linker',
            'query-interpreter',
            'quality-auditor'
          ]
        },
        metadata: {
          version: '1.0.0',
          lastUpdated: new Date().toISOString().split('T')[0],
          configSchemaVersion: '1.0'
        }
      };
    }

    const content = fs.readFileSync(CONFIG_PATH, 'utf8');
    return yaml.load(content);
  } catch (error) {
    console.error(chalk.red(`Error loading config: ${error.message}`));
    process.exit(1);
  }
}

/**
 * Save vault configuration to YAML file
 * @param {Object} config - Configuration object
 */
function saveConfig(config) {
  try {
    // Update metadata
    config.metadata = config.metadata || {};
    config.metadata.lastUpdated = new Date().toISOString().split('T')[0];

    const yamlContent = yaml.dump(config, {
      indent: 2,
      lineWidth: 120,
      noRefs: true
    });

    fs.writeFileSync(CONFIG_PATH, yamlContent, 'utf8');
    console.log(chalk.green('✓ Configuration saved'));
  } catch (error) {
    console.error(chalk.red(`Error saving config: ${error.message}`));
    process.exit(1);
  }
}

/**
 * Find vault by ID in configuration
 * @param {Object} config - Configuration object
 * @param {string} vaultId - Vault ID to find
 * @returns {Object|null} Vault object or null
 */
function findVault(config, vaultId) {
  return config.vaults.find(v => v.id === vaultId);
}

/**
 * Generate unique vault ID
 * @param {Object} config - Configuration object
 * @returns {string} Unique vault ID
 */
function generateVaultId(config) {
  const timestamp = Date.now();
  let counter = 1;
  let id = `vault-${timestamp}`;

  while (findVault(config, id)) {
    id = `vault-${timestamp}-${counter}`;
    counter++;
  }

  return id;
}

/**
 * Command: configure
 * Interactive setup wizard
 */
async function commandConfigure() {
  console.log(chalk.cyan.bold('\n╔═══════════════════════════════════════╗'));
  console.log(chalk.cyan.bold('║  BMAD 2nd Brain - Configuration Wizard  ║'));
  console.log(chalk.cyan.bold('╚═══════════════════════════════════════╝\n'));

  const config = loadConfig();

  // Step 1: Detect vaults
  console.log(chalk.yellow('📡 Detecting Obsidian vaults...\n'));

  let discoveredVaults = [];
  try {
    discoveredVaults = vaultDiscovery.discoverVaults();
    console.log(chalk.green(`✓ Found ${discoveredVaults.length} accessible vault(s)\n`));
  } catch (error) {
    console.log(chalk.yellow(`⚠ Could not auto-detect vaults: ${error.message}`));
    console.log(chalk.yellow('You can add vaults manually.\n'));
  }

  // Step 2: Select vaults to configure
  if (discoveredVaults.length > 0) {
    const vaultChoices = discoveredVaults.map(v => ({
      name: `${v.path} (ID: ${v.id})`,
      value: v,
      checked: true
    }));

    const { selectedVaults } = await inquirer.prompt([
      {
        type: 'checkbox',
        name: 'selectedVaults',
        message: 'Select vaults to configure:',
        choices: vaultChoices
      }
    ]);

    // Step 3: Analyze and configure each vault
    for (const vault of selectedVaults) {
      console.log(chalk.cyan(`\n━━━ Configuring: ${vault.path} ━━━\n`));

      // Analyze vault structure
      const analysis = vaultAnalyzer.analyzeVault(vault.path);

      console.log(chalk.blue(`Detected: ${analysis.organizationMethod} (${Math.round(analysis.confidence * 100)}% confidence)`));

      // Ask user to confirm or override
      const { confirmOrg } = await inquirer.prompt([
        {
          type: 'confirm',
          name: 'confirmOrg',
          message: `Use detected organization method "${analysis.organizationMethod}"?`,
          default: analysis.confidence > 0.7
        }
      ]);

      let orgMethod = analysis.organizationMethod;

      if (!confirmOrg) {
        const { manualOrg } = await inquirer.prompt([
          {
            type: 'list',
            name: 'manualOrg',
            message: 'Select organization method:',
            choices: ['para', 'zettelkasten', 'lyt', 'johnny-decimal', 'custom']
          }
        ]);
        orgMethod = manualOrg;
      }

      // Configure agents
      const { selectedAgents } = await inquirer.prompt([
        {
          type: 'checkbox',
          name: 'selectedAgents',
          message: 'Select agents to enable:',
          choices: [
            { name: 'Inbox Triage Agent', value: 'inbox-triage-agent', checked: true },
            { name: 'Atomic Note Creator', value: 'atomic-note-creator', checked: true },
            { name: 'Semantic Linker', value: 'semantic-linker', checked: true },
            { name: 'Query Interpreter', value: 'query-interpreter', checked: true },
            { name: 'Quality Auditor', value: 'quality-auditor', checked: true }
          ]
        }
      ]);

      // Configure auto-processing
      const { enableAutoProcessing } = await inquirer.prompt([
        {
          type: 'confirm',
          name: 'enableAutoProcessing',
          message: 'Enable auto-processing?',
          default: false
        }
      ]);

      let schedule = 'manual';
      let time = '09:00';

      if (enableAutoProcessing) {
        const scheduleAnswers = await inquirer.prompt([
          {
            type: 'list',
            name: 'schedule',
            message: 'Select schedule:',
            choices: ['daily', 'weekly', 'manual']
          },
          {
            type: 'input',
            name: 'time',
            message: 'Enter time (HH:MM):',
            default: '09:00',
            validate: input => /^\d{2}:\d{2}$/.test(input) || 'Please enter time in HH:MM format'
          }
        ]);
        schedule = scheduleAnswers.schedule;
        time = scheduleAnswers.time;
      }

      // Create vault configuration
      const vaultConfig = {
        id: generateVaultId(config),
        name: path.basename(vault.path),
        path: vault.path,
        enabled: true,
        organizationMethod: orgMethod,
        keyLocations: analysis.keyLocations || {},
        agentsEnabled: selectedAgents,
        autoProcessing: {
          enabled: enableAutoProcessing,
          schedule,
          time
        },
        excludedFolders: ['.trash', '.obsidian']
      };

      // Add to config
      config.vaults.push(vaultConfig);

      console.log(chalk.green(`✓ Vault configured: ${vaultConfig.id}`));
    }
  } else {
    console.log(chalk.yellow('No vaults detected. Use "vault:add <path>" to add vaults manually.'));
  }

  // Save configuration
  if (config.vaults.length > 0) {
    saveConfig(config);
    console.log(chalk.green.bold('\n✓ Configuration complete!'));
    console.log(chalk.blue(`\nConfigured ${config.vaults.length} vault(s)`));
  } else {
    console.log(chalk.yellow('\nNo vaults configured.'));
  }
}

/**
 * Command: detect-vaults
 * Discover Obsidian vaults
 */
function commandDetectVaults() {
  console.log(chalk.cyan.bold('\n📡 Detecting Obsidian Vaults...\n'));

  try {
    const summary = vaultDiscovery.getVaultSummary();

    console.log(chalk.blue('Summary:'));
    console.log(`  Total: ${summary.total}`);
    console.log(`  Accessible: ${summary.accessible}`);
    console.log(`  Valid: ${summary.valid}\n`);

    if (summary.vaults.length > 0) {
      console.log(chalk.cyan('Discovered Vaults:\n'));
      for (const vault of summary.vaults) {
        const status = vault.errors.length === 0 ? chalk.green('✓') : chalk.yellow('⚠');
        console.log(`${status} ${vault.path}`);
        console.log(`   ID: ${vault.id}`);
        console.log(`   Type: ${vault.type}`);
        console.log(`   Valid: ${vault.isValidVault ? 'Yes' : 'No'}`);

        if (vault.errors.length > 0) {
          console.log(chalk.yellow(`   Issues: ${vault.errors.join(', ')}`));
        }

        console.log('');
      }
    } else {
      console.log(chalk.yellow('No vaults found.'));
    }
  } catch (error) {
    console.error(chalk.red(`Error: ${error.message}`));
    process.exit(1);
  }
}

/**
 * Command: vault:add <path>
 * Add a vault to configuration
 */
async function commandVaultAdd(vaultPath) {
  if (!vaultPath) {
    console.error(chalk.red('Error: Vault path is required'));
    console.log('Usage: vault:add <path>');
    process.exit(1);
  }

  const config = loadConfig();

  // Validate path
  try {
    const validatedPath = vaultDiscovery.validatePath(vaultPath);

    // Check if vault already exists
    const existingVault = config.vaults.find(v => v.path === validatedPath);
    if (existingVault) {
      console.log(chalk.yellow(`⚠ Vault already configured: ${existingVault.id}`));
      return;
    }

    // Check if valid Obsidian vault
    if (!vaultDiscovery.isValidVault(validatedPath)) {
      console.error(chalk.red('Error: Not a valid Obsidian vault (missing .obsidian directory)'));
      process.exit(1);
    }

    // Analyze vault
    console.log(chalk.blue('Analyzing vault structure...'));
    const analysis = vaultAnalyzer.analyzeVault(validatedPath);

    // Create vault configuration
    const vaultConfig = vaultAnalyzer.generateConfigSuggestion(analysis);
    vaultConfig.id = generateVaultId(config);

    // Add to config
    config.vaults.push(vaultConfig);
    saveConfig(config);

    console.log(chalk.green(`✓ Vault added: ${vaultConfig.id}`));
    console.log(chalk.blue(`  Name: ${vaultConfig.name}`));
    console.log(chalk.blue(`  Organization: ${vaultConfig.organizationMethod}`));
    console.log(chalk.blue(`  Enabled: ${vaultConfig.enabled}`));

  } catch (error) {
    console.error(chalk.red(`Error: ${error.message}`));
    process.exit(1);
  }
}

/**
 * Command: vault:remove <id>
 * Remove a vault from configuration
 */
function commandVaultRemove(vaultId) {
  if (!vaultId) {
    console.error(chalk.red('Error: Vault ID is required'));
    console.log('Usage: vault:remove <id>');
    process.exit(1);
  }

  const config = loadConfig();
  const index = config.vaults.findIndex(v => v.id === vaultId);

  if (index === -1) {
    console.error(chalk.red(`Error: Vault not found: ${vaultId}`));
    process.exit(1);
  }

  const removed = config.vaults.splice(index, 1)[0];
  saveConfig(config);

  console.log(chalk.green(`✓ Vault removed: ${removed.id}`));
  console.log(chalk.blue(`  Name: ${removed.name}`));
  console.log(chalk.blue(`  Path: ${removed.path}`));
}

/**
 * Command: vault:list
 * List all configured vaults
 */
function commandVaultList() {
  const config = loadConfig();

  if (config.vaults.length === 0) {
    console.log(chalk.yellow('No vaults configured.'));
    return;
  }

  console.log(chalk.cyan.bold(`\n📚 Configured Vaults (${config.vaults.length})\n`));

  for (const vault of config.vaults) {
    const status = vault.enabled ? chalk.green('●') : chalk.gray('○');
    console.log(`${status} ${chalk.bold(vault.id)}`);
    console.log(`   Name: ${vault.name}`);
    console.log(`   Path: ${vault.path}`);
    console.log(`   Organization: ${vault.organizationMethod}`);
    console.log(`   Enabled: ${vault.enabled ? 'Yes' : 'No'}`);
    console.log(`   Agents: ${vault.agentsEnabled.length}`);
    console.log(`   Auto-processing: ${vault.autoProcessing.enabled ? vault.autoProcessing.schedule : 'Disabled'}`);
    console.log('');
  }
}

/**
 * Command: vault:enable <id>
 * Enable a vault
 */
function commandVaultEnable(vaultId) {
  if (!vaultId) {
    console.error(chalk.red('Error: Vault ID is required'));
    console.log('Usage: vault:enable <id>');
    process.exit(1);
  }

  const config = loadConfig();
  const vault = findVault(config, vaultId);

  if (!vault) {
    console.error(chalk.red(`Error: Vault not found: ${vaultId}`));
    process.exit(1);
  }

  vault.enabled = true;
  saveConfig(config);

  console.log(chalk.green(`✓ Vault enabled: ${vaultId}`));
}

/**
 * Command: vault:disable <id>
 * Disable a vault
 */
function commandVaultDisable(vaultId) {
  if (!vaultId) {
    console.error(chalk.red('Error: Vault ID is required'));
    console.log('Usage: vault:disable <id>');
    process.exit(1);
  }

  const config = loadConfig();
  const vault = findVault(config, vaultId);

  if (!vault) {
    console.error(chalk.red(`Error: Vault not found: ${vaultId}`));
    process.exit(1);
  }

  vault.enabled = false;
  saveConfig(config);

  console.log(chalk.green(`✓ Vault disabled: ${vaultId}`));
}

/**
 * Command: set-organization <id> <method>
 * Set organization method for a vault
 */
function commandSetOrganization(vaultId, method) {
  if (!vaultId || !method) {
    console.error(chalk.red('Error: Vault ID and organization method are required'));
    console.log('Usage: set-organization <id> <method>');
    console.log('Methods: para, zettelkasten, lyt, johnny-decimal, custom');
    process.exit(1);
  }

  const validMethods = ['para', 'zettelkasten', 'lyt', 'johnny-decimal', 'custom'];
  if (!validMethods.includes(method)) {
    console.error(chalk.red(`Error: Invalid organization method: ${method}`));
    console.log(`Valid methods: ${validMethods.join(', ')}`);
    process.exit(1);
  }

  const config = loadConfig();
  const vault = findVault(config, vaultId);

  if (!vault) {
    console.error(chalk.red(`Error: Vault not found: ${vaultId}`));
    process.exit(1);
  }

  vault.organizationMethod = method;
  saveConfig(config);

  console.log(chalk.green(`✓ Organization method updated: ${vaultId} → ${method}`));
}

/**
 * Display help
 */
function displayHelp() {
  console.log(chalk.cyan.bold('\nBMAD 2nd Brain - Vault Management CLI\n'));
  console.log('Commands:\n');
  console.log(chalk.yellow('  configure') + '                         Interactive setup wizard');
  console.log(chalk.yellow('  detect-vaults') + '                     Discover Obsidian vaults');
  console.log(chalk.yellow('  vault:add <path>') + '                  Add a vault to configuration');
  console.log(chalk.yellow('  vault:remove <id>') + '                 Remove a vault from configuration');
  console.log(chalk.yellow('  vault:list') + '                        List all configured vaults');
  console.log(chalk.yellow('  vault:enable <id>') + '                 Enable a vault');
  console.log(chalk.yellow('  vault:disable <id>') + '                Disable a vault');
  console.log(chalk.yellow('  set-organization <id> <method>') + '    Set organization method for vault');
  console.log('');
  console.log('Examples:');
  console.log(chalk.gray('  node vault-cli.js configure'));
  console.log(chalk.gray('  node vault-cli.js vault:add /Users/username/Documents/MyVault'));
  console.log(chalk.gray('  node vault-cli.js vault:list'));
  console.log(chalk.gray('  node vault-cli.js set-organization vault-001 para'));
  console.log('');
}

/**
 * Main CLI entry point
 */
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === 'help' || command === '--help' || command === '-h') {
    displayHelp();
    return;
  }

  try {
    switch (command) {
      case 'configure': {
        await commandConfigure();
        break;
      }

      case 'detect-vaults': {
        commandDetectVaults();
        break;
      }

      case 'vault:add': {
        await commandVaultAdd(args[1]);
        break;
      }

      case 'vault:remove': {
        commandVaultRemove(args[1]);
        break;
      }

      case 'vault:list': {
        commandVaultList();
        break;
      }

      case 'vault:enable': {
        commandVaultEnable(args[1]);
        break;
      }

      case 'vault:disable': {
        commandVaultDisable(args[1]);
        break;
      }

      case 'set-organization': {
        commandSetOrganization(args[1], args[2]);
        break;
      }

      default: {
        console.error(chalk.red(`Unknown command: ${command}`));
        displayHelp();
        process.exit(1);
      }
    }
  } catch (error) {
    console.error(chalk.red(`\nError: ${error.message}`));
    if (process.env.DEBUG) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}

// Run CLI if executed directly
if (require.main === module) {
  main().catch(error => {
    console.error(chalk.red(`Fatal error: ${error.message}`));
    process.exit(1);
  });
}

module.exports = {
  loadConfig,
  saveConfig,
  findVault,
  generateVaultId
};
