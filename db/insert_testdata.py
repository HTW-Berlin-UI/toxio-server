from sqlalchemy.ext.associationproxy import association_proxy
from db import connections
#from db import models_manual
from db import models

"""
run this file before queries!!!


"""


if __name__ == "__main__":

    session = connections.make_session()


    # insert test data into table chem_scan_hs_substance (join table between
    # _hs and _substance which is empty)
    # data: Oxytocin substance_id 3, hs_id 1258
    #       Atropine substance_id 54, hs_id 1259
    #       DL-Tryptophan, substance_id 136, hs_id 1260
    # test sds file_names for oxy, atro and trypto link to these hs_ids


    oxy = models.ChemScanHsSubstance(substance_id=3, hs_id=1258, amount=10)
    session.add(oxy)
    atro = models.ChemScanHsSubstance(substance_id=54, hs_id=1259, amount=10)
    session.add(atro)
    trypto = models.ChemScanHsSubstance(substance_id=136, hs_id=1260, amount=10)
    session.add(trypto)

    session.commit()




