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


if __name__ == "__main__":

    session = connections.make_session()

    testchem1 = 'Oxytocin'
    testchem2 = 'Atropine'
    testchem3 = 'DL-Tryptophan'
    testorg_id = 19   # Musterunternehmen
    testunit_id = 162  # Standort Köln









# Bei Anlegen einer neuen Anwendung Zuordnung zu Plant über hs_usage_plant
# Zuordnung zu einer HS und einer Organisation über hs_substitute


