from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager


app = Flask(__name__)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))


Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)


@app.route('/')
def home():
    return 'А тут нічого!, Модель знаходиться: api/v1/items'


@app.route('/api/v1/items', methods=['GET'])
def get_list():
    parseritems = Parseritem.query.all()
    serialized = []
    for parseritem in parseritems:
        serialized.append(
                    {
                        'id': parseritem.id,
                        'title': parseritem.title,
                        'usd_price': parseritem.usd_price,
                        'city': parseritem.city,
                        'description': parseritem.description
                        }
                    )
    return jsonify(serialized)


@app.route('/api/v1/items/<int:item_id>', methods=['GET'])
def get_list_id(item_id):
    item = filter(lambda t: t['id'] == item_id, items)
    if len(item) == 0:
        abort(404)
    return jsonify({'item': item[0]})


@app.route('/api/v1/items', methods=['POST'])
def create_list():
    new_one = Parseritem(**request.json)
    session.add(new_one)
    session.commit()
    serialized = {
        'id': new_one.id,
        'title': new_one.title,
        'usd_price': new_one.usd_price,
        'city': new_one.city,
        'description': new_one.description
        }
    return jsonify(serialized)


@app.route('/api/v1/items/<int:item_id>', methods=['PUT'])
def update_list(item_id):
    item = Parseritem.query.filter(Parseritem.id == item_id).first()
    params = request.json
    if not item:
        return {'message': 'No parseritems with this id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialized = {
        'id': item.id,
        'title': item.title,
        'usd_price': item.usd_price,
        'city': item.city,
        'description': item.description
        }


@app.route('/api/v1/items/<int:item_id>', methods=['DELETE'])
def delete_list(item_id):
    item = Parseritem.query.filter(Parseritem.id == item_id).first()
    if not item:
        return {'message': 'No parseritems with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()



if __name__ == '__main__':
    app.run(debug=True)