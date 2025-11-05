<!-- SHARD METADATA -->
<!-- Original: react-hooks-research-report.md -->
<!-- Shard: 4 of 7 -->

<!-- Sections: Technical Findings, Code Examples Discovered (Part 1: Examples 1-2) -->
<!-- Split Date: 2025-10-26 -->
<!-- END METADATA -->

## Technical Findings

### Key Technical Findings

1. **Hooks eliminate "wrapper hell"**: Multiple sources confirm that hooks reduce deeply nested component hierarchies caused by HOCs and render props. This is a primary design goal and one of the strongest selling points.
   - _Official: [Motivation for Hooks](https://react.dev/learn) - React Team_
   - _Community: [Practical Benefits of Hooks](https://kentcdodds.com/blog/react-hooks-whats-going-to-happen-to-my-tests) - Kent C. Dodds_

2. **useState is synchronous within render, async for updates**: useState returns current state immediately, but state updates are batched and applied asynchronously. This is a common source of confusion for developers migrating from class components.
   - _Official: [useState Reference](https://react.dev/reference/react/useState) - React Docs_
   - _Community: Multiple Stack Overflow discussions confirm this behavior_

3. **useEffect runs after paint, not after render**: As of React 18, useEffect runs after the browser has painted, which is different from componentDidUpdate. For synchronous effects, use useLayoutEffect instead.
   - _Official: [useEffect Timing](https://react.dev/reference/react/useEffect) - React Docs_
   - _Expert: [useEffect vs useLayoutEffect](https://kentcdodds.com/blog/useeffect-vs-uselayouteffect) - Kent C. Dodds_

## Code Examples Discovered

### Example 1: Basic useState Hook

```javascript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

**Demonstrates**: Basic useState syntax, state initialization, state updates

**Source**: [React Docs - useState](https://react.dev/reference/react/useState) (Official)

**Applicability**: Direct use in introductory section

**Notes**: Clean example, perfect for beginners

### Example 2: Data Fetching with useEffect

```javascript
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchUser() {
      try {
        setLoading(true);
        const response = await fetch(`/api/users/${userId}`, {
          signal: controller.signal,
        });
        const data = await response.json();
        setUser(data);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err);
        }
      } finally {
        setLoading(false);
      }
    }

    fetchUser();

    return () => controller.abort();
  }, [userId]);
```

<!-- SHARD END -->
<!-- Continue to react-hooks-shard-5.md -->
