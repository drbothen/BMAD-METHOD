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
