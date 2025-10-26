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
