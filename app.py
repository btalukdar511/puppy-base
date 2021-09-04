from flask import Flask, jsonify, request, redirect, url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Puppy, Base

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('puppyFunction'))

@app.route('/puppies', methods=['GET', 'POST'])
def puppyFunction():
    if request.method == 'GET':
        return getAllPuppies()
    elif request.method == 'POST':
        for x in request.args:
            print(x)
        name = request.args.get('name', '')
        description = request.args.get('description', '')
        return makeANewPuppy(name, description)


@app.route("/puppiesFunction/<int:pid>", methods=['GET', 'PUT', 'DELETE'])
def puppiesFunction(pid):
    if request.method == 'GET':
        return getPuppy(pid)
    elif request.method == 'PUT':
        name = request.args.get('name', '')
        description = request.args.get('description', '')
        return updatePuppy(pid, name, description)
    elif request.method == 'DELETE':
        return deletePuppy(pid)


def getAllPuppies():
    puppies = session.query(Puppy).all()
    return jsonify(Puppies=[i.serialize for i in puppies])


def getPuppy(pid):
    puppy = session.query(Puppy).filter_by(id=pid).one()
    return jsonify(puppy=puppy.serialize)


def makeANewPuppy(name, description):
    puppy = Puppy(name=name, description=description)
    session.add(puppy)
    session.commit()
    return jsonify(puppy=puppy.serialize)


def updatePuppy(pid, name, description):
    puppy = session.query(Puppy).filter_by(id=pid).one()
    if not name:
        puppy.name = name
    if not description:
        puppy.description = description
    session.add(puppy)
    session.commit()
    return "updated puppy with id %s" % pid


def deletePuppy(pid):
    puppy = session.query(Puppy).filter_by(id=pid).one()
    session.delete(puppy)
    session.commit()
    return "deleted puppy with id %s" % pid


app.secret_key = 'super_secret_key'
app.debug = True
app.run(host='127.0.0.1', port=2000)
