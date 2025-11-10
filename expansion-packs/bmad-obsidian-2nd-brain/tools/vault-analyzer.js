
/**
 * Vault Analyzer Utility
 * ======================
 * Analyzes Obsidian vault folder structure to detect organization method
 * and automatically identify key folder locations.
 *
 * Features:
 * - Detects organization method (PARA, Zettelkasten, LYT, Johnny Decimal, Custom)
 * - Identifies key folder locations (inbox, projects, areas, resources, etc.)
 * - Provides confidence scores for detected organization method
 * - Validates detected structure
 * - Supports manual override of detection
 *
 * Detection Logic:
 * - PARA: Looks for "Projects", "Areas", "Resources", "Archive" folders
 * - Zettelkasten: Flat structure, "Fleeting", "Permanent", "Literature" notes
 * - LYT: Heavy MOC usage, "MOCs" folder, extensive linking
 * - Johnny Decimal: Numerical folder names (10-19, 20-29, etc.)
 * - Custom: User-defined structure that doesn't match patterns
 *
 * Usage:
 *   const { analyzeVault } = require('./vault-analyzer.js');
 *   const analysis = analyzeVault('/path/to/vault');
 */

const fs = require('node:fs');
const path = require('node:path');

/**
 * Organization method detection patterns
 * Each pattern includes keywords and structural indicators
 */
const ORGANIZATION_PATTERNS = {
  para: {
    name: 'PARA',
    description: 'Projects, Areas, Resources, Archives',
    keywords: [
      'projects', 'project',
      'areas', 'area',
      'resources', 'resource',
      'archives', 'archive'
    ],
    folderPatterns: [
      /^\d+\s*[-–—]?\s*projects?/i,
      /^\d+\s*[-–—]?\s*areas?/i,
      /^\d+\s*[-–—]?\s*resources?/i,
      /^\d+\s*[-–—]?\s*archives?/i,
      /^projects?$/i,
      /^areas?$/i,
      /^resources?$/i,
      /^archives?$/i
    ],
    requiredMatches: 3, // Need at least 3 of 4 categories
    confidence: 0.8
  },

  zettelkasten: {
    name: 'Zettelkasten',
    description: 'Flat structure with atomic notes and heavy linking',
    keywords: [
      'fleeting', 'permanent', 'literature',
      'slip', 'notes', 'zettel', 'atomic',
      'reference', 'bibliography'
    ],
    folderPatterns: [
      /^fleeting/i,
      /^permanent/i,
      /^literature/i,
      /^reference/i,
      /^\d{12,14}/  // Timestamp-based IDs (e.g., 202501091430)
    ],
    structureIndicators: {
      flatStructure: true,  // Minimal hierarchy
      maxDepth: 2           // Typically very shallow
    },
    requiredMatches: 2,
    confidence: 0.75
  },

  lyt: {
    name: 'LYT',
    description: 'Linking Your Thinking - MOC-centric organization',
    keywords: [
      'moc', 'mocs', 'map of content',
      'home', 'index', 'atlas',
      'sources', 'thinking'
    ],
    folderPatterns: [
      /^mocs?$/i,
      /^maps?$/i,
      /^atlas/i,
      /^home/i,
      /^\d+\s*[-–—]?\s*mocs?/i
    ],
    requiredMatches: 1,
    confidence: 0.7
  },

  johnnyDecimal: {
    name: 'Johnny Decimal',
    description: 'Strict numerical categorization (10-19, 20-29, etc.)',
    keywords: [],
    folderPatterns: [
      /^\d{2}-\d{2}/,        // Format: 10-19, 20-29
      /^\d{2}\s+/,           // Format: 10 Projects
      /^\d{2}\.\d{2}/        // Format: 10.01
    ],
    structureIndicators: {
      numericalNaming: true,
      strictHierarchy: true
    },
    requiredMatches: 3,
    confidence: 0.85
  },

  custom: {
    name: 'Custom',
    description: 'User-defined structure',
    keywords: [],
    folderPatterns: [],
    requiredMatches: 0,
    confidence: 0.3  // Fallback option
  }
};

/**
 * Common folder purpose mappings
 * Used to identify key folder locations
 */
const FOLDER_PURPOSE_KEYWORDS = {
  inbox: ['inbox', 'capture', 'fleeting', 'quick', 'unsorted', 'new'],
  projects: ['projects', 'active', 'current', 'doing'],
  areas: ['areas', 'responsibilities', 'ongoing', 'roles'],
  resources: ['resources', 'reference', 'library', 'knowledge', 'wiki'],
  archive: ['archive', 'old', 'inactive', 'completed', 'done'],
  atomicNotes: ['atomic', 'permanent', 'zettel', 'notes', 'thinking'],
  mocs: ['mocs', 'maps', 'index', 'structure', 'atlas', 'home'],
  templates: ['templates', 'meta', 'system'],
  agentOutput: ['ai', 'generated', 'agent', 'output', 'automated']
};

/**
 * Get all folders in a directory (non-recursive)
 * @param {string} dirPath - Directory path to scan
 * @param {number} maxDepth - Maximum depth to scan (default: 3)
 * @returns {Array} Array of folder objects with name and path
 */
function getFolders(dirPath, maxDepth = 3, currentDepth = 0) {
  const folders = [];

  try {
    if (!fs.existsSync(dirPath)) {
      return folders;
    }

    const entries = fs.readdirSync(dirPath, { withFileTypes: true });

    for (const entry of entries) {
      // Skip hidden folders and Obsidian system folders
      if (entry.name.startsWith('.') || entry.name === 'node_modules') {
        continue;
      }

      if (entry.isDirectory()) {
        const folderPath = path.join(dirPath, entry.name);
        folders.push({
          name: entry.name,
          path: folderPath,
          depth: currentDepth
        });

        // Recursively get subfolders up to maxDepth
        if (currentDepth < maxDepth) {
          const subfolders = getFolders(folderPath, maxDepth, currentDepth + 1);
          folders.push(...subfolders);
        }
      }
    }

  } catch {
    // Silently skip inaccessible directories
  }

  return folders;
}

/**
 * Calculate structure depth (max folder nesting level)
 * @param {Array} folders - Array of folder objects
 * @returns {number} Maximum depth found
 */
function calculateStructureDepth(folders) {
  return folders.reduce((max, folder) => Math.max(max, folder.depth), 0);
}

/**
 * Check if folder name matches any pattern in array
 * @param {string} folderName - Folder name to check
 * @param {Array} patterns - Array of regex patterns
 * @returns {boolean} True if matches any pattern
 */
function matchesPattern(folderName, patterns) {
  return patterns.some(pattern => pattern.test(folderName));
}

/**
 * Detect organization method based on folder structure
 * @param {Array} folders - Array of folder objects
 * @returns {Object} Detection results with method, confidence, and matches
 */
function detectOrganizationMethod(folders) {
  const results = {};
  const folderNames = folders.map(f => f.name);
  const depth = calculateStructureDepth(folders);

  // Test each organization method
  for (const [methodKey, pattern] of Object.entries(ORGANIZATION_PATTERNS)) {
    let matches = 0;
    const matchedFolders = [];

    // Check folder patterns
    for (const folderName of folderNames) {
      // Check keywords
      const keywordMatches = pattern.keywords.filter(keyword =>
        folderName.toLowerCase().includes(keyword.toLowerCase())
      );

      // Check regex patterns
      const patternMatches = pattern.folderPatterns.filter(regex =>
        regex.test(folderName)
      );

      if (keywordMatches.length > 0 || patternMatches.length > 0) {
        matches++;
        matchedFolders.push({
          folder: folderName,
          keywords: keywordMatches,
          patterns: patternMatches.map(p => p.source)
        });
      }
    }

    // Check structure indicators
    let structureScore = 0;
    if (pattern.structureIndicators) {
      if (pattern.structureIndicators.flatStructure && depth <= 2) {
        structureScore += 0.2;
      }
      if (pattern.structureIndicators.numericalNaming) {
        const numericalCount = folderNames.filter(name => /^\d{2}/.test(name)).length;
        structureScore += (numericalCount / folderNames.length) * 0.3;
      }
    }

    // Calculate confidence score
    const baseConfidence = pattern.confidence || 0.5;
    const matchRatio = matches / (pattern.requiredMatches || 1);
    const confidence = Math.min(1, (baseConfidence * matchRatio) + structureScore);

    results[methodKey] = {
      method: pattern.name,
      description: pattern.description,
      matches,
      requiredMatches: pattern.requiredMatches,
      matchedFolders,
      confidence: matches >= pattern.requiredMatches ? confidence : confidence * 0.5,
      detected: matches >= pattern.requiredMatches
    };
  }

  // Find best match (highest confidence)
  const bestMatch = Object.entries(results).reduce((best, [key, result]) => {
    return result.confidence > (best.confidence || 0) ? { key, ...result } : best;
  }, {});

  return {
    detected: bestMatch.key,
    confidence: bestMatch.confidence,
    method: bestMatch.method,
    description: bestMatch.description,
    allResults: results,
    structureDepth: depth
  };
}

/**
 * Detect key folder locations based on folder names
 * @param {Array} folders - Array of folder objects
 * @returns {Object} Detected key locations mapping
 */
function detectKeyLocations(folders) {
  const keyLocations = {};

  for (const [purpose, keywords] of Object.entries(FOLDER_PURPOSE_KEYWORDS)) {
    // Find folders matching this purpose
    const candidates = folders.filter(folder => {
      const folderNameLower = folder.name.toLowerCase();
      return keywords.some(keyword => folderNameLower.includes(keyword));
    });

    // Prefer top-level folders (depth 0) over nested ones
    candidates.sort((a, b) => {
      if (a.depth !== b.depth) return a.depth - b.depth;
      return a.name.localeCompare(b.name);
    });

    if (candidates.length > 0) {
      // Use folder name (relative to vault root)
      const bestMatch = candidates[0];
      keyLocations[purpose] = bestMatch.name;
    }
  }

  return keyLocations;
}

/**
 * Validate detected structure
 * @param {Object} detection - Detection results
 * @param {Object} keyLocations - Detected key locations
 * @returns {Object} Validation results with warnings and suggestions
 */
function validateStructure(detection, keyLocations) {
  const warnings = [];
  const suggestions = [];

  // Check confidence
  if (detection.confidence < 0.5) {
    warnings.push(`Low confidence in detected organization method (${(detection.confidence * 100).toFixed(0)}%)`);
    suggestions.push('Consider manually specifying the organization method');
  }

  // Check for missing key folders
  const requiredFolders = ['inbox'];
  const missingFolders = requiredFolders.filter(folder => !keyLocations[folder]);

  if (missingFolders.length > 0) {
    warnings.push(`Missing recommended folders: ${missingFolders.join(', ')}`);
    suggestions.push('Consider creating an inbox folder for new notes');
  }

  // Check structure depth
  if (detection.structureDepth > 5) {
    warnings.push('Deep folder structure detected (may complicate navigation)');
    suggestions.push('Consider flattening the structure for better note accessibility');
  }

  return {
    isValid: warnings.length === 0,
    warnings,
    suggestions
  };
}

/**
 * Analyze vault folder structure
 * @param {string} vaultPath - Absolute path to vault
 * @param {Object} options - Analysis options
 * @returns {Object} Complete analysis results
 */
function analyzeVault(vaultPath, options = {}) {
  const {
    maxDepth = 3,
    includeValidation = true
  } = options;

  try {
    // Validate vault path
    if (!fs.existsSync(vaultPath)) {
      throw new Error(`Vault path does not exist: ${vaultPath}`);
    }

    const obsidianDir = path.join(vaultPath, '.obsidian');
    if (!fs.existsSync(obsidianDir)) {
      throw new Error(`Not a valid Obsidian vault (missing .obsidian directory): ${vaultPath}`);
    }

    // Get folder structure
    const folders = getFolders(vaultPath, maxDepth);

    // Detect organization method
    const detection = detectOrganizationMethod(folders);

    // Detect key folder locations
    const keyLocations = detectKeyLocations(folders);

    // Validate structure if enabled
    const validation = includeValidation
      ? validateStructure(detection, keyLocations)
      : null;

    return {
      vaultPath,
      organizationMethod: detection.detected,
      confidence: detection.confidence,
      methodDescription: detection.description,
      structureDepth: detection.structureDepth,
      totalFolders: folders.length,
      keyLocations,
      validation,
      detectionDetails: detection.allResults,
      folders: folders.map(f => ({ name: f.name, depth: f.depth }))
    };

  } catch (error) {
    return {
      vaultPath,
      error: error.message,
      success: false
    };
  }
}

/**
 * Generate configuration suggestion based on analysis
 * @param {Object} analysis - Analysis results
 * @returns {Object} Suggested vault configuration
 */
function generateConfigSuggestion(analysis) {
  if (analysis.error) {
    return null;
  }

  const config = {
    id: `vault-${Date.now()}`,
    name: path.basename(analysis.vaultPath),
    path: analysis.vaultPath,
    enabled: true,
    organizationMethod: analysis.organizationMethod,
    keyLocations: analysis.keyLocations,
    agentsEnabled: [
      'inbox-triage-agent',
      'atomic-note-creator',
      'semantic-linker',
      'query-interpreter',
      'quality-auditor'
    ],
    autoProcessing: {
      enabled: false,
      schedule: 'daily',
      time: '09:00'
    },
    excludedFolders: [
      '.trash',
      '.obsidian',
      'Templates',
      'Archive'
    ]
  };

  // Add confidence note
  config._detectionConfidence = `${(analysis.confidence * 100).toFixed(0)}%`;
  config._manualReviewNeeded = analysis.confidence < 0.7;

  return config;
}

// Export functions
module.exports = {
  analyzeVault,
  detectOrganizationMethod,
  detectKeyLocations,
  validateStructure,
  getFolders,
  generateConfigSuggestion,
  ORGANIZATION_PATTERNS,
  FOLDER_PURPOSE_KEYWORDS
};

// CLI usage
if (require.main === module) {
  const vaultPath = process.argv[2];

  if (!vaultPath) {
    console.error('Usage: node vault-analyzer.js <vault-path>');
    process.exit(1);
  }

  console.log('🔬 BMAD 2nd Brain - Vault Analyzer\n');
  console.log(`Analyzing vault: ${vaultPath}\n`);

  const analysis = analyzeVault(vaultPath);

  if (analysis.error) {
    console.error('❌ Error:', analysis.error);
    process.exit(1);
  }

  console.log('📊 Analysis Results:\n');
  console.log(`Organization Method: ${analysis.organizationMethod} (${(analysis.confidence * 100).toFixed(0)}% confidence)`);
  console.log(`Description: ${analysis.methodDescription}`);
  console.log(`Structure Depth: ${analysis.structureDepth} levels`);
  console.log(`Total Folders: ${analysis.totalFolders}\n`);

  console.log('📁 Detected Key Locations:');
  if (Object.keys(analysis.keyLocations).length > 0) {
    for (const [purpose, folder] of Object.entries(analysis.keyLocations)) {
      console.log(`   ${purpose}: ${folder}`);
    }
  } else {
    console.log('   None detected');
  }
  console.log('');

  if (analysis.validation) {
    console.log('✓ Validation:');
    console.log(`   Valid: ${analysis.validation.isValid ? 'Yes' : 'No'}`);

    if (analysis.validation.warnings.length > 0) {
      console.log('   Warnings:');
      for (const w of analysis.validation.warnings) console.log(`     - ${w}`);
    }

    if (analysis.validation.suggestions.length > 0) {
      console.log('   Suggestions:');
      for (const s of analysis.validation.suggestions) console.log(`     - ${s}`);
    }
    console.log('');
  }

  console.log('💡 Suggested Configuration:');
  const suggestion = generateConfigSuggestion(analysis);
  console.log(JSON.stringify(suggestion, null, 2));

  process.exit(0);
}
