## Section 5.6: Transactions and Error Handling

Reliable database operations require proper transaction management and error handling to maintain data integrity.

### Understanding Transactions

Transactions group multiple operations into atomic units:

```python
session = Session()
try:
    # Create user
    user = User(username="bob", email="bob@example.com")
    session.add(user)

    # Create post for user
    post = Post(title="First Post", content="Hello!", author=user)
    session.add(post)

    # Commit both together
    session.commit()
    print("Transaction successful")
except Exception as e:
    # Rollback on error
    session.rollback()
    print(f"Transaction failed: {e}")
finally:
    session.close()
```

If either operation fails, both are rolled back—the user won't be created without their post.

### Context Managers

Use context managers for automatic cleanup:

```python
from contextlib import contextmanager

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Use the context manager
with get_session() as session:
    user = User(username="charlie", email="charlie@example.com")
    session.add(user)
# Auto-commits on success, auto-rolls back on error
```

### Handling Common Errors

Catch specific database exceptions:

```python
from sqlalchemy.exc import IntegrityError, OperationalError

try:
    user = User(username="alice", email="alice@example.com")
    session.add(user)
    session.commit()
except IntegrityError as e:
    session.rollback()
    print("Duplicate username or email")
except OperationalError as e:
    session.rollback()
    print("Database connection error")
except Exception as e:
    session.rollback()
    print(f"Unexpected error: {e}")
```

### Savepoints

Create intermediate save points:

```python
session.begin_nested()  # Create savepoint
try:
    user = User(username="david", email="david@example.com")
    session.add(user)
    session.commit()  # Commit to savepoint
except Exception:
    session.rollback()  # Rollback to savepoint only
```

### Connection Pooling

Configure connection pools for production:

```python
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://user:pass@localhost/db',
    pool_size=20,          # Number of persistent connections
    max_overflow=10,       # Additional connections if needed
    pool_timeout=30,       # Seconds to wait for connection
    pool_recycle=3600      # Recycle connections after 1 hour
)
```

### Best Practices Summary

**DO:**
- ✓ Always use try/except/finally for database operations
- ✓ Close sessions promptly
- ✓ Commit related changes together
- ✓ Use connection pooling in production
- ✓ Log errors for debugging

**DON'T:**
- ✗ Leave sessions open indefinitely
- ✗ Ignore exceptions
- ✗ Mix committed and uncommitted data
- ✗ Create new engines repeatedly
- ✗ Commit after every single operation

With proper transaction management and error handling, your database operations will be reliable and maintainable.
