#!/bin/bash
#
# format-for-packtpub.sh
#
# Complete PacktPub manuscript formatting workflow:
# 1. Pre-conversion validation (validate-manuscript.py)
# 2. Pandoc conversion (Markdown → Word with PACKT template)
# 3. Python style application (apply-packt-styles-v6.py)
# 4. Post-conversion verification (verify-packt-document.py)
#
# Usage:
#   ./format-for-packtpub.sh manuscript.md [output-directory]
#
# Requirements:
#   - Pandoc (pandoc --version)
#   - Python 3 with python-docx (pip3 install python-docx)
#   - Optional: Pillow for image validation (pip3 install Pillow)
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory (where this script and other tools are located)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Default paths
AUTHOR_BUNDLE_DIR="$SCRIPT_DIR"
SAMPLE_CHAPTER="$AUTHOR_BUNDLE_DIR/Sample Chapter.docx"
VALIDATE_SCRIPT="$AUTHOR_BUNDLE_DIR/validate-manuscript.py"
APPLY_STYLES_SCRIPT="$AUTHOR_BUNDLE_DIR/apply-packt-styles-v6.py"
VERIFY_SCRIPT="$AUTHOR_BUNDLE_DIR/verify-packt-document.py"

# Functions
print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

check_requirements() {
    print_header "Checking Requirements"

    # Check Pandoc
    if ! command -v pandoc &> /dev/null; then
        print_error "Pandoc not installed"
        echo "Install: brew install pandoc (macOS) or see https://pandoc.org/installing.html"
        exit 1
    fi
    print_success "Pandoc found: $(pandoc --version | head -1)"

    # Check Python 3
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 not installed"
        exit 1
    fi
    print_success "Python 3 found: $(python3 --version)"

    # Check python-docx
    if ! python3 -c "import docx" 2> /dev/null; then
        print_error "python-docx not installed"
        echo "Install: pip3 install python-docx"
        exit 1
    fi
    print_success "python-docx installed"

    # Check Pillow (optional)
    if ! python3 -c "import PIL" 2> /dev/null; then
        print_warning "Pillow not installed - image validation will be skipped"
        echo "Install: pip3 install Pillow"
    else
        print_success "Pillow installed"
    fi

    # Check Sample Chapter template
    if [ ! -f "$SAMPLE_CHAPTER" ]; then
        print_error "Sample Chapter.docx template not found at: $SAMPLE_CHAPTER"
        exit 1
    fi
    print_success "Sample Chapter template found"

    # Check scripts
    for script in "$VALIDATE_SCRIPT" "$APPLY_STYLES_SCRIPT" "$VERIFY_SCRIPT"; do
        if [ ! -f "$script" ]; then
            print_error "Script not found: $script"
            exit 1
        fi
        chmod +x "$script"  # Ensure executable
    done
    print_success "All scripts found"
}

validate_manuscript() {
    local manuscript=$1
    local output_dir=$2
    local report="$output_dir/pre-conversion-validation.md"

    print_header "Step 1: Pre-Conversion Validation"

    python3 "$VALIDATE_SCRIPT" "$manuscript" --report "$report"
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        print_success "Pre-conversion validation passed"
    else
        print_error "Pre-conversion validation failed"
        echo ""
        echo "Review validation report: $report"
        echo ""
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Aborted by user"
            exit 1
        fi
    fi
}

convert_with_pandoc() {
    local manuscript=$1
    local output_dir=$2
    local temp_output="$output_dir/temp-pandoc-output.docx"

    print_header "Step 2: Pandoc Conversion"

    echo "Converting: $manuscript"
    echo "Template: $SAMPLE_CHAPTER"
    echo "Output: $temp_output"
    echo ""

    pandoc "$manuscript" \
        -o "$temp_output" \
        --reference-doc="$SAMPLE_CHAPTER" \
        --standalone \
        --highlight-style=tango

    if [ $? -eq 0 ]; then
        print_success "Pandoc conversion complete"
    else
        print_error "Pandoc conversion failed"
        exit 1
    fi
}

apply_packt_styles() {
    local temp_output=$1
    local final_output=$2

    print_header "Step 3: Apply PACKT Styles"

    echo "Input: $temp_output"
    echo "Output: $final_output"
    echo ""

    python3 "$APPLY_STYLES_SCRIPT" "$temp_output" "$final_output"

    if [ $? -eq 0 ]; then
        print_success "PACKT styles applied successfully"

        # Clean up temp file
        rm "$temp_output"
        print_success "Removed temporary file"
    else
        print_error "Style application failed"
        exit 1
    fi
}

verify_document() {
    local final_output=$1
    local output_dir=$2
    local report="$output_dir/post-conversion-verification.md"

    print_header "Step 4: Post-Conversion Verification"

    python3 "$VERIFY_SCRIPT" "$final_output" --report "$report"
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        print_success "Post-conversion verification passed"
    else
        print_warning "Post-conversion verification found issues"
        echo ""
        echo "Review verification report: $report"
    fi
}

# Main script
main() {
    # Parse arguments
    if [ $# -lt 1 ]; then
        echo "Usage: $0 manuscript.md [output-directory]"
        echo ""
        echo "Complete PacktPub manuscript formatting workflow"
        echo ""
        echo "Arguments:"
        echo "  manuscript.md        Path to Markdown manuscript file"
        echo "  output-directory     Output directory (default: ./packtpub-formatted/)"
        echo ""
        echo "Example:"
        echo "  $0 chapter-05-react-hooks.md"
        echo "  $0 chapter-05-react-hooks.md ./output/"
        exit 1
    fi

    MANUSCRIPT=$1
    OUTPUT_DIR=${2:-"./packtpub-formatted"}

    # Validate inputs
    if [ ! -f "$MANUSCRIPT" ]; then
        print_error "Manuscript file not found: $MANUSCRIPT"
        exit 1
    fi

    # Create output directory
    mkdir -p "$OUTPUT_DIR"

    # Determine output filename
    BASENAME=$(basename "$MANUSCRIPT" .md)
    FINAL_OUTPUT="$OUTPUT_DIR/${BASENAME}-packtpub.docx"

    # Print workflow summary
    print_header "PacktPub Formatting Workflow"
    echo "Manuscript: $MANUSCRIPT"
    echo "Output: $FINAL_OUTPUT"
    echo "Reports: $OUTPUT_DIR/"
    echo ""

    # Check requirements
    check_requirements

    # Execute workflow
    validate_manuscript "$MANUSCRIPT" "$OUTPUT_DIR"

    convert_with_pandoc "$MANUSCRIPT" "$OUTPUT_DIR"

    apply_packt_styles "$OUTPUT_DIR/temp-pandoc-output.docx" "$FINAL_OUTPUT"

    verify_document "$FINAL_OUTPUT" "$OUTPUT_DIR"

    # Final summary
    print_header "Workflow Complete"
    echo ""
    print_success "Formatted document: $FINAL_OUTPUT"
    echo ""
    echo "Generated files:"
    echo "  • $FINAL_OUTPUT"
    echo "  • $OUTPUT_DIR/pre-conversion-validation.md"
    echo "  • $OUTPUT_DIR/post-conversion-verification.md"
    echo ""
    echo "Next steps:"
    echo "  1. Open $FINAL_OUTPUT in Microsoft Word"
    echo "  2. Review formatting and apply manual touches (info boxes, tips, warnings)"
    echo "  3. Run PacktPub submission checklist"
    echo "  4. Submit via PacktPub AuthorSight portal"
    echo ""
    print_success "Ready for PacktPub submission!"
}

# Run main
main "$@"
