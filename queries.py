import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from db import connections
#from db import models_manual
from db import models



def query_get_substance(testchem):
    """enter substance name and get substance_id from chem_scan_substance"""
    for instance in session.query(models.ChemScanSubstance).filter(
        models.ChemScanSubstance.name == testchem):
        return instance.name

def query_get_hs_id(testchem):
    """ enter substance name and get hs_id from chem_scan_hs"""
    for instance in session.query(models.ChemScanH).join(models.ChemScanHsSubstance).filter(
        models.ChemScanH.id == models.ChemScanHsSubstance.hs_id).join(
        models.ChemScanSubstance).filter(models.ChemScanHsSubstance.substance_id==
        models.ChemScanSubstance.id).filter(models.ChemScanSubstance.name==testchem):
            return instance.id


def query_get_sds(testchem):
    """enter a substance name and get the filename for the sds"""
    hs_id = query_get_hs_id(testchem)
    for instance in session.query(models.OroAttachmentFile).join(
        models.ChemScanSafetyDatasheet).filter(models.OroAttachmentFile.id ==
        models.ChemScanSafetyDatasheet.document_id).join(models.ChemScanH).filter(
        models.ChemScanSafetyDatasheet.hs_id == models.ChemScanH.id).filter(
        models.ChemScanH.id == hs_id):
            return instance.filename


def query_get_plant1(testorg_id, testunit_id):
    """enter organization AND unit and get all plants ->
    test data plant = Lackierroboter AL-Pig I"""

    query = session.query(models.ChemScanPlant).join(models.OroOrganization).filter(
        models.OroOrganization.id == models.ChemScanPlant.organization_id).join(
        models.ChemScanOrganizationUnit).filter(models.ChemScanOrganizationUnit.id==
        models.ChemScanPlant.organization_unit_id).filter(models.OroOrganization.id == testorg_id,
        models.ChemScanOrganizationUnit.id == testunit_id).all()
    return query

def query_get_plant2(testorg_id):
    """enter an organization and get all plants"""
    query = session.query(models.ChemScanPlant).join(models.OroOrganization).filter(
        models.OroOrganization.id == models.ChemScanPlant.organization_id).filter(
                models.OroOrganization.id == testorg_id).all()
    return query


def query_get_scope(testorg_id):
    """list of scopes for given organization"""
    query = session.query(models.ChemScanScope).filter(
            models.ChemScanScope.organization_id == testorg_id).all()
    return query

def query_get_proc():
    """list of all procs"""
    query = session.query(models.ChemScanProc).all()
    return query

def query_get_purpose():
    """list of all purposes"""
    query = session.query(models.ChemScanPurpose).all()
    return query

def query_get_procedure():
    """list of all procedures"""
    query = session.query(models.ChemScanProcedure).all()
    return query

def query_get_material():
    """list of all materials"""
    query = session.query(models.ChemScanMaterial).all()
    return query


def insert_new_hs_org(test_hs_id, testorg_id, level):
    """before inserting a new usage, inserts data into chem_scan_hs_organization"""
    new_hs_org = models.ChemScanHsOrganization(hs_id=test_hs_id,
                                               organization_id=testorg_id,
                                               active=level)

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


def new_usage(hs_id, org_id, plant_id, level, scope_id, proc_id, purpose_id,
              material_id, procedure_id, quant, ex, frequ, sur, dur, air,
              flamm, sys, dust):
    """all inserts necessary to make a new usage:
    - connection usage to organization: entry to chem_scan_hs_organization
    - new usage: entry to chem_scan_hs_usage
    - connection between usage and plant: entry to chem_scan_hs_usage_plant
    - necessary entry to chem_scan_hs_substitution
    - connection between usage and hazard substance: entry to chem_scan_hs_substitute
    """
    new_hs_org = insert_new_hs_org(hs_id, org_id, level)
    session.add(new_hs_org)
    session.commit()
    new_id = new_hs_org.id  # usage needs id from chem_scan_hs_org
    new_usage = insert_new_usage(new_id, scope_id, proc_id, purpose_id, material_id,
                     procedure_id, quant, ex, frequ, sur, dur, air, flamm,
                     sys, dust)
    session.add(new_usage)
    session.commit()
    new_hs_usage_id = new_usage.id
    new_hs_plant = hs_plant(new_hs_usage_id, plant_id, quant)
    session.add(new_hs_plant)
    session.commit()
    new_hs_substitution = hs_substitution(hs_id, new_hs_usage_id,
                    org_id, purpose_id, material_id,
                    procedure_id, proc_id, quant, ex, frequ, sur, dur,
                    air)
    session.add(new_hs_substitution)
    session.commit()
    new_hs_sub = new_substitute(new_hs_substitution, org_id, hs_id, new_hs_usage_id)
    session.add(new_hs_sub)
    session.commit()



if __name__ == "__main__":

    session = connections.make_session()

    testchem1 = 'Oxytocin'
    testchem2 = 'Atropine'
    testchem3 = 'DL-Tryptophan'
    test_hs_id = 1258 # Oxytocin
    testorg_id = 19   # Musterunternehmen
    testunit_id = 162  # Standort Köln
    testplant_id = 197 # Anlage Münster

    #testdata for new usage:
    testscope_id = 73   # Oberflächenbehandlung
    testproc_id = 7  # PROC15
    testpurpose_id = 8  # Kalibrierung
    testmaterial_id = 6 # Glas
    testprocedure_id = 3  # Streichen
    testquantity = 15
    testdate = datetime.datetime.now
    not_null = 0  # where not null but no value available
    testlevel = 5
    # for qty (quantity), ex(excrete), frequ(frequency), sur (surface),
    # dur (duration), air (air_supply), flamm (flammable), sys (closed_system)
    # dust (dusting) enter low, middle, high or v_high
    low = 1
    middle = 2
    high = 4
    v_high = 8


    # new usage: hs_organization_id (from chem_scan_hs_organization!!!), scope_id, proc_id, purpose_id, material_id,
    # procedure_id, qty, excrete,frequency, surface, duration, air_supply, flammable,
    # closed_system, dusting


    new_usage(test_hs_id, testorg_id, testplant_id, testlevel, testscope_id,
              testproc_id, testpurpose_id, testmaterial_id, testprocedure_id,
              testquantity, middle, high, low, low, v_high, low, high, middle)













