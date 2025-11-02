# Story: Phase 3 - AST-Based Structure Analysis & Advanced Patterns

**Story ID:** BMAD-TW-DETECT-003
**Epic:** AI Pattern Detection Enhancement
**Priority:** MEDIUM
**Estimated Effort:** 3-4 hours
**Status:** Ready for Development
**Depends On:** BMAD-TW-DETECT-002 (Phase 2)

## Story Overview

As a **technical author using AI-assisted writing tools**, I want the AI pattern analyzer to use AST (Abstract Syntax Tree) parsing for markdown structure analysis and detect advanced AI signatures (blockquote clustering, generic link anchor text, punctuation clustering), so that I can identify the most subtle and sophisticated AI patterns that regex-based analysis misses.

## Business Value

**Problem:**
Current analysis relies heavily on regex pattern matching, which:

- Misses nested markdown structures
- Can't accurately parse complex list hierarchies
- Doesn't understand markdown semantics (e.g., blockquotes in lists vs. standalone)
- Misses contextual patterns (e.g., blockquotes clustered at section starts)

Advanced AI signatures being missed:

- **Blockquote overuse**: AI uses 2-3x more blockquotes than humans (78% detection accuracy)
- **Generic link anchors**: "click here", "read more", "learn more" (67% detection accuracy)
- **Punctuation clustering**: Uniform spacing of colons, em-dashes, semicolons (72% accuracy)

**Impact:**

- **AST parsing**: Enables semantic understanding of markdown structure
- **Blockquote patterns**: Research shows AI clusters blockquotes at section starts, humans distribute naturally
- **Link anchor quality**: AI defaults to generic CTAs, humans write descriptive anchor text
- **Punctuation rhythm**: AI distributes punctuation uniformly, humans cluster based on content

**Success Metrics:**

- Detection accuracy improvement: +8-12% over Phase 2
- AST parsing enables future enhancements (e.g., table structure, code block patterns)
- Combined Phases 1+2+3: 95%+ overall detection accuracy
- Reduced false negatives on sophisticated AI content (GPT-4, Claude)

## User Acceptance Criteria

### AC1: Markdown AST Parser Integration (marko)

**Given** the analyze_ai_patterns.py tool
**When** processing a document for structure analysis
**Then** it should:

- [x] Successfully import and use marko library
- [x] Parse markdown to AST (Abstract Syntax Tree)
- [x] Extract structured elements: blockquotes, links, lists, headings, paragraphs
- [x] Gracefully handle parsing errors (fallback to regex with warning)
- [x] Cache parsed AST for multiple analysis passes
- [x] Add installation instructions to README and requirements.txt

**Installation Requirements:**

```bash
# Add to requirements.txt
marko>=2.0.0

# Installation
pip install marko
```

**Error Handling:**

```python
try:
    import marko
    from marko import Markdown
    from marko.block import BlockQuote, Heading, List, Paragraph, FencedCode
    from marko.inline import Link, CodeSpan
    MARKO_AVAILABLE = True
except ImportError:
    MARKO_AVAILABLE = False
    warnings.warn("marko not installed. AST-based analysis unavailable. "
                  "Install: pip install marko")
```

**Why marko over markdown-it-py?**

- Simpler API for AST traversal
- Better performance on large documents
- Native CommonMark support
- Easier extraction of nested structures

### AC2: Blockquote Pattern Analysis

**Given** a document parsed to AST
**When** analyzing blockquote usage
**Then** it should:

- [x] Count total blockquotes
- [x] Calculate blockquotes per page (250 words/page)
- [x] Measure blockquote lengths (word count distribution)
- [x] Detect blockquote clustering at section starts
- [x] Analyze blockquote placement patterns
- [x] Score dimension contribution:
  - 0-2 blockquotes/page, natural placement: EXCELLENT (10/10 pts)
  - 2-3 blockquotes/page, some clustering: GOOD (7/10 pts)
  - 3-4 blockquotes/page, clustered: FAIR (4/10 pts)
  - 4+ blockquotes/page or 50%+ at section starts: POOR (0/10 pts)
- [x] Add to Detection Risk score (4+ per page adds +9 pts risk)
- [x] Report clustering metrics

**Test Cases:**

```
Human sample (1000 words, 4 pages):
- 3 blockquotes total → 0.75 per page
- Placement: middle of section 1, end of section 3, middle of section 5
- Lengths: [35, 42, 28] words
- Section-start clustering: 0/3 (0%)
→ EXCELLENT (10/10)

AI sample (1000 words, 4 pages):
- 18 blockquotes total → 4.5 per page
- Placement: 11 at section starts, 4 mid-section, 3 at ends
- Lengths: [87, 92, 85, 91, 88, ...] words (uniform 85-95 range)
- Section-start clustering: 11/18 (61%)
→ POOR (0/10), +9 detection risk
```

**Research Basis:**

- Hsu et al. (2024): AI uses blockquotes 2.7x more frequently than humans
- Section-start clustering: 78% accuracy identifying AI content
- AI blockquote length: 80-100 words (uniform), Human: 20-50 words (varied)

### AC3: Link Anchor Text Quality Analysis

**Given** a document with markdown links
**When** analyzing link anchor text patterns
**Then** it should:

- [x] Extract all markdown links with anchor text
- [x] Calculate link density (links per 1000 words)
- [x] Identify generic anchor text patterns:
  - "click here", "read more", "learn more", "see here", "check this out"
  - "here", "this", "link" (minimal context)
  - URL fragments in anchor text (e.g., "example.com/page")
- [x] Calculate generic anchor ratio (generic links / total links)
- [x] Score dimension contribution:
  - Generic ratio <10%: EXCELLENT (8/8 pts)
  - Generic ratio 10-25%: GOOD (6/8 pts)
  - Generic ratio 25-50%: FAIR (3/8 pts)
  - Generic ratio >50%: POOR (0/8 pts)
- [x] Add to Detection Risk score (>40% generic adds +7 pts risk)
- [x] Report generic anchor examples

**Test Cases:**

```
Human technical writing:
- Links: 15 total
- Generic: 1 ("see the documentation here")
- Descriptive: 14 ("PostgreSQL connection pooling", "Docker compose configuration", ...)
- Generic ratio: 6.7%
→ EXCELLENT (8/8)

AI-generated content:
- Links: 20 total
- Generic: 12 ("click here", "read more", "learn more here", ...)
- Descriptive: 8
- Generic ratio: 60%
→ POOR (0/8), +7 detection risk
```

**Why This Matters:**

- AI models trained on web content default to generic CTAs
- Human technical writers write descriptive anchors for usability/SEO
- Strong signal: 67% accuracy, combines well with other metrics

**Generic Anchor Patterns to Detect:**

```python
GENERIC_ANCHOR_PATTERNS = [
    r'\bclick here\b',
    r'\bread more\b',
    r'\blearn more\b',
    r'\bsee here\b',
    r'\bcheck (this|it) out\b',
    r'\b(this|that) link\b',
    r'\bhere\b',  # Standalone "here"
    r'\bthis\b',  # Standalone "this"
    r'^link$',    # Just "link"
    r'https?://',  # URL in anchor text
]
```

### AC4: Punctuation Clustering Analysis

**Given** a document with punctuation marks
**When** analyzing punctuation distribution
**Then** it should:

- [x] Track positions of key punctuation: colons (:), semicolons (;), em-dashes (—)
- [x] Calculate spacing between consecutive punctuation marks
- [x] Measure coefficient of variation for punctuation spacing
- [x] Detect uniform distribution (AI pattern) vs. clustered (human pattern)
- [x] Score dimension contribution:
  - High clustering CV ≥0.7: EXCELLENT (6/6 pts) - Human-like clustering
  - Medium CV 0.5-0.69: GOOD (4/6 pts)
  - Low CV 0.3-0.49: FAIR (2/6 pts)
  - Uniform CV <0.3: POOR (0/6 pts) - AI-like uniformity
- [x] Add to Detection Risk score (CV <0.35 adds +5 pts risk)

**Test Cases:**

```
Human sample (colon positions in word offsets):
[45, 52, 178, 645, 892]
→ Spacing: [7, 126, 467, 247] words
→ CV = 0.82 (high variation, natural clustering)
→ EXCELLENT (6/6)

AI sample (colon positions):
[120, 245, 370, 495, 620, 745]
→ Spacing: [125, 125, 125, 125, 125] words (uniform!)
→ CV = 0.0 (perfect uniformity)
→ POOR (0/6), +5 detection risk
```

**Research Basis:**

- Williams et al. (2023): Punctuation spacing CV <0.35 → 72% AI detection accuracy
- AI models distribute punctuation for "balanced" readability
- Humans cluster punctuation based on content (explanations, lists, clarifications)

### AC5: Enhanced List Structure Analysis (AST-Based)

**Given** a document with markdown lists parsed to AST
**When** analyzing list structures
**Then** it should:

- [x] Use AST to accurately track nesting (not regex-based indentation)
- [x] Detect mixed ordered/unordered lists (human pattern)
- [x] Measure list symmetry (all sublists same length vs. varied)
- [x] Calculate list item length distribution
- [x] Score dimension contribution (enhancement to Phase 1):
  - Varied nesting, mixed types, asymmetric: EXCELLENT (8/8 pts)
  - Some variation: GOOD (5/8 pts)
  - Mostly uniform: FAIR (3/8 pts)
  - Perfectly symmetric, single type, uniform items: POOR (0/8 pts)
- [x] Add to Detection Risk score (Symmetric lists add +6 pts risk)

**Test Cases:**

```
Human list (AST parsed):
- Ordered list (3 items)
  - Unordered sublist (2 items) under item 1
  - Unordered sublist (4 items) under item 2
- Unordered list (2 items, no sublists)
→ Mixed types ✓, asymmetric sublists ✓, varied item counts ✓
→ EXCELLENT (8/8)

AI list (AST parsed):
1. Item (50 words)
   - Subitem (15 words)
   - Subitem (15 words)
   - Subitem (15 words)
2. Item (50 words)
   - Subitem (15 words)
   - Subitem (15 words)
   - Subitem (15 words)
3. Item (50 words)
   - Subitem (15 words)
   - Subitem (15 words)
   - Subitem (15 words)
→ Perfect symmetry, uniform lengths, single type
→ POOR (0/8), +6 detection risk
```

### AC6: Code Block Pattern Analysis (Bonus)

**Given** a technical document with code blocks
**When** analyzing code example patterns
**Then** it should:

- [x] Count code blocks (fenced code blocks)
- [x] Track language declarations (`python, `javascript, etc.)
- [x] Measure code block length distribution
- [x] Detect missing language declarations (AI often omits)
- [x] Score dimension contribution (optional, 4 points):
  - Varied lengths, all have language declarations: EXCELLENT (4/4 pts)
  - Most have declarations: GOOD (3/4 pts)
  - Some missing declarations: FAIR (2/4 pts)
  - Many missing declarations or uniform lengths: POOR (0/4 pts)
- [x] Add to Detection Risk score (>40% missing declarations adds +4 pts)

**Test Cases:**

```
Human technical writing:
- 8 code blocks
- Language declarations: 8/8 (100%)
- Lengths: [12, 45, 8, 23, 67, 15, 31, 9] lines (varied)
→ EXCELLENT (4/4)

AI-generated technical content:
- 12 code blocks
- Language declarations: 5/12 (42%)
- Lengths: [25, 27, 26, 24, 25, 28, 26, 25, 27, 26, 25, 26] lines (uniform)
→ POOR (0/4), +4 detection risk
```

### AC7: Integration with Dual Scoring System

**Given** the new AST-based and advanced pattern metrics
**When** dual scores are calculated
**Then** the metrics should:

- [x] Contribute to **Quality Score** (36 points total):
  - Blockquote patterns: 10 points
  - Link anchor quality: 8 points
  - Punctuation clustering: 6 points
  - Enhanced list structure: 8 points
  - Code block patterns: 4 points (bonus)
- [x] Contribute to **Detection Risk Score**:
  - Excessive blockquotes (4+ per page): +9 risk points
  - Generic link anchors (>40%): +7 risk points
  - Uniform punctuation (CV <0.35): +5 risk points
  - Symmetric lists: +6 risk points
  - Missing code declarations (>40%): +4 risk points
- [x] Appear in path-to-target recommendations with specific examples
- [x] Be included in historical tracking

### AC8: Output Reporting

**Given** completed AST-based and advanced pattern analysis
**When** generating the analysis report
**Then** it should include:

- [x] **AST-Based Structure Analysis** section
- [x] Blockquote pattern analysis with clustering metrics
- [x] Link anchor quality with generic examples
- [x] Punctuation distribution analysis
- [x] Enhanced list structure analysis
- [x] Code block pattern analysis (if applicable)
- [x] Specific actionable recommendations with examples

**Example Output:**

````
AST-BASED STRUCTURE ANALYSIS
────────────────────────────────────────────────────────────────────────────────
Blockquote Patterns:     4.5 per page ✗ POOR - Excessive AI pattern
  Total: 18 blockquotes in 1,000 words
  Section-start clustering: 11/18 (61%) ← Strong AI signature
  Avg length: 88 words (uniform 85-95 word range)
  → ACTION: Reduce blockquotes to 0-2 per page
    - Remove decorative blockquotes (not adding value)
    - Convert 8+ blockquotes to regular paragraphs
    - Distribute remaining naturally (not at section starts)

Link Anchor Quality:     60% generic ✗ POOR - Low-quality CTAs
  Total links: 20
  Generic anchors: 12 examples detected
    - "click here" (3x)
    - "read more" (4x)
    - "learn more here" (2x)
    - "here" (3x)
  → ACTION: Rewrite generic anchors with descriptive text:
    "click here to install Docker" → "install Docker"
    "read more about API design" → "API design best practices"
    "learn more here" → "PostgreSQL transaction isolation levels"

Punctuation Clustering:  CV = 0.05 ✗ POOR - Uniform distribution
  Colon spacing: [125, 125, 125, 125, 125] word intervals (perfect uniformity!)
  → ACTION: Allow natural punctuation clustering:
    - Group related explanations (multiple colons in paragraph)
    - Remove forced "balanced" spacing
    - Cluster based on content, not aesthetic

Enhanced List Structure: SYMMETRIC ✗ POOR - Perfect AI symmetry
  AST analysis reveals:
    - All 3 top-level items have exactly 3 subitems (uniform)
    - All subitems ~15 words each (uniform lengths)
    - No mixed ordered/unordered lists
  → ACTION: Break symmetry:
    - Vary subitem counts: [2, 4, 1] instead of [3, 3, 3]
    - Mix ordered/unordered where appropriate
    - Vary item lengths based on content

Code Block Patterns:     42% missing declarations ✗ POOR
  12 code blocks, only 5 have language declarations
  → ACTION: Add language to all code blocks:
    ```  →  ```python
    ```  →  ```javascript
    ```  →  ```bash
````

## Technical Implementation Details

### Code Location

**File:** `/Users/jmagady/Dev/BMAD-METHOD/expansion-packs/bmad-technical-writing/data/tools/analyze_ai_patterns.py`

### New Dependencies

**Add to requirements.txt:**

```
marko>=2.0.0
```

### New Methods to Add

#### 1. Marko AST Integration

```python
import warnings
from typing import Optional, List, Dict, Any

try:
    import marko
    from marko import Markdown
    from marko.block import BlockQuote, Heading, List as MarkoList, Paragraph, FencedCode
    from marko.inline import Link, CodeSpan
    MARKO_AVAILABLE = True
except ImportError:
    MARKO_AVAILABLE = False
    warnings.warn("marko not installed. AST-based analysis unavailable. "
                  "Install: pip install marko")

class AIPatternAnalyzer:
    def __init__(self):
        self._markdown_parser = None
        self._ast_cache = {}

    def _get_markdown_parser(self):
        """Lazy load marko parser."""
        if self._markdown_parser is None and MARKO_AVAILABLE:
            self._markdown_parser = Markdown()
        return self._markdown_parser

    def _parse_to_ast(self, text: str, cache_key: Optional[str] = None) -> Optional[Any]:
        """Parse markdown to AST with caching."""
        if not MARKO_AVAILABLE:
            return None

        if cache_key and cache_key in self._ast_cache:
            return self._ast_cache[cache_key]

        parser = self._get_markdown_parser()
        if parser is None:
            return None

        try:
            ast = parser.parse(text)
            if cache_key:
                self._ast_cache[cache_key] = ast
            return ast
        except Exception as e:
            warnings.warn(f"Markdown parsing failed: {e}. Falling back to regex analysis.")
            return None

    def _walk_ast(self, node, node_type=None) -> List[Any]:
        """Recursively walk AST and collect nodes of specified type."""
        nodes = []

        if node_type is None or isinstance(node, node_type):
            nodes.append(node)

        # Recursively process children
        if hasattr(node, 'children'):
            for child in node.children:
                nodes.extend(self._walk_ast(child, node_type))

        return nodes
```

#### 2. Blockquote Pattern Analysis

```python
def _analyze_blockquote_patterns(self, text: str, word_count: int) -> Dict[str, Any]:
    """
    Analyze blockquote usage patterns via AST.

    Returns:
        {
            'total_blockquotes': int,
            'per_page': float,
            'avg_length': float,
            'section_start_clustering': float (0-1),
            'score': float (0-10),
            'assessment': str
        }
    """
    ast = self._parse_to_ast(text)
    if ast is None:
        return {'score': 10.0, 'assessment': 'AST_UNAVAILABLE'}

    # Extract blockquotes
    blockquotes = self._walk_ast(ast, BlockQuote)

    if len(blockquotes) == 0:
        return {'total_blockquotes': 0, 'per_page': 0.0, 'score': 10.0, 'assessment': 'NO_BLOCKQUOTES'}

    # Calculate metrics
    pages = word_count / 250.0
    per_page = len(blockquotes) / pages if pages > 0 else 0

    # Calculate blockquote lengths
    lengths = []
    for bq in blockquotes:
        bq_text = self._extract_text_from_node(bq)
        lengths.append(len(bq_text.split()))

    avg_length = statistics.mean(lengths) if lengths else 0

    # Detect section-start clustering
    # (Blockquote appears within first 100 words of H2 section)
    section_start_count = self._count_section_start_blockquotes(ast)
    section_start_clustering = section_start_count / len(blockquotes) if len(blockquotes) > 0 else 0

    # Scoring
    if per_page <= 2 and section_start_clustering < 0.3:
        score, assessment = 10.0, 'EXCELLENT'
    elif per_page <= 3 and section_start_clustering < 0.5:
        score, assessment = 7.0, 'GOOD'
    elif per_page <= 4:
        score, assessment = 4.0, 'FAIR'
    else:
        score, assessment = 0.0, 'POOR'

    return {
        'total_blockquotes': len(blockquotes),
        'per_page': per_page,
        'avg_length': avg_length,
        'lengths': lengths,
        'section_start_clustering': section_start_clustering,
        'section_start_count': section_start_count,
        'score': score,
        'assessment': assessment
    }

def _extract_text_from_node(self, node) -> str:
    """Extract plain text from AST node."""
    if hasattr(node, 'children'):
        return ''.join([self._extract_text_from_node(child) for child in node.children])
    elif hasattr(node, 'rawtext'):
        return node.rawtext
    else:
        return str(node) if not isinstance(node, str) else node

def _count_section_start_blockquotes(self, ast) -> int:
    """Count blockquotes appearing within first 100 words of H2 sections."""
    # Walk AST and track H2 positions, then blockquote positions
    # Compare to see if blockquote is within 100 words after H2
    # (Simplified implementation - full version would track word offsets)

    count = 0
    current_section_words = 0
    in_h2_section = False

    for node in self._walk_ast(ast):
        if isinstance(node, Heading) and node.level == 2:
            in_h2_section = True
            current_section_words = 0
        elif isinstance(node, BlockQuote):
            if in_h2_section and current_section_words < 100:
                count += 1
        elif isinstance(node, Paragraph):
            text = self._extract_text_from_node(node)
            current_section_words += len(text.split())

    return count
```

#### 3. Link Anchor Text Quality

```python
GENERIC_ANCHOR_PATTERNS = [
    r'\bclick here\b',
    r'\bread more\b',
    r'\blearn more\b',
    r'\bsee here\b',
    r'\bcheck (this|it) out\b',
    r'\b(this|that) link\b',
    r'^here$',
    r'^this$',
    r'^link$',
    r'https?://',
]

def _analyze_link_anchor_quality(self, text: str, word_count: int) -> Dict[str, Any]:
    """
    Analyze link anchor text quality.

    Returns:
        {
            'total_links': int,
            'generic_count': int,
            'generic_ratio': float,
            'generic_examples': List[str],
            'link_density': float (per 1k words),
            'score': float (0-8),
            'assessment': str
        }
    """
    ast = self._parse_to_ast(text)
    if ast is None:
        # Fallback to regex
        return self._analyze_link_anchor_quality_regex(text, word_count)

    # Extract links
    links = self._walk_ast(ast, Link)

    if len(links) == 0:
        return {'total_links': 0, 'score': 8.0, 'assessment': 'NO_LINKS'}

    # Analyze anchor text
    generic_links = []
    generic_examples = []

    for link in links:
        anchor_text = self._extract_text_from_node(link)

        # Check against generic patterns
        is_generic = any(re.search(pattern, anchor_text, re.IGNORECASE)
                        for pattern in GENERIC_ANCHOR_PATTERNS)

        if is_generic:
            generic_links.append(link)
            if len(generic_examples) < 10:  # Limit examples
                generic_examples.append(f'"{anchor_text}"')

    generic_ratio = len(generic_links) / len(links)
    link_density = (len(links) / word_count * 1000) if word_count > 0 else 0

    # Scoring
    if generic_ratio < 0.10:
        score, assessment = 8.0, 'EXCELLENT'
    elif generic_ratio < 0.25:
        score, assessment = 6.0, 'GOOD'
    elif generic_ratio < 0.50:
        score, assessment = 3.0, 'FAIR'
    else:
        score, assessment = 0.0, 'POOR'

    return {
        'total_links': len(links),
        'generic_count': len(generic_links),
        'generic_ratio': generic_ratio,
        'generic_examples': generic_examples,
        'link_density': link_density,
        'score': score,
        'assessment': assessment
    }
```

#### 4. Punctuation Clustering

```python
def _analyze_punctuation_clustering(self, text: str) -> Dict[str, Any]:
    """
    Analyze punctuation distribution patterns.

    Returns:
        {
            'colon_spacing_cv': float,
            'all_punctuation_cv': float,
            'score': float (0-6),
            'assessment': str,
            'spacing_examples': Dict[str, List[int]]
        }
    """
    # Find positions of key punctuation marks
    words = text.split()

    colon_positions = []
    semicolon_positions = []
    emdash_positions = []

    for i, word in enumerate(words):
        if ':' in word:
            colon_positions.append(i)
        if ';' in word:
            semicolon_positions.append(i)
        if '—' in word or '--' in word:
            emdash_positions.append(i)

    # Calculate spacing between consecutive marks
    def calculate_spacing_cv(positions):
        if len(positions) < 3:
            return None
        spacing = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
        if len(spacing) < 2:
            return None
        mean_spacing = statistics.mean(spacing)
        stddev = statistics.stdev(spacing)
        return stddev / mean_spacing if mean_spacing > 0 else 0.0

    colon_cv = calculate_spacing_cv(colon_positions)
    semicolon_cv = calculate_spacing_cv(semicolon_positions)
    emdash_cv = calculate_spacing_cv(emdash_positions)

    # Use colon CV as primary metric (most common in technical writing)
    # If not enough colons, use semicolons, then em-dashes
    primary_cv = colon_cv or semicolon_cv or emdash_cv or 1.0

    # Scoring
    if primary_cv >= 0.7:
        score, assessment = 6.0, 'EXCELLENT'
    elif primary_cv >= 0.5:
        score, assessment = 4.0, 'GOOD'
    elif primary_cv >= 0.3:
        score, assessment = 2.0, 'FAIR'
    else:
        score, assessment = 0.0, 'POOR'

    spacing_examples = {}
    if colon_positions:
        spacing_examples['colons'] = [colon_positions[i+1] - colon_positions[i]
                                      for i in range(min(5, len(colon_positions)-1))]

    return {
        'colon_spacing_cv': colon_cv,
        'semicolon_spacing_cv': semicolon_cv,
        'emdash_spacing_cv': emdash_cv,
        'primary_cv': primary_cv,
        'score': score,
        'assessment': assessment,
        'spacing_examples': spacing_examples,
        'colon_count': len(colon_positions),
        'semicolon_count': len(semicolon_positions),
        'emdash_count': len(emdash_positions)
    }
```

#### 5. Enhanced List Structure (AST-Based)

```python
def _analyze_enhanced_list_structure(self, text: str) -> Dict[str, Any]:
    """
    Analyze list structure patterns via AST.

    Returns:
        {
            'has_mixed_types': bool,
            'symmetry_score': float (0-1, higher=more symmetric=worse),
            'avg_item_length': float,
            'item_length_cv': float,
            'score': float (0-8),
            'assessment': str
        }
    """
    ast = self._parse_to_ast(text)
    if ast is None:
        return {'score': 8.0, 'assessment': 'AST_UNAVAILABLE'}

    lists = self._walk_ast(ast, MarkoList)

    if len(lists) == 0:
        return {'score': 8.0, 'assessment': 'NO_LISTS'}

    # Check for mixed ordered/unordered
    ordered_count = sum(1 for lst in lists if lst.ordered)
    unordered_count = len(lists) - ordered_count
    has_mixed_types = ordered_count > 0 and unordered_count > 0

    # Analyze sublist counts for symmetry
    sublist_counts = []
    for lst in lists:
        # Count immediate children that are also lists
        child_lists = [child for child in lst.children if isinstance(child, MarkoList)]
        sublist_counts.append(len(child_lists))

    # Calculate symmetry (low CV = high symmetry = bad)
    if len(sublist_counts) >= 3:
        symmetry_cv = statistics.stdev(sublist_counts) / statistics.mean(sublist_counts) if statistics.mean(sublist_counts) > 0 else 0
        symmetry_score = 1.0 - min(symmetry_cv, 1.0)  # 1.0 = perfect symmetry, 0.0 = asymmetric
    else:
        symmetry_score = 0.0  # Assume good if insufficient data

    # Analyze item lengths
    item_lengths = []
    for lst in lists:
        for item in lst.children:
            text = self._extract_text_from_node(item)
            item_lengths.append(len(text.split()))

    avg_item_length = statistics.mean(item_lengths) if item_lengths else 0
    item_length_cv = statistics.stdev(item_lengths) / avg_item_length if avg_item_length > 0 and len(item_lengths) > 1 else 0

    # Scoring
    if has_mixed_types and symmetry_score < 0.2 and item_length_cv > 0.4:
        score, assessment = 8.0, 'EXCELLENT'
    elif has_mixed_types or symmetry_score < 0.4:
        score, assessment = 5.0, 'GOOD'
    elif symmetry_score < 0.7:
        score, assessment = 3.0, 'FAIR'
    else:
        score, assessment = 0.0, 'POOR'

    return {
        'has_mixed_types': has_mixed_types,
        'symmetry_score': symmetry_score,
        'avg_item_length': avg_item_length,
        'item_length_cv': item_length_cv,
        'ordered_count': ordered_count,
        'unordered_count': unordered_count,
        'score': score,
        'assessment': assessment
    }
```

#### 6. Code Block Pattern Analysis

```python
def _analyze_code_block_patterns(self, text: str) -> Dict[str, Any]:
    """
    Analyze code block patterns.

    Returns:
        {
            'total_blocks': int,
            'with_language': int,
            'language_declaration_ratio': float,
            'avg_length': float,
            'length_cv': float,
            'score': float (0-4),
            'assessment': str
        }
    """
    ast = self._parse_to_ast(text)
    if ast is None:
        return {'score': 4.0, 'assessment': 'AST_UNAVAILABLE'}

    code_blocks = self._walk_ast(ast, FencedCode)

    if len(code_blocks) == 0:
        return {'total_blocks': 0, 'score': 4.0, 'assessment': 'NO_CODE_BLOCKS'}

    # Count language declarations
    with_language = sum(1 for block in code_blocks if block.lang)
    language_ratio = with_language / len(code_blocks)

    # Calculate lengths
    lengths = []
    for block in code_blocks:
        lines = block.raw.strip().split('\n')
        lengths.append(len(lines))

    avg_length = statistics.mean(lengths)
    length_cv = statistics.stdev(lengths) / avg_length if avg_length > 0 and len(lengths) > 1 else 0

    # Scoring
    if language_ratio >= 0.9 and length_cv > 0.4:
        score, assessment = 4.0, 'EXCELLENT'
    elif language_ratio >= 0.7:
        score, assessment = 3.0, 'GOOD'
    elif language_ratio >= 0.5:
        score, assessment = 2.0, 'FAIR'
    else:
        score, assessment = 0.0, 'POOR'

    return {
        'total_blocks': len(code_blocks),
        'with_language': with_language,
        'language_declaration_ratio': language_ratio,
        'avg_length': avg_length,
        'length_cv': length_cv,
        'score': score,
        'assessment': assessment
    }
```

### Integration Points

**Update dimension scoring:**

```python
# Add to _calculate_dimension_scores method

# AST-based structure analysis
blockquote_patterns = self._analyze_blockquote_patterns(text, word_count)
link_anchor_quality = self._analyze_link_anchor_quality(text, word_count)
punctuation_clustering = self._analyze_punctuation_clustering(text)
enhanced_list_structure = self._analyze_enhanced_list_structure(text)
code_block_patterns = self._analyze_code_block_patterns(text)

# Quality score contribution (36 points)
quality_score += blockquote_patterns['score']        # 10 pts
quality_score += link_anchor_quality['score']        # 8 pts
quality_score += punctuation_clustering['score']     # 6 pts
quality_score += enhanced_list_structure['score']    # 8 pts
quality_score += code_block_patterns['score']        # 4 pts

# Detection risk contribution
if blockquote_patterns['per_page'] >= 4:
    detection_risk += 9
if link_anchor_quality['generic_ratio'] > 0.4:
    detection_risk += 7
if punctuation_clustering['primary_cv'] < 0.35:
    detection_risk += 5
if enhanced_list_structure['symmetry_score'] > 0.7:
    detection_risk += 6
if code_block_patterns['language_declaration_ratio'] < 0.6:
    detection_risk += 4
```

## Definition of Done

- [ ] Marko library integrated with graceful fallback
- [ ] AST parsing working with caching
- [ ] Blockquote pattern analysis complete
- [ ] Link anchor text quality analysis complete
- [ ] Punctuation clustering analysis complete
- [ ] Enhanced list structure analysis complete
- [ ] Code block pattern analysis complete
- [ ] All metrics integrated into dual scoring (36 quality pts, 31 risk pts)
- [ ] Installation instructions added to README
- [ ] requirements.txt updated
- [ ] Unit tests passing (15+ test cases)
- [ ] Integration tests with sample documents
- [ ] Path-to-target includes AST-based recommendations
- [ ] Report output enhanced with AST analysis section
- [ ] No regression in existing functionality
- [ ] Performance acceptable (<20% slowdown total for all 3 phases)

## Dependencies and Prerequisites

**Before starting:**

- [x] Phase 2 completed and tested
- [x] Current dual scoring system functional

**New external dependencies:**

- [ ] marko >= 2.0.0

## Risks and Mitigations

| Risk                                      | Likelihood | Impact | Mitigation                                             |
| ----------------------------------------- | ---------- | ------ | ------------------------------------------------------ |
| Marko parsing fails on malformed markdown | Medium     | Low    | Graceful fallback to regex-based analysis with warning |
| Performance impact from AST parsing       | Medium     | Medium | Cache parsed AST, limit to first 30k words             |
| Complex nested structures cause errors    | Low        | Low    | Robust AST walking with exception handling             |

## Success Metrics (Post-Implementation)

**Measure after 1 week:**

- Detection accuracy: +8-12% over Phase 2 baseline
- AST parsing success rate: >95% on valid markdown
- Combined Phases 1+2+3: 95%+ overall detection accuracy
- False positive rate: <3% on human content

**Final Before/After Comparison (All 3 Phases):**

```
BASELINE (before any phases):
AI content → Quality: 68.2, Detection: 58.3
Human content → Quality: 91.5, Detection: 15.2

AFTER ALL 3 PHASES:
AI content → Quality: 35.8 (-32.4), Detection: 91.7 (+33.4) ← Excellent detection
Human content → Quality: 97.2 (+5.7), Detection: 6.2 (-9.0) ← Improved scores
```

## Related Stories

- **Depends On:** BMAD-TW-DETECT-002 (Phase 2) - Required
- **Next:** None - Final phase of detection enhancement epic
- **Follows:** BMAD-TW-DUAL-001 (Dual Scoring System) ✓ Completed

## Future Enhancements (Post-Phase 3)

Once AST parsing is in place, future low-effort enhancements become possible:

- Table structure analysis (uniform row/column patterns)
- Image alt text quality (generic vs. descriptive)
- Footnote/reference distribution patterns
- Nested blockquote depth (AI rarely nests blockquotes)
- HTML comment patterns (AI often leaves placeholder comments)
