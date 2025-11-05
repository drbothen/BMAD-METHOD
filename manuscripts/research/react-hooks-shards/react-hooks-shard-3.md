<!-- SHARD METADATA -->
<!-- Original: react-hooks-research-report.md -->
<!-- Shard: 3 of 7 -->

<!-- Sections: Research Questions & Answers (Part 2: Q3-Q6, Learning Progression, Expert Insights) -->
<!-- Split Date: 2025-10-26 -->
<!-- END METADATA -->

_Source: [Using the Effect Hook](https://react.dev/reference/react/useEffect) (Official Docs) - Accessed 2025-10-25_

**Q: How do you create a custom hook in React?**

A: Custom hook example for form input:

```javascript
function useFormInput(initialValue) {
  const [value, setValue] = useState(initialValue);

  function handleChange(e) {
    setValue(e.target.value);
  }

  return {
    value,
    onChange: handleChange,
  };
}

// Usage
function Form() {
  const name = useFormInput('');
  const email = useFormInput('');

  return (
    <form>
      <input {...name} />
      <input {...email} />
    </form>
  );
}
```

_Source: [Building Your Own Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks) (Official Docs) - Accessed 2025-10-25_

### Learning Progression

**Q: What should readers know about React before learning hooks?**

A: Prerequisites:

- Understanding of React components (functional and class)
- Knowledge of props and state concepts
- Familiarity with React rendering and re-rendering
- Basic JavaScript ES6 features (arrow functions, destructuring)
- Understanding of JSX

_Source: [React Prerequisites](https://react.dev/learn) (Official Docs) - Accessed 2025-10-25_

**Q: What are common mistakes beginners make with useEffect?**

A: Most common mistakes:

1. **Missing dependencies**: Forgetting to include values used inside effect in dependency array
2. **Infinite loops**: Setting state in useEffect without proper dependencies
3. **No cleanup**: Not returning cleanup function for subscriptions/timers
4. **Stale closures**: Not understanding that function closures capture old values

_Source: [A Complete Guide to useEffect](https://overreacted.io/a-complete-guide-to-useeffect/) by Dan Abramov (Expert Blog) - Accessed 2025-10-25_

### Expert Insights

**Q: What are performance considerations when using hooks?**

A: Key performance insights:

1. **Don't optimize prematurely**: useMemo and useCallback should be used when you have measured performance problems, not preemptively
2. **useState initializer function**: Use function form `useState(() => expensiveComputation())` for expensive initial state
3. **useEffect dependencies**: Missing dependencies can cause stale data, but over-including can cause unnecessary re-runs
4. **Custom hooks**: Extract complex logic into custom hooks for better memoization opportunities

_Source: [React Performance Optimization](https://react.dev/learn/render-and-commit) (Official Docs) + [When to useMemo and useCallback](https://kentcdodds.com/blog/usememo-and-usecallback) by Kent C. Dodds (Expert Blog) - Accessed 2025-10-25_

<!-- SHARD END -->
<!-- Continue to react-hooks-shard-4.md -->
