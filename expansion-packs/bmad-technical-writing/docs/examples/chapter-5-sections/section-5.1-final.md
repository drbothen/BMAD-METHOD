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
