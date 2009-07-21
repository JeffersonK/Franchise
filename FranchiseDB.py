import ObjectDB

gsFranchiseDB = None

def initFranchiseDB():
    gsFranchiseDB = ObjectDB.ObjectDB("franchises", "frn")
