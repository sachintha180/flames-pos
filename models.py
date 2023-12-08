from sqlalchemy import Column, DateTime, Integer, String, create_engine, text
from sqlalchemy.orm import declarative_base

# String URL Format: dialect+driver://username:password@host:port/database
# The statement below uses Lazy Initialization:
# Engine has not tried to connect to the database yet, and will only happen once a task needs to be performed on the database.

# Reference: https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls

engine = create_engine("sqlite+pysqlite:///flames.db")

# commit-as-you-go style
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()

# begin-once-commit-at-end style
# with engine.begin() as conn:
#     conn.execute(
#         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
#         [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
#     )


# Base = declarative_base()


# class User(Base):
#     __tablename__ = "user"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     fullName = Column(String)
#     password = Column(String, nullable=False)
#     role = Column(String, nullable=False)
#     lastLogged = Column(DateTime)
#     createdOn = Column(DateTime, nullable=False)

#     def __repr__(self):
#         return f"<User(id={self.id}, name='{self.name}', password='{self.password}', role='{self.role}', lastLogged={self.lastLogged}, createdOn={self.createdOn})"
