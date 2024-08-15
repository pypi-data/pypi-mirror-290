from sqlalchemy import Engine
from sqlalchemy.orm import Session


def insert(engine: Engine, *args):
    with Session(engine) as session:
        session.add_all(args)
        session.commit()
