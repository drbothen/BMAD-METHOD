/**
 * Convert BMAD Technical Writing Task YAML Frontmatter
 *
 * Converts string-based inputs/steps fields to proper YAML arrays
 * for better machine-readability and consistency.
 */

const fs = require('node:fs');
const path = require('node:path');

function convertTaskYAML(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  let modified = false;

  // Pattern: inputs: - item1 - item2 - item3
  // Convert to proper YAML array
  const inputsMatch = content.match(/^inputs: - (.+)$/m);
  if (inputsMatch) {
    const itemsString = inputsMatch[1];
    const items = itemsString.split(' - ').map((item) => item.trim());
    const yamlArray = items.map((item) => `  - ${item}`).join('\n');
    content = content.replace(/^inputs: - .+$/m, `inputs:\n${yamlArray}`);
    modified = true;
  }

  // Pattern: steps: - step1 - step2 - step3
  // Convert to proper YAML array
  const stepsMatch = content.match(/^steps: - (.+)$/m);
  if (stepsMatch) {
    const itemsString = stepsMatch[1];
    const items = itemsString.split(' - ').map((item) => item.trim());
    const yamlArray = items.map((item) => `  - ${item}`).join('\n');
    content = content.replace(/^steps: - .+$/m, `steps:\n${yamlArray}`);
    modified = true;
  }

  if (modified) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✓ Converted: ${path.basename(filePath)}`);
    return true;
  } else {
    console.log(`  Skipped: ${path.basename(filePath)} (no conversion needed)`);
    return false;
  }
}

// Main execution
const tasksDir = path.join(__dirname, '../expansion-packs/bmad-technical-writing/tasks');
const files = fs.readdirSync(tasksDir).filter((f) => f.endsWith('.md'));

console.log(`\nConverting YAML frontmatter in ${files.length} task files...\n`);

let convertedCount = 0;
for (const file of files) {
  const filePath = path.join(tasksDir, file);
  if (convertTaskYAML(filePath)) {
    convertedCount++;
  }
}

console.log(`\n✓ Conversion complete: ${convertedCount} files modified\n`);
