from flask import Flask
from flask import request
from flask_restplus import Api, Resource, fields, marshal
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import reqparse

from db import queries

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'mysql+mysqlconnector://root:root@localhost/chem_scan'

db = SQLAlchemy(app)
api = Api(app)

# API endpoints, include only neccessary fields (not things like additional_info, serialized_data...)
# Endpoints:
# GET: all procedures, all materials, all procs, all purposes,
# all scopes for specific organization; endpoint that combines all these together
# -> substances/resources; endpoint for all substances; endpoint get all plants
# for specific organization and unit; endpoint for sds
# POST: new usage


@api.route('/substances')
class Substances(Resource):
    model = api.model('Model', {
        'id': fields.Integer,
        'name': fields.String,
        'eg': fields.String,
        'cas': fields.String,
        'formula': fields.String,
    })

    @api.marshal_with(model)
    def get(self, **kwargs):
        Substances = queries.query_get_all_substances()
        return Substances

@api.route('/procedures')
class Procedures(Resource):
    model = api.model('Model', {
        'id': fields.Integer,
        'name': fields.String,
    })

    @api.marshal_with(model)
    def get(self, **kwargs):
        Procedures = queries.query_get_procedures()
        return Procedures


@api.param('id', 'id of the organization the user is registered to')
@api.route('/scopes/<int:id>')
class Scopes(Resource):
    model = api.model('Model', {
        'id': fields.Integer,
        'area': fields.String,
    })

    @api.marshal_with(model)
    def get(self,id):
        Scopes = queries.query_get_scopes(id)
        return Scopes


@api.route('/materials')
class Materials(Resource):
    model = api.model('Model', {
        'id': fields.Integer,
        'name': fields.String,
    })

    @api.marshal_with(model)
    def get(self, **kwargs):
        Materials = queries.query_get_materials()
        return Materials


@api.route('/procs')
class Procs(Resource):
    model = api.model('Model', {
        'id': fields.Integer,
        'proc': fields.String,
        'description': fields.String,
    })

    @api.marshal_with(model)
    def get(self, **kwargs):
        procs = queries.query_get_procs()
        return procs


@api.route('/purposes')
class Purposes(Resource):
    model = api.model('Model', {
        'id': fields.Integer,
        'name': fields.String,
    })

    @api.marshal_with(model)
    def get(self, **kwargs):
        purposes = queries.query_get_purposes()
        return purposes


@api.param('org_id', 'id of the organization the plant belongs to')
@api.param('unit_id', 'id of the unit the plant belongs to')
@api.route('/plants/<int:org_id>/<int:unit_id>')
class Plants(Resource):
    model = api.model('Model', {
        'id': fields.Integer,
        'abbr': fields.String,
        'name': fields.String,
    })

    @api.marshal_with(model)
    def get(self, org_id, unit_id):
        plants = queries.query_get_plant1(org_id, unit_id)
        return plants


@api.param('id', 'substance_id of the chemical')
@api.doc('filename includes path of the requested file')
@api.route('/sds/<int:id>')
class SDS(Resource):
    model = api.model('Model', {
        'id': fields.Integer,
        'filename': fields.String,
    })
# !!! dummy path!!! needs to be changed in queries.py!!!
    @api.marshal_with(model)
    def get(self, id):
        SDS = queries.query_get_sds(id)
        return SDS


@api.param('org_id', 'organization_id for scopes')
@api.param('unit_id', 'unit id for plants')
@api.route('/usages/resources/<int:org_id>/<int:unit_id>')
class CSResources(Resource):
    """get all necessary data for a new usage: procedures, scopes,materials,
     procs, purposes, plants, and put them into a nested dictionary"""

    procedure_fields = api.model('Procedures', {
        'id': fields.Integer,
        'name': fields.String,
    })

    scope_fields = api.model('Scopes', {
        'id': fields.Integer,
        'area': fields.String,
    })

    materials_fields = api.model('Materials', {
        'id': fields.Integer,
        'proc': fields.String,
        'description': fields.String,
    })

    procs_fields = api.model('Procs', {
        'id': fields.Integer,
        'proc': fields.String,
        'description': fields.String,
    })

    purpose_fields = api.model('Model', {
        'id': fields.Integer,
        'name': fields.String,
    })

    plant_fields = api.model('Model', {
        'id': fields.Integer,
        'abbr': fields.String,
        'name': fields.String,
    })

    resources_list_fields = api.model('ResourcesList', {
        'procedures': fields.List(fields.Nested(procedure_fields)),
        'scopes': fields.List(fields.Nested(scope_fields)),
        'materials': fields.List(fields.Nested(materials_fields)),
        'procs': fields.List(fields.Nested(procs_fields)),
        'purposes': fields.List(fields.Nested(purpose_fields)),
        'plants': fields.List(fields.Nested(plant_fields))
    })


    @api.marshal_with(resources_list_fields)
    def get(self, org_id, unit_id):
        procedures = queries.query_get_procedures()
        scopes = queries.query_get_scopes(org_id)
        materials = queries.query_get_materials()
        procs = queries.query_get_procs()
        purposes = queries.query_get_purposes()
        plants = queries.query_get_plant1(org_id, unit_id)
        resource_dict = {'procedures': procedures, 'scopes': scopes,
                         'materials': materials, 'procs': procs, 'purposes':
                         purposes, 'plants': plants,}

        return resource_dict


@api.route('/usages')
class Usage(Resource):
    model = api.model('Model', {
        'hs_id': fields.Integer(required=True),
        'org_id': fields.Integer(required=True),
        'plant_id': fields.Integer(required=True),
        'active': fields.Integer(required=True),
        'scope_id': fields.Integer(required=True),
        'proc_id': fields.Integer(required=True),
        'purpose_id': fields.Integer(required=True),
        'material_id': fields.Integer(required=True),
        'procedure_id': fields.Integer(required=True),
        'qty': fields.Integer(required=True),
        'excrete': fields.Integer(required=True),
        'frequency': fields.Integer(required=True),
        'surface': fields.Integer(required=True),
        'duration': fields.Integer(required=True),
        'air_supply': fields.Integer(required=True),
        'flammable': fields.Integer(required=True),
        'closed_system': fields.Integer(required=True),
        'dusting': fields.Integer(required=True)
    })


    @api.expect(model)
    def post(self):
        # api.payload is a dict -> all values have to be extracted before
        # passing to new_usage function
        queries.post_new_usage(api.payload)



if __name__ == '__main__':

    app.run('127.0.0.1', 5000, debug=True)
