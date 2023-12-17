"""
setup.py (docstring generated by DuetAI).

This script is used to initialize the database with the default administrator user.
"""

# IMPORTANT:
#   This script must be MANUALLY run once,
#   ONLY IF instance/flames.db EXISTS.

# TODO: Running `python setup.py` doesn't work; produces a "Failed to create administrator" error

from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from flask_bcrypt import generate_password_hash
from base import DB_FILEPATH

ADMIN = {
    "username": "admin",
    "password": "Pi$$a@456",
    "name": "Flames POS Administrator",
    "mobile_no": "0121231234",
    "role": "admin",
}

if __name__ == "__main__":
    engine = create_engine(f"sqlite:///{DB_FILEPATH}", echo=True)

    with Session(engine) as session:
        try:
            admin_user = User(
                username=ADMIN["username"],
                password=generate_password_hash(ADMIN["password"]),
                name=ADMIN["name"],
                mobile_no=ADMIN["mobile_no"],
                role=ADMIN["role"],
            )
            session.add(admin_user)
            session.commit()
        except:
            print("> Failed to create administrator")

    engine.dispose()
