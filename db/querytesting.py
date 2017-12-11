from sqlalchemy.ext.associationproxy import association_proxy
from db import connections
#from db import models_manual
from db import models
import datetime
import queries


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


   # queries.new_usage(test_hs_id, testorg_id, testplant_id, testlevel, testscope_id,
    #          testproc_id, testpurpose_id, testmaterial_id, testprocedure_id,
   #           testquantity, middle, high, low, low, v_high, low, high, middle)


    id = queries.testquery('Atropine', session)
    print(id)




