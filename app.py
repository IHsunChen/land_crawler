from flask import Flask, render_template, request, jsonify, Response
import requests
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy import Column, Table
from sqlalchemy import String, Float, Integer, Text, Date
from sqlalchemy.dialects.postgresql import insert

app = Flask(__name__, static_url_path='', template_folder='./')


def convert_to_date(roc_date_string):
  # 将中华民国日期字符串分割为年、月、日
  roc_year, roc_month, roc_day = map(int, roc_date_string.split('/'))

  # 将中华民国年份转换为西元年份
  year = roc_year + 1911

  # 构建日期对象
  date = datetime(year, roc_month, roc_day).date()

  return date
  
@app.route('/')
def index():
  return render_template('query_price.html')

@app.route('/SERVICE/QueryPrice/<param>')
def getParam(param):
  q = request.args.get('q')
  res = requests.get("https://lvr.land.moi.gov.tw/SERVICE/QueryPrice/{}?q={}".format(param, q))
  # tradeData = res.json()
  # with engine.connect() as conn:
  #   for data in tradeData:
  #     if(data['p'].replace(",", "") == ''):
  #       data['p'] = None
  #     else:
  #       data['p'] = float(data['p'].replace(",", ""))
  #     tmp = {
  #       "location": data['a'],
  #       "city": data['city'],
  #       "town": data["twn"],
  #       "trade_date": convert_to_date(data['e']),
  #       "land_num": int(data['j']),
  #       "lat": float(data['lat']),
  #       "lon": float(data['lon']),
  #       "note": data['note'],
  #       "per_price": data['p'],
  #       'transaction_target': data['t'],
  #       'total_price': float(data['tp'].replace(",", ""))
  #     }
  #     insert_stmt = insert(landTransactionTable).values(tmp)
  #     conn.execute(insert_stmt)
  #   conn.commit()
  return res.json()


if __name__ == '__main__':
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
      "land_transaction",
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
  # meta.create_all(engine)
  app.run()
    