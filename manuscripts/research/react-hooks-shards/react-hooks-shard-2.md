<!-- SHARD METADATA -->
<!-- Original: react-hooks-research-report.md -->
<!-- Shard: 2 of 7 -->

<!-- Sections: Research Questions & Answers (Part 1: Technical Concepts, Code Examples Q1-Q2) -->
<!-- Split Date: 2025-10-26 -->
<!-- END METADATA -->

## Research Questions & Answers

### Technical Concepts

**Q: What is the React Hooks API and why was it introduced?**

A: React Hooks were introduced in React 16.8 to allow functional components to use state and other React features without writing class components. They solve the problems of component logic reuse, complex component hierarchies, and confusing lifecycle methods. Hooks enable developers to extract stateful logic from components so it can be tested independently and reused without changing component hierarchy.

_Source: [React Hooks Documentation](https://react.dev/reference/react) (Official Docs) - Accessed 2025-10-25_

**Q: What are the rules of hooks and why do they exist?**

A: Hooks have two rules: (1) Only call hooks at the top level (not in loops, conditions, or nested functions), (2) Only call hooks from React function components or custom hooks. These rules ensure hooks are called in the same order on every render, which is how React tracks hook state between renders. Breaking these rules causes bugs where state gets mixed up.

_Source: [Rules of Hooks](https://react.dev/warnings/invalid-hook-call-warning) (Official Docs) - Accessed 2025-10-25_

**Q: How do hooks differ from class component lifecycle methods?**

A: Hooks unify related logic that was previously split across multiple lifecycle methods. For example, data fetching logic that requires componentDidMount, componentDidUpdate, and componentWillUnmount in classes can be consolidated into a single useEffect hook. Hooks also eliminate the confusion around "this" binding and allow better code organization by feature rather than by lifecycle.

_Source: [Motivation for Hooks](https://react.dev/learn) (Official Docs) - Accessed 2025-10-25_

### Code Examples

**Q: Show me a simple example of useState and useEffect in React**

A: Basic counter with side effect:

```javascript
import { useState, useEffect } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `Count: ${count}`;
  }, [count]);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

_Source: [React Hooks Documentation - useState](https://react.dev/reference/react/useState) (Official Docs) - Accessed 2025-10-25_

**Q: What are common patterns for using useEffect with cleanup?**

A: Cleanup pattern for subscriptions and timers:

```javascript
useEffect(() => {
  const subscription = props.source.subscribe();

  return () => {
    // Cleanup function runs before next effect and on unmount
    subscription.unsubscribe();
  };
}, [props.source]);
```

<!-- SHARD END -->
<!-- Continue to react-hooks-shard-3.md -->
