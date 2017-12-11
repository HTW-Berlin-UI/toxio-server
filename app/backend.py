from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db import connections
from db import models
from flask import request
from flask_restplus import Api, Resource, fields
import queries



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'mysql+mysqlconnector://root:root@localhost/chem_scan'

db = SQLAlchemy(app)
api = Api(app)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


model = api.model('Model', {
    'id': fields.Integer,
    'name': fields.String,
    'eg': fields.String,
    'cas': fields.String,
    'reach_nr': fields.String,
    'formula': fields.String,
    'approved': fields.Integer,
    'serialized_data': fields.String})

@api.route('/substance')
class GetId(Resource):
        @api.marshal_with(model, envelope='resource')
        def get(self, **kwargs):
            return queries.testquery('atropine', session)





if __name__ == '__main__':
    session = connections.make_session()
    app.run('127.0.0.1', 5000)
