"""
Perplexity dimension analyzer.

Analyzes AI vocabulary usage and formulaic transitions - two of the strongest
signals for AI-generated content detection.
"""

import re
from typing import Dict, List, Any
from ai_pattern_analyzer.dimensions.base import DimensionAnalyzer
from ai_pattern_analyzer.core.results import VocabInstance, TransitionInstance
from ai_pattern_analyzer.utils.pattern_matching import AI_VOCABULARY, FORMULAIC_TRANSITIONS
from ai_pattern_analyzer.utils.text_processing import count_words
from ai_pattern_analyzer.scoring.dual_score import THRESHOLDS


# Replacement suggestions for AI vocabulary
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

# Transition replacements for suggestions
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


class PerplexityAnalyzer(DimensionAnalyzer):
    """Analyzes perplexity dimension - AI vocabulary and formulaic transitions."""

    def analyze(self, text: str, lines: List[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Analyze text for AI vocabulary and formulaic transitions.

        Args:
            text: Full text content
            lines: Text split into lines (optional)
            **kwargs: Additional parameters

        Returns:
            Dict with perplexity analysis results
        """
        ai_vocab = self._analyze_ai_vocabulary(text)
        formulaic = self._analyze_formulaic_transitions(text)

        return {
            'ai_vocabulary': ai_vocab,
            'formulaic_transitions': formulaic,
        }

    def analyze_detailed(self, lines: List[str], html_comment_checker=None) -> Dict[str, Any]:
        """
        Detailed analysis with line numbers and suggestions.

        Args:
            lines: Text split into lines
            html_comment_checker: Function to check if line is in HTML comment

        Returns:
            Dict with detailed analysis including instances
        """
        vocab_instances = self._analyze_ai_vocabulary_detailed(lines, html_comment_checker)
        transition_instances = self._analyze_transitions_detailed(lines, html_comment_checker)

        return {
            'vocab_instances': vocab_instances,
            'transition_instances': transition_instances,
        }

    def score(self, analysis_results: Dict[str, Any]) -> tuple:
        """
        Calculate perplexity score.

        Args:
            analysis_results: Results dict with ai_vocabulary_per_1k field

        Returns:
            Tuple of (score_value, score_label)
        """
        ai_per_1k = analysis_results.get('ai_vocabulary_per_1k', 0)

        if ai_per_1k <= THRESHOLDS.AI_VOCAB_MEDIUM_THRESHOLD:
            return (10.0, "HIGH")
        elif ai_per_1k <= THRESHOLDS.AI_VOCAB_LOW_THRESHOLD:
            return (7.0, "MEDIUM")
        elif ai_per_1k <= THRESHOLDS.AI_VOCAB_VERY_LOW_THRESHOLD:
            return (4.0, "LOW")
        else:
            return (2.0, "VERY LOW")

    def _analyze_ai_vocabulary(self, text: str) -> Dict:
        """Detect AI-characteristic vocabulary."""
        words_found = []
        for pattern in AI_VOCABULARY:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            words_found.extend([m.group() for m in matches])

        word_count = count_words(text)
        per_1k = (len(words_found) / word_count * 1000) if word_count > 0 else 0

        return {
            'count': len(words_found),
            'per_1k': round(per_1k, 2),
            'words': words_found[:20]  # Limit to first 20 for readability
        }

    def _analyze_formulaic_transitions(self, text: str) -> Dict:
        """Detect formulaic transitions."""
        transitions_found = []
        for pattern in FORMULAIC_TRANSITIONS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            transitions_found.extend([m.group() for m in matches])

        return {
            'count': len(transitions_found),
            'transitions': transitions_found[:15]
        }

    def _analyze_ai_vocabulary_detailed(self, lines: List[str], html_comment_checker=None) -> List[VocabInstance]:
        """Detect AI vocabulary with line numbers and context."""
        instances = []

        for line_num, line in enumerate(lines, start=1):
            # Skip HTML comments, headings, and code blocks
            if html_comment_checker and html_comment_checker(line):
                continue
            if line.strip().startswith('#') or line.strip().startswith('```'):
                continue

            for pattern, suggestions in AI_VOCAB_REPLACEMENTS.items():
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

    def _analyze_transitions_detailed(self, lines: List[str], html_comment_checker=None) -> List[TransitionInstance]:
        """Detect formulaic transitions with context."""
        instances = []

        for line_num, line in enumerate(lines, start=1):
            # Skip HTML comments and headings
            if html_comment_checker and html_comment_checker(line):
                continue
            if line.strip().startswith('#'):
                continue

            for pattern in FORMULAIC_TRANSITIONS:
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    transition = match.group()
                    # Get full sentence context
                    context = line.strip()

                    # Get suggestions from mapping (case-insensitive lookup)
                    suggestions = None
                    for key, values in TRANSITION_REPLACEMENTS.items():
                        if transition.lower() == key.lower():
                            suggestions = values
                            break

                    if suggestions is None:
                        suggestions = ['Remove transition entirely', 'Use natural flow']

                    instances.append(TransitionInstance(
                        line_number=line_num,
                        transition=transition,
                        context=context,
                        suggestions=suggestions[:5]
                    ))

        return instances
