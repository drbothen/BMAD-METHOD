<!-- SHARD METADATA -->
<!-- Original: react-hooks-research-report.md -->
<!-- Shard: 6 of 7 -->

<!-- Sections: Expert Insights Captured, Integration into Chapter Outline -->
<!-- Split Date: 2025-10-26 -->
<!-- END METADATA -->

## Expert Insights Captured

### 1. Hooks simplify component logic organization

> "With Hooks, you can extract stateful logic from a component so it can be tested independently and reused. Hooks allow you to reuse stateful logic without changing your component hierarchy." - React Team

**Source**: [Motivation for Hooks](https://react.dev/learn) (Official Docs)

**Relevance**: Key selling point to emphasize in introduction

### 2. Common mistake: Missing dependencies in useEffect

> "If you forget to include dependencies in the dependency array, your effect will use stale values from previous renders. The React team strongly recommends using the eslint-plugin-react-hooks to catch these bugs automatically." - Dan Abramov

**Source**: [A Complete Guide to useEffect](https://overreacted.io/a-complete-guide-to-useeffect/) (Expert Blog)

**Relevance**: Must include in "Common Pitfalls" section with concrete example

### 3. Performance optimization with useMemo and useCallback

> "Don't optimize prematurely. useMemo and useCallback should be used when you have measured performance problems, not preemptively for every function and calculation. Most of the time, you don't need them." - Kent C. Dodds

**Source**: [When to useMemo and useCallback](https://kentcdodds.com/blog/usememo-and-usecallback) (Expert Blog)

**Relevance**: Include in advanced optimization section with this important caveat

### 4. Testing hooks requires special consideration

> "Custom hooks are just JavaScript functions that use hooks, so they can be tested by calling them. However, hooks can't be called outside of a React component, so use React Testing Library's renderHook utility." - Kent C. Dodds

**Source**: [How to Test Custom React Hooks](https://kentcdodds.com/blog/how-to-test-custom-react-hooks) (Expert Blog)

**Relevance**: Essential for testing section of custom hooks chapter

## Integration into Chapter Outline

### Proposed Chapter Outline

**Chapter 5: Understanding React Hooks** (15-18 pages total)

**5.1 Introduction to Hooks** (2-3 pages)

- Why hooks were created (eliminate wrapper hell, simplify logic reuse)
- Key benefits over class components
- Overview of built-in hooks (useState, useEffect, useContext, etc.)
- Rules of hooks and why they matter
- _Uses: Finding #1 (wrapper hell), Q&A on rules_

**5.2 State Management with useState** (3-4 pages)

- Basic usage and syntax (Code Example #1)
- How state updates work (Finding #2: sync/async behavior)
- Functional updates for computed state
- Common mistake: Stale state in closures (Expert Insight #2)
- Exercise: Build a counter with multiple state variables

**5.3 Side Effects with useEffect** (4-5 pages)

- What are side effects in functional components
- Basic useEffect syntax and execution timing (Finding #3: after paint)
- Dependency array explained
- Cleanup functions (Code Example: subscription pattern)
- Common pitfall: Missing dependencies (Expert Insight #2)
- Data fetching pattern (Code Example #2: fetch with AbortController)
- Exercise: Build a data fetching component

**5.4 Creating Custom Hooks** (3-4 pages)

- When and why to create custom hooks
- Custom hook naming convention (must start with "use")
- useFormInput example (from Q&A)
- useLocalStorage example (Code Example #3)
- Testing custom hooks (Expert Insight #4)
- Exercise: Create a custom hook for form validation

**5.5 Advanced Hooks and Optimization** (2-3 pages)

- useMemo and useCallback (Expert Insight #3: don't over-optimize)
- useRef for persisting values without re-renders
- useReducer for complex state logic
- When to reach for advanced hooks
- Performance measurement and optimization strategies

**5.6 Common Patterns and Best Practices** (1-2 pages)

- Hooks composition patterns
- Error handling with hooks
- Debugging hooks with React DevTools
- ESLint plugin for hooks rules enforcement (Expert Insight #2)

<!-- SHARD END -->
<!-- Continue to react-hooks-shard-7.md -->
