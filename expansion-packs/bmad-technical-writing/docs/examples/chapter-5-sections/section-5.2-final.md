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
