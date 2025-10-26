# Chapter 5: Database Operations

Databases are the backbone of most modern applications, storing everything from user accounts to transaction histories. Whether you're building a web app, mobile application, or data processing pipeline, you'll likely need to interact with a database. In this chapter, you'll learn how to work with PostgreSQL—one of the most powerful and widely-used relational databases—using Python and SQLAlchemy.

By the end of this chapter, you'll be able to connect to databases, design table structures, perform all the essential CRUD operations, write sophisticated queries, work with relationships between tables, and handle transactions safely. These are the fundamental database skills that every backend developer needs.

**What You'll Build**: A complete database-backed user management system with posts, supporting full CRUD operations, complex queries, and transactional integrity.

**Prerequisites**:
- Python 3.8 or later installed
- Basic understanding of Python classes and objects
- PostgreSQL installed locally (or access to a PostgreSQL server)
- Familiarity with command-line operations

**Time Commitment**: 4-6 hours to complete all sections and exercises

**Learning Objectives**:
1. Establish and manage database connections using psycopg2 and SQLAlchemy
2. Define database schemas using SQLAlchemy's ORM and create tables programmatically
3. Perform all CRUD operations (Create, Read, Update, Delete) on database records
4. Write complex queries with filtering, sorting, pagination, and pattern matching
5. Model and query relationships between tables using foreign keys and joins
6. Handle transactions safely with proper error handling and rollback mechanisms

---

## Section 5.1: Connecting to PostgreSQL

PostgreSQL is a powerful, open-source relational database that you'll use throughout this chapter. Before you can work with data, you need to establish a connection.

### Installing the Required Libraries

First, install the necessary Python packages:

```bash
pip install psycopg2-binary sqlalchemy
```

The `psycopg2` library provides the PostgreSQL adapter, while `SQLAlchemy` gives you a high-level ORM interface.

### Creating a Database Connection

Here's how to connect to a PostgreSQL database:

```python
import psycopg2
from sqlalchemy import create_engine

# Direct connection with psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="myapp",
    user="myuser",
    password="mypassword"
)

# SQLAlchemy engine (preferred for ORM)
engine = create_engine(
    'postgresql://myuser:mypassword@localhost/myapp'
)
```

**Important:** Never hardcode credentials in production code. Use environment variables or configuration files.

### Testing the Connection

Verify your connection works:

```python
# Test psycopg2 connection
cursor = conn.cursor()
cursor.execute("SELECT version()")
version = cursor.fetchone()
print(f"PostgreSQL version: {version[0]}")
cursor.close()

# Test SQLAlchemy engine
with engine.connect() as connection:
    result = connection.execute("SELECT 1")
    print(f"Connection successful: {result.fetchone()}")
```

If you see the PostgreSQL version printed, your connection is working correctly.

### Troubleshooting Connection Issues

**Issue:** `psycopg2.OperationalError: could not connect to server`

**Solution:** Ensure PostgreSQL is running: `sudo systemctl status postgresql`

**Issue:** Authentication failed for user

**Solution:** Check your credentials and verify the user exists in PostgreSQL

Now that you can connect to PostgreSQL successfully, you're ready to define your database schema. SQLAlchemy's ORM lets you describe tables as Python classes, making it easy to keep your code and database in sync.

## Section 5.2: Creating Tables with SQLAlchemy

With your database connection established, you can define and create tables using SQLAlchemy's declarative ORM.

### Defining a Model

SQLAlchemy models are Python classes that map to database tables:

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
```

Each `Column` defines a field in your table with its data type and constraints.

### Creating Tables in the Database

Use the `create_all()` method to create tables from your models:

```python
# Create all tables defined by Base subclasses
Base.metadata.create_all(engine)
```

This generates the SQL `CREATE TABLE` statements and executes them.

### Verifying Table Creation

Check that your table exists:

```python
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tables in database: {tables}")
```

You should see `['users']` in the output.

### Common Column Types

SQLAlchemy supports many column types:

- `Integer` - Whole numbers
- `String(length)` - Variable-length text
- `Text` - Unlimited text
- `Boolean` - True/False
- `DateTime` - Date and time
- `Float` - Decimal numbers
- `JSON` - JSON data (PostgreSQL 9.3+)

Choose the appropriate type based on your data requirements.

With your User table created, let's put it to work. In the next section, you'll learn the four fundamental database operations—Create, Read, Update, and Delete—that you'll use constantly when building applications.

## Section 5.3: CRUD Operations

CRUD stands for Create, Read, Update, Delete—the four basic operations you'll perform on database records.

### Creating Records

Add new records using SQLAlchemy sessions:

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# Create a new user
new_user = User(
    username="alice",
    email="alice@example.com"
)

# Add to session and commit
session.add(new_user)
session.commit()

print(f"Created user with ID: {new_user.id}")
```

The session tracks changes and commits them to the database.

### Reading Records

Query the database to retrieve records:

```python
# Get all users
all_users = session.query(User).all()
for user in all_users:
    print(user)

# Get specific user by ID
user = session.query(User).filter_by(id=1).first()
print(f"User 1: {user.username}")

# Get user by username
alice = session.query(User).filter_by(username="alice").first()
print(f"Found: {alice.email}")
```

The `query()` method creates queries, and `filter_by()` adds conditions.

### Updating Records

Modify existing records:

```python
# Find user and update
user = session.query(User).filter_by(username="alice").first()
user.email = "alice.new@example.com"
session.commit()

print(f"Updated email to: {user.email}")
```

Changes are tracked automatically once the object is loaded in a session.

### Deleting Records

Remove records from the database:

```python
# Find and delete user
user = session.query(User).filter_by(username="alice").first()
session.delete(user)
session.commit()

print("User deleted successfully")
```

**Warning:** Deletions are permanent. Always double-check before committing deletes.

### Best Practices

- **Always close sessions:** Use `session.close()` or context managers
- **Handle exceptions:** Wrap operations in try/except blocks
- **Use transactions:** Commit related changes together
- **Validate input:** Never trust user data directly

```python
try:
    session.add(new_user)
    session.commit()
except Exception as e:
    session.rollback()
    print(f"Error: {e}")
finally:
    session.close()
```

These basic CRUD operations work great for simple cases, but real applications need more sophisticated queries. Building on the query techniques you just learned, let's explore how to filter, sort, and search your data precisely.

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

So far, you've worked with a single User table in isolation. But real applications organize data across multiple related tables—users have posts, posts have comments, and so on. Let's explore how to model and query these relationships effectively.

## Section 5.5: Joins and Relationships

Real applications store related data across multiple tables. Relationships let you connect records and query them together.

### Defining Relationships

Add relationships to your models:

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)

    # Relationship to posts
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationship to user
    author = relationship("User", back_populates="posts")
```

The `relationship()` defines how tables connect, while `ForeignKey` enforces the database constraint.

### Accessing Related Records

Navigate relationships naturally:

```python
# Get user and their posts
user = session.query(User).filter_by(username="alice").first()
for post in user.posts:
    print(f"{user.username} wrote: {post.title}")

# Get post and its author
post = session.query(Post).filter_by(id=1).first()
print(f"Author: {post.author.username}")
```

SQLAlchemy automatically loads related records when you access them.

### Join Queries

Explicitly join tables for more control:

```python
# Inner join
results = session.query(User, Post).join(Post).all()
for user, post in results:
    print(f"{user.username}: {post.title}")

# Filter across joined tables
posts = session.query(Post).join(User).filter(
    User.username == "alice"
).all()

# Select specific columns
results = session.query(
    User.username,
    Post.title
).join(Post).all()
```

### Left Outer Joins

Include records even when related records don't exist:

```python
# Get all users, including those without posts
results = session.query(User).outerjoin(Post).all()
```

### Eager Loading

Optimize queries by loading relationships upfront:

```python
from sqlalchemy.orm import joinedload

# Load users with their posts in one query
users = session.query(User).options(
    joinedload(User.posts)
).all()

# Avoid N+1 query problem
for user in users:
    print(f"{user.username} has {len(user.posts)} posts")
```

Without `joinedload`, accessing `user.posts` triggers a separate query for each user.

### Many-to-Many Relationships

Use association tables for many-to-many:

```python
from sqlalchemy import Table

# Association table
post_tags = Table('post_tags', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")

# Update Post model
Post.tags = relationship("Tag", secondary=post_tags, back_populates="posts")
```

Now posts can have multiple tags, and tags can be on multiple posts.

You now know how to create, query, filter, and relate data across tables. But what happens when something goes wrong? Database errors, network failures, and constraint violations can corrupt your data if not handled properly. Let's explore how to make your database operations reliable and safe for production use.

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

## Summary

Congratulations! You've completed Chapter 5 and learned the essential skills for working with PostgreSQL databases in Python. You started with basic connection setup and progressed through table creation, CRUD operations, advanced querying, relationships, and transaction management—everything you need to build robust database-backed applications.

**Key Concepts Covered**:
- Database connections using psycopg2 and SQLAlchemy
- ORM model definitions and table creation
- CRUD operations (Create, Read, Update, Delete)
- Query filtering, sorting, pagination, and pattern matching
- Table relationships (one-to-many, many-to-many) and joins
- Transaction management with proper error handling

**Skills Developed**:
- Connect to PostgreSQL and verify connectivity
- Define database schemas using SQLAlchemy's declarative ORM
- Perform all CRUD operations safely with proper error handling
- Write complex queries with filtering, sorting, and joins
- Model and navigate relationships between tables
- Handle transactions atomically with rollback capability

**In the Next Chapter**:

Building on your database foundation, Chapter 6 explores advanced topics like database migrations, query optimization, full-text search, and caching strategies. You'll learn how to evolve your schema over time without data loss, optimize slow queries for production scale, and implement caching to reduce database load.

**Further Reading**:
- SQLAlchemy Official Documentation: https://docs.sqlalchemy.org/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- "SQL Performance Explained" by Markus Winand
- Flask-SQLAlchemy Guide: https://flask-sqlalchemy.palletsprojects.com/
