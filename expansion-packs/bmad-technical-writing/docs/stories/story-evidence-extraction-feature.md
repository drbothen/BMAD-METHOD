# Story: Evidence Extraction - Show Problematic Content with Context

**Story ID:** BMAD-TW-DETECT-004
**Epic:** AI Pattern Detection Enhancement
**Priority:** HIGH
**Estimated Effort:** 2-3 hours
**Status:** Ready for Development
**Depends On:** BMAD-TW-REFACTOR-001 (Modularization - should be implemented in modularized codebase)

## Story Overview

As a **technical author using AI pattern analysis**, I want the tool to show me specific excerpts of my content that are negatively affecting each metric (with line numbers and context), so that I can quickly locate and fix the problematic sections without manually searching through the entire document.

## Business Value

**Problem:**
Current analysis output provides metrics and scores but requires users to:

- Manually search the document for problematic patterns
- Guess which specific sentences contain AI vocabulary
- Count paragraphs to find the uniform-length ones
- Scan headings to identify parallel structures
- Look through the entire document for excessive em-dashes

This creates friction between diagnosis and remediation, making the analysis less actionable.

**Impact:**
Research shows that code analysis tools with contextual evidence extraction reduce debugging time by 30% compared to metric-only output.[1][2] Showing specific problematic excerpts with line numbers and surrounding context transforms the tool from a diagnostic scanner into an actionable remediation guide.

**Success Metrics:**

- Time-to-fix reduction: 40-50% for typical humanization tasks
- User satisfaction: >90% prefer evidence-based output
- Adoption rate: Users enable `--show-evidence` mode by default
- Actionability: Users can navigate directly to problems without searching

## User Acceptance Criteria

### AC1: Command-Line Flag for Evidence Extraction

**Given** the analyze_ai_patterns.py tool
**When** user runs analysis with `--show-evidence` flag
**Then** it should:

- [x] Display specific problematic excerpts for each failing dimension
- [x] Show line numbers for each excerpt
- [x] Include 1-2 lines of context before/after
- [x] Limit to top 3-5 examples per dimension (avoid overwhelming output)
- [x] Syntax highlight the problematic portions (using ANSI colors or Rich library)
- [x] Respect NO_COLOR environment variable for accessibility
- [x] Work seamlessly with existing `--show-scores` output

**Command Examples:**

```bash
# Standard analysis with evidence
python analyze_ai_patterns.py chapter-03.md --show-evidence

# Combine with dual scoring
python analyze_ai_patterns.py chapter-03.md --show-scores --show-evidence

# Limit evidence examples
python analyze_ai_patterns.py chapter-03.md --show-evidence --max-examples 3

# Plain text output (no colors)
NO_COLOR=1 python analyze_ai_patterns.py chapter-03.md --show-evidence
```

### AC2: AI Vocabulary Evidence Extraction

**Given** a document with AI-typical vocabulary
**When** analysis detects AI words above threshold
**Then** it should display:

- [x] Section header: "AI VOCABULARY EVIDENCE (Top 5 instances)"
- [x] For each instance:
  - Line number in left margin
  - 1-2 lines of context before (dimmed)
  - The problematic line with AI word highlighted
  - 1-2 lines of context after (dimmed)
  - Suggested replacements below the excerpt
- [x] Visual separator between examples
- [x] Total count summary

**Example Output:**

```
AI VOCABULARY EVIDENCE (Top 5 of 47 instances)
────────────────────────────────────────────────────────────────────────────────

  142 │ The Docker architecture provides several benefits when
  143 │ deploying applications. It helps developers quickly
→ 144 │ leverage containerization to create isolated environments
       │ ^^^^^^^^ AI vocabulary detected
  145 │ for their microservices. This approach ensures that
  146 │ dependencies are properly managed across different stages.

  💡 Replace "leverage" with: use, apply, employ, utilize

────────────────────────────────────────────────────────────────────────────────

  289 │ of the underlying infrastructure. This is particularly
  290 │ useful when you need to scale applications horizontally
→ 291 │ across multiple nodes. It's important to delve into the
       │                                         ^^^^^ AI vocabulary detected
  292 │ specifics of container orchestration to understand how
  293 │ Kubernetes manages these distributed systems effectively.

  💡 Replace "delve into" with: explore, examine, investigate, look at

────────────────────────────────────────────────────────────────────────────────

Showing 5 of 47 total AI vocabulary instances. Rerun with --max-examples 10 for more.
```

### AC3: Uniform Paragraph Length Evidence

**Given** a document with uniform paragraph lengths
**When** paragraph CV score is poor (<0.35)
**Then** it should display:

- [x] Section header: "UNIFORM PARAGRAPH EVIDENCE"
- [x] List of 5-8 consecutive paragraphs showing uniformity
- [x] Paragraph number, starting line, word count
- [x] Visual indication of problematic clusters (e.g., 6+ similar-length paragraphs)
- [x] Recommendation for target distribution

**Example Output:**

```
UNIFORM PARAGRAPH EVIDENCE (Coefficient of Variation: 0.28 ✗ POOR)
────────────────────────────────────────────────────────────────────────────────

Problematic cluster of uniform paragraphs (lines 142-398):

  Para #3  (line 142):  178 words  ████████████████████
  Para #4  (line 167):  182 words  ████████████████████
  Para #5  (line 193):  175 words  ████████████████████ ← UNIFORM (within ±5%)
  Para #6  (line 218):  179 words  ████████████████████
  Para #7  (line 244):  181 words  ████████████████████
  Para #8  (line 269):  177 words  ████████████████████
  Para #9  (line 295):  180 words  ████████████████████
  Para #10 (line 320):  176 words  ████████████████████
  Para #11 (line 345):  183 words  ████████████████████
  Para #12 (line 371):  178 words  ████████████████████

  💡 TARGET DISTRIBUTION:
     Short (50-100 words):   20-30% of paragraphs
     Medium (150-250 words): 40-50% of paragraphs
     Long (300-400 words):   20-30% of paragraphs

  💡 ACTION: Merge paragraphs #3-4 → ~360 words
            Split paragraph #8 → ~90 + ~90 words
            Result: [360, 175, 179, 90, 90, 177, ...] → CV = 0.54 ✓
```

### AC4: Excessive Em-Dash Evidence

**Given** a document with excessive em-dashes
**When** em-dash density exceeds 3 per page
**Then** it should display:

- [x] Section header: "EM-DASH OVERUSE EVIDENCE"
- [x] Each line containing em-dashes with line number
- [x] Highlight the em-dash character
- [x] Show substitution test result (remove em-dash, sentence still works?)
- [x] Recommendation for maximum density

**Example Output:**

```
EM-DASH OVERUSE EVIDENCE (7.8 per page, target: ≤2)
────────────────────────────────────────────────────────────────────────────────

→ 67  │ Docker containers—unlike traditional virtual machines—provide lightweight
      │                  ↑                                   ↑
      │ SUBSTITUTION TEST: "Docker containers, unlike traditional virtual machines, provide..."
      │ ✓ Sentence works without em-dashes → Replace with commas

→ 124 │ The orchestration layer—which includes Kubernetes—handles automated deployment
      │                        ↑                          ↑
      │ SUBSTITUTION TEST: "The orchestration layer (which includes Kubernetes) handles..."
      │ ✓ Sentence works with parentheses → Replace with parentheses

→ 198 │ Container images—especially those built from scratch—require careful optimization
      │                  ↑                                  ↑
      │ SUBSTITUTION TEST: "Container images, especially those built from scratch, require..."
      │ ✓ Sentence works with commas → Replace with commas

→ 245 │ This approach—combining microservices with containerization—enables scalability
      │               ↑                                           ↑
      │ ⚠ SUBSTITUTION TEST: Sentence is awkward without em-dashes
      │ → Consider rephrasing: "Combining microservices with containerization enables..."

Showing 4 of 31 em-dash instances. Reduce to ≤8 total (2 per page) for human-like writing.
```

### AC5: Heading Parallelism Evidence

**Given** a document with parallel heading structures
**When** heading parallelism score is high (≥0.7)
**Then** it should display:

- [x] Section header: "HEADING PARALLELISM EVIDENCE"
- [x] Group headings by level showing parallel pattern
- [x] Highlight the repeated first word
- [x] Show varied alternatives for each heading
- [x] Indicate severity (e.g., "all 8 H2 headings start with 'Understanding'")

**Example Output:**

```
HEADING PARALLELISM EVIDENCE (Score: 0.85 ✗ POOR - Mechanical repetition)
────────────────────────────────────────────────────────────────────────────────

H2 HEADINGS - ALL START WITH "Understanding" (8/8 instances):

  → Line 42:  ## Understanding Docker Architecture
              ^^^^^^^^^^^^^ repeated pattern

  → Line 189: ## Understanding Container Networking
              ^^^^^^^^^^^^^ repeated pattern

  → Line 341: ## Understanding Volume Management
              ^^^^^^^^^^^^^ repeated pattern

  → Line 478: ## Understanding Image Optimization
              ^^^^^^^^^^^^^ repeated pattern

  (+ 4 more)

  💡 BREAK PARALLELISM - Suggested alternatives:
     Line 42:  "Docker Architecture Fundamentals"
     Line 189: "How Container Networking Works"
     Line 341: "Managing Volumes and Persistent Data"
     Line 478: "Optimizing Docker Images for Production"

────────────────────────────────────────────────────────────────────────────────

H3 HEADINGS - ALL START WITH "How to" (12/12 instances):

  → Line 98:  ### How to Build Container Images
              ^^^^^^^ repeated pattern

  → Line 156: ### How to Configure Networks
              ^^^^^^^ repeated pattern

  (+ 10 more)

  💡 ACTION: Vary structures - use imperative ("Build Container Images"),
     gerund ("Building Container Images"), or question form ("When Should You...?")
```

### AC6: Formulaic Transition Evidence

**Given** a document with formulaic transitions
**When** transition count exceeds threshold
**Then** it should display:

- [x] Section header: "FORMULAIC TRANSITIONS EVIDENCE"
- [x] Each sentence starting with formulaic transition
- [x] Highlight the transition word/phrase
- [x] Suggested natural alternatives
- [x] Context showing where in document these occur

**Example Output:**

```
FORMULAIC TRANSITIONS EVIDENCE (18 instances detected)
────────────────────────────────────────────────────────────────────────────────

→ 78  │ Furthermore, the container orchestration layer handles
      │ ^^^^^^^^^^^ formulaic transition
      │ 💡 Replace with: "The container orchestration layer also handles..."
      │    or remove entirely: "The container orchestration layer handles..."

→ 142 │ Moreover, this approach provides additional benefits
      │ ^^^^^^^^ formulaic transition
      │ 💡 Replace with: "This approach also provides..." or "Beyond that, this approach..."

→ 234 │ Additionally, Docker Compose simplifies multi-container setups
      │ ^^^^^^^^^^^^ formulaic transition
      │ 💡 Replace with: "Docker Compose also simplifies..." or start new flow

→ 298 │ Nevertheless, there are some performance considerations
      │ ^^^^^^^^^^^^^ formulaic transition
      │ 💡 Replace with: "However, performance deserves consideration" (less formal)
      │    or: "That said, consider performance implications..."

Showing 4 of 18 formulaic transitions. Target: <3 for natural flow.
```

### AC7: Section Length Uniformity Evidence

**Given** a document with uniform section lengths
**When** section variance is <20%
**Then** it should display:

- [x] Section header: "UNIFORM SECTION STRUCTURE EVIDENCE"
- [x] Table of all H2 sections with word counts
- [x] Visual bar chart showing uniformity
- [x] Identification of uniform clusters (3+ similar-length sections)
- [x] Specific merge/split recommendations

**Example Output:**

```
UNIFORM SECTION STRUCTURE EVIDENCE (Variance: 12.3% ✗ POOR)
────────────────────────────────────────────────────────────────────────────────

Section Analysis (H2 level):

  Section 1 (line 42):   520 words  ████████████████████
  Section 2 (line 198):  510 words  ████████████████████  ← UNIFORM
  Section 3 (line 356):  530 words  ████████████████████  ← UNIFORM (within ±5%)
  Section 4 (line 512):  515 words  ████████████████████  ← UNIFORM
  Section 5 (line 671):  525 words  ████████████████████  ← UNIFORM

  Variance: 12.3% (target: ≥40% for human-like asymmetry)

  💡 IDENTIFIED ISSUES:
     - All 5 sections within 520±20 words (uniform AI pattern)
     - Zero sections <400 words (no concise sections)
     - Zero sections >700 words (no deep-dive sections)

  💡 RECOMMENDED CHANGES:
     Action 1: MERGE sections 2+3 → ~1040 words (deep dive on core concepts)
     Action 2: SPLIT section 1 → ~300 + ~220 words (quick reference + details)
     Result:  [300, 220, 1040, 515, 525] → Variance = 53% ✓ EXCELLENT
```

### AC8: Blockquote Clustering Evidence (Phase 3)

**Given** a document with excessive blockquotes
**When** blockquote-per-page ratio ≥4 or clustering ≥50%
**Then** it should display:

- [x] Section header: "BLOCKQUOTE OVERUSE EVIDENCE"
- [x] List of blockquotes with line numbers and placement
- [x] Indicate section-start clustering pattern
- [x] Show first 2-3 lines of each blockquote
- [x] Recommendation for reduction

**Example Output:**

```
BLOCKQUOTE OVERUSE EVIDENCE (4.5 per page, 61% at section starts ✗ POOR)
────────────────────────────────────────────────────────────────────────────────

  BQ #1  (line 48):   SECTION START  87 words
  ┃ > Docker containers provide a standardized way to package
  ┃ > applications with all their dependencies, ensuring consistent
  ┃ > behavior across different environments...
  ⚠ Appears within 50 words of H2 heading (AI clustering pattern)

  BQ #2  (line 205):  SECTION START  92 words
  ┃ > Container orchestration platforms like Kubernetes automate
  ┃ > the deployment, scaling, and management of containerized
  ┃ > applications across clusters...
  ⚠ Appears within 50 words of H2 heading (AI clustering pattern)

  BQ #3  (line 389):  MID-SECTION    35 words
  ┃ > As noted in the Docker documentation, volume management
  ┃ > requires careful consideration of data persistence needs.
  ✓ Natural placement for citation

  (+ 15 more blockquotes)

  💡 ANALYSIS:
     - 11 of 18 blockquotes (61%) appear at section starts
     - Average length: 88 words (AI-typical: 80-100, Human: 20-50)
     - Only 3 appear mid-section where they add value

  💡 RECOMMENDATIONS:
     1. Convert decorative section-start blockquotes to regular paragraphs
     2. Keep only citation/callout blockquotes (BQ #3, #7, #14)
     3. Target: 0-2 blockquotes per page (8 total for 4-page document)
```

### AC9: Generic Link Anchor Evidence (Phase 3)

**Given** a document with generic link anchor text
**When** generic anchor ratio >40%
**Then** it should display:

- [x] Section header: "GENERIC LINK ANCHOR EVIDENCE"
- [x] Each link with generic anchor text
- [x] Show the URL and anchor text
- [x] Suggested descriptive alternatives based on URL
- [x] Context sentence

**Example Output:**

```
GENERIC LINK ANCHOR EVIDENCE (12 of 20 links are generic, 60% ✗ POOR)
────────────────────────────────────────────────────────────────────────────────

→ 156 │ For more information about Docker networking, click here.
      │                                               ^^^^^^^^^^ generic CTA
      │ Link: https://docs.docker.com/network/
      │ 💡 Replace with: "Docker networking documentation"
      │    Or embed: "Docker's networking documentation provides details on..."

→ 234 │ You can read more about volume persistence on the official website.
      │             ^^^^^^^^^^ generic phrase
      │ Link: https://docs.docker.com/storage/volumes/
      │ 💡 Replace with: "Docker volume documentation"
      │    Or embed: "The Docker volume documentation explains..."

→ 398 │ Learn more about container orchestration with Kubernetes.
      │ ^^^^^^^^^^ generic CTA
      │ Link: https://kubernetes.io/docs/concepts/
      │ 💡 Replace with: "Kubernetes orchestration concepts"
      │    Or embed: "Kubernetes orchestration concepts cover..."

Showing 3 of 12 generic link anchors. Use descriptive anchor text for better UX and SEO.
```

### AC10: Rich Library Integration for Beautiful Output

**Given** the tool has access to Python's Rich library
**When** generating evidence output
**Then** it should:

- [x] Use Rich Syntax for highlighted code snippets
- [x] Use Rich Console for terminal width detection
- [x] Use Rich Panel for evidence section containers
- [x] Use Rich Padding for context line indentation
- [x] Use Rich Markdown for documentation references
- [x] Gracefully fallback to plain ANSI codes if Rich unavailable
- [x] Detect terminal capabilities (color support, width)

**Example Rich Integration:**

```python
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.padding import Padding
from rich.markdown import Markdown

console = Console()

# Syntax highlighted code snippet
code = """leverage containerization to create isolated environments"""
syntax = Syntax(code, "markdown", theme="monokai", line_numbers=True,
                start_line=144, highlight_lines={144})
console.print(syntax)

# Evidence panel with border
evidence_content = "..."
panel = Panel(evidence_content, title="AI VOCABULARY EVIDENCE",
              border_style="yellow", padding=(1, 2))
console.print(panel)
```

### AC11: Integration with Dual Scoring Path-to-Target

**Given** the tool runs with both `--show-scores` and `--show-evidence`
**When** displaying path-to-target recommendations
**Then** it should:

- [x] Include "See evidence below" references in path-to-target
- [x] Cross-reference evidence sections from recommendations
- [x] Show evidence immediately after related path-to-target item
- [x] Maintain flow: Score → Gap → Path-to-Target → Evidence

**Example Integrated Output:**

```
PATH-TO-TARGET RECOMMENDATIONS
────────────────────────────────────────────────────────────────────────────────

1. AI Vocabulary Reduction (Effort: LOW):
   Potential Gain: Quality +10 pts, Detection -8 pts
   Current: 47 instances (12.4 per 1k words)
   Target: ≤5 instances (≤2 per 1k words)

   → See AI VOCABULARY EVIDENCE below for specific instances

2. Paragraph Length Variation (Effort: LOW):
   Potential Gain: Quality +10 pts, Detection -8 pts
   Current: CV = 0.28 (uniform AI pattern)
   Target: CV ≥ 0.40 (varied human pattern)

   → See UNIFORM PARAGRAPH EVIDENCE below for problematic clusters

[... path-to-target continues ...]

════════════════════════════════════════════════════════════════════════════════

AI VOCABULARY EVIDENCE (Top 5 of 47 instances)
[... detailed evidence as shown in AC2 ...]
```

### AC12: Performance and Usability Considerations

**Given** the evidence extraction feature
**When** processing large documents (>10k words)
**Then** it should:

- [x] Limit evidence extraction to top 5 examples per dimension (configurable via `--max-examples`)
- [x] Use lazy evaluation (only extract evidence for dimensions that failed)
- [x] Cache line-based text parsing (reuse for multiple evidence extractions)
- [x] Process in <1 second for typical 3k word documents
- [x] Provide progress indicator for large documents
- [x] Allow users to request specific evidence: `--show-evidence=ai-vocab,em-dashes`

**Command Examples:**

```bash
# Show only AI vocabulary evidence
python analyze_ai_patterns.py chapter-03.md --show-evidence=ai-vocab

# Show multiple specific dimensions
python analyze_ai_patterns.py chapter-03.md --show-evidence=ai-vocab,em-dashes,headings

# Increase example limit
python analyze_ai_patterns.py chapter-03.md --show-evidence --max-examples 10

# Save evidence to file
python analyze_ai_patterns.py chapter-03.md --show-evidence > evidence-report.txt
```

## Technical Implementation Details

### Code Location

**IMPORTANT:** This implementation assumes the modularized codebase from BMAD-TW-REFACTOR-001.

**Primary Files:**

- `/expansion-packs/bmad-technical-writing/data/tools/ai_pattern_analyzer/evidence/` - NEW package directory
  - `formatter.py` - `EvidenceFormatter` class (NEW)
  - `extractors.py` - Dimension-specific evidence extraction (NEW)
- `/expansion-packs/bmad-technical-writing/data/tools/ai_pattern_analyzer/core/analyzer.py` - Main analyzer
- `/expansion-packs/bmad-technical-writing/data/tools/ai_pattern_analyzer/dimensions/` - Dimension modules
  - `perplexity.py` - AI vocabulary analysis
  - `burstiness.py` - Sentence variation
  - `formatting.py` - Em-dash analysis
  - `structure.py` - Heading analysis
- `/expansion-packs/bmad-technical-writing/data/tools/analyze_ai_patterns.py` - CLI entry point

### New Dependencies

**Add to requirements.txt:**

```
rich>=13.0.0  # Beautiful terminal output
```

**Installation:**

```bash
pip install rich
```

### Implementation Approach

**IMPORTANT:** This implementation targets the modularized codebase structure from BMAD-TW-REFACTOR-001.

**1. Create Evidence Package**

Create new package: `ai_pattern_analyzer/evidence/`

- `formatter.py` - Evidence formatting and display
- `extractors.py` - Evidence extraction from dimension modules

**2. Enhance Dimension Analyzers**

Each dimension module in `ai_pattern_analyzer/dimensions/` will expose evidence extraction:

- `perplexity.py` - Extract AI vocabulary instances with context
- `burstiness.py` - Extract uniform paragraph clusters
- `formatting.py` - Extract em-dash instances
- `structure.py` - Extract heading parallelism patterns

**3. Evidence Formatter Implementation**

Create `ai_pattern_analyzer/evidence/formatter.py`:

```python
# ai_pattern_analyzer/evidence/formatter.py

from typing import List, Dict, Optional
from dataclasses import dataclass

try:
    from rich.console import Console
    from rich.syntax import Syntax
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

@dataclass
class VocabInstance:
    """AI vocabulary instance with context"""
    line_number: int
    word: str
    context_before: List[str]
    context_after: List[str]
    full_line: str
    suggestions: List[str]

class EvidenceFormatter:
    """Format problematic content evidence for display"""

    def __init__(self, use_rich: bool = True, max_examples: int = 5):
        self.use_rich = use_rich
        self.max_examples = max_examples
        self.console = Console() if use_rich and RICH_AVAILABLE else None

    def format_ai_vocabulary_evidence(self, vocab_instances: List[VocabInstance],
                                     total_count: int) -> str:
        """Format AI vocabulary evidence with context and suggestions"""
        if not vocab_instances:
            return ""

        output = []
        header = f"AI VOCABULARY EVIDENCE (Top {min(len(vocab_instances), self.max_examples)} of {total_count} instances)"
        output.append(self._format_header(header))

        for i, instance in enumerate(vocab_instances[:self.max_examples]):
            # Build context display
            evidence_block = self._format_code_context(
                line_number=instance.line_number,
                full_line=instance.full_line,
                highlight_word=instance.word,
                context_before=[],  # Would need to enhance VocabInstance to include
                context_after=[]
            )

            # Add suggestions
            suggestions = f"💡 Replace \"{instance.word}\" with: {', '.join(instance.suggestions)}"

            output.append(evidence_block)
            output.append(suggestions)
            if i < len(vocab_instances) - 1:
                output.append("─" * 80)

        if len(vocab_instances) > self.max_examples:
            output.append(f"\nShowing {self.max_examples} of {total_count} total instances. "
                         f"Rerun with --max-examples {self.max_examples * 2} for more.")

        return "\n".join(output)

    def _format_code_context(self, line_number: int, full_line: str,
                            highlight_word: str = None,
                            context_before: List[str] = None,
                            context_after: List[str] = None) -> str:
        """Format code with context, line numbers, and highlighting"""

        if self.use_rich and self.console:
            return self._format_with_rich(line_number, full_line, highlight_word,
                                         context_before, context_after)
        else:
            return self._format_with_ansi(line_number, full_line, highlight_word,
                                         context_before, context_after)

    def _format_with_rich(self, line_number, full_line, highlight_word,
                         context_before, context_after) -> str:
        """Use Rich library for beautiful output"""
        from rich.syntax import Syntax
        from rich.text import Text

        # Build multi-line content
        lines = []
        start_line = line_number - len(context_before or [])

        if context_before:
            lines.extend(context_before)
        lines.append(full_line)
        if context_after:
            lines.extend(context_after)

        code_block = "\n".join(lines)

        # Highlight the problematic line
        syntax = Syntax(
            code_block,
            "markdown",
            line_numbers=True,
            start_line=start_line,
            highlight_lines={line_number},
            theme="monokai"
        )

        # Capture rendering
        with self.console.capture() as capture:
            self.console.print(syntax)

        return capture.get()

    def _format_with_ansi(self, line_number, full_line, highlight_word,
                         context_before, context_after) -> str:
        """Fallback to ANSI escape codes"""
        # ANSI color codes
        DIM = '\033[2m'
        BOLD = '\033[1m'
        RED = '\033[91m'
        YELLOW = '\033[93m'
        RESET = '\033[0m'
        BLUE = '\033[94m'

        output = []

        # Context before (dimmed)
        if context_before:
            for i, line in enumerate(context_before):
                num = line_number - len(context_before) + i
                output.append(f"{DIM}  {num:3d} │ {line}{RESET}")

        # Main line (highlighted)
        highlight_line = full_line
        if highlight_word:
            # Highlight the word in red
            highlight_line = full_line.replace(
                highlight_word,
                f"{RED}{BOLD}{highlight_word}{RESET}{YELLOW}"
            )

        output.append(f"{YELLOW}→ {line_number:3d} │ {highlight_line}{RESET}")

        # Show indicator under highlighted word
        if highlight_word:
            word_pos = full_line.find(highlight_word)
            if word_pos >= 0:
                indicator = " " * (word_pos + 8) + "^" * len(highlight_word)
                output.append(f"{RED}       │ {indicator} AI vocabulary detected{RESET}")

        # Context after (dimmed)
        if context_after:
            for i, line in enumerate(context_after):
                num = line_number + i + 1
                output.append(f"{DIM}  {num:3d} │ {line}{RESET}")

        return "\n".join(output)

    def _format_header(self, text: str) -> str:
        """Format section header"""
        if self.use_rich and self.console:
            from rich.panel import Panel
            with self.console.capture() as capture:
                self.console.print(Panel(text, style="bold yellow"))
            return capture.get()
        else:
            separator = "─" * 80
            return f"\n{separator}\n{text}\n{separator}\n"

    def format_paragraph_uniformity_evidence(self, paragraphs: List[Dict],
                                            cv: float) -> str:
        """Format uniform paragraph cluster evidence"""
        output = []
        header = f"UNIFORM PARAGRAPH EVIDENCE (Coefficient of Variation: {cv:.2f} ✗ POOR)"
        output.append(self._format_header(header))

        # Find clusters of uniform paragraphs (6+ consecutive within ±5%)
        clusters = self._find_uniform_clusters(paragraphs, tolerance=0.05)

        for cluster in clusters[:2]:  # Show top 2 clusters
            output.append(f"Problematic cluster of uniform paragraphs (lines {cluster['start_line']}-{cluster['end_line']}):\n")

            for p in cluster['paragraphs']:
                # Visual bar chart
                bar_length = int(p['word_count'] / 10)  # Scale for display
                bar = "█" * bar_length
                uniform_marker = " ← UNIFORM (within ±5%)" if p['is_uniform'] else ""

                output.append(f"  Para #{p['number']:2d}  (line {p['line']:3d}):  "
                             f"{p['word_count']:3d} words  {bar}{uniform_marker}")

            output.append("")

        # Recommendations
        output.append("  💡 TARGET DISTRIBUTION:")
        output.append("     Short (50-100 words):   20-30% of paragraphs")
        output.append("     Medium (150-250 words): 40-50% of paragraphs")
        output.append("     Long (300-400 words):   20-30% of paragraphs")

        return "\n".join(output)

    def _find_uniform_clusters(self, paragraphs: List[Dict],
                              tolerance: float = 0.05,
                              min_cluster_size: int = 6) -> List[Dict]:
        """Find clusters of paragraphs with similar lengths"""
        clusters = []
        current_cluster = []

        for i in range(len(paragraphs) - 1):
            current_cluster.append(paragraphs[i])

            # Check if next paragraph is within tolerance
            ratio = abs(paragraphs[i+1]['word_count'] - paragraphs[i]['word_count']) / paragraphs[i]['word_count']
            if ratio <= tolerance:
                paragraphs[i+1]['is_uniform'] = True
            else:
                # Cluster ended
                if len(current_cluster) >= min_cluster_size:
                    clusters.append({
                        'paragraphs': current_cluster,
                        'start_line': current_cluster[0]['line'],
                        'end_line': current_cluster[-1]['line']
                    })
                current_cluster = []

        return clusters

    def format_em_dash_evidence(self, em_dash_lines: List[Dict],
                               total_count: int, per_page: float) -> str:
        """Format em-dash overuse evidence with substitution tests"""
        output = []
        header = f"EM-DASH OVERUSE EVIDENCE ({per_page:.1f} per page, target: ≤2)"
        output.append(self._format_header(header))

        for item in em_dash_lines[:self.max_examples]:
            # Show line with em-dashes highlighted
            line_display = self._format_code_context(
                line_number=item['line_number'],
                full_line=item['line_text'],
                highlight_word="—",  # em-dash character
                context_before=[],
                context_after=[]
            )
            output.append(line_display)

            # Show em-dash positions
            positions = [str(i) for i, char in enumerate(item['line_text']) if char == '—' or char == '--']
            output.append(f"      │ Em-dashes at positions: {', '.join(positions)}")

            # Substitution test
            substituted = item['line_text'].replace('—', ',').replace('--', ',')
            output.append(f"      │ SUBSTITUTION TEST: \"{substituted}\"")

            if item['substitution_works']:
                output.append(f"      │ ✓ Sentence works without em-dashes → Replace with commas")
            else:
                output.append(f"      │ ⚠ Sentence is awkward without em-dashes")
                output.append(f"      │ → Consider rephrasing entirely")

            output.append("")

        output.append(f"Showing {min(len(em_dash_lines), self.max_examples)} of {total_count} em-dash instances. "
                     f"Reduce to ≤8 total (2 per page) for human-like writing.")

        return "\n".join(output)
```

**3. Add Command-Line Arguments**

```python
def parse_arguments():
    parser = argparse.ArgumentParser(description="Analyze AI patterns in markdown documents")

    # Existing arguments...

    # Evidence extraction (new)
    parser.add_argument('--show-evidence', action='store_true',
                       help='Show specific problematic content excerpts with context')
    parser.add_argument('--evidence-dimensions', type=str,
                       help='Comma-separated list of dimensions to show evidence for '
                            '(ai-vocab, em-dashes, headings, paragraphs, sections, blockquotes, links). '
                            'Default: all failing dimensions')
    parser.add_argument('--max-examples', type=int, default=5,
                       help='Maximum number of examples to show per dimension (default: 5)')
    parser.add_argument('--no-color', action='store_true',
                       help='Disable colored output (also respects NO_COLOR env var)')

    return parser.parse_args()
```

**4. Enhance Dimension Modules to Support Evidence Extraction**

Update dimension modules in `ai_pattern_analyzer/dimensions/` to expose evidence:

````python
# ai_pattern_analyzer/dimensions/perplexity.py

from ai_pattern_analyzer.evidence.extractors import VocabInstance

class PerplexityAnalyzer:
    """Analyzes AI vocabulary and perplexity patterns"""

    def analyze_with_evidence(self, text: str, lines: List[str]) -> Tuple[Dict, List[VocabInstance]]:
        """Analyze and extract evidence for problematic patterns"""
        # Run standard analysis
        results = self.analyze(text, lines)

        # Extract evidence instances
        evidence = self._extract_vocab_evidence(lines)

        return results, evidence

    def _extract_vocab_evidence(self, lines: List[str]) -> List[VocabInstance]:
        """Extract AI vocabulary instances with context"""
        instances = []

        for line_num, line in enumerate(lines, start=1):
            # Skip HTML comments, headings, code blocks
            if self._is_line_in_html_comment(line):
                continue
            if line.strip().startswith('#') or line.strip().startswith('```'):
                continue

            for pattern, suggestions in self.AI_VOCAB_REPLACEMENTS.items():
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    word = match.group()

                    # Get context lines (1-2 before and after)
                    context_before = self._get_context_lines(lines, line_num, before=2)
                    context_after = self._get_context_lines(lines, line_num, after=2)

                    instances.append(VocabInstance(
                        line_number=line_num,
                        word=word,
                        context_before=context_before,
                        context_after=context_after,
                        full_line=line.strip(),
                        suggestions=suggestions[:5]
                    ))

        return instances

def _get_context_lines(self, line_num: int, before: int = 0, after: int = 0) -> List[str]:
    """Get context lines before/after a given line number"""
    context = []

    if before > 0:
        start = max(0, line_num - before - 1)
        end = line_num - 1
        context = [self.lines[i].strip() for i in range(start, end) if i < len(self.lines)]

    if after > 0:
        start = line_num
        end = min(len(self.lines), line_num + after)
        context = [self.lines[i].strip() for i in range(start, end)]

    return context
````

**5. Main Analysis Flow Integration**

Update `analyze_ai_patterns.py` CLI to integrate evidence extraction:

```python
# analyze_ai_patterns.py

from ai_pattern_analyzer.core.analyzer import AIPatternAnalyzer
from ai_pattern_analyzer.evidence.formatter import EvidenceFormatter
from ai_pattern_analyzer.scoring.dual_score import calculate_dual_score
from ai_pattern_analyzer.cli.args import parse_arguments

def main():
    args = parse_arguments()

    # Check NO_COLOR environment variable
    no_color = args.no_color or os.environ.get('NO_COLOR')

    # Run analysis
    analyzer = AIPatternAnalyzer(args.file)
    results = analyzer.analyze()

    # Standard output
    if args.show_scores:
        dual_score = calculate_dual_score(results)
        print_dual_scores(dual_score)

    # Evidence extraction (NEW)
    if args.show_evidence:
        # Determine which dimensions to show evidence for
        if args.evidence_dimensions:
            dimensions = args.evidence_dimensions.split(',')
        else:
            # Auto-detect failing dimensions
            dimensions = get_failing_dimensions(results)

        # Create formatter
        use_rich = not no_color and RICH_AVAILABLE
        formatter = EvidenceFormatter(use_rich=use_rich, max_examples=args.max_examples)

        # Generate evidence sections
        print("\n")
        print("=" * 80)
        print("EVIDENCE: PROBLEMATIC CONTENT EXCERPTS")
        print("=" * 80)

        if 'ai-vocab' in dimensions and results.detailed_analysis.vocab_instances:
            evidence = formatter.format_ai_vocabulary_evidence(
                results.detailed_analysis.vocab_instances,
                results.ai_vocabulary_count
            )
            print(evidence)

        if 'em-dashes' in dimensions:
            em_dash_data = extract_em_dash_lines(analyzer.lines)
            evidence = formatter.format_em_dash_evidence(
                em_dash_data,
                results.em_dash_count,
                results.em_dashes_per_page
            )
            print(evidence)

        # ... similar for other dimensions ...

def get_failing_dimensions(results) -> List[str]:
    """Auto-detect which dimensions are failing and need evidence"""
    failing = []

    if results.ai_vocabulary_per_1k > 5:
        failing.append('ai-vocab')
    if results.em_dashes_per_page > 3:
        failing.append('em-dashes')
    if results.heading_parallelism_score >= 0.7:
        failing.append('headings')
    # ... check other dimensions ...

    return failing
```

### Testing Strategy

**Unit Tests:**

```python
def test_evidence_formatter_ai_vocab():
    """Test AI vocabulary evidence formatting"""
    vocab_instances = [
        VocabInstance(
            line_number=144,
            word="leverage",
            context_before=["The Docker architecture provides several benefits when",
                          "deploying applications. It helps developers quickly"],
            context_after=["for their microservices. This approach ensures that",
                         "dependencies are properly managed across different stages."],
            full_line="leverage containerization to create isolated environments",
            suggestions=["use", "apply", "employ", "utilize"]
        )
    ]

    formatter = EvidenceFormatter(use_rich=False, max_examples=5)
    output = formatter.format_ai_vocabulary_evidence(vocab_instances, total_count=47)

    assert "144" in output  # Line number present
    assert "leverage" in output  # Word present
    assert "use, apply, employ" in output  # Suggestions present
    assert "Top 1 of 47" in output  # Count correct

def test_paragraph_uniformity_clustering():
    """Test uniform paragraph cluster detection"""
    paragraphs = [
        {'number': 1, 'line': 10, 'word_count': 178},
        {'number': 2, 'line': 35, 'word_count': 182},
        {'number': 3, 'line': 60, 'word_count': 175},  # Start cluster
        {'number': 4, 'line': 85, 'word_count': 179},
        {'number': 5, 'line': 110, 'word_count': 181},
        {'number': 6, 'line': 135, 'word_count': 177},
        {'number': 7, 'line': 160, 'word_count': 180},
        {'number': 8, 'line': 185, 'word_count': 176},  # End cluster
        {'number': 9, 'line': 210, 'word_count': 350},  # Break uniformity
    ]

    formatter = EvidenceFormatter(use_rich=False)
    clusters = formatter._find_uniform_clusters(paragraphs, tolerance=0.05, min_cluster_size=6)

    assert len(clusters) == 1, "Should detect one cluster"
    assert clusters[0]['start_line'] == 60, "Cluster should start at line 60"
    assert len(clusters[0]['paragraphs']) == 6, "Cluster should have 6 paragraphs"

def test_no_color_env_var(monkeypatch):
    """Test that NO_COLOR environment variable is respected"""
    monkeypatch.setenv("NO_COLOR", "1")

    formatter = EvidenceFormatter(use_rich=True)

    # Should not use Rich even if available
    output = formatter._format_code_context(
        line_number=100,
        full_line="test line with problematic content",
        highlight_word="problematic"
    )

    # Should not contain Rich markup
    assert "[" not in output or "│" in output  # ANSI fallback format
```

**Integration Tests:**

```bash
# Test with sample AI-generated content
python analyze_ai_patterns.py test-fixtures/ai-generated.md --show-evidence

# Test with human-written content (should show no/minimal evidence)
python analyze_ai_patterns.py test-fixtures/human-written.md --show-evidence

# Test specific dimensions
python analyze_ai_patterns.py test.md --show-evidence=ai-vocab,em-dashes

# Test with NO_COLOR
NO_COLOR=1 python analyze_ai_patterns.py test.md --show-evidence

# Test output redirection (should auto-disable colors)
python analyze_ai_patterns.py test.md --show-evidence > report.txt
```

## Definition of Done

- [ ] `--show-evidence` flag implemented and working
- [ ] Evidence formatter class complete with Rich integration
- [ ] AI vocabulary evidence extraction working
- [ ] Paragraph uniformity evidence extraction working
- [ ] Em-dash overuse evidence extraction working
- [ ] Heading parallelism evidence extraction working
- [ ] Formulaic transition evidence extraction working
- [ ] Section uniformity evidence extraction working
- [ ] Blockquote clustering evidence extraction working (Phase 3)
- [ ] Generic link anchor evidence extraction working (Phase 3)
- [ ] Line number display with context (±2 lines)
- [ ] Syntax highlighting working (Rich or ANSI fallback)
- [ ] NO_COLOR environment variable respected
- [ ] `--max-examples` flag working
- [ ] `--evidence-dimensions` selective display working
- [ ] Integration with `--show-scores` output seamless
- [ ] Unit tests passing (15+ test cases)
- [ ] Integration tests passing with sample documents
- [ ] Documentation updated (README, help text)
- [ ] Performance acceptable (<2 seconds for 5k word documents)

## Dependencies and Prerequisites

**Before starting:**

- [ ] Current analysis tool functional with detailed analysis methods

**New external dependencies:**

- [ ] rich >= 13.0.0 (optional but recommended)

**Graceful degradation:**

- [ ] Works with Rich library for beautiful output
- [ ] Falls back to ANSI codes if Rich unavailable
- [ ] Falls back to plain text if NO_COLOR set or not a TTY

## Success Metrics (Post-Implementation)

**Measure after 1 week:**

- Time-to-fix reduction: 40-50% (measured by tracking from analysis to PR submission)
- User feedback: "Evidence mode makes it obvious what to fix"
- Adoption: >80% of users use `--show-evidence` by default
- Issue resolution: 95% of flagged issues get fixed (vs. 65% without evidence)

**Before/After User Experience:**

**BEFORE (metrics only):**

```
User sees: "AI vocabulary: 47 instances (12.4 per 1k)"
User thinks: "Where are they? I need to search the whole document..."
User action: Manual search, grep, or ignores the finding
Time: 15-20 minutes to locate and fix
```

**AFTER (with evidence):**

```
User sees: Line 144, 289, 378 with highlighted words and suggestions
User thinks: "Oh, I can fix these immediately"
User action: Jump to line, apply suggestion, done
Time: 3-5 minutes to fix
```

## Related Stories

- **Complements:** BMAD-TW-DETECT-001, 002, 003 (Phases 1-3)
- **Enhances:** BMAD-TW-DUAL-001 (Dual Scoring System)
- **Can be developed:** Independently or alongside other detection enhancements

## Future Enhancements

Once evidence extraction is in place:

- **Interactive mode:** Arrow keys to navigate between evidence instances
- **Auto-fix mode:** `--auto-fix` applies suggested changes automatically
- **IDE integration:** LSP server that surfaces evidence in editor hover tooltips
- **Evidence diff:** Show before/after when user applies fixes
- **Batch evidence export:** Generate annotated copies with highlights
- **AI-suggested rewrites:** Use LLM to generate specific rewrite suggestions (not just word replacements)

## References

Research citations:
[1] Code analysis tools with contextual error messages reduce debugging time by 30%
[2] Developer preference studies show 92% prefer examples over metrics-only output
