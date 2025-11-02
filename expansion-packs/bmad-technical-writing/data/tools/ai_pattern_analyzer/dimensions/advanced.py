"""
Advanced dimension analyzer.

Analyzes advanced AI detection patterns:
- GLTR (Giant Language Model Test Room) analysis - 95% accuracy
- HDD (Hypergeometric Distribution D) - robust lexical diversity
- Yule's K - vocabulary richness via frequency distribution
- MATTR (Moving Average Type-Token Ratio) - window-based diversity
- RTTR (Root Type-Token Ratio) - length-independent measure
- Token probability distribution
- Entropy analysis
- High-predictability segment detection

Requires optional dependencies: transformers, torch, scipy, textacy, spacy

Research: Advanced metrics provide +8-10% accuracy improvement over basic features.
"""

import re
import sys
import math
import statistics
from typing import Dict, List, Any, Optional
from collections import Counter
from ai_pattern_analyzer.dimensions.base import DimensionAnalyzer
from ai_pattern_analyzer.core.results import HighPredictabilitySegment
from ai_pattern_analyzer.scoring.dual_score import THRESHOLDS
from ai_pattern_analyzer.utils.text_processing import safe_ratio

# Required imports (no longer optional)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.utils import logging as transformers_logging
transformers_logging.set_verbosity_error()

from scipy.stats import hypergeom

import spacy
nlp_spacy = spacy.load('en_core_web_sm')

import textacy
from textacy import text_stats


# Global model instances (lazy loading)
_perplexity_model = None
_perplexity_tokenizer = None


class AdvancedAnalyzer(DimensionAnalyzer):
    """Analyzes advanced dimension - GLTR, HDD, MATTR, transformer-based detection."""

    def analyze(self, text: str, lines: List[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Analyze text for advanced AI patterns.

        Args:
            text: Full text content
            lines: Text split into lines (optional)
            **kwargs: Additional parameters

        Returns:
            Dict with advanced analysis results
        """
        results = {}

        # GLTR analysis
        gltr_metrics = self._calculate_gltr_metrics(text)
        results.update(gltr_metrics)

        # Advanced lexical diversity
        advanced_lexical = self._calculate_advanced_lexical_diversity(text)
        results.update(advanced_lexical)

        # Textacy metrics
        textacy_metrics = self._calculate_textacy_lexical_diversity(text)
        results.update(textacy_metrics)

        results['available'] = True
        return results

    def analyze_detailed(self, lines: List[str], html_comment_checker=None) -> List[HighPredictabilitySegment]:
        """
        Detailed analysis with line numbers and suggestions.

        Args:
            lines: Text split into lines
            html_comment_checker: Function to check if line is in HTML comment

        Returns:
            List of HighPredictabilitySegment objects
        """
        return self._analyze_high_predictability_segments_detailed(lines, html_comment_checker)

    def score(self, analysis_results: Dict[str, Any]) -> tuple:
        """
        Calculate advanced analysis score.

        Args:
            analysis_results: Results dict with advanced metrics

        Returns:
            Tuple of (score_value, score_label)
        """
        if not analysis_results.get('available', False):
            return (5.0, "UNAVAILABLE")

        # Score based on GLTR if available
        gltr_top10 = analysis_results.get('gltr_top10_percentage', 0.55)

        # AI signature: >70% top-10, Human: <55%
        if gltr_top10 < 0.50:
            return (10.0, "HIGH")  # Very human-like
        elif gltr_top10 < 0.60:
            return (7.0, "MEDIUM")
        elif gltr_top10 < 0.70:
            return (4.0, "LOW")
        else:
            return (2.0, "VERY LOW")  # Strong AI signature

    def _calculate_gltr_metrics(self, text: str) -> Dict:
        """
        Calculate GLTR (Giant Language Model Test Room) metrics.

        GLTR analyzes where each token ranks in the model's probability distribution.
        AI-generated text shows high concentration of top-10 tokens (>70%).
        Human writing is more unpredictable (<55%).

        Research: 95% accuracy on GPT-3/ChatGPT detection.
        """
        try:
            global _perplexity_model, _perplexity_tokenizer

            # Lazy load model if not already loaded
            if _perplexity_model is None:
                print("Loading DistilGPT-2 model for GLTR analysis (one-time setup)...", file=sys.stderr)
                _perplexity_model = AutoModelForCausalLM.from_pretrained('distilgpt2')
                _perplexity_tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
                _perplexity_model.eval()

            # Remove code blocks and limit length
            text = re.sub(r'```[\s\S]*?```', '', text)
            text = text[:2000]  # GLTR on first 2000 chars (faster)

            # Tokenize
            tokens = _perplexity_tokenizer.encode(text)

            if len(tokens) < 10:
                return {}  # Not enough tokens for reliable analysis

            ranks = []

            # Analyze each token's rank in model prediction
            for i in range(1, min(len(tokens), 500)):  # Limit to 500 tokens for speed
                input_ids = torch.tensor([tokens[:i]])

                with torch.no_grad():
                    outputs = _perplexity_model(input_ids)
                    logits = outputs.logits[0, -1, :]
                    probs = torch.softmax(logits, dim=-1)

                    # Get rank of actual next token
                    sorted_indices = torch.argsort(probs, descending=True)
                    actual_token = tokens[i]
                    rank = (sorted_indices == actual_token).nonzero(as_tuple=True)[0].item()
                    ranks.append(rank)

            if not ranks:
                return {}

            # Calculate GLTR metrics
            top10_percentage = safe_ratio(sum(1 for r in ranks if r < 10), len(ranks), 0)
            top100_percentage = safe_ratio(sum(1 for r in ranks if r < 100), len(ranks), 0)
            mean_rank = sum(ranks) / len(ranks)
            rank_variance = statistics.variance(ranks) if len(ranks) > 1 else 0

            # AI likelihood based on top-10 concentration
            # Research: AI >70%, Human <55%
            if top10_percentage > 0.70:
                ai_likelihood = 0.90
            elif top10_percentage > 0.65:
                ai_likelihood = 0.75
            elif top10_percentage > 0.60:
                ai_likelihood = 0.60
            elif top10_percentage < 0.50:
                ai_likelihood = 0.20
            else:
                ai_likelihood = 0.50

            return {
                'gltr_top10_percentage': round(top10_percentage, 3),
                'gltr_top100_percentage': round(top100_percentage, 3),
                'gltr_mean_rank': round(mean_rank, 2),
                'gltr_rank_variance': round(rank_variance, 2),
                'gltr_likelihood': round(ai_likelihood, 2)
            }
        except Exception as e:
            print(f"Warning: GLTR analysis failed: {e}", file=sys.stderr)
            return {}

    def _calculate_advanced_lexical_diversity(self, text: str) -> Dict:
        """
        Calculate advanced lexical diversity metrics using scipy.

        HDD (Hypergeometric Distribution D):
        - Most robust lexical diversity metric
        - AI: 0.40-0.55, Human: 0.65-0.85
        - Accounts for text length and vocabulary distribution

        Yule's K:
        - Vocabulary richness via frequency distribution
        - AI: 100-150, Human: 60-90
        - Lower = more diverse, higher = more repetitive

        Research: +8% accuracy improvement over TTR/MTLD
        """
        try:
            # Remove code blocks and extract words
            text = re.sub(r'```[\s\S]*?```', '', text)
            words = re.findall(r'\b[a-z]{3,}\b', text.lower())

            if len(words) < 50:
                return {}  # Not enough text for reliable metrics

            # Calculate word frequencies
            word_freq = Counter(words)
            N = len(words)  # Total tokens
            V = len(word_freq)  # Unique tokens (types)

            # ============================================================
            # 1. HDD (Hypergeometric Distribution D)
            # ============================================================
            # HDD = (sum of P(word drawn at least once in 42-token sample))
            # More robust than TTR because it's sample-size independent
            sample_size = 42  # Standard HDD sample size
            if N < sample_size:
                hdd_score = None
            else:
                hdd_sum = 0.0
                for word, count in word_freq.items():
                    # Probability word is NOT drawn in sample
                    # P(not drawn) = hypergeom.pmf(0, N, count, sample_size)
                    prob_not_drawn = hypergeom.pmf(0, N, count, sample_size)
                    # P(drawn at least once) = 1 - P(not drawn)
                    prob_drawn = 1.0 - prob_not_drawn
                    hdd_sum += prob_drawn

                hdd_score = round(hdd_sum / V, 3)

            # ============================================================
            # 2. Yule's K (Vocabulary Richness)
            # ============================================================
            # K = 10^4 * (M2 - M1) / M1^2
            # where M1 = sum of frequencies, M2 = sum of (freq * (freq - 1))
            M1 = N
            M2 = sum(freq * (freq - 1) for freq in word_freq.values())

            if M1 > 0:
                yules_k = 10000 * (M2 - M1) / (M1 ** 2)
                yules_k = round(yules_k, 2)
            else:
                yules_k = None

            # ============================================================
            # 3. Maas (Length-Corrected TTR)
            # ============================================================
            # Maas = (log(N) - log(V)) / log(N)^2
            # Less affected by text length than raw TTR
            if N > 0 and V > 0:
                maas_score = (math.log(N) - math.log(V)) / (math.log(N) ** 2)
                maas_score = round(maas_score, 3)
            else:
                maas_score = None

            # ============================================================
            # 4. Vocabulary Concentration (Zipfian Analysis)
            # ============================================================
            # Measure how concentrated vocabulary is in high-frequency words
            # AI text tends to have higher concentration (more repetitive)
            sorted_freqs = sorted(word_freq.values(), reverse=True)
            top_10_percent = max(1, V // 10)
            top_10_concentration = sum(sorted_freqs[:top_10_percent]) / N

            return {
                'hdd_score': hdd_score,
                'yules_k': yules_k,
                'maas_score': maas_score,
                'vocab_concentration': round(top_10_concentration, 3)
            }
        except Exception as e:
            print(f"Warning: Advanced lexical diversity calculation failed: {e}", file=sys.stderr)
            return {}

    def _calculate_textacy_lexical_diversity(self, text: str) -> Dict:
        """
        Calculate MATTR and RTTR using textacy (Advanced lexical diversity metrics).

        MATTR (Moving Average Type-Token Ratio):
        - Window size 100 (research-validated default)
        - AI: <0.65, Human: ≥0.70
        - 0.89 correlation with human judgments (McCarthy & Jarvis, 2010)

        RTTR (Root Type-Token Ratio):
        - RTTR = Types / √Tokens
        - Length-independent measure
        - AI: <7.5, Human: ≥7.5

        Returns:
            Dict with mattr, rttr, scores, and assessments
        """
        try:
            # Remove code blocks for accurate text analysis
            text_clean = re.sub(r'```[\s\S]*?```', '', text)

            # Process with spaCy
            doc = nlp_spacy(text_clean[:100000])  # Limit for performance

            # Calculate MATTR (window size 100 is research-validated)
            try:
                mattr = text_stats.mattr(doc, window_size=100)
            except Exception:
                # Fallback if text too short for window size 100
                mattr = 0.0

            # Calculate RTTR
            # Count only alphabetic tokens for consistency
            tokens = [token for token in doc if token.is_alpha and not token.is_stop]
            types = set([token.text.lower() for token in tokens])
            n_tokens = len(tokens)
            n_types = len(types)

            rttr = n_types / (n_tokens ** 0.5) if n_tokens > 0 else 0.0

            # Score MATTR (12 points max)
            if mattr >= 0.75:
                mattr_score, mattr_assessment = 12.0, 'EXCELLENT'
            elif mattr >= 0.70:
                mattr_score, mattr_assessment = 9.0, 'GOOD'
            elif mattr >= 0.65:
                mattr_score, mattr_assessment = 5.0, 'FAIR'
            else:
                mattr_score, mattr_assessment = 0.0, 'POOR'

            # Score RTTR (8 points max)
            if rttr >= 8.5:
                rttr_score, rttr_assessment = 8.0, 'EXCELLENT'
            elif rttr >= 7.5:
                rttr_score, rttr_assessment = 6.0, 'GOOD'
            elif rttr >= 6.5:
                rttr_score, rttr_assessment = 3.0, 'FAIR'
            else:
                rttr_score, rttr_assessment = 0.0, 'POOR'

            return {
                'available': True,
                'mattr': round(mattr, 3),
                'mattr_score': mattr_score,
                'mattr_assessment': mattr_assessment,
                'rttr': round(rttr, 2),
                'rttr_score': rttr_score,
                'rttr_assessment': rttr_assessment,
                'types': n_types,
                'tokens': n_tokens
            }
        except Exception as e:
            print(f"Warning: Textacy lexical diversity calculation failed: {e}", file=sys.stderr)
            return {
                'available': False,
                'mattr': 0.0,
                'mattr_score': 0.0,
                'mattr_assessment': 'ERROR',
                'rttr': 0.0,
                'rttr_score': 0.0,
                'rttr_assessment': 'ERROR'
            }

    def _analyze_high_predictability_segments_detailed(self, lines: List[str], html_comment_checker=None) -> List[HighPredictabilitySegment]:
        """Identify text segments with high GLTR scores (AI-like predictability)."""
        issues = []

        try:
            global _perplexity_model, _perplexity_tokenizer

            if _perplexity_model is None:
                # Model not loaded yet
                return []

            # Analyze in 50-100 word chunks
            chunk_size = 75  # words
            current_chunk = []
            chunk_start_line = 1

            for line_num, line in enumerate(lines, start=1):
                stripped = line.strip()

                # Skip HTML comments (metadata), headings, and code blocks
                if html_comment_checker and html_comment_checker(line):
                    continue
                if stripped.startswith('#') or stripped.startswith('```'):
                    continue

                if stripped:
                    words = re.findall(r'\b\w+\b', stripped)
                    current_chunk.extend(words)

                    if len(current_chunk) >= chunk_size:
                        # Analyze this chunk
                        chunk_text = ' '.join(current_chunk)

                        # Calculate GLTR for chunk
                        try:
                            tokens = _perplexity_tokenizer.encode(chunk_text, add_special_tokens=True)
                            if len(tokens) < 10:
                                current_chunk = []
                                chunk_start_line = line_num + 1
                                continue

                            ranks = []
                            for i in range(1, min(len(tokens), 100)):
                                input_ids = torch.tensor([tokens[:i]])
                                with torch.no_grad():
                                    outputs = _perplexity_model(input_ids)
                                    logits = outputs.logits[0, -1, :]
                                    probs = torch.softmax(logits, dim=-1)
                                    sorted_indices = torch.argsort(probs, descending=True)
                                    actual_token = tokens[i]
                                    rank = (sorted_indices == actual_token).nonzero(as_tuple=True)[0].item()
                                    ranks.append(rank)

                            if ranks:
                                top10_pct = sum(1 for r in ranks if r < 10) / len(ranks)

                                # High predictability: >70% in top-10
                                if top10_pct > 0.70:
                                    preview = chunk_text[:150] + '...' if len(chunk_text) > 150 else chunk_text
                                    issues.append(HighPredictabilitySegment(
                                        start_line=chunk_start_line,
                                        end_line=line_num,
                                        segment_preview=preview,
                                        gltr_score=top10_pct,
                                        problem=f'High predictability (GLTR={top10_pct:.2f}, AI threshold >0.70)',
                                        suggestion='Rewrite with less common word choices, vary sentence structure, add unexpected turns'
                                    ))

                        except Exception as e:
                            print(f"Warning: GLTR chunk analysis failed: {e}", file=sys.stderr)

                        # Reset chunk
                        current_chunk = []
                        chunk_start_line = line_num + 1

        except Exception as e:
            print(f"Warning: High predictability segment analysis failed: {e}", file=sys.stderr)

        return issues
