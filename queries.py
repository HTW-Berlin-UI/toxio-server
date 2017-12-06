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


if __name__ == "__main__":

    session = connections.make_session()

    testchem1 = 'Oxytocin'
    testchem2 = 'Atropine'
    testchem3 = 'DL-Tryptophan'
    test_hs_id = 1258 # Oxytocin
    testorg_id = 19   # Musterunternehmen
    testunit_id = 162  # Standort Köln

    #testdata for new usage:
    testscope_id = 73   # Oberflächenbehandlung
    testproc_id = 7  # PROC15
    testpurpose_id = 8  # Kalibrierung
    testmaterial_id = 6 # Glas
    testprocedure_id = 3  # Streichen
    low = 1
    middle = 2
    high = 4
    testquantity = 15
    testdate = datetime.datetime.now
    flammability = 1
    dusty=3

    # new usage: hs_organization_id (from chem_scan_hs_organization!!!), scope_id, proc_id, purpose_id, material_id,
    # procedure_id, qty, excrete,frequency, surface, duration, air_supply, flammable,
    # closed_system, dusting

    new_hs_org = insert_new_hs_org(test_hs_id, testorg_id, low)
    session.add(new_hs_org)
    session.commit()

    new_id = new_hs_org.id


    new_usage = insert_new_usage(new_id, testscope_id, testproc_id,
                                 testpurpose_id, testmaterial_id, testprocedure_id,
                                 testquantity, ex=high, frequ=low, sur=middle,
                                 dur=low, air=high, flamm=flammability, sys=low,
                                 dust=dusty)


    session.add(new_usage)
    session.commit()

    # connect plant and usage via hs_usage_plant
    # connect usage and hs via hs_substitute


# Bei Anlegen einer neuen Anwendung Zuordnung zu Plant über hs_usage_plant
# Zuordnung zu einer HS und einer Organisation über hs_substitute


# new usage consists of: insert_new_hs_org, insert_new_usage,
# + connection plant to usage via _hs_usage_plant, and connection usage to hs via _hs_substitute
# -> noch zu machen: new ChemScanHsUsagePlant, new ChemScanHsSubstitute