# Chapter 5: Understanding React Hooks

If you have followed the previous chapters closely, you will now have a solid foundation in React fundamentals. In this chapter, we will explore React Hooks, a powerful feature that allows you to use state and other React features in functional components.

We will focus on the essential hooks and their practical applications. Specifically, we will cover the following topics:

- Introduction to Hooks
- Using useState for state management
- Managing side effects with useEffect
- Creating custom hooks
- Best practices and common pitfalls

## Introduction to Hooks

React Hooks were introduced in React 16.8 to address several challenges that developers faced with class components. **Hooks** are functions that let you "hook into" React state and lifecycle features from functional components.

The main benefits of using hooks include:

- Simpler component logic without class syntax
- Easier code reuse through custom hooks
- Better organization of related logic

> Before Hooks, stateful logic could only be used in class components. Hooks changed that paradigm entirely, making functional components the preferred approach.

## Using useState for state management

The `useState` hook is the most fundamental hook in React. It allows you to add state to functional components.

### Basic syntax

Here's a simple example of `useState` in action:

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

Let's break down what's happening here:

1. We import the `useState` hook from React
2. We call `useState(0)` to initialize state with a value of 0
3. `useState` returns an array with two elements: the current state value and a setter function
4. We use array destructuring to name these: `count` and `setCount`
5. When the button is clicked, we call `setCount` to update the state

**Important**: State updates are asynchronous. React batches multiple `setState` calls for performance optimization.

### Multiple state variables

You can use multiple `useState` calls in a single component:

```javascript
function UserProfile() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [age, setAge] = useState(0);

  return (
    <form>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
    </form>
  );
}
```

## Managing side effects with useEffect

The `useEffect` hook lets you perform side effects in functional components. Side effects are operations that affect something outside the component, such as:

- Fetching data from an API
- Setting up subscriptions
- Manually changing the DOM
- Setting up timers

### Basic useEffect usage

Here's how to fetch data when a component mounts:

```javascript
import { useState, useEffect } from 'react';

function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://api.example.com/users')
      .then((res) => res.json())
      .then((data) => {
        setUsers(data);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

The empty dependency array `[]` ensures this effect runs only once, when the component mounts.

**Tip**: Always include all values from the component scope that change over time and are used by the effect in the dependency array. This prevents bugs caused by stale closures.

### Cleanup functions

When your effect sets up a subscription or timer, you need to clean it up to prevent memory leaks:

```javascript
useEffect(() => {
  const timer = setInterval(() => {
    console.log('Tick');
  }, 1000);

  return () => clearInterval(timer);
}, []);
```

The function returned from `useEffect` is the cleanup function. React calls it before running the effect again and when the component unmounts.

## Creating custom hooks

Custom hooks let you extract component logic into reusable functions. A custom hook is simply a JavaScript function whose name starts with `use` and that may call other hooks.

### Example: useFetch custom hook

```javascript
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        setError(null);
      })
      .catch((err) => setError(err))
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading, error };
}
```

Now you can use this custom hook in any component:

```javascript
function UserProfile({ userId }) {
  const { data, loading, error } = useFetch(`/api/users/${userId}`);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return <div>{data.name}</div>;
}
```

You have now learned how to extract reusable logic into custom hooks. This pattern helps keep your components clean and promotes code reuse across your application.

## Best practices and common pitfalls

### Rules of Hooks

React has two essential rules for using hooks:

1. **Only call hooks at the top level** - Don't call hooks inside loops, conditions, or nested functions
2. **Only call hooks from React functions** - Call hooks from React functional components or custom hooks, not regular JavaScript functions

### Common mistakes

**Mistake 1: Forgetting dependencies**

```javascript
// ❌ Wrong - missing dependency
useEffect(() => {
  console.log(count);
}, []);

// ✅ Correct - include all dependencies
useEffect(() => {
  console.log(count);
}, [count]);
```

**Mistake 2: Updating state based on previous state incorrectly**

```javascript
// ❌ Wrong - may cause issues with multiple updates
setCount(count + 1);

// ✅ Correct - use functional update
setCount((prevCount) => prevCount + 1);
```

**Mistake 3: Creating new objects/arrays in dependency arrays**

```javascript
// ❌ Wrong - new array every render causes infinite loop
useEffect(() => {
  console.log('Effect ran');
}, [someValue]);

// ✅ Correct - use values from the array directly
useEffect(() => {
  console.log('Effect ran');
}, [someValue[0], someValue[1]]);
```

## Summary

In this chapter, you learned about React Hooks and how they enable you to use state and lifecycle features in functional components. You can now:

- Use `useState` to manage component state
- Implement side effects with `useEffect` and proper cleanup
- Create custom hooks to extract and reuse component logic
- Avoid common pitfalls by following the Rules of Hooks

These skills form the foundation for modern React development. You now understand how to write cleaner, more maintainable React code using the hooks API.

In the next chapter, we will explore advanced React patterns including context API, reducers, and performance optimization techniques.
