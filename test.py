from sqlalchemy import create_engine
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy import Column, Table
from sqlalchemy import String, Float, Integer, Text, Date
from sqlalchemy.dialects.postgresql import insert
import selenium

engine_url = "postgresql+psycopg2://postgres:q12345sk@127.0.0.1:5432/landCrawler"
engine = create_engine(engine_url, echo=True)

meta = MetaData()

cityTable = Table(
    "city",
    meta,
    Column("label", String(1), primary_key = True),
    Column("city_name", String(10)),
    Column("lat", Float),
    Column("lon", Float)
)

townTable = Table(
    "town",
    meta,
    Column("city_label", String(1)),
    Column("town_label", String(3), primary_key = True),
    Column("town_name", String(10)),
    Column("lat", Float),
    Column("lon", Float)
)

landTransactionTable = Table(
    "transaction",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("city", String(1), ForeignKey("city.label")),
    Column("town", String(3), ForeignKey("town.town_label")),
    Column("location", String(50)),
    Column("trade_date", Date),
    Column("land_num", Integer),
    Column("lon", Float),
    Column("lat", Float),
    Column("note", Text),
    Column("per_price", Float),
    Column("total_price", Float),
    Column("transaction_target", String(10))
)

meta.create_all(engine)