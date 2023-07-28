import databaseManagement as dm

def createTables(database):
    try:
        engine = dm.openSession(database)
        from tables import Base
        Base.metadata.create_all(engine)
        return True
    except Exception as e:
        print(e)
        return False
    

