from flask import Flask,redirect,render_template,url_for
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

app = Flask(__name__)
Bootstrap(app)
engine = create_engine('sqlite:///data.db',echo=True)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()


class SPO(Base):
    __tablename__ = "SPO"
    id = Column(Integer, primary_key=True, autoincrement=True)
    S = Column(String)
    P = Column(String)
    O = Column(String)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/entity/<subject>')
def entity(subject):
    spo = SPO(S=subject)
    session = DBSession()
    list = session.query(SPO).filter(SPO.S == subject).all()
    models = []
    for s in list:
        models.append({"p":s.P,"o":s.O})
    print(models)
    return render_template("entity.html",keyword=subject,result = models)


@app.route('/search/<keyword>',methods=['GET','POST'])
def search(keyword):
    spo = SPO(S=keyword)
    session = DBSession()
    queryLikeStr = "%" + keyword + "%"
    list = session.query(SPO.S).distinct().filter(SPO.S.like(queryLikeStr)).all()
    # print(list)
    models = []
    for s in list:
        models.append(s.S)
    return render_template("keyword.html",keyword=keyword,result = models)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80)