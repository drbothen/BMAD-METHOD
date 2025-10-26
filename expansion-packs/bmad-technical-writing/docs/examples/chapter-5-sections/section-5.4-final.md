## Section 5.4: Query Filtering

Simple queries return all records, but production applications need precise filtering to find specific data efficiently.

### Basic Filters

Filter records using `filter_by()` for simple conditions:

```python
# Find users with specific username
users = session.query(User).filter_by(username="alice").all()

# Multiple conditions (AND)
users = session.query(User).filter_by(
    username="alice",
    email="alice@example.com"
).all()
```

### Advanced Filters with filter()

For complex conditions, use `filter()` with SQLAlchemy expressions:

```python
from sqlalchemy import or_, and_

# Greater than
recent_users = session.query(User).filter(
    User.created_at > datetime(2024, 1, 1)
).all()

# OR condition
users = session.query(User).filter(
    or_(
        User.username == "alice",
        User.username == "bob"
    )
).all()

# Complex AND/OR combinations
users = session.query(User).filter(
    and_(
        User.created_at > datetime(2024, 1, 1),
        or_(
            User.username.like("a%"),
            User.email.like("%@gmail.com")
        )
    )
).all()
```

### Sorting Results

Order your query results:

```python
# Sort by username ascending
users = session.query(User).order_by(User.username).all()

# Sort by created_at descending
users = session.query(User).order_by(User.created_at.desc()).all()

# Multiple sort columns
users = session.query(User).order_by(
    User.created_at.desc(),
    User.username
).all()
```

### Limiting Results

Control how many records are returned:

```python
# Get first 10 users
users = session.query(User).limit(10).all()

# Skip first 10, get next 10 (pagination)
users = session.query(User).offset(10).limit(10).all()

# Get single record (first match or None)
user = session.query(User).filter_by(username="alice").first()
```

### Counting Records

Count matching records without fetching them:

```python
# Count all users
total = session.query(User).count()
print(f"Total users: {total}")

# Count filtered results
recent_count = session.query(User).filter(
    User.created_at > datetime(2024, 1, 1)
).count()
```

### Pattern Matching

Use LIKE and ILIKE for text searches:

```python
# Case-sensitive pattern match
users = session.query(User).filter(
    User.username.like("ali%")
).all()

# Case-insensitive (PostgreSQL)
users = session.query(User).filter(
    User.email.ilike("%@GMAIL.COM")
).all()

# Contains
users = session.query(User).filter(
    User.username.contains("ice")
).all()
```

These filtering techniques give you precise control over which records your queries return.
