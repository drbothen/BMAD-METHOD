<!-- Powered by BMAD™ Core -->

# Performance Review

---

task:
id: performance-review
name: Performance Review
description: Analyze code example performance to identify bottlenecks and optimization opportunities
persona_default: technical-reviewer
inputs: - code_path - performance_targets - language
steps: - Identify code to analyze and performance targets - Review performance-considerations-checklist.md - Set up profiling tools for the language - Create performance benchmarks - Profile code execution (time, memory, CPU) - Analyze results against targets and best practices - Identify performance bottlenecks - Provide optimization recommendations - Generate performance analysis report
output: docs/performance/performance-report.md

---

## Purpose

This task guides you through analyzing the performance characteristics of code examples to ensure they demonstrate efficient patterns and avoid performance anti-patterns. Technical books should teach not just correctness but also performance-aware coding.

## Prerequisites

Before starting this task:

- Code examples have been created and are working correctly
- Target programming language(s) identified
- Performance targets defined (if any)
- Access to profiling tools for target language(s)
- Access to performance-considerations-checklist.md
- Understanding of algorithm complexity and performance patterns

## Workflow Steps

### 1. Identify Code and Performance Targets

Define what will be analyzed:

**Code Inventory:**

- List all code files to analyze
- Identify performance-critical code
- Note algorithms and data structures used
- Flag database queries
- Identify I/O operations
- Note concurrent/parallel operations

**Performance Targets:**

Set appropriate expectations:

- **Execution time**: Acceptable runtime for typical inputs
- **Memory usage**: Maximum memory consumption
- **CPU usage**: CPU efficiency expectations
- **Scalability**: How performance changes with input size
- **Response time**: For web/API examples

**Priority Assessment:**

- **High priority**: Algorithms, database queries, loops over large data
- **Medium priority**: I/O operations, API calls
- **Low priority**: Simple calculations, one-time setup

**Context Consideration:**

Remember this is educational code:

- Clarity often trumps micro-optimizations
- Demonstrate good patterns, not extreme optimization
- Avoid anti-patterns and obvious inefficiencies
- Balance educational value with performance

### 2. Review Performance Considerations

Use performance-considerations-checklist.md to understand what to look for:

**Algorithm Efficiency:**

- [ ] Appropriate time complexity
- [ ] Efficient data structures
- [ ] No unnecessary iterations
- [ ] Early termination where possible

**Database Performance:**

- [ ] No N+1 query problems
- [ ] Appropriate indexing mentioned
- [ ] Query optimization shown
- [ ] Connection pooling used

**Memory Management:**

- [ ] No obvious memory leaks
- [ ] Efficient data structure usage
- [ ] Resource cleanup demonstrated

**Caching:**

- [ ] Caching used where appropriate
- [ ] Cache invalidation handled

**Network Performance:**

- [ ] API calls minimized
- [ ] Batch operations used
- [ ] Async operations for I/O

### 3. Set Up Profiling Tools

Install appropriate tools for the language:

#### JavaScript/Node.js

**Built-in Profiler:**

```bash
# V8 profiler
node --prof app.js
node --prof-process isolate-*.log > processed.txt

# Chrome DevTools
node --inspect app.js
# Then open chrome://inspect
```

**Tools:**

```bash
# Install clinic.js for comprehensive profiling
npm install -g clinic

# Flame graphs
clinic flame -- node app.js

# Memory leaks
clinic doctor -- node app.js

# Performance benchmarking
npm install -D benchmark
```

**Memory Profiling:**

```bash
# Heap snapshot
node --inspect --heap-prof app.js

# Memory usage tracking
node --trace-gc app.js
```

#### Python

**Built-in Profiler:**

```python
# cProfile (built-in)
python -m cProfile -o profile.stats script.py

# Analyze results
python -m pstats profile.stats
```

**Tools:**

```bash
# Install profiling tools
pip install memory_profiler line_profiler py-spy

# Line-by-line profiling
kernprof -l -v script.py

# Memory profiling
python -m memory_profiler script.py

# Sampling profiler (no code changes needed)
py-spy top --pid <process_id>
```

**Visualization:**

```bash
# Install snakeviz for visual profiling
pip install snakeviz
snakeviz profile.stats
```

#### Ruby

**Built-in Profiler:**

```ruby
# ruby-prof
gem install ruby-prof

# Run profiler
ruby-prof script.rb

# Flat profile
ruby-prof --printer=flat script.rb
```

**Tools:**

```bash
# Memory profiling
gem install memory_profiler

# Benchmarking
# Built-in Benchmark module
```

#### Go

**Built-in Profiler:**

```go
// Import profiling
import _ "net/http/pprof"

// Enable profiling
go func() {
    log.Println(http.ListenAndServe("localhost:6060", nil))
}()
```

**Command Line:**

```bash
# CPU profiling
go test -cpuprofile cpu.prof -bench .

# Memory profiling
go test -memprofile mem.prof -bench .

# Analyze with pprof
go tool pprof cpu.prof

# Web visualization
go tool pprof -http=:8080 cpu.prof
```

#### Java

**Built-in Profiler:**

```bash
# JVM flight recorder
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr MyApp

# Analyze with JMC (Java Mission Control)
```

**Tools:**

- JProfiler (commercial)
- YourKit (commercial)
- VisualVM (free)
- Async-profiler (open source)

```bash
# VisualVM (free, included with JDK)
jvisualvm

# Async-profiler
./profiler.sh -d 30 -f flamegraph.html <pid>
```

#### C# / .NET

**Built-in Tools:**

```bash
# dotnet-trace
dotnet tool install --global dotnet-trace

# Collect trace
dotnet trace collect --process-id <pid>

# dotnet-counters
dotnet tool install --global dotnet-counters
dotnet counters monitor --process-id <pid>
```

**Tools:**

- Visual Studio Profiler
- PerfView (free)
- JetBrains dotTrace

#### Rust

**Built-in Tools:**

```bash
# Cargo bench (built-in)
cargo bench

# Flamegraph
cargo install flamegraph
cargo flamegraph

# Memory profiling
cargo install heaptrack
```

### 4. Create Performance Benchmarks

Create reproducible performance tests:

#### Benchmark Design

**Step 1: Define Test Cases**

```python
# Python example with timeit
import timeit

# Small input
small_input = list(range(100))

# Medium input
medium_input = list(range(1000))

# Large input
large_input = list(range(10000))
```

**Step 2: Create Benchmark Functions**

```python
def benchmark_function():
    """Test function performance with various input sizes"""

    # Measure execution time
    small_time = timeit.timeit(
        lambda: process_data(small_input),
        number=1000
    )

    medium_time = timeit.timeit(
        lambda: process_data(medium_input),
        number=1000
    )

    large_time = timeit.timeit(
        lambda: process_data(large_input),
        number=1000
    )

    return {
        'small': small_time,
        'medium': medium_time,
        'large': large_time
    }
```

**Step 3: Measure Multiple Metrics**

```python
import tracemalloc
import time

def comprehensive_benchmark(func, input_data):
    """Measure time, memory, and CPU"""

    # Start memory tracking
    tracemalloc.start()

    # Measure execution time
    start_time = time.perf_counter()
    result = func(input_data)
    end_time = time.perf_counter()

    # Get memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        'execution_time': end_time - start_time,
        'current_memory': current / 1024 / 1024,  # MB
        'peak_memory': peak / 1024 / 1024,  # MB
        'result': result
    }
```

**Step 4: Compare Approaches**

```python
# Compare different implementations
results = {
    'approach_1': benchmark_function(approach_1),
    'approach_2': benchmark_function(approach_2),
}

# Analyze which is faster/more efficient
```

#### Language-Specific Benchmarking

**JavaScript:**

```javascript
// Using benchmark.js
const Benchmark = require('benchmark');
const suite = new Benchmark.Suite();

suite
  .add('Approach 1', function () {
    // Code to test
  })
  .add('Approach 2', function () {
    // Alternative code
  })
  .on('cycle', function (event) {
    console.log(String(event.target));
  })
  .on('complete', function () {
    console.log('Fastest is ' + this.filter('fastest').map('name'));
  })
  .run();
```

**Go:**

```go
// Using testing.B
func BenchmarkApproach1(b *testing.B) {
    for i := 0; i < b.N; i++ {
        approach1(testData)
    }
}

func BenchmarkApproach2(b *testing.B) {
    for i := 0; i < b.N; i++ {
        approach2(testData)
    }
}
```

**Ruby:**

```ruby
require 'benchmark'

Benchmark.bm do |x|
  x.report("Approach 1:") { approach_1(data) }
  x.report("Approach 2:") { approach_2(data) }
end
```

### 5. Profile Code Execution

Run profilers and collect data:

#### Time Profiling

**What to measure:**

- Total execution time
- Time per function
- Hot spots (most time-consuming functions)
- Call counts
- Call stack

**Python Example:**

```python
import cProfile
import pstats

# Profile code
profiler = cProfile.Profile()
profiler.enable()

# Run code
result = your_function(data)

profiler.disable()

# Analyze results
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

#### Memory Profiling

**What to measure:**

- Memory allocation
- Memory leaks
- Peak memory usage
- Memory per function
- Object counts

**Python Example:**

```python
from memory_profiler import profile

@profile
def analyze_memory():
    # Your code here
    data = [0] * 1000000
    return data

# Run with: python -m memory_profiler script.py
```

#### CPU Profiling

**What to measure:**

- CPU time vs wall time
- CPU-bound vs I/O-bound
- Parallel efficiency
- CPU utilization

### 6. Analyze Results

Interpret profiling data:

#### Performance Analysis Checklist

**Algorithm Complexity:**

- [ ] Measure how execution time scales with input size
- [ ] Verify O(n), O(n log n), O(n²), etc.
- [ ] Compare to theoretical complexity
- [ ] Identify if complexity matches expectations

**Bottleneck Identification:**

- [ ] Find functions taking most time
- [ ] Identify unnecessary loops
- [ ] Find repeated calculations
- [ ] Identify I/O bottlenecks
- [ ] Find database query issues

**Memory Analysis:**

- [ ] Identify memory leaks
- [ ] Find excessive allocations
- [ ] Identify large objects
- [ ] Check for memory fragmentation
- [ ] Verify resource cleanup

**Comparison Against Targets:**

- [ ] Execution time within acceptable range
- [ ] Memory usage reasonable
- [ ] Scales appropriately with input
- [ ] No unexpected behavior

#### Common Performance Issues to Look For

**O(n²) When O(n) Is Possible:**

```python
# ❌ O(n²) - inefficient
def find_duplicates_slow(items):
    duplicates = []
    for i in items:
        for j in items:
            if i == j and i not in duplicates:
                duplicates.append(i)
    return duplicates

# ✅ O(n) - efficient
def find_duplicates_fast(items):
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)
```

**N+1 Query Problem:**

```python
# ❌ N+1 queries - inefficient
users = User.query.all()
for user in users:
    # Each iteration makes a new query
    posts = Post.query.filter_by(user_id=user.id).all()

# ✅ Single query with join - efficient
users = User.query.join(Post).all()
```

**Inefficient String Concatenation:**

```python
# ❌ Inefficient (creates new string each time)
result = ""
for item in items:
    result += str(item) + "\n"

# ✅ Efficient
result = "\n".join(str(item) for item in items)
```

**Memory Leaks:**

```javascript
// ❌ Memory leak - event listener not removed
element.addEventListener('click', handler);
// Element removed but listener remains

// ✅ Proper cleanup
element.addEventListener('click', handler);
// Later:
element.removeEventListener('click', handler);
```

**Unnecessary Recomputation:**

```python
# ❌ Recomputes same value repeatedly
def process_items(items):
    for item in items:
        if item > expensive_calculation():
            # expensive_calculation() called every iteration
            process(item)

# ✅ Compute once
def process_items(items):
    threshold = expensive_calculation()
    for item in items:
        if item > threshold:
            process(item)
```

### 7. Review Against Performance Checklist

Execute execute-checklist.md task with performance-considerations-checklist.md:

- Systematically verify each checklist item
- Document any issues found
- Ensure comprehensive coverage
- Note best practices demonstrated

### 8. Provide Optimization Recommendations

For each performance issue, provide guidance:

**Recommendation Template:**

````markdown
### Performance Issue: [Issue Title]

**Severity:** Critical / High / Medium / Low

**Location:** file.py:42

**Current Performance:**

- Execution time: 5.2 seconds
- Memory usage: 450 MB
- Complexity: O(n²)

**Issue:**
[Describe the performance problem]

**Impact:**
[Explain why this matters for production/real-world use]

**Root Cause:**
[Explain what's causing the issue]

**Recommendation:**

[Priority 1: Immediate Improvement]

```python
# Optimized code
```
````

- Expected improvement: 80% faster
- Execution time: ~1.0 seconds
- Complexity: O(n log n)

[Priority 2: Further Optimization]

- Additional techniques if needed
- Caching, indexing, etc.

**Trade-offs:**

- Increased code complexity: Low/Medium/High
- Memory vs speed: [Explanation]
- Readability impact: [Explanation]

**Educational Note:**
[For technical books, explain if optimization is appropriate for teaching context]

**Benchmarks:**

```
Original: 5.2s (100%)
Optimized: 1.0s (19% of original time)
Improvement: 5.2x faster
```

````

#### Optimization Priority Guidelines

**Critical (Must fix before publication):**
- O(n³) or worse when better algorithm exists
- Memory leaks
- Blocking I/O on main thread
- N+1 query problems in examples

**High (Should fix):**
- O(n²) when O(n log n) is straightforward
- Inefficient data structure choices
- Excessive memory usage
- Missing caching for repeated operations

**Medium (Consider fixing):**
- Minor inefficiencies
- Micro-optimizations with clear benefits
- Performance that doesn't scale well

**Low (Educational decision):**
- Micro-optimizations that hurt readability
- Premature optimization
- Optimizations not relevant to teaching goal

### 9. Generate Performance Analysis Report

Create comprehensive report:

**Report Structure:**

```markdown
# Performance Analysis Report

**Date:** YYYY-MM-DD
**Reviewer:** [Name]
**Code Version:** [Commit hash or version]
**Languages:** [JavaScript, Python, etc.]

## Executive Summary

- Total code examples analyzed: X
- Performance issues found: X
- Critical issues: X (must fix)
- High priority: X (should fix)
- Medium priority: X (consider)
- Low priority: X (optional)
- Overall assessment: [Good/Acceptable/Needs Improvement]

## Analysis Scope

**Code Analyzed:**
1. example1.py - Algorithm implementation
2. example2.js - API server example
3. ...

**Performance Targets:**
- Execution time: < 1 second for typical inputs
- Memory usage: < 100 MB
- Scales linearly with input size

**Profiling Tools Used:**
- Python: cProfile, memory_profiler
- JavaScript: clinic.js, Chrome DevTools
- ...

## Performance Metrics Summary

| Example | Time | Memory | CPU | Complexity | Status |
|---------|------|--------|-----|------------|--------|
| example1.py | 0.5s | 45MB | 80% | O(n log n) | ✅ Good |
| example2.py | 8.2s | 850MB | 95% | O(n²) | ❌ Poor |
| example3.js | 0.1s | 25MB | 40% | O(n) | ✅ Good |

## Detailed Analysis

### Example: example1.py

**Performance Profile:**
````

Total time: 0.523s
Peak memory: 45.2 MB
CPU usage: 78%
Algorithm complexity: O(n log n)

```

**Function Breakdown:**
| Function | Calls | Time | % |
|----------|-------|------|---|
| sort_data | 1 | 0.301s | 57% |
| process_item | 1000 | 0.198s | 38% |
| validate | 1000 | 0.024s | 5% |

**Assessment:** ✅ Good
- Performance within targets
- Appropriate algorithm choice
- No obvious bottlenecks
- Scales well with input size

### Example: example2.py

**Performance Profile:**
```

Total time: 8.234s ⚠️ SLOW
Peak memory: 850 MB ⚠️ HIGH
CPU usage: 95%
Algorithm complexity: O(n²) ⚠️ INEFFICIENT

````

**Function Breakdown:**
| Function | Calls | Time | % |
|----------|-------|------|---|
| find_matches | 1000 | 7.892s | 96% |
| load_data | 1 | 0.298s | 4% |
| save_results | 1 | 0.044s | <1% |

**Assessment:** ❌ Needs Improvement
- Execution time exceeds target (8.2s vs < 1s)
- Memory usage too high (850MB vs < 100MB)
- O(n²) algorithm when O(n) possible
- find_matches function is bottleneck

**Hot Spot:**
```python
# Line 42-48: Nested loop causing O(n²) complexity
for item in list1:  # O(n)
    for match in list2:  # O(n) - nested!
        if item == match:
            results.append(item)
````

**Recommendation:** See detailed recommendations below

## Performance Issues Found

### Critical Issues

[Use Performance Issue template from section 8]

### High Priority Issues

[List issues]

### Medium/Low Priority Issues

[Summarized list]

## Optimization Recommendations

### Priority 1: Critical Fixes

1. **Fix O(n²) algorithm in example2.py**
   - Current: 8.2s
   - Expected after fix: ~0.8s
   - Improvement: 10x faster

2. **Fix memory leak in example5.js**
   - Current: Memory grows unbounded
   - Expected: Stable memory usage

### Priority 2: High Priority Improvements

[List recommendations]

### Priority 3: Optional Enhancements

[List recommendations]

## Performance Best Practices Demonstrated

- [x] Appropriate data structures used (mostly)
- [x] Database queries optimized (where applicable)
- [ ] Caching used where beneficial (missing in some examples)
- [x] Async operations for I/O
- [x] Resource cleanup demonstrated

## Scalability Analysis

**How code scales with input size:**

| Example     | 100 items | 1K items | 10K items | Scalability   |
| ----------- | --------- | -------- | --------- | ------------- |
| example1.py | 0.05s     | 0.52s    | 5.8s      | ✅ O(n log n) |
| example2.py | 0.08s     | 8.23s    | ~820s\*   | ❌ O(n²)      |
| example3.js | 0.01s     | 0.11s    | 1.2s      | ✅ O(n)       |

\*Projected based on measured complexity

## Checklist Results

[Reference to performance-considerations-checklist.md completion]

## Educational Context

**Balance Considerations:**

This is educational code where clarity often trumps extreme optimization:

✅ **Appropriate for teaching:**

- example1.py: Good balance of clarity and efficiency
- example3.js: Clear and efficient

⚠️ **Needs improvement:**

- example2.py: Performance is poor enough to teach bad habits

**Recommendations:**

1. Fix critical inefficiencies that teach anti-patterns
2. Keep minor inefficiencies if they improve clarity
3. Add performance notes explaining trade-offs
4. Show optimization path in advanced sections

## Sign-off

- [ ] All critical performance issues resolved
- [ ] Code demonstrates appropriate performance patterns
- [ ] Performance anti-patterns eliminated
- [ ] Educational value maintained
- [ ] Performance review complete

**Reviewer Signature:** ******\_******
**Date:** ******\_******

```

### 10. Troubleshooting Common Issues

**Profiler Overhead:**
- Profiling adds overhead, making code slower
- Compare relative times, not absolute
- Use sampling profilers for less overhead
- Profile multiple runs and average

**Inconsistent Results:**
- System load affects measurements
- Run benchmarks multiple times
- Close other applications
- Use consistent test environment
- Consider CPU frequency scaling

**Profiling Changes Behavior:**
- Memory profiling adds memory overhead
- Timing can be affected by profiler
- Use sampling profilers when possible
- Profile production-like scenarios

**Large Amounts of Data:**
- Profiling data can be huge
- Filter to relevant functions
- Focus on hot spots (top 20 functions)
- Use visualization tools

**Language-Specific Issues:**

*Python:*
- GIL (Global Interpreter Lock) affects multithreading
- cProfile adds overhead
- Use py-spy for lower overhead sampling

*JavaScript:*
- JIT compilation affects early runs
- Need warm-up runs for accurate benchmarks
- Event loop makes timing complex

*Java:*
- JVM warm-up required
- JIT compilation affects timing
- GC pauses can skew results

## Success Criteria

A complete performance review has:

- [ ] All code examples analyzed
- [ ] Profiling tools successfully run
- [ ] Performance benchmarks created
- [ ] Execution time, memory, and CPU measured
- [ ] Results compared against targets
- [ ] Performance bottlenecks identified
- [ ] performance-considerations-checklist.md completed
- [ ] Optimization recommendations provided
- [ ] Performance analysis report generated
- [ ] Critical performance issues resolved

## Common Pitfalls to Avoid

- **Premature optimization**: Don't optimize before profiling
- **Micro-optimization**: Don't sacrifice clarity for tiny gains
- **Ignoring algorithm complexity**: Data structures matter
- **Not measuring**: Profile, don't guess
- **Single run benchmarks**: Always run multiple times
- **Wrong tool for language**: Use language-appropriate profilers
- **Optimizing non-bottlenecks**: Focus on hot spots
- **No baseline**: Measure before and after optimizations
- **Forgetting educational context**: Code clarity matters for teaching
- **No scalability testing**: Test with realistic input sizes

## Performance Optimization Resources

**General:**
- "The Art of Computer Programming" - Donald Knuth
- "Programming Pearls" - Jon Bentley
- "Algorithm Design Manual" - Steven Skiena

**Language-Specific:**

*Python:*
- "High Performance Python" - Gorelick & Ozsvald
- Python Performance Tips: https://wiki.python.org/moin/PythonSpeed

*JavaScript:*
- V8 Performance tips: https://v8.dev/blog/
- Web.dev Performance: https://web.dev/performance/

*Go:*
- Go Performance: https://go.dev/doc/diagnostics
- pprof guide: https://go.dev/blog/pprof

*Java:*
- "Java Performance" - Scott Oaks
- JVM Performance Engineering: https://openjdk.org/groups/hotspot/

## Next Steps

After performance review is complete:

1. **Fix critical issues**: Resolve performance anti-patterns
2. **Add performance notes**: Explain performance in code comments
3. **Create performance guide**: Section on optimization for readers
4. **Set up performance CI/CD**: Automated performance regression testing
5. **Benchmark across versions**: Test on different language versions
6. **Document trade-offs**: Explain performance vs clarity decisions
7. **Review with technical reviewer**: Get expert opinion
8. **Test at scale**: Verify performance with production-like data
```
