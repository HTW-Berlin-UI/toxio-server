from flask import Flask
from flask import request
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

from db import queries

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'mysql+mysqlconnector://root:root@localhost/chem_scan'

db = SQLAlchemy(app)
api = Api(app)



@api.route('/substances/<int:id>')
class Substance(Resource):
    """models describes the resource"""
    model = api.model('Model', {
        'id': fields.Integer,
        'name': fields.String,
        'eg': fields.String,
        'cas': fields.String,
        'reach_nr': fields.String,
        'formula': fields.String,
        'approved': fields.Integer,
        'serialized_data': fields.String})

    @api.marshal_with(model)
    def get(self, **kwargs):

        return queries.testquery('atropine')





if __name__ == '__main__':
    # session = connections.make_session()
    app.run('127.0.0.1', 5000, debug=True)
