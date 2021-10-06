from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from schemas import ParsSchema
from flask_apispec import use_kwargs, marshal_with


app = Flask(__name__)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))


Base = declarative_base()
Base.query = session.query_property()

docs = FlaskApiSpec()

docs.init_app(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='parseritems',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/'
})


from models import *

Base.metadata.create_all(bind=engine)


@app.route('/')
def home():
    return 'А тут нічого!, Модель знаходиться: api/v1/items'


@app.route('/api/v1/items', methods=['GET'])
@marshal_with(ParsSchema(many=True))
def get_list():
    parseitems = Parseritem.query.all()
    return parseitems


@app.route('/api/v1/items/<int:item_id>', methods=['GET'])
@marshal_with(ParsSchema)
def get_id(item_id):
    item = Parseritem.query.filter(Parseritem.id == item_id).first()
    if not item:
        return {'message': 'No parseritem with this id'}, 400
    session.commit()
    return 'good', 204


@app.route('/api/v1/items', methods=['POST'])
@use_kwargs(ParsSchema)
@marshal_with(ParsSchema)
def create_list(**kwargs):
    new_one = Parseritem(**kwargs)
    session.commit()
    session.add(new_one)
    session.commit()
    return new_one


@app.route('/api/v1/items/<int:item_id>', methods=['PUT'])
@use_kwargs(ParsSchema)
@marshal_with(ParsSchema)
def update_list(item_id, **kwargs):
    item = Parseritem.query.filter(Parseritem.id == item_id).first()
    params = request.json
    if not item:
        return {'message': 'No parseitems with this id'}, 400
    for key, value in kwargs.items():
        setattr(item, key, value)
    session.commit()
    return item


@app.route('/api/v1/items/<int:item_id>', methods=['DELETE'])
@marshal_with(ParsSchema)
def delete_list(item_id):
    item = Parseritem.query.filter(Parseritem.id == item_id).first()
    if not item:
        return {'message': 'No parseitems with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


docs.register(get_list)
docs.register(get_id)
docs.register(create_list)
docs.register(update_list)
docs.register(delete_list)



if __name__ == '__main__':
    app.run(debug=True)