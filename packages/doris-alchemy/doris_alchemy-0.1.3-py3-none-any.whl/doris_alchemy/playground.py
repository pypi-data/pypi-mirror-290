from datetime import datetime
import os
from sqlalchemy import BigInteger, Column, DateTime, Engine, Integer, String, Table, Text, create_engine, insert, select
from sqlalchemy.orm import Mapped, mapped_column, Session

from doris_alchemy.dialect import HASH, RANGE
from doris_alchemy.orm_base import METADATA, DorisBase

USER = os.environ['DORIS_PROD_USER']
PWD = os.environ['DORIS_PROD_PWD']
HOST = '10.0.100.115'
PORT = '9030'
DB = 'test'

def make_eng() -> Engine:
    return create_engine(f"doris+mysqldb://{USER}:{PWD}@{HOST}:{PORT}/{DB}")


table = Table(
    'dummy_table',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('name', String(64), nullable=False),
    Column('description', Text),
    Column('date', DateTime),
    
    doris_unique_key=('id'),
    doris_partition_by=RANGE('id'),
    doris_distributed_by=HASH('id'),
    doris_properties={"replication_allocation": "tag.location.default: 1"},
)


class Dummy(DorisBase):
    __tablename__ = 'dummy_two'
    
    id:             Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name:           Mapped[str] = mapped_column(String(127))
    description:    Mapped[str]
    date:           Mapped[datetime]
    
    __table_args__ = {
        'doris_properties': {"replication_allocation": "tag.location.default: 1"}
        }
    doris_unique_key = 'id'
    doris_distributed_by = HASH('id')
    doris_partition_by = RANGE('id')


ROWS = [
    ('BMW', 'A car brand', datetime(2024, 1, 1)),
    ('Airbus', 'Construction bureau', datetime(2024, 2, 10)),
    ('Volvo', 'A car brand', datetime(2022, 12, 1, 10, 35))
]

def __mk_row(id :int, row: tuple[str, str, datetime]):
    return {
        'id': id,
        'name': row[0],
        'description': row[1],
        'date': row[2]
    }

if __name__ == '__main__':
    engine = make_eng()
    try:
        Dummy.drop(engine)
    except:
        print("Doesn't exist")
    Dummy.create(engine)
    # with Session(engine) as s:
    #     print(engine.dialect.has_table(s.connection(), 'dummy_two'))
    #     vals = [__mk_row(i, ROWS[i]) for i in range(len(ROWS))]
    #     q = insert(Dummy).values(vals)
    #     s.execute(q)
    #     s.execute(q)
    #     sel = select(Dummy)
    #     res = s.execute(sel)
    #     pprint(list(res))
    
    
    row = {
        'id': 0,
        'name': 'Airbus',
        'description': 'Construction bureau',
        'date': datetime(2024, 2, 10)
    }
    
    with Session(engine) as s:
        q = insert(Dummy).values([row])
        s.execute(q)
        sel = select(Dummy)
        res = s.execute(sel)
        print(list(res))
    pass