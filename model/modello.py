from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._years = []
        self._shapes = []
        self._sightings = []
        self._idMapS = {}
        self._graph = nx.DiGraph()

    def getAllYears(self):
        self._years = DAO.getAllYears()
        return self._years

    def getAllShapes(self,year):
        self._shapes = DAO.getAllShapes(year)
        return self._shapes

    def getAllNodes(self,shape,year):
        self._sightings = DAO.getAllNodes(shape,year)
        return self._sightings

    def creaGrafo(self,shape,year):
        self._graph.clear()
        self._sightings = DAO.getAllNodes(shape,year)
        for s in self._sightings:
            self._idMapS[s.id] = s
        self._graph.add_nodes_from(self._sightings)

        allEdges = DAO.getAllEdges(shape,year, self._idMapS)
        for e in allEdges:
            self._graph.add_edge(e.s1, e.s2)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getCompConnessa(self):
        comp_connesse = list(nx.weakly_connected_components(self._graph))
        if len(comp_connesse) == 0:
            return 0, []  # Ritorna 0 componenti e una lista vuota

        num = len(comp_connesse)
        comp_max = max(comp_connesse, key=len)
        return num, comp_max