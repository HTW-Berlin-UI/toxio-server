import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from db import connections
#from db import models_manual
from db import models

# some constants
VERY_HIGH = "VERY_HIGH"
HIGH = "HIGH"
MIDDLE = "MIDDLE"
LOW = "LOW"

EXPOSITION_FOO = {
    VERY_HIGH: 8,
    HIGH: 4,
    MIDDLE: 2,
    LOW: 1
}



def query_get_all_substances():
    """get a list of all chemicals in chem_scan_substance"""
    session = connections.get_session()
    query = session.query(models.ChemScanSubstance).all()
    return query


def query_get_all_hs():
    """joins chem_scan_hs and chem_scan_substance"""
    session = connections.get_session()

    query = session.query(models.ChemScanH, models.ChemScanSubstance).join(models.ChemScanHsSubstance).filter(
        models.ChemScanH.id == models.ChemScanHsSubstance.hs_id).join(
        models.ChemScanSubstance).filter(models.ChemScanHsSubstance.substance_id==
        models.ChemScanSubstance.id).all()

    return query



def query_get_hsid(query_id):
    """enter a substance id and get matching hs id"""
    session = connections.get_session()
    for instance in session.query(models.ChemScanHsSubstance).filter(
        models.ChemScanHsSubstance.substance_id == query_id):
        return instance

def testquery(testchem):
    session = connections.get_session()

    for instance in session.query(models.ChemScanSubstance).filter(
        models.ChemScanSubstance.name == testchem):

        return instance




def query_get_substance(testchem):
    """enter substance name and get substance_id from chem_scan_substance"""
    session = connections.get_session()
    for instance in session.query(models.ChemScanSubstance).filter(
        models.ChemScanSubstance.name == testchem):

        return instance.name





def query_get_hs_id(query_id):
    """ enter substance name and get hs_id from chem_scan_hs"""
    session = connections.get_session()
    for instance in session.query(models.ChemScanH).join(models.ChemScanHsSubstance).filter(
        models.ChemScanH.id == models.ChemScanHsSubstance.hs_id).join(
        models.ChemScanSubstance).filter(models.ChemScanHsSubstance.substance_id==
        models.ChemScanSubstance.id).filter(models.ChemScanSubstance.id==query_id):
        return instance.id


def query_get_sds(query_id):
    """enter a substance name and get the filename for the sds"""
    session = connections.get_session()
    # first get hs_id for given substance_id (query_id)
    hs_id = query_get_hs_id(query_id)
    for instance in session.query(models.OroAttachmentFile).join(
        models.ChemScanSafetyDatasheet).filter(models.OroAttachmentFile.id ==
        models.ChemScanSafetyDatasheet.document_id).join(models.ChemScanH).filter(
        models.ChemScanSafetyDatasheet.hs_id == models.ChemScanH.id).filter(
        models.ChemScanH.id == hs_id):
        # add a path to find document with filename
        instance.filename = '/..path../' + instance.filename
        return instance


def query_get_plant1(testorg_id, testunit_id):
    """enter organization AND unit and get all plants ->
    test data plant = Lackierroboter AL-Pig I"""
    session = connections.get_session()

    query = session.query(models.ChemScanPlant).join(models.OroOrganization).filter(
        models.OroOrganization.id == models.ChemScanPlant.organization_id).join(
        models.ChemScanOrganizationUnit).filter(models.ChemScanOrganizationUnit.id==
        models.ChemScanPlant.organization_unit_id).filter(models.OroOrganization.id == testorg_id,
        models.ChemScanOrganizationUnit.id == testunit_id).all()
    return query

def query_get_plant2(testorg_id):
    """enter an organization and get all plants"""
    session = connections.get_session()
    query = session.query(models.ChemScanPlant).join(models.OroOrganization).filter(
        models.OroOrganization.id == models.ChemScanPlant.organization_id).filter(
                models.OroOrganization.id == testorg_id).all()
    return query


def query_get_scopes(testorg_id):
    """list of scopes for given organization"""
    session = connections.get_session()
    query = session.query(models.ChemScanScope).filter(
            models.ChemScanScope.organization_id == testorg_id).all()
    return query

def query_get_procs():
    """list of all procs"""
    session = connections.get_session()
    query = session.query(models.ChemScanProc).all()
    return query

def query_get_purposes():
    """list of all purposes"""
    session = connections.get_session()
    query = session.query(models.ChemScanPurpose).all()
    return query

def query_get_procedures():
    """list of all procedures"""
    session = connections.get_session()
    query = session.query(models.ChemScanProcedure).all()
    return query

def query_get_materials():
    """list of all materials"""
    session = connections.get_session()
    query = session.query(models.ChemScanMaterial).all()
    return query


def insert_new_hs_org(test_hs_id, testorg_id, active):
    """before inserting a new usage, inserts data into chem_scan_hs_organization"""
    new_hs_org = models.ChemScanHsOrganization(hs_id=test_hs_id,
                                               organization_id=testorg_id,
                                               active=active)

    return new_hs_org


def insert_new_usage(new_id, scope_id, proc_id, purpose_id, material_id,
                     procedure_id, quant, ex, frequ, sur,
                     dur, air, flamm, sys, dust):
    """inserts emkg data into table chem_scan_hs_usage"""
    usage = models.ChemScanHsUsage(hs_organization_id=new_id,
                                       scope_id=scope_id,
                                       proc_id=proc_id,
                                       purpose_id=purpose_id,
                                       material_id=material_id,
                                       procedure_id=procedure_id,
                                       qty=quant, excrete=ex,
                                       frequency=frequ, surface=sur,
                                       duration=dur, air_supply=air,
                                       flammable=flamm,
                                       closed_system=sys, dusting=dust)
    return usage




def hs_plant(hs_usage_id, plant_id, quant):
    """connects a usage to a plant, entry to chem_scan_hs_usage_plant"""

    hs_plant = models.ChemScanHsUsagePlant(hs_usage_id=hs_usage_id,
                                           plant_id=plant_id, qty=quant)

    return hs_plant


def hs_substitution(hs_id, hs_usage_id, org_id, purpose_id, material_id,
                    procedure_id, proc_id, quant, ex, frequ, sur, dur,
                    air):
    """entry to table chem_scan_hs_substitution"""
    # substitute_id does not refer to table chem_scan_hs_substitute but chem_scan_hs!!!
    new_hs_substitution = models.ChemScanHsSubstitution(hs_id=hs_id,
                            hs_usage_id=hs_usage_id, hs_substitute_id=hs_id, organization_id=org_id,
                            purpose_id=purpose_id, material_id=material_id,
                            procedure_id=procedure_id, proc_id=proc_id, qty=quant,
                            excrete=ex, frequency=frequ, surface=sur, duration=dur,
                            air_supply=air, sds_revision=0,
                            hs_data=0, hs_substitute_data=0)

    return new_hs_substitution


def new_substitute(new_hs_substitution, org_id, hs_id, new_hs_usage_id):
    """entry to table chem_scan_hs_substitute"""

    new_hs_substitution_id = new_hs_substitution.id

    new_hs_sub = models.ChemScanHsSubstitute(organization_id=org_id,
                                             hs_id=hs_id,
                                             hs_usage_id=new_hs_usage_id,
                                             hs_substitution_id=new_hs_substitution_id)

    return new_hs_sub


def new_usage(hs_id, org_id, plant_id, active, scope_id, proc_id, purpose_id,
              material_id, procedure_id, qty, excrete, frequency, surface,
              duration, air_supply, flammable, closed_system, dusting):
    """all inserts necessary to make a new usage:
    - connection usage to organization: entry to chem_scan_hs_organization
    - new usage: entry to chem_scan_hs_usage
    - connection between usage and plant: entry to chem_scan_hs_usage_plant
    - necessary entry to chem_scan_hs_substitution
    - connection between usage and hazard substance: entry to chem_scan_hs_substitute

    """

    excrete = EXPOSITION_FOO[excrete]

    session = connections.get_session()
    new_hs_org = insert_new_hs_org(hs_id, org_id, active)
    session.add(new_hs_org)
    session.commit()
    new_id = new_hs_org.id  # usage needs id from chem_scan_hs_org
    new_usage = insert_new_usage(new_id, scope_id, proc_id, purpose_id,
                                 material_id, procedure_id, qty, excrete,
                                 frequency, surface, duration, air_supply,
                                 flammable, closed_system, dusting)
    session.add(new_usage)
    session.commit()
    new_hs_usage_id = new_usage.id
    new_hs_plant = hs_plant(new_hs_usage_id, plant_id, qty)
    session.add(new_hs_plant)
    session.commit()
    new_hs_substitution = hs_substitution(hs_id, new_hs_usage_id,
                                          org_id, purpose_id, material_id,
                                          procedure_id, proc_id, qty,
                                          excrete, frequency, surface,
                                          duration, air_supply)

    session.add(new_hs_substitution)
    session.commit()
    new_hs_sub = new_substitute(new_hs_substitution, org_id, hs_id,
                                new_hs_usage_id)
    session.add(new_hs_sub)
    session.commit()


def post_new_usage(hs_id, org_id, plant_id, active, scope_id, proc_id, purpose_id,
              material_id, procedure_id, qty, excrete, frequency, surface,
              duration, air_supply, flammable, closed_system, dusting):


    new_usage(hs_id, org_id, plant_id, active, scope_id, proc_id, purpose_id,
              material_id, procedure_id, qty, excrete, frequency, surface,
              duration, air_supply, flammable, closed_system, dusting)













