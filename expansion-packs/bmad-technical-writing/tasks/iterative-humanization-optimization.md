# Task: Iterative Humanization Optimization

<!-- Powered by BMAD™ Core -->

## Purpose

Systematically optimize AI-generated content through iterative humanization passes until dual score targets are met. Uses the AI Pattern Analysis Tool's dual scoring system (Quality Score + Detection Risk) to guide incremental improvements and track progress toward publication-ready quality.

## When to Use This Task

- **For AI-generated content** that needs to reach specific quality targets
- When you want **systematic, measurable improvement** rather than one-pass editing
- For **high-stakes content** (book chapters, publications, client deliverables)
- When content needs to meet **publisher or compliance standards**
- To **track humanization effectiveness** quantitatively across iterations
- When initial analysis shows **substantial work needed** (Quality < 70)

## Prerequisites

- Python 3.7+ installed (Python 3.9+ recommended)
- AI Pattern Analysis Tool with dual scoring (`{{config.root}}/tools/analyze_ai_patterns.py`)
- Python virtual environment set up with required dependencies (see analyze-ai-patterns.md task for setup)
- AI-generated content ready for humanization
- Clear understanding of target scores (defaults: Quality ≥85, Detection ≤30)
- 1-3 hours budgeted for iterative optimization (varies by content quality)

## Target Scores

**Default Publication Targets**:

- **Quality Score**: ≥85 (EXCELLENT - Minimal AI signatures)
- **Detection Risk**: ≤30 (MEDIUM or better - May be flagged by some detectors)

**Adjustable Based on Context**:

- **Stricter** (book chapters): Quality ≥90, Detection ≤20
- **Standard** (blog posts): Quality ≥85, Detection ≤30
- **Relaxed** (drafts/internal): Quality ≥75, Detection ≤40

## Workflow Steps

### 0. Environment Setup (First Time Only)

**CRITICAL**: Complete Python environment setup before first use.

See `analyze-ai-patterns.md` task Step 0 for complete setup instructions, or run:

```bash
cd {{config.root}}/tools
python3 -m venv nlp-env
source nlp-env/bin/activate
pip install -r requirements.txt
python -m nltk.downloader punkt punkt_tab vader_lexicon
python -m spacy download en_core_web_sm
```

### 1. Load Configuration and Set Targets

**Read configuration**:

```yaml
# From .bmad-technical-writing/config.yaml
config.manuscript.root
config.manuscript.chapters
config.manuscript.sections
```

**Define optimization targets**:

- **Content type**: Book chapter / Blog post / Documentation / Tutorial
- **Quality target**: Default 85, adjust based on stakes (75-95)
- **Detection target**: Default 30, adjust based on requirements (15-40)
- **Maximum iterations**: Default 5, adjust based on time budget
- **Minimum improvement threshold**: Default +5 quality points per iteration

**Document targets**:

```
Optimization Targets for {{content_name}}:
- Quality Score Target: ≥{{quality_target}}
- Detection Risk Target: ≤{{detection_target}}
- Maximum Iterations: {{max_iterations}}
- Time Budget: {{time_budget}} hours
```

### 2. Baseline Analysis - Iteration 0

**Activate environment**:

```bash
cd {{config.root}}/tools
source nlp-env/bin/activate
```

**Run initial dual score analysis**:

```bash
python analyze_ai_patterns.py PATH_TO_FILE \
  --show-scores \
  --quality-target {{quality_target}} \
  --detection-target {{detection_target}} \
  --domain-terms "Domain,Specific,Terms" \
  > iteration-0-baseline.txt
```

**Example**:

```bash
python analyze_ai_patterns.py ../manuscript/chapters/chapter-03.md \
  --show-scores \
  --quality-target 85 \
  --detection-target 30 \
  --domain-terms "Docker,Kubernetes,PostgreSQL" \
  > chapter-03-iteration-0.txt
```

**Review output and document baseline**:

- Current Quality Score: {{quality_0}}
- Current Detection Risk: {{detection_0}}
- Quality Gap: {{quality_target}} - {{quality_0}} = {{quality_gap}}
- Detection Gap: {{detection_0}} - {{detection_target}} = {{detection_gap}}

**Historical tracking automatically created**:

- Score history saved to: `{{file_parent}}/.score-history/{{filename}}.history.json`
- Trend will show on subsequent runs

### 3. Review Path-to-Target Recommendations

**From dual score output, note the path-to-target actions** (sorted by ROI):

Example output:

```
PATH TO TARGET (4 actions, sorted by ROI)
────────────────────────────────────────────────────────────────────────────────

1. GLTR Token Ranking (Effort: HIGH)
   Current: 3.0/12.0 → Gain: +9.0 pts → Cumulative: 76.8
   Action: Rewrite high-predictability segments (>70% top-10 tokens)

2. Burstiness (Sentence Variation) (Effort: MEDIUM)
   Current: 9.0/12.0 → Gain: +3.0 pts → Cumulative: 79.8
   Action: Improve Burstiness (Sentence Variation)

3. AI Detection Ensemble (Effort: HIGH)
   Current: 5.0/10.0 → Gain: +5.0 pts → Cumulative: 84.8
   Action: Increase emotional variation (sentiment variance > 0.15)

4. Advanced Lexical (HDD/Yule's K) (Effort: HIGH)
   Current: 4.0/8.0 → Gain: +4.0 pts → Cumulative: 88.8
   Action: Increase vocabulary diversity (target HDD > 0.65)
```

**Create prioritized action plan**:

- **Iteration 1 Focus**: Top 1-2 actions from path-to-target (highest ROI)
- **Effort Level**: Note LOW/MEDIUM/HIGH for time planning
- **Expected Gain**: Sum potential gains from selected actions
- **Estimated Time**: 20-45 min depending on effort levels

### 4. Iteration Loop - Execute and Measure

**FOR EACH ITERATION (until targets met OR max iterations reached)**:

#### 4.1. Execute Humanization Pass

**Apply techniques from path-to-target recommendations**:

**For LOW effort actions** (15-30 min):

- Heading hierarchy flattening
- Em-dash reduction
- Formatting pattern fixes
- Stylometric marker removal

**For MEDIUM effort actions** (30-45 min):

- Sentence variation editing
- Perplexity (vocabulary) improvements
- Structure and transitions
- List-to-prose conversion

**For HIGH effort actions** (45-90 min):

- GLTR token ranking improvements (rewrite predictable segments)
- Advanced lexical diversity (sophisticated vocabulary expansion)
- Voice & authenticity injection
- AI detection ensemble (emotional variation)
- Syntactic complexity enhancement

**Use targeted humanization**:

- Refer to `humanize-post-generation.md` for specific techniques
- Focus ONLY on dimensions flagged in path-to-target
- Don't over-edit areas already scoring well
- Preserve technical accuracy at all times

**Document changes made**:

```
Iteration {{N}} Changes:
- Action 1: [What you did]
- Action 2: [What you did]
- Estimated effort: {{minutes}} minutes
- Focus dimensions: [List dimensions targeted]
```

#### 4.2. Re-analyze After Changes

**Run dual score analysis again** (environment should still be activated):

```bash
python analyze_ai_patterns.py PATH_TO_FILE \
  --show-scores \
  --quality-target {{quality_target}} \
  --detection-target {{detection_target}} \
  > iteration-{{N}}-analysis.txt
```

**Review updated scores**:

```
Iteration {{N}} Results:
- Quality Score: {{quality_N}} (was {{quality_N-1}}, change: {{quality_change}})
- Detection Risk: {{detection_N}} (was {{detection_N-1}}, change: {{detection_change}})
- Quality Gap Remaining: {{quality_target - quality_N}}
- Detection Gap Remaining: {{detection_N - detection_target}}
```

**Check historical trend automatically displayed**:

```
HISTORICAL TREND ({{N+1}} scores tracked)
────────────────────────────────────────────────────────────────────────────────

Quality:   IMPROVING (+3.2 pts)
Detection: IMPROVING (-5.1 pts)
```

#### 4.3. Evaluate Progress and Decide

**Check termination conditions**:

**✅ SUCCESS - Stop iterating if**:

- Quality Score ≥ {{quality_target}} AND
- Detection Risk ≤ {{detection_target}}
- → Document success and finalize

**🔄 CONTINUE - Another iteration if**:

- Targets not yet met AND
- Iteration < {{max_iterations}} AND
- Last iteration showed improvement (≥+5 quality points OR -5 detection points)
- → Proceed to next iteration focusing on next path-to-target actions

**⚠️ PLATEAU - Escalate if**:

- Two consecutive iterations with minimal improvement (<+3 quality points)
- OR reaching iteration limit without meeting targets
- → Consider: Regeneration with humanization prompt, alternative techniques, or accepting current quality

**❌ REGRESSION - Investigate if**:

- Quality score decreased OR detection risk increased
- → Likely over-editing or technical accuracy issues
- → Revert last changes and try different approach

### 5. Final Validation and Documentation

**When targets achieved, perform final checks**:

**Technical Accuracy Verification**:

- [ ] Code examples tested and functional
- [ ] Technical terminology correct
- [ ] Version numbers and specifics intact
- [ ] No facts altered during optimization
- [ ] Procedures and commands validated

**Qualitative Read-Aloud Test**:

- [ ] Read 3-5 paragraphs aloud
- [ ] Natural flow and rhythm
- [ ] No awkward phrasings
- [ ] Varied sentence rhythm
- [ ] Authentic voice present

**Document final results**:

```
Optimization Complete for {{content_name}}

Baseline (Iteration 0):
- Quality: {{quality_0}} ({{quality_0_interpretation}})
- Detection: {{detection_0}} ({{detection_0_interpretation}})

Final (Iteration {{N}}):
- Quality: {{quality_final}} ({{quality_final_interpretation}})
- Detection: {{detection_final}} ({{detection_final_interpretation}})

Improvement:
- Quality: +{{quality_improvement}} points ({{improvement_percentage}}%)
- Detection: {{detection_improvement}} points
- Iterations: {{total_iterations}}
- Total Time: {{total_time}} minutes

Path to Success:
Iteration 1: {{summary}}
Iteration 2: {{summary}}
...

Lessons Learned:
- {{lesson_1}}
- {{lesson_2}}
```

### 6. Score History Management

**Historical tracking is automatic**:

- Scores saved to: `{{file_parent}}/.score-history/{{filename}}.history.json`
- Trend displayed on each analysis run
- No manual management needed

**View full history**:

```bash
cat {{file_parent}}/.score-history/{{filename}}.history.json
```

**Example history file**:

```json
{
  "file_path": "/path/to/chapter-03.md",
  "scores": [
    {
      "timestamp": "2025-01-15T10:30:00",
      "quality_score": 67.8,
      "detection_risk": 38.8,
      "quality_interpretation": "MIXED - Needs moderate work",
      "detection_interpretation": "MEDIUM - May be flagged",
      "total_words": 4532,
      "notes": ""
    },
    {
      "timestamp": "2025-01-15T11:45:00",
      "quality_score": 79.2,
      "detection_risk": 25.3,
      "quality_interpretation": "GOOD - Natural with minor tells",
      "detection_interpretation": "LOW - Unlikely flagged",
      "total_words": 4581,
      "notes": ""
    }
  ]
}
```

## Output Deliverables

**Required**:

- Iteration analysis reports (iteration-0, iteration-1, etc.)
- Final optimized content meeting targets
- Optimization summary with before/after metrics
- Lessons learned for future content

**Recommended**:

- Iteration change logs (what was done each pass)
- Time tracking per iteration
- Score history visualization (if applicable)

**Optional**:

- Technical accuracy verification report
- Read-aloud test notes
- Side-by-side before/after comparison

## Success Criteria

✅ Target scores achieved (Quality ≥{{quality_target}}, Detection ≤{{detection_target}})
✅ Technical accuracy preserved 100%
✅ Content reads naturally (passes read-aloud test)
✅ Improvement documented and quantified
✅ Iterative process tracked with clear progression
✅ Lessons learned captured for future optimization

## Common Pitfalls to Avoid

❌ **Changing too much in one iteration** - Makes it hard to understand what worked
❌ **Ignoring path-to-target priorities** - Wastes effort on low-ROI changes
❌ **Over-editing** - Can introduce awkwardness or technical errors
❌ **Skipping re-analysis** - Can't measure improvement without data
❌ **Continuing past plateau** - Know when to stop or try different approach
❌ **Sacrificing accuracy for scores** - Technical correctness always comes first
❌ **Not documenting changes** - Loses valuable learning for future content

## Integration with Other Tasks

**Pre-requisites**:

1. `analyze-ai-patterns.md` - Understand tool and scoring system

**During optimization**:

1. `humanize-post-generation.md` - Specific humanization techniques
2. `humanization-qa-check.md` - Additional quality checks (optional, each iteration)

**After optimization**:

1. `copy-edit-chapter.md` - Final polish
2. Technical review - Verify accuracy preserved

## Quick Reference - Typical Optimization Flow

```
ITERATION 0 (Baseline)
├─ Run: --show-scores
├─ Quality: 67.8, Detection: 38.8
├─ Gap: Need +17.2 quality, -8.8 detection
└─ Path: Focus on GLTR (9pts) + Burstiness (3pts)

ITERATION 1 (High-Impact Actions)
├─ Apply: Rewrite high-predictability segments, vary sentences
├─ Time: 45 minutes
├─ Run: --show-scores
├─ Quality: 79.2 (+11.4), Detection: 25.3 (-13.5)
├─ Gap: Need +5.8 quality, TARGET MET for detection ✓
└─ Path: Focus on Voice (6pts) + Heading (2.5pts)

ITERATION 2 (Remaining Gap)
├─ Apply: Add personal perspective, flatten headings
├─ Time: 30 minutes
├─ Run: --show-scores
├─ Quality: 86.5 (+7.3), Detection: 22.1 (-3.2)
├─ TARGETS MET ✓✓
└─ Final validation → Publication ready

Total: 2 iterations, 75 minutes, +18.7 quality points
```

## Tool Command Reference

```bash
# Environment activation (every session)
cd {{config.root}}/tools
source nlp-env/bin/activate  # macOS/Linux
# OR nlp-env\Scripts\activate  # Windows

# Baseline analysis
python analyze_ai_patterns.py FILE.md --show-scores \
  --quality-target 85 --detection-target 30 \
  --domain-terms "Term1,Term2,Term3" \
  > iteration-0-baseline.txt

# Subsequent iterations (same command)
python analyze_ai_patterns.py FILE.md --show-scores \
  --quality-target 85 --detection-target 30 \
  > iteration-N-analysis.txt

# JSON output for automation
python analyze_ai_patterns.py FILE.md --show-scores --format json \
  > iteration-N.json

# Deactivate when done
deactivate
```

## Time Estimates by Starting Quality

| Starting Quality  | Target 85 | Iterations | Estimated Time |
| ----------------- | --------- | ---------- | -------------- |
| 40-50 (AI-LIKE)   | ✓         | 4-5        | 2.5-3.5 hours  |
| 50-70 (MIXED)     | ✓         | 3-4        | 1.5-2.5 hours  |
| 70-80 (GOOD)      | ✓         | 2-3        | 1-1.5 hours    |
| 80-85 (EXCELLENT) | ✓         | 1-2        | 0.5-1 hour     |

_Note: Times include analysis + editing. Higher starting quality requires fewer, shorter iterations._

## Notes

- **Dual scoring is optimization-friendly**: Path-to-target shows exactly what to improve
- **Historical tracking is automatic**: No manual score tracking needed
- **ROI-based prioritization**: Focus on high-gain, low-effort actions first
- **Plateau detection**: Know when diminishing returns mean it's time to stop
- **Measurable progress**: Unlike subjective assessment, dual scores are quantifiable
- **Context-appropriate targets**: Adjust based on content type and stakes
- **Effort estimation built-in**: Each action tagged LOW/MEDIUM/HIGH for planning
- **Iterative > one-pass**: Multiple small improvements often better than one large edit
