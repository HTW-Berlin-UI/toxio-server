import io

from flask import Flask, Response
from flask import request
from flask_restplus import Api, Resource, fields, marshal
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


from flask_restplus import reqparse
import qrcode
import qrcode.image.svg

from db import queries, connections

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = connections.make_dsn()


db = SQLAlchemy(app)
api = Api(app)
CORS(app)



# API endpoints, include only neccessary fields (not things like additional_info, serialized_data...)
# Endpoints:
# GET: all procedures, all materials, all procs, all purposes,
# all scopes for specific organization; endpoint that combines all these together
# -> substances/resources; endpoint for all substances; endpoint get all plants
# for specific organization and unit; endpoint for sds
# POST: new usage



@api.route('/substances/<int:hs_id>/<int:organization_id>/<int:unit_id>/qrcode')
class QrCode(Resource):
    def get(self, hs_id, organization_id, unit_id):
        # data for qr code
        qr_hs_number = queries.query_get_hsnumber(hs_id)

        # schema: <prefix>?<organizationID>-<unitID>-<hsNumber>-<hsID>
        qr_data = "toxio://open?{}-{}-{}-{}".format(organization_id,
                                                    unit_id,
                                                    qr_hs_number,
                                                    hs_id)


        # create qr code with white background
        factory = qrcode.image.svg.SvgFillImage
        img = qrcode.make(data=qr_data, image_factory=factory)
        # create buffered stream to write in
        stream = io.BytesIO()
        # save image into stream
        img.save(stream)
        # Response expects bytes -> cast
        buffer = bytes(stream.getbuffer())

        return Response(buffer, mimetype="image/svg+xml")




@api.route('/substances')
class Substances(Resource):
    model = api.model('Substance', {
        'id': fields.Integer,
        'name': fields.String,
        'eg': fields.String,
        'cas': fields.String,
        'formula': fields.String,
    })

    @api.marshal_with(model)
    def get(self, **kwargs):
        substances = queries.query_get_all_substances()
        return substances



@api.route('/hazardsubstances')
class HazardSubstances(Resource):
    model = api.model('HazardSubstance', {
        'substance_id': fields.Integer,
        'hs_number': fields.String,
        'active': fields.Integer,
        'manufacturer_id': fields.Integer,
        'substance_name': fields.String,
        'approved': fields.Integer,
        'substance_eg': fields.String,
        'substance_cas': fields.String,
        'substance_formula': fields.String,
    })

    @api.marshal_with(model)
    def get(self, **kwargs):

        hazardsubstances = queries.query_get_all_hs()
        result = [{

            "substance_id": s.ChemScanSubstance.id,
            "hs_number": s.ChemScanH.hs_number,
            "active": s.ChemScanH.active,
            "manufacturer_id": s.ChemScanH.manufacturer_id,
            "substance_name": s.ChemScanSubstance.name,
            "approved": s.ChemScanH.approved,
            "substance_eg": s.ChemScanSubstance.eg,
            "substance_cas": s.ChemScanSubstance.cas,
            "substance_formula": s.ChemScanSubstance.formula,
        } for s in hazardsubstances]

        return result


@api.route('/procedures')
class Procedures(Resource):
    model = api.model('Procedure', {
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
    model = api.model('Scope', {
        'id': fields.Integer,
        'area': fields.String,
    })

    @api.marshal_with(model)
    def get(self,id):
        Scopes = queries.query_get_scopes(id)
        return Scopes


@api.route('/materials')
class Materials(Resource):
    model = api.model('Material', {
        'id': fields.Integer,
        'name': fields.String,
    })

    @api.marshal_with(model)
    def get(self, **kwargs):
        Materials = queries.query_get_materials()
        return Materials


@api.route('/procs')
class Procs(Resource):
    model = api.model('Proc', {
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
    model = api.model('Purpose', {
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
    model = api.model('Plant', {
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
    model = api.model('SDS', {
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
        'name': fields.String,
    })

    procs_fields = api.model('Procs', {
        'id': fields.Integer,
        'proc': fields.String,
        'description': fields.String,
    })

    purpose_fields = api.model('Purpose', {
        'id': fields.Integer,
        'name': fields.String,
    })

    plant_fields = api.model('Plant', {
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
    # for adding several plants


    model = api.model('Usage', {
        'hs_id': fields.Integer(required=True),
        'org_id': fields.Integer(required=True),
        'plant_ids': fields.List(fields.Integer(), required=True),
        'active': fields.Integer(required=False),
        'scope_id': fields.Integer(required=True),
        'proc_id': fields.Integer(required=False),
        'purpose_id': fields.Integer(required=True),
        'material_id': fields.Integer(required=True),
        'procedure_id': fields.Integer(required=False),
        'qty': fields.String(required=True),
        'excrete': fields.String(required=True),
        'frequency': fields.String(required=True),
        'surface': fields.String(required=True),
        'duration': fields.String(required=True),
        'air_supply': fields.String(required=True),
        'flammable': fields.String(required=True),  # yes or no -> 1 or 0
        'closed_system': fields.String(required=True), # yes or no -> 1 or 0
        'dusting': fields.String(required=False)
    })


    @api.expect(model)
    def post(self):
        # api.payload is a dict -> all values have to be extracted before
        # passing to new_usage function

        hs_id = api.payload['hs_id']
        org_id = api.payload['org_id']
        plant_ids = api.payload['plant_ids']
        active = api.payload.get('active', 'NO')
        scope_id = api.payload['scope_id']
        proc_id = api.payload.get('proc_id')
        purpose_id = api.payload['purpose_id']
        material_id = api.payload['material_id']
        procedure_id = api.payload.get('procedure_id')
        qty = api.payload['qty']
        excrete = api.payload['excrete']
        frequency = api.payload['frequency']
        surface = api.payload['surface']
        duration = api.payload['duration']
        air_supply = api.payload['air_supply']
        flammable = api.payload['flammable']
        closed_system = api.payload['closed_system']
        dusting = api.payload.get('dusting')

        queries.create_usage(hs_id, org_id, plant_ids, active, scope_id,
                             proc_id, purpose_id, material_id, procedure_id,
                             qty, excrete, frequency, surface, duration,
                             air_supply, flammable, closed_system, dusting)




if __name__ == '__main__':

    app.run('127.0.0.1', 5000, debug=True)
