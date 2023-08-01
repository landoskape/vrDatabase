import databaseManagement as dm

def createTables(database=None):
    try:
        engine = dm.createEngine(database)
        from tables import Base
        Base.metadata.create_all(engine)
        return True
    except Exception as e:
        print(e)
        return False
    

