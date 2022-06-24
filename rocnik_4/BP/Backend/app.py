from datetime import datetime
from flask import (
    Flask,
    request,
    Response,
)
from database import db_session, init_db

from models import (
    Record,
    Pressure
)




app = Flask(__name__)


@app.route("/pressure", methods=["POST"])
def add_pressure():
    datas = request.json
    for data in datas:
        print(data)
        time = data["Čas"]
        date = data["\ufeffDátum"]
        date_time = date+" "+time
        mytime = datetime.strptime(date_time, '%Y-%m-%d %H:%M')
        record = Pressure(int(data["Dia"]), int(data["Pulz"]), int(data["Sys"]), mytime)
        db_session.add(record)
        db_session.commit()
    return Response(status=201)

@app.route("/upload", methods=["POST"])
def add_record():
    data = request.json
    record = Record(data["Oxy"], data["Rate"], data["Object"], data["Ambient"])
    db_session.add(record)
    db_session.commit()
    return Response(status=201)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    init_db()
    app.run(port=5000, host="0.0.0.0")

