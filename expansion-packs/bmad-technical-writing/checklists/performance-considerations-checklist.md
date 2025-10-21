# Performance Considerations Checklist

Use this checklist to assess performance implications of code examples and recommendations.

## Algorithm Efficiency

- [ ] Algorithm complexity appropriate (avoid O(n²) where O(n) possible)
- [ ] Data structures chosen appropriately
- [ ] Unnecessary iterations avoided
- [ ] Early termination conditions used where applicable
- [ ] Recursive vs iterative approaches considered

## Database Performance

- [ ] N+1 query problem avoided
- [ ] Appropriate use of indexes mentioned
- [ ] Query optimization demonstrated
- [ ] Lazy loading vs eager loading discussed
- [ ] Database connection pooling recommended
- [ ] Pagination implemented for large datasets

## Caching

- [ ] Caching strategies mentioned where beneficial
- [ ] Cache invalidation discussed
- [ ] Appropriate cache levels considered (application, database, CDN)
- [ ] Memory vs speed tradeoffs explained

## Memory Management

- [ ] No obvious memory leaks
- [ ] Large data structures handled appropriately
- [ ] Memory usage patterns reasonable
- [ ] Object pooling or reuse considered where relevant
- [ ] Garbage collection implications discussed

## Network Performance

- [ ] API calls minimized
- [ ] Batch operations used where appropriate
- [ ] Compression mentioned for large payloads
- [ ] Async operations used for I/O
- [ ] Connection reuse demonstrated

## Scalability

- [ ] Solutions scale to production workloads
- [ ] Resource constraints considered
- [ ] Horizontal scaling implications discussed
- [ ] Stateless design patterns where appropriate
- [ ] Load distribution strategies mentioned

## Optimization Balance

- [ ] Premature optimization avoided
- [ ] Clarity prioritized over micro-optimizations
- [ ] Performance tradeoffs explained
- [ ] When to optimize discussed (profiling first)
- [ ] Educational clarity maintained

## Profiling & Monitoring

- [ ] Profiling tools mentioned where relevant
- [ ] Performance testing approaches suggested
- [ ] Monitoring best practices referenced
- [ ] Bottleneck identification techniques shown
- [ ] Benchmarking guidance provided

## Resource Usage

- [ ] File handles closed properly
- [ ] Database connections released
- [ ] Thread/process management appropriate
- [ ] Timeouts configured
- [ ] Rate limiting considered for APIs

## Production Considerations

- [ ] Development vs production differences noted
- [ ] Logging performance impact discussed
- [ ] Debug mode disabled in production examples
- [ ] Production-ready patterns demonstrated
- [ ] Performance SLAs considered
