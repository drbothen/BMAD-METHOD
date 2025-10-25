#!/usr/bin/env python3
"""
Validate Markdown Manuscript for PacktPub Submission

Pre-conversion validation checks:
- Code block line counts (20 ideal, 30 max)
- Image format and resolution requirements
- Structure requirements (intro, summary, etc.)

Usage:
    python3 validate-manuscript.py manuscript.md [--images-dir ./images] [--report validation-report.md]
"""

import argparse
import re
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Warning: PIL/Pillow not installed. Image validation will be skipped.")
    print("Install with: pip install Pillow")
    Image = None


class ValidationResult:
    """Stores validation results with severity levels"""

    def __init__(self):
        self.errors = []      # Critical issues (must fix)
        self.warnings = []    # Should fix
        self.info = []        # Nice to have

    def add_error(self, message):
        self.errors.append(message)

    def add_warning(self, message):
        self.warnings.append(message)

    def add_info(self, message):
        self.info.append(message)

    def has_errors(self):
        return len(self.errors) > 0

    def summary(self):
        total = len(self.errors) + len(self.warnings) + len(self.info)
        if len(self.errors) > 0:
            return f"🔴 FAIL - {len(self.errors)} critical issues"
        elif len(self.warnings) > 0:
            return f"🟡 WARNINGS - {len(self.warnings)} warnings"
        else:
            return f"✅ PASS - All checks passed"


def validate_code_blocks(content):
    """Validate code block line counts"""
    results = ValidationResult()

    # Find all code blocks
    code_blocks = re.findall(r'```[\s\S]*?```', content)

    for i, block in enumerate(code_blocks, 1):
        # Count lines (subtract 2 for fence lines)
        lines = block.count('\n') - 2

        if lines > 30:
            results.add_error(f"Code block #{i}: {lines} lines (MAX: 30)")
        elif lines > 20:
            results.add_warning(f"Code block #{i}: {lines} lines (IDEAL: ≤20)")
        elif lines == 0:
            results.add_info(f"Code block #{i}: Empty code block")

    results.add_info(f"Total code blocks: {len(code_blocks)}")

    return results


def validate_images(content, base_path, images_dir):
    """Validate image references and specifications"""
    results = ValidationResult()

    if not Image:
        results.add_warning("PIL/Pillow not available - image validation skipped")
        return results

    # Find all image references
    image_refs = re.findall(r'!\[.*?\]\((.*?)\)', content)

    if len(image_refs) == 0:
        results.add_info("No images found in manuscript")
        return results

    results.add_info(f"Total images referenced: {len(image_refs)}")

    for img_path in image_refs:
        # Try to find image
        full_path = None

        # Try relative to markdown file
        test_path = os.path.join(base_path, img_path)
        if os.path.exists(test_path):
            full_path = test_path

        # Try in images_dir if provided
        if not full_path and images_dir:
            test_path = os.path.join(images_dir, os.path.basename(img_path))
            if os.path.exists(test_path):
                full_path = test_path

        if not full_path:
            results.add_error(f"Image not found: {img_path}")
            continue

        # Check format
        if img_path.lower().endswith('.jpg') or img_path.lower().endswith('.jpeg'):
            results.add_error(f"JPG format not allowed (use PNG/TIFF): {img_path}")

        # Check resolution
        try:
            with Image.open(full_path) as img:
                width, height = img.size
                dpi = img.info.get('dpi', (72, 72))

                shortest_edge = min(width, height)

                if shortest_edge < 2000:
                    results.add_error(f"Image too small ({shortest_edge}px, need 2000px min): {img_path}")
                elif shortest_edge < 2200:
                    results.add_warning(f"Image close to minimum ({shortest_edge}px, target 2000px+): {img_path}")

                if dpi[0] < 300 or dpi[1] < 300:
                    results.add_error(f"Image DPI too low ({dpi[0]}x{dpi[1]}, need 300 DPI): {img_path}")

                # Check file size
                file_size = os.path.getsize(full_path)
                if file_size < 1000000:  # Less than 1MB
                    results.add_warning(f"Image file size small ({file_size // 1024}KB, recommend ≥1000KB): {img_path}")

        except Exception as e:
            results.add_error(f"Cannot read image {img_path}: {e}")

    return results


def validate_structure(content):
    """Validate chapter structure requirements"""
    results = ValidationResult()

    lines = content.split('\n')

    # Check for H1 (chapter title)
    h1_matches = [i for i, line in enumerate(lines) if line.startswith('# ')]
    if len(h1_matches) == 0:
        results.add_error("Missing chapter title (H1 heading)")
    elif len(h1_matches) > 1:
        results.add_warning(f"Multiple H1 headings found ({len(h1_matches)}). Should be one chapter title.")

    # Check for introduction before first H2
    first_h2_index = next((i for i, line in enumerate(lines) if line.startswith('## ')), None)

    if first_h2_index:
        intro_section = '\n'.join(lines[:first_h2_index])

        # Check intro length
        intro_paras = [p for p in intro_section.split('\n\n') if p.strip() and not p.startswith('#')]
        if len(intro_paras) < 1:
            results.add_error("Missing chapter introduction (should have text before first H2)")
        elif len(intro_paras) > 5:
            results.add_warning(f"Introduction very long ({len(intro_paras)} paragraphs). Keep to 1-3 paragraphs.")

        # Check for bullet list in intro
        if '- ' not in intro_section and '* ' not in intro_section:
            results.add_warning("Missing bullet list of topics in introduction")
    else:
        results.add_warning("No H2 sections found")

    # Check for summary section
    has_summary = any('summary' in line.lower() or 'conclusion' in line.lower()
                     for line in lines if line.startswith('##'))
    if not has_summary:
        results.add_error("Missing Summary or Conclusion section")

    # Check for consecutive headers
    consecutive_headers = []
    for i in range(len(lines) - 1):
        if lines[i].startswith('#') and lines[i+1].strip() and lines[i+1].startswith('#'):
            consecutive_headers.append(i + 1)

    if consecutive_headers:
        results.add_warning(f"Consecutive headers found at lines: {consecutive_headers}. Add lead-in text between headings.")

    # Check for consecutive images
    consecutive_images = []
    for i in range(len(lines) - 1):
        if lines[i].startswith('![') and lines[i+1].startswith('!['):
            consecutive_images.append(i + 1)

    if consecutive_images:
        results.add_warning(f"Consecutive images found at lines: {consecutive_images}. Add framing text between images.")

    # Check heading verb forms ("-ing" verbs)
    headings = [line for line in lines if line.startswith('##')]
    non_ing_headings = []
    for line in headings:
        # Extract heading text (remove ## and leading/trailing spaces)
        heading_text = line.lstrip('#').strip()
        # Check if first word ends in -ing
        first_word = heading_text.split()[0] if heading_text else ""
        if first_word and not first_word.endswith('ing'):
            non_ing_headings.append(heading_text[:50])

    if non_ing_headings:
        results.add_info(f"Consider using '-ing' verbs in headings: {len(non_ing_headings)} headings don't use -ing form")

    results.add_info(f"Total headings (H2+): {len(headings)}")

    return results


def validate_content_quality(content):
    """Validate content quality indicators"""
    results = ValidationResult()

    # Check for code explanation
    code_blocks = re.findall(r'```[\s\S]*?```', content)

    for i, block in enumerate(code_blocks, 1):
        # Find position of code block
        block_pos = content.find(block)

        # Check for text before code block (within 500 chars)
        before_text = content[max(0, block_pos - 500):block_pos].strip()
        if len(before_text) < 50:
            results.add_warning(f"Code block #{i}: Missing explanatory text before code")

        # Check for text after code block (within 500 chars)
        after_text = content[block_pos + len(block):min(len(content), block_pos + len(block) + 500)].strip()
        if len(after_text) < 50:
            results.add_warning(f"Code block #{i}: Missing explanatory text after code")

    # Check for image framing
    images = re.findall(r'!\[.*?\]\(.*?\)', content)

    for i, img in enumerate(images, 1):
        img_pos = content.find(img)

        # Check for text before image
        before_text = content[max(0, img_pos - 300):img_pos].strip()
        if len(before_text) < 30:
            results.add_warning(f"Image #{i}: Missing framing text before image")

        # Check for text after image
        after_text = content[img_pos + len(img):min(len(content), img_pos + len(img) + 300)].strip()
        if len(after_text) < 30:
            results.add_warning(f"Image #{i}: Missing framing text after image")

    return results


def generate_report(manuscript_path, code_results, image_results, structure_results, content_results, output_path):
    """Generate validation report"""

    all_results = [code_results, image_results, structure_results, content_results]

    total_errors = sum(len(r.errors) for r in all_results)
    total_warnings = sum(len(r.warnings) for r in all_results)
    total_info = sum(len(r.info) for r in all_results)

    # Determine overall status
    if total_errors > 0:
        overall = "🔴 FAIL"
    elif total_warnings > 0:
        overall = "🟡 WARNINGS"
    else:
        overall = "✅ PASS"

    report = f"""# PacktPub Manuscript Validation Report

**Manuscript**: {manuscript_path}
**Date**: {Path(manuscript_path).stat().st_mtime}

## Overall Status

{overall} - {total_errors} errors, {total_warnings} warnings, {total_info} info

## Summary

### Critical Issues (MUST FIX): {total_errors}
### Warnings (SHOULD FIX): {total_warnings}
### Information: {total_info}

---

## Code Block Validation

{code_results.summary()}

"""

    if code_results.errors:
        report += "\n### ❌ Errors\n"
        for error in code_results.errors:
            report += f"- {error}\n"

    if code_results.warnings:
        report += "\n### ⚠️ Warnings\n"
        for warning in code_results.warnings:
            report += f"- {warning}\n"

    if code_results.info:
        report += "\n### ℹ️ Information\n"
        for info in code_results.info:
            report += f"- {info}\n"

    report += "\n---\n\n## Image Validation\n\n"
    report += f"{image_results.summary()}\n"

    if image_results.errors:
        report += "\n### ❌ Errors\n"
        for error in image_results.errors:
            report += f"- {error}\n"

    if image_results.warnings:
        report += "\n### ⚠️ Warnings\n"
        for warning in image_results.warnings:
            report += f"- {warning}\n"

    if image_results.info:
        report += "\n### ℹ️ Information\n"
        for info in image_results.info:
            report += f"- {info}\n"

    report += "\n---\n\n## Structure Validation\n\n"
    report += f"{structure_results.summary()}\n"

    if structure_results.errors:
        report += "\n### ❌ Errors\n"
        for error in structure_results.errors:
            report += f"- {error}\n"

    if structure_results.warnings:
        report += "\n### ⚠️ Warnings\n"
        for warning in structure_results.warnings:
            report += f"- {warning}\n"

    if structure_results.info:
        report += "\n### ℹ️ Information\n"
        for info in structure_results.info:
            report += f"- {info}\n"

    report += "\n---\n\n## Content Quality\n\n"
    report += f"{content_results.summary()}\n"

    if content_results.warnings:
        report += "\n### ⚠️ Warnings\n"
        for warning in content_results.warnings:
            report += f"- {warning}\n"

    report += "\n---\n\n## Recommendations\n\n"

    if total_errors > 0:
        report += "### Required Actions (MUST FIX before conversion):\n\n"
        for results in all_results:
            for error in results.errors:
                report += f"1. {error}\n"
        report += "\n"

    if total_warnings > 0:
        report += "### Suggested Improvements (SHOULD FIX for best results):\n\n"
        for results in all_results:
            for warning in results.warnings[:5]:  # Limit to top 5
                report += f"- {warning}\n"
        if total_warnings > 5:
            report += f"\n... and {total_warnings - 5} more warnings\n"
        report += "\n"

    report += """
## Next Steps

"""

    if total_errors > 0:
        report += "1. **Fix all critical errors** listed above\n"
        report += "2. Re-run validation: `python3 validate-manuscript.py " + str(manuscript_path) + "`\n"
        report += "3. Once errors resolved, proceed with format conversion\n"
    else:
        report += "1. **Review warnings** and address as needed\n"
        report += "2. Proceed with format conversion: `./format-for-packtpub.sh " + str(manuscript_path) + "`\n"

    # Write report
    if output_path:
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"\n✓ Report saved to: {output_path}")
    else:
        print(report)

    return total_errors == 0


def main():
    parser = argparse.ArgumentParser(
        description='Validate Markdown manuscript for PacktPub submission',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 validate-manuscript.py chapter-05.md
  python3 validate-manuscript.py chapter-05.md --images-dir ./images
  python3 validate-manuscript.py chapter-05.md --report validation-report.md
        """
    )

    parser.add_argument('manuscript', help='Path to Markdown manuscript file')
    parser.add_argument('--images-dir', help='Directory containing images (if not in manuscript dir)')
    parser.add_argument('--report', help='Output validation report file (default: print to stdout)')

    args = parser.parse_args()

    # Validate inputs
    manuscript_path = Path(args.manuscript)
    if not manuscript_path.exists():
        print(f"Error: Manuscript file not found: {manuscript_path}")
        sys.exit(1)

    # Read manuscript
    with open(manuscript_path, 'r') as f:
        content = f.read()

    # Run validations
    print("PacktPub Manuscript Validation")
    print("=" * 70)
    print(f"Manuscript: {manuscript_path}")
    print()

    print("Running validations...")

    base_path = manuscript_path.parent
    images_dir = args.images_dir if args.images_dir else None

    code_results = validate_code_blocks(content)
    print(f"  Code blocks: {code_results.summary()}")

    image_results = validate_images(content, base_path, images_dir)
    print(f"  Images: {image_results.summary()}")

    structure_results = validate_structure(content)
    print(f"  Structure: {structure_results.summary()}")

    content_results = validate_content_quality(content)
    print(f"  Content: {content_results.summary()}")

    # Generate report
    success = generate_report(
        manuscript_path,
        code_results,
        image_results,
        structure_results,
        content_results,
        args.report
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
