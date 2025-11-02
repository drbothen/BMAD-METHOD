"""
Core AIPatternAnalyzer orchestration class.

This is the main analysis engine that coordinates all dimension analyzers,
calculates scores, manages history, and produces final results.

Extracted from monolithic analyze_ai_patterns.py (7,079 lines) as part of
modularization effort (Phase 3).
"""

import re
import json
import sys
import statistics
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import asdict

# Core results
from ai_pattern_analyzer.core.results import (
    AnalysisResults, DetailedAnalysis,
    VocabInstance, HeadingIssue, UniformParagraph,
    EmDashInstance, TransitionInstance
)

# Scoring and history
from ai_pattern_analyzer.scoring.dual_score import (
    DualScore, ScoreCategory, ScoreDimension,
    ImprovementAction, THRESHOLDS
)
from ai_pattern_analyzer.history.tracker import ScoreHistory, HistoricalScore
from ai_pattern_analyzer.utils.text_processing import safe_divide, safe_ratio

# Dimension analyzers
from ai_pattern_analyzer.dimensions.perplexity import PerplexityAnalyzer
from ai_pattern_analyzer.dimensions.burstiness import BurstinessAnalyzer
from ai_pattern_analyzer.dimensions.structure import StructureAnalyzer
from ai_pattern_analyzer.dimensions.formatting import FormattingAnalyzer
from ai_pattern_analyzer.dimensions.voice import VoiceAnalyzer
from ai_pattern_analyzer.dimensions.syntactic import SyntacticAnalyzer
from ai_pattern_analyzer.dimensions.lexical import LexicalAnalyzer
from ai_pattern_analyzer.dimensions.stylometric import StylometricAnalyzer
from ai_pattern_analyzer.dimensions.advanced import AdvancedAnalyzer
from ai_pattern_analyzer.scoring.dual_score_calculator import calculate_dual_score as _calculate_dual_score

# Optional dependencies
try:
    import marko
    from marko import Markdown
    from marko.block import Quote, Heading, List as MarkoList, Paragraph, FencedCode
    from marko.inline import Link, CodeSpan
    HAS_MARKO = True
except ImportError:
    HAS_MARKO = False
    import warnings
    warnings.warn("marko not installed. AST-based structure analysis unavailable. "
                  "Install with: pip install marko>=2.0.0", UserWarning)


class AIPatternAnalyzer:
    """
    Main analyzer class that orchestrates all dimension analyzers.

    This class coordinates the analysis workflow:
    1. Load and preprocess text
    2. Run dimension-specific analyses
    3. Calculate scores across all dimensions
    4. Generate comprehensive results
    5. Track history over time
    """

    # Replacement suggestions for AI vocabulary (for detailed mode)
    AI_VOCAB_REPLACEMENTS = {
        r'\bdelv(e|es|ing)\b': ['explore', 'examine', 'investigate', 'look at', 'dig into'],
        r'\brobust(ness)?\b': ['reliable', 'powerful', 'solid', 'effective', 'well-designed'],
        r'\bleverag(e|es|ing)\b': ['use', 'apply', 'take advantage of', 'employ', 'work with'],
        r'\bharness(es|ing)?\b': ['use', 'apply', 'employ', 'tap into', 'utilize'],
        r'\bfacilitat(e|es|ing)\b': ['enable', 'help', 'make easier', 'allow', 'support'],
        r'\bunderscore(s|d|ing)?\b': ['emphasize', 'highlight', 'stress', 'point out', 'show'],
        r'\bpivotal\b': ['key', 'important', 'critical', 'essential', 'crucial'],
        r'\bseamless(ly)?\b': ['smooth', 'easy', 'straightforward', 'effortless', 'natural'],
        r'\bholistic(ally)?\b': ['complete', 'comprehensive', 'full', 'thorough', 'whole'],
        r'\bcomprehensive(ly)?\b': ['thorough', 'complete', 'detailed', 'full', 'extensive'],
        r'\boptimiz(e|es|ing|ation)\b': ['improve', 'enhance', 'fine-tune', 'make better', 'refine'],
        r'\bstreamlin(e|ed|ing)\b': ['simplify', 'improve', 'make efficient', 'refine', 'enhance'],
        r'\butiliz(e|es|ation|ing)\b': ['use', 'employ', 'apply', 'work with'],
        r'\bunpack(s|ing)?\b': ['explain', 'explore', 'break down', 'examine', 'analyze'],
        r'\bmyriad\b': ['many', 'countless', 'numerous', 'various', 'multiple'],
        r'\bplethora\b': ['many', 'abundance', 'wealth', 'plenty', 'lots'],
        r'\bparamount\b': ['critical', 'essential', 'crucial', 'vital', 'key'],
        r'\bquintessential\b': ['typical', 'classic', 'perfect example', 'ideal', 'archetypal'],
        r'\binnovative\b': ['new', 'creative', 'novel', 'original', 'fresh'],
        r'\bcutting-edge\b': ['advanced', 'modern', 'latest', 'state-of-the-art', 'new'],
        r'\brevolutionary\b': ['groundbreaking', 'major', 'significant', 'transformative', 'game-changing'],
        r'\bgame-changing\b': ['significant', 'major', 'important', 'transformative', 'impactful'],
        r'\btransformative\b': ['significant', 'major', 'powerful', 'game-changing', 'impactful'],
        r'\bdive deep\b': ['explore thoroughly', 'examine closely', 'investigate', 'look closely at', 'study'],
        r'\bdeep dive\b': ['thorough look', 'detailed examination', 'close look', 'in-depth analysis', 'careful study'],
        r'\becosystem\b': ['environment', 'system', 'network', 'platform', 'framework'],
        r'\blandscape\b': ['field', 'area', 'space', 'domain', 'world'],
        r'\bparadigm\s+shift\b': ['major change', 'fundamental shift', 'big change', 'transformation', 'sea change'],
        r'\bsynerg(y|istic)\b': ['cooperation', 'collaboration', 'combined effect', 'teamwork', 'partnership'],
        r'\bcommence(s|d)?\b': ['start', 'begin', 'initiate', 'launch', 'kick off'],
        r'\bendeavor(s)?\b': ['effort', 'project', 'attempt', 'undertaking', 'initiative'],
    }

    # Transition replacements (for detailed mode)
    TRANSITION_REPLACEMENTS = {
        'Furthermore,': ['Plus,', 'What\'s more,', 'Beyond that,', 'And here\'s the thing,', 'On top of that,'],
        'Moreover,': ['Plus,', 'On top of that,', 'And,', 'What\'s more,', 'Beyond that,'],
        'Additionally,': ['Also,', 'Plus,', 'And,', 'What\'s more,', 'On top of that,'],
        'In addition,': ['Also,', 'Plus,', 'What\'s more,', 'Beyond that,', 'And,'],
        'First and foremost,': ['First,', 'To start,', 'Most importantly,', 'Above all,', 'First off,'],
        'It is important to note that': ['Note that', 'Keep in mind', 'Remember', 'Worth noting:', 'Key point:'],
        'It is worth mentioning that': ['Worth noting', 'Keep in mind', 'Note that', 'Also', 'Interestingly,'],
        'When it comes to': ['For', 'With', 'Regarding', 'As for', 'Looking at'],
        'In conclusion,': ['Finally,', 'To sum up,', 'In short,', 'Bottom line:', 'To wrap up,'],
        'To summarize,': ['In short,', 'Briefly,', 'To sum up,', 'Bottom line:', 'In a nutshell,'],
        'In summary,': ['In short,', 'Briefly,', 'To recap,', 'Bottom line:', 'To sum up,'],
        'As mentioned earlier,': ['Earlier,', 'As noted,', 'Remember,', 'Recall that', 'As we saw,'],
        'It should be noted that': ['Note that', 'Keep in mind', 'Remember', 'Worth noting:', 'Important:'],
        'With that said,': ['That said,', 'Still,', 'Even so,', 'But', 'However,'],
        'Having said that,': ['That said,', 'Still,', 'Even so,', 'But', 'However,'],
    }

    # Domain-specific technical terms (customizable per project)
    DOMAIN_TERMS_DEFAULT = [
        # Example cybersecurity terms - customize for your domain
        r'\bTriton\b', r'\bTrisis\b', r'\bSIS\b', r'\bPLC\b', r'\bSCADA\b',
        r'\bDCS\b', r'\bICS\b', r'\bOT\b', r'\bransomware\b', r'\bmalware\b',
        r'\bNIST\b', r'\bISA\b', r'\bIEC\b', r'\bMITRE\b', r'\bSOC\b',
        r'\bSIEM\b', r'\bIDS\b', r'\bIPS\b',
    ]

    def __init__(self, domain_terms: Optional[List[str]] = None):
        """
        Initialize analyzer with optional custom domain terms.

        Pre-compiles all regex patterns for 20-30% performance improvement.
        Instantiates all dimension analyzers.

        Args:
            domain_terms: Optional list of domain-specific regex patterns
        """
        self.domain_terms = domain_terms or self.DOMAIN_TERMS_DEFAULT
        self.lines = []  # Will store line-by-line content for detailed mode

        # HTML comment pattern (metadata blocks to ignore)
        self._html_comment_pattern = re.compile(r'<!--.*?-->', re.DOTALL)

        # Phase 3: AST parser and cache (marko)
        self._markdown_parser = None
        self._ast_cache = {}

        # Initialize all dimension analyzers
        self.perplexity_analyzer = PerplexityAnalyzer()
        self.burstiness_analyzer = BurstinessAnalyzer()
        self.structure_analyzer = StructureAnalyzer()
        self.formatting_analyzer = FormattingAnalyzer()
        self.voice_analyzer = VoiceAnalyzer()
        self.syntactic_analyzer = SyntacticAnalyzer()
        self.lexical_analyzer = LexicalAnalyzer()
        self.stylometric_analyzer = StylometricAnalyzer()
        self.advanced_analyzer = AdvancedAnalyzer()

    # ========================================================================
    # AST PARSING HELPERS (marko)
    # ========================================================================

    def _get_markdown_parser(self):
        """Lazy load marko parser."""
        if self._markdown_parser is None and HAS_MARKO:
            self._markdown_parser = Markdown()
        return self._markdown_parser

    def _parse_to_ast(self, text: str, cache_key: Optional[str] = None):
        """Parse markdown to AST with caching."""
        if not HAS_MARKO:
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
            import warnings
            warnings.warn(f"Markdown parsing failed: {e}. Falling back to regex analysis.", UserWarning)
            return None

    def _walk_ast(self, node, node_type=None):
        """Recursively walk AST and collect nodes of specified type."""
        nodes = []

        if node_type is None or isinstance(node, node_type):
            nodes.append(node)

        # Recursively process children
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                nodes.extend(self._walk_ast(child, node_type))

        return nodes

    def _extract_text_from_node(self, node) -> str:
        """Extract plain text from AST node recursively."""
        if hasattr(node, 'children') and node.children:
            return ''.join([self._extract_text_from_node(child) for child in node.children])
        elif hasattr(node, 'children') and isinstance(node.children, str):
            return node.children
        elif hasattr(node, 'dest'):  # Link destination
            return ''
        elif isinstance(node, str):
            return node
        else:
            return ''

    # ========================================================================
    # PREPROCESSING
    # ========================================================================

    def _strip_html_comments(self, text: str) -> str:
        """Remove HTML comment blocks (metadata) from text for analysis."""
        return self._html_comment_pattern.sub('', text)

    def _is_line_in_html_comment(self, line: str) -> bool:
        """Check if a line is inside or is an HTML comment."""
        # Line contains complete comment
        if '<!--' in line and '-->' in line:
            return True
        # Line is start or middle of comment
        if '<!--' in line or '-->' in line:
            return True
        return False

    # ========================================================================
    # MAIN ANALYSIS METHOD
    # ========================================================================

    def analyze_file(self, file_path: str) -> AnalysisResults:
        """
        Analyze a single markdown file for AI patterns.

        This is the main entry point that orchestrates all dimension analyses,
        calculates scores, and produces comprehensive results.

        Args:
            file_path: Path to markdown file to analyze

        Returns:
            AnalysisResults object with complete analysis

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Strip HTML comments (metadata blocks) before analysis
        text = self._strip_html_comments(text)

        # Split into lines for detailed analysis
        lines = text.splitlines()

        # Run all dimension analyses
        word_count = self._count_words(text)

        # Core analyses using dimension analyzers
        perplexity_results = self.perplexity_analyzer.analyze(text, lines)
        burstiness_results = self.burstiness_analyzer.analyze(text, lines)
        structure_results = self.structure_analyzer.analyze(text, lines)
        formatting_results = self.formatting_analyzer.analyze(text, lines)
        voice_results = self.voice_analyzer.analyze(text, lines)

        # Enhanced analyses (optional dependencies)
        syntactic_results = self.syntactic_analyzer.analyze(text, lines)
        lexical_results = self.lexical_analyzer.analyze(text, lines)
        stylometric_results = self.stylometric_analyzer.analyze(text, lines)
        advanced_results = self.advanced_analyzer.analyze(text, lines)

        # Calculate pages (estimate: 750 words per page)
        estimated_pages = max(1, word_count / 750)

        # Build results object
        # Extract values from dimension analysis results
        ai_vocab = perplexity_results.get('ai_vocabulary', {})
        formulaic = perplexity_results.get('formulaic_transitions', {})
        burstiness = burstiness_results.get('sentence_variation', {})
        paragraphs = burstiness_results.get('paragraph_variation', {})
        lexical = lexical_results.get('lexical_diversity', {})
        structure = structure_results.get('structure', {})
        headings = structure_results.get('headings', {})
        voice = voice_results.get('voice', {})
        formatting = formatting_results.get('formatting', {})

        results = AnalysisResults(
            file_path=file_path,
            total_words=word_count,
            total_sentences=burstiness.get('total_sentences', 0),
            total_paragraphs=paragraphs.get('total_paragraphs', 0),

            ai_vocabulary_count=ai_vocab.get('count', 0),
            ai_vocabulary_per_1k=ai_vocab.get('per_1k', 0.0),
            ai_vocabulary_list=ai_vocab.get('words', []),
            formulaic_transitions_count=formulaic.get('count', 0),
            formulaic_transitions_list=formulaic.get('transitions', []),

            sentence_mean_length=burstiness.get('mean', 0.0),
            sentence_stdev=burstiness.get('stdev', 0.0),
            sentence_min=burstiness.get('min', 0),
            sentence_max=burstiness.get('max', 0),
            sentence_range=(burstiness.get('min', 0), burstiness.get('max', 0)),
            short_sentences_count=burstiness.get('short', 0),
            medium_sentences_count=burstiness.get('medium', 0),
            long_sentences_count=burstiness.get('long', 0),
            sentence_lengths=burstiness.get('lengths', []),

            paragraph_mean_words=paragraphs.get('mean', 0.0),
            paragraph_stdev=paragraphs.get('stdev', 0.0),
            paragraph_range=(paragraphs.get('min', 0), paragraphs.get('max', 0)),

            unique_words=lexical.get('unique', 0),
            lexical_diversity=lexical.get('diversity', 0.0),

            bullet_list_lines=structure.get('bullet_lines', 0),
            numbered_list_lines=structure.get('numbered_lines', 0),
            total_headings=headings.get('total', 0),
            heading_depth=headings.get('depth', 0),
            h1_count=headings.get('h1', 0),
            h2_count=headings.get('h2', 0),
            h3_count=headings.get('h3', 0),
            h4_plus_count=headings.get('h4_plus', 0),
            headings_per_page=headings.get('total', 0) / estimated_pages,

            heading_parallelism_score=headings.get('parallelism_score', 0.0),
            verbose_headings_count=headings.get('verbose_count', 0),
            avg_heading_length=headings.get('avg_length', 0.0),

            first_person_count=voice.get('first_person', 0),
            direct_address_count=voice.get('direct_address', 0),
            contraction_count=voice.get('contractions', 0),

            domain_terms_count=0,  # TODO: Implement domain term detection
            domain_terms_list=[],

            em_dash_count=formatting.get('em_dashes', 0),
            em_dashes_per_page=formatting.get('em_dashes', 0) / estimated_pages,
            bold_markdown_count=formatting.get('bold', 0),
            italic_markdown_count=formatting.get('italics', 0),

            # Enhanced metrics from dimension analyzers
            **self._flatten_optional_metrics(syntactic_results, lexical_results,
                                             stylometric_results, advanced_results)
        )

        # Calculate all dimension scores
        results.perplexity_score = self.perplexity_analyzer.score(perplexity_results)[1]
        results.burstiness_score = self.burstiness_analyzer.score(burstiness_results)[1]
        results.structure_score = self.structure_analyzer.score(structure_results)[1]
        results.voice_score = self.voice_analyzer.score(voice_results)[1]
        results.formatting_score = self.formatting_analyzer.score(formatting_results)[1]
        results.syntactic_score = self.syntactic_analyzer.score(syntactic_results)[1] if syntactic_results.get('syntactic') else "UNKNOWN"
        results.stylometric_score = self.stylometric_analyzer.score(stylometric_results)[1] if stylometric_results else "UNKNOWN"

        # Technical score (TODO: implement domain term detection)
        results.technical_score = "MEDIUM"

        # Overall assessment
        results.overall_assessment = self._assess_overall(results)

        return results

    def _count_words(self, text: str) -> int:
        """Count total words in text, excluding code blocks."""
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        # Count words
        words = re.findall(r"\b[\w'-]+\b", text)
        return len(words)

    def _flatten_optional_metrics(self, syntactic_results, lexical_results,
                                  stylometric_results, advanced_results) -> Dict:
        """Flatten optional metrics from dimension analyzers into flat dict for AnalysisResults."""
        metrics = {}

        # Syntactic metrics
        if syntactic_results.get('syntactic'):
            synt = syntactic_results['syntactic']
            metrics['syntactic_repetition_score'] = synt.get('syntactic_repetition_score')
            metrics['pos_diversity'] = synt.get('pos_diversity')
            metrics['avg_dependency_depth'] = synt.get('avg_dependency_depth')
            metrics['subordination_index'] = synt.get('subordination_index')

        # Lexical metrics
        if lexical_results.get('lexical_diversity'):
            metrics['mtld_score'] = lexical_results['lexical_diversity'].get('mtld_score')
            metrics['stemmed_diversity'] = lexical_results['lexical_diversity'].get('stemmed_diversity')

        # Advanced metrics
        if advanced_results.get('gltr'):
            gltr = advanced_results['gltr']
            metrics['gltr_top10_percentage'] = gltr.get('top10_percentage')
            metrics['gltr_score'] = "HIGH" if gltr.get('top10_percentage', 100) < 60 else "LOW"

        if advanced_results.get('advanced_lexical'):
            adv_lex = advanced_results['advanced_lexical']
            metrics['hdd_score'] = adv_lex.get('hdd')
            metrics['yules_k'] = adv_lex.get('yules_k')
            metrics['advanced_lexical_score'] = "HIGH" if adv_lex.get('hdd', 0) > 0.65 else "LOW"

        return metrics

    def _assess_overall(self, results: AnalysisResults) -> str:
        """Calculate overall assessment based on all dimension scores."""
        score_map = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "VERY LOW": 0, "UNKNOWN": 2}

        scores = [
            score_map[results.perplexity_score],
            score_map[results.burstiness_score],
            score_map[results.structure_score],
            score_map[results.voice_score],
            score_map[results.formatting_score],
        ]

        avg = sum(scores) / len(scores)

        if avg >= 2.5:
            return "HUMAN-LIKE"
        elif avg >= 1.5:
            return "MIXED"
        else:
            return "AI-LIKELY"

    # ========================================================================
    # DUAL SCORE CALCULATION
    # ========================================================================

    def calculate_dual_score(self, results: AnalysisResults,
                            detection_target: float = 30.0,
                            quality_target: float = 85.0) -> DualScore:
        """
        Calculate dual scores: Detection Risk (0-100, lower=better) and Quality Score (0-100, higher=better).

        Delegates to the dual_score_calculator module for the actual calculation.

        Args:
            results: AnalysisResults from analysis
            detection_target: Target detection risk (default 30 = low risk)
            quality_target: Target quality score (default 85 = excellent)

        Returns:
            DualScore with comprehensive breakdown and optimization path
        """
        return _calculate_dual_score(results, detection_target, quality_target)

    # ========================================================================
    # HISTORY TRACKING
    # ========================================================================

    def _get_history_file_path(self, file_path: str) -> Path:
        """Get path to history JSON file for a document."""
        doc_path = Path(file_path)
        history_dir = doc_path.parent / '.ai-analysis-history'
        history_dir.mkdir(exist_ok=True)
        return history_dir / f"{doc_path.stem}.history.json"

    def load_score_history(self, file_path: str) -> ScoreHistory:
        """Load score history for a document."""
        history_file = self._get_history_file_path(file_path)

        if not history_file.exists():
            return ScoreHistory(file_path=file_path, scores=[])

        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Reconstruct ScoreHistory from JSON
            scores = [HistoricalScore(**score_data) for score_data in data.get('scores', [])]
            return ScoreHistory(file_path=data.get('file_path', file_path), scores=scores)

        except Exception as e:
            print(f"Warning: Could not load history from {history_file}: {e}", file=sys.stderr)
            return ScoreHistory(file_path=file_path, scores=[])

    def save_score_history(self, history: ScoreHistory):
        """Save score history for a document."""
        history_file = self._get_history_file_path(history.file_path)

        try:
            # Convert to dict for JSON serialization
            data = {
                'file_path': history.file_path,
                'scores': [asdict(score) for score in history.scores]
            }

            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Warning: Could not save history to {history_file}: {e}", file=sys.stderr)

    # ========================================================================
    # DETAILED ANALYSIS (LINE-BY-LINE)
    # ========================================================================

    def analyze_file_detailed(self, file_path: str) -> DetailedAnalysis:
        """
        Analyze file with detailed line-by-line diagnostics.

        This method provides actionable feedback for each AI pattern detected,
        including line numbers, context, and specific suggestions for improvement.

        Args:
            file_path: Path to markdown file to analyze

        Returns:
            DetailedAnalysis object with line-by-line findings

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
            self.lines = text.splitlines()

        # Run standard analysis for summary
        standard_results = self.analyze_file(file_path)

        # Run detailed analyses using dimension analyzers
        html_checker = self._is_line_in_html_comment

        # Call dimension analyzers' analyze_detailed methods
        vocab_instances = self._analyze_ai_vocabulary_detailed()
        heading_issues = self._analyze_headings_detailed()
        uniform_paras = self._analyze_sentence_uniformity_detailed()
        em_dash_instances = self._analyze_em_dashes_detailed()
        transition_instances = self._analyze_transitions_detailed()

        # Advanced detailed analyses
        burstiness_issues = self.burstiness_analyzer.analyze_detailed(self.lines, html_checker) if hasattr(self.burstiness_analyzer, 'analyze_detailed') else []
        syntactic_issues = self.syntactic_analyzer.analyze_detailed(self.lines, html_checker) if hasattr(self.syntactic_analyzer, 'analyze_detailed') else []
        stylometric_issues = self.stylometric_analyzer.analyze_detailed(self.lines, html_checker) if hasattr(self.stylometric_analyzer, 'analyze_detailed') else []
        formatting_issues = self.formatting_analyzer.analyze_detailed(self.lines, html_checker) if hasattr(self.formatting_analyzer, 'analyze_detailed') else []
        high_pred_segments = self.advanced_analyzer.analyze_detailed(self.lines, html_checker) if hasattr(self.advanced_analyzer, 'analyze_detailed') else []

        # Build summary dict from standard results
        summary = {
            'overall_assessment': standard_results.overall_assessment,
            'perplexity_score': standard_results.perplexity_score,
            'burstiness_score': standard_results.burstiness_score,
            'structure_score': standard_results.structure_score,
            'voice_score': standard_results.voice_score,
            'technical_score': standard_results.technical_score,
            'formatting_score': standard_results.formatting_score,
            'total_words': standard_results.total_words,
            'total_sentences': standard_results.total_sentences,
            'ai_vocab_per_1k': standard_results.ai_vocabulary_per_1k,
            'sentence_stdev': standard_results.sentence_stdev,
            'em_dashes_per_page': standard_results.em_dashes_per_page,
            'heading_depth': standard_results.heading_depth,
            'heading_parallelism': standard_results.heading_parallelism_score,
            # Advanced metrics
            'gltr_score': getattr(standard_results, 'gltr_score', "N/A"),
            'advanced_lexical_score': getattr(standard_results, 'advanced_lexical_score', "N/A"),
            'stylometric_score': getattr(standard_results, 'stylometric_score', "N/A"),
            'ai_detection_score': getattr(standard_results, 'ai_detection_score', "N/A"),
        }

        return DetailedAnalysis(
            file_path=file_path,
            summary=summary,
            # Original detailed findings
            ai_vocabulary=vocab_instances[:15],  # Limit to top 15
            heading_issues=heading_issues,
            uniform_paragraphs=uniform_paras,
            em_dashes=em_dash_instances[:20],  # Limit to top 20
            transitions=transition_instances[:15],  # Limit to top 15
            # Advanced detailed findings
            burstiness_issues=burstiness_issues[:10] if isinstance(burstiness_issues, list) else [],
            syntactic_issues=syntactic_issues[:20] if isinstance(syntactic_issues, list) else [],
            stylometric_issues=stylometric_issues[:15] if isinstance(stylometric_issues, list) else [],
            formatting_issues=formatting_issues[:15] if isinstance(formatting_issues, list) else [],
            high_predictability_segments=high_pred_segments[:10] if isinstance(high_pred_segments, list) else [],
        )

    def _analyze_ai_vocabulary_detailed(self) -> List[VocabInstance]:
        """Detect AI vocabulary with line numbers and context."""
        instances = []

        for line_num, line in enumerate(self.lines, start=1):
            # Skip HTML comments (metadata), headings, and code blocks
            if self._is_line_in_html_comment(line):
                continue
            if line.strip().startswith('#') or line.strip().startswith('```'):
                continue

            for pattern, suggestions in self.AI_VOCAB_REPLACEMENTS.items():
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    word = match.group()
                    # Extract context (20 chars each side)
                    start = max(0, match.start() - 20)
                    end = min(len(line), match.end() + 20)
                    context = f"...{line[start:end]}..."

                    instances.append(VocabInstance(
                        line_number=line_num,
                        word=word,
                        context=context,
                        full_line=line.strip(),
                        suggestions=suggestions[:5]  # Top 5 suggestions
                    ))

        return instances

    def _analyze_headings_detailed(self) -> List[HeadingIssue]:
        """Analyze headings with specific issues and line numbers."""
        issues = []
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

        for line_num, line in enumerate(self.lines, start=1):
            match = heading_pattern.match(line.strip())
            if not match:
                continue

            level_marks, text = match.groups()
            level = len(level_marks)
            words = text.split()
            word_count = len(words)

            # Check for issues
            issue_type = None
            problem = None
            suggestion = None

            # Verbose headings (>8 words)
            if word_count > 8:
                issue_type = 'verbose'
                problem = f'Heading too long ({word_count} words, typical: 3-6 words)'
                suggestion = 'Shorten to key concept: focus on 3-6 impactful words'

            # Deep hierarchy (H5, H6)
            elif level >= 5:
                issue_type = 'deep_hierarchy'
                problem = f'Deep hierarchy (H{level}, max recommended: H4)'
                suggestion = 'Restructure content to use H1-H4 only'

            # Parallel structure detection (all starting with same word at this level)
            # This is simplified - full implementation would track all headings at each level
            elif text.split()[0] in ['How', 'What', 'Why', 'Understanding', 'Exploring', 'Introduction']:
                issue_type = 'parallel'
                problem = 'Potentially mechanical parallel structure'
                suggestion = 'Vary heading styles: mix questions, statements, and imperatives'

            if issue_type:
                issues.append(HeadingIssue(
                    line_number=line_num,
                    level=level,
                    text=text,
                    issue_type=issue_type,
                    problem=problem,
                    suggestion=suggestion
                ))

        return issues

    def _analyze_sentence_uniformity_detailed(self) -> List[UniformParagraph]:
        """Detect unnaturally uniform paragraphs."""
        uniform_paragraphs = []

        # Split into paragraphs
        paragraphs = []
        current_para = []
        current_start_line = 1

        for line_num, line in enumerate(self.lines, start=1):
            stripped = line.strip()

            # Skip headings and code blocks
            if stripped.startswith('#') or stripped.startswith('```'):
                if current_para:
                    paragraphs.append((current_start_line, '\n'.join(current_para)))
                    current_para = []
                continue

            # Blank line = end of paragraph
            if not stripped:
                if current_para:
                    paragraphs.append((current_start_line, '\n'.join(current_para)))
                    current_para = []
                    current_start_line = line_num + 1
            else:
                if not current_para:
                    current_start_line = line_num
                current_para.append(line)

        # Add final paragraph
        if current_para:
            paragraphs.append((current_start_line, '\n'.join(current_para)))

        # Analyze sentence uniformity within each paragraph
        for start_line, para_text in paragraphs:
            if len(para_text) < 50:  # Skip short paragraphs
                continue

            # Split into sentences
            sent_pattern = re.compile(r'(?<=[.!?])\s+')
            sentences = [s.strip() for s in sent_pattern.split(para_text) if s.strip()]

            if len(sentences) < 3:
                continue

            # Count words per sentence
            sent_lengths = [len(re.findall(r"[\w'-]+", sent)) for sent in sentences]

            if not sent_lengths:
                continue

            # Calculate coefficient of variation
            mean_len = statistics.mean(sent_lengths)
            if mean_len == 0:
                continue
            stdev = statistics.stdev(sent_lengths) if len(sent_lengths) > 1 else 0
            cv = stdev / mean_len

            # Flag if too uniform (CV < 0.3 is AI-like)
            if cv < 0.3:
                uniform_paragraphs.append(UniformParagraph(
                    start_line=start_line,
                    sentence_count=len(sentences),
                    mean_length=round(mean_len, 1),
                    stdev=round(stdev, 1),
                    cv=round(cv, 2),
                    problem=f'Uniform sentence lengths (CV={cv:.2f}, typical human: >0.4)',
                    suggestion='Vary sentence length: mix short (5-10w), medium (15-25w), and long (30-45w) sentences'
                ))

        return uniform_paragraphs

    def _analyze_em_dashes_detailed(self) -> List[EmDashInstance]:
        """Detect em-dash usage with line numbers."""
        instances = []
        em_dash_pattern = re.compile(r'—|--')

        for line_num, line in enumerate(self.lines, start=1):
            # Skip HTML comments, headings, code blocks
            if self._is_line_in_html_comment(line):
                continue
            if line.strip().startswith('#') or line.strip().startswith('```'):
                continue

            for match in em_dash_pattern.finditer(line):
                # Extract context (40 chars each side)
                start = max(0, match.start() - 40)
                end = min(len(line), match.end() + 40)
                context = f"...{line[start:end]}..."

                instances.append(EmDashInstance(
                    line_number=line_num,
                    context=context,
                    problem='Em-dash overuse (ChatGPT uses 10x more than humans)',
                    suggestion='Replace with: comma, semicolon, period (new sentence), or parentheses'
                ))

        return instances

    def _analyze_transitions_detailed(self) -> List[TransitionInstance]:
        """Detect formulaic transitions with line numbers."""
        instances = []

        formulaic_patterns = [
            r'\bFurthermore,\b', r'\bMoreover,\b', r'\bAdditionally,\b',
            r'\bIn addition,\b', r'\bIt is important to note that\b',
            r'\bIt is worth mentioning that\b', r'\bWhen it comes to\b',
            r'\bOne of the key aspects\b', r'\bFirst and foremost,\b',
        ]

        for line_num, line in enumerate(self.lines, start=1):
            # Skip HTML comments, headings, code blocks
            if self._is_line_in_html_comment(line):
                continue
            if line.strip().startswith('#') or line.strip().startswith('```'):
                continue

            for pattern in formulaic_patterns:
                for match in re.finditer(pattern, line):
                    phrase = match.group()
                    # Extract context
                    start = max(0, match.start() - 20)
                    end = min(len(line), match.end() + 60)
                    context = f"...{line[start:end]}..."

                    # Get suggestions from TRANSITION_REPLACEMENTS
                    suggestions = self.TRANSITION_REPLACEMENTS.get(phrase, ['Rephrase naturally'])

                    instances.append(TransitionInstance(
                        line_number=line_num,
                        phrase=phrase,
                        context=context,
                        problem='Formulaic AI transition (humans use simpler connectives)',
                        suggestions=suggestions[:5]
                    ))

        return instances
