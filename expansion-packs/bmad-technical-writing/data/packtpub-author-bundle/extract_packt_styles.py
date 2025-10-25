#!/usr/bin/env python3
"""
Extract style information from PacktPub Word templates
Option 3: Multi-tool solution for style extraction and markdown conversion
"""

from docx import Document
import json
import sys
from pathlib import Path

def extract_styles_detailed(docx_path, output_json='packt_styles.json'):
    """Extract comprehensive style information from PacktPub Word template"""
    print(f"Analyzing template: {docx_path}")

    doc = Document(docx_path)

    styles_info = {
        'metadata': {
            'template_file': str(docx_path),
            'total_styles': 0
        },
        'paragraph_styles': {},
        'character_styles': {},
        'table_styles': {},
        'numbering_styles': {},
        'packt_styles': []  # List of [PACKT] styles
    }

    for style in doc.styles:
        style_dict = {
            'name': style.name,
            'style_id': style.style_id if hasattr(style, 'style_id') else None,
            'type': str(style.type),
            'builtin': style.builtin,
            'hidden': style.hidden if hasattr(style, 'hidden') else None,
            'priority': style.priority if hasattr(style, 'priority') else None,
        }

        # Check if this is a PACKT style
        is_packt_style = '[PACKT]' in style.name
        if is_packt_style:
            styles_info['packt_styles'].append(style.name)

        # Extract paragraph formatting if available
        if hasattr(style, 'paragraph_format') and style.paragraph_format:
            pf = style.paragraph_format
            style_dict['paragraph_format'] = {
                'alignment': str(pf.alignment) if pf.alignment else None,
                'left_indent': str(pf.left_indent) if pf.left_indent else None,
                'right_indent': str(pf.right_indent) if pf.right_indent else None,
                'first_line_indent': str(pf.first_line_indent) if pf.first_line_indent else None,
                'space_before': str(pf.space_before) if pf.space_before else None,
                'space_after': str(pf.space_after) if pf.space_after else None,
                'line_spacing': pf.line_spacing if pf.line_spacing else None,
                'line_spacing_rule': str(pf.line_spacing_rule) if pf.line_spacing_rule else None,
                'keep_together': pf.keep_together if hasattr(pf, 'keep_together') else None,
                'keep_with_next': pf.keep_with_next if hasattr(pf, 'keep_with_next') else None,
                'page_break_before': pf.page_break_before if hasattr(pf, 'page_break_before') else None,
            }

        # Extract font formatting if available
        if hasattr(style, 'font') and style.font:
            font = style.font
            style_dict['font'] = {
                'name': font.name,
                'size': str(font.size) if font.size else None,
                'bold': font.bold,
                'italic': font.italic,
                'underline': str(font.underline) if font.underline else None,
                'color': str(font.color.rgb) if font.color and hasattr(font.color, 'rgb') else None,
                'all_caps': font.all_caps if hasattr(font, 'all_caps') else None,
                'small_caps': font.small_caps if hasattr(font, 'small_caps') else None,
            }

        # Categorize by type
        style_type = str(style.type)
        if 'PARAGRAPH' in style_type:
            styles_info['paragraph_styles'][style.name] = style_dict
        elif 'CHARACTER' in style_type:
            styles_info['character_styles'][style.name] = style_dict
        elif 'TABLE' in style_type:
            styles_info['table_styles'][style.name] = style_dict
        elif 'NUMBERING' in style_type or 'LIST' in style_type:
            styles_info['numbering_styles'][style.name] = style_dict

    styles_info['metadata']['total_styles'] = len(doc.styles)
    styles_info['metadata']['packt_style_count'] = len(styles_info['packt_styles'])
    styles_info['metadata']['paragraph_count'] = len(styles_info['paragraph_styles'])
    styles_info['metadata']['character_count'] = len(styles_info['character_styles'])

    # Save to JSON
    with open(output_json, 'w') as f:
        json.dump(styles_info, f, indent=2, default=str)

    print(f"\n✓ Extracted {styles_info['metadata']['total_styles']} total styles")
    print(f"✓ Found {styles_info['metadata']['packt_style_count']} [PACKT] styles")
    print(f"✓ Paragraph styles: {styles_info['metadata']['paragraph_count']}")
    print(f"✓ Character styles: {styles_info['metadata']['character_count']}")
    print(f"✓ Saved to: {output_json}\n")

    return styles_info

def create_markdown_style_mapping(styles_info, output_file='packt_markdown_mapping.json'):
    """Create a mapping from Markdown elements to PacktPub styles"""

    mapping = {
        'markdown_to_packt': {
            'h1': 'Heading 1 [PACKT]',
            'h2': 'Heading 2 [PACKT]',
            'h3': 'Heading 3 [PACKT]',
            'h4': 'Heading 4 [PACKT]',
            'paragraph': 'Normal [PACKT]',
            'code_block': 'Code [PACKT]',
            'code_inline': 'Code In Text [PACKT]',
            'bullet': 'Bullet [PACKT]',
            'numbered': 'Numbered Bullet [PACKT]',
            'quote': 'Quote [PACKT]',
            'emphasis': 'Italics [PACKT]',
            'strong': 'Key Word [PACKT]',
            'url': 'URL [PACKT]',
            'screen_text': 'Screen Text [PACKT]',
            'info_box': 'Information Box [PACKT]',
            'tip_heading': 'Tip Heading [PACKT]',
            'tip_content': 'Tip [PACKT]',
            'table_heading': 'Table Column Heading [PACKT]',
            'command_line': 'Command Line [PACKT]',
            'code_highlighted': 'Code Highlighted [PACKT]',
            'key': 'Key [PACKT]',
        },
        'available_packt_styles': styles_info.get('packt_styles', []),
        'style_categories': {
            'character_styles': list(styles_info.get('character_styles', {}).keys()),
            'paragraph_styles': list(styles_info.get('paragraph_styles', {}).keys()),
        }
    }

    with open(output_file, 'w') as f:
        json.dump(mapping, f, indent=2)

    print(f"✓ Created Markdown → PacktPub style mapping: {output_file}\n")
    return mapping

def print_packt_styles_summary(styles_info):
    """Print a human-readable summary of PACKT styles"""

    print("=" * 70)
    print("PACKTPUB TEMPLATE STYLES SUMMARY")
    print("=" * 70)

    print("\n📝 PARAGRAPH STYLES [PACKT]:")
    print("-" * 70)
    packt_para = {k: v for k, v in styles_info['paragraph_styles'].items() if '[PACKT]' in k}
    for name, info in sorted(packt_para.items()):
        font_info = info.get('font', {})
        font_name = font_info.get('name', 'N/A')
        font_size = font_info.get('size', 'N/A')
        print(f"  • {name:40} | Font: {font_name:15} {font_size}")

    print("\n✏️  CHARACTER STYLES [PACKT]:")
    print("-" * 70)
    packt_char = {k: v for k, v in styles_info['character_styles'].items() if '[PACKT]' in k}
    for name, info in sorted(packt_char.items()):
        font_info = info.get('font', {})
        font_name = font_info.get('name', 'N/A')
        bold = '**Bold**' if font_info.get('bold') else ''
        italic = '*Italic*' if font_info.get('italic') else ''
        print(f"  • {name:40} | {bold} {italic}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    # Find template files
    base_dir = Path(__file__).parent
    templates_dir = base_dir / "Templates"

    print("\nPacktPub Style Extraction Tool")
    print("=" * 70 + "\n")

    # Look for template files
    template_files = list(templates_dir.glob("*.docx")) + list(templates_dir.glob("*.dotx"))

    if not template_files:
        print("❌ No template files found in Templates/ directory")
        print("Looking for .dot or .dotx files...")
        sys.exit(1)

    print(f"Found {len(template_files)} template file(s):\n")
    for i, tf in enumerate(template_files, 1):
        print(f"  {i}. {tf.name}")

    print("\n" + "-" * 70 + "\n")

    # Process each template
    for template_file in template_files:
        try:
            output_json = base_dir / f"{template_file.stem}_styles.json"
            mapping_json = base_dir / f"{template_file.stem}_markdown_mapping.json"

            # Extract styles
            styles_info = extract_styles_detailed(template_file, output_json)

            # Create markdown mapping
            create_markdown_style_mapping(styles_info, mapping_json)

            # Print summary
            print_packt_styles_summary(styles_info)

        except Exception as e:
            print(f"❌ Error processing {template_file.name}: {e}")
            import traceback
            traceback.print_exc()

    print("\n✅ Style extraction complete!")
    print("=" * 70 + "\n")
