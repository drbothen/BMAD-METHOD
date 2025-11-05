<!-- SHARD METADATA -->
<!-- Original: react-hooks-research-report.md -->
<!-- Shard: 5 of 7 -->

<!-- Sections: Code Examples Discovered (Part 2: Example 2 continued, Example 3) -->
<!-- Split Date: 2025-10-26 -->
<!-- END METADATA -->

if (loading) return <div>Loading...</div>;
if (error) return <div>Error: {error.message}</div>;
return <div>{user?.name}</div>;
}

````

**Demonstrates**: useEffect with async/await, cleanup with AbortController, loading/error states, dependency array

**Source**: [Modern Data Fetching with React Hooks](https://react.dev/reference/react/useEffect#fetching-data-with-effects) (Official Docs)

**Applicability**: Excellent real-world example for intermediate section

**Notes**: Modern pattern using AbortController, handles all edge cases

### Example 3: Custom Hook for Local Storage

```javascript
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  const setValue = (value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
}
````

**Demonstrates**: Custom hook pattern, lazy initialization, error handling, API design

**Source**: [useHooks.com - useLocalStorage](https://usehooks.com/uselocalstorage/) (Community Resource)

**Applicability**: Great example for custom hooks chapter section

**Notes**: Production-ready pattern, handles all edge cases

<!-- SHARD END -->
<!-- Continue to react-hooks-shard-6.md -->
