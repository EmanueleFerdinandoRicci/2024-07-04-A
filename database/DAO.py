from database.DB_connect import DBConnect
from model.arco import Arco
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(SUBSTRING(s.`datetime`, 1, 4)) as year
                        from sighting s
                        order by s.`datetime` desc """
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllShapes(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(s.shape) as shape
                        from sighting s
                        where substring(s.`datetime`,1,4) = %s and s.shape != "" and s.shape != "unknown"
                        order by s.shape asc"""
            cursor.execute(query, (year,))

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(shape,year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.*
                        from sighting s
                        where s.shape = %s and substring(s.`datetime`,1,4) = %s"""
            cursor.execute(query, (shape,year,))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(shape, year, idMapS):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s1.id as id1, s2.id as id2, s1.`datetime`, s2.`datetime` 
                        from sighting s1, sighting s2
                        where s1.state = s2.state and s1.id != s2.id and s1.`datetime` < s2.`datetime` 
                        and s1.shape = %s and s2.shape = %s and substring(s1.`datetime`,1,4) = %s and substring(s2.`datetime`,1,4) = %s"""
            cursor.execute(query, (shape, shape, year, year,))

            for row in cursor:
                result.append(Arco(idMapS[row["id1"]], idMapS[row["id2"]]))
            cursor.close()
            cnx.close()
        return result