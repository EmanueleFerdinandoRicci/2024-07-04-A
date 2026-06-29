import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._years = []
        self._shapes = []
        self._sightings = []
        self._idMapS = {}
        self._graph = nx.DiGraph()
        self._bestPath = []
        self._bestScore = 0

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

    def getBestPath(self):
        # Inizializziamo le strutture per salvare il cammino migliore
        self._bestPath = []
        self._bestScore = 0

        # Proviamo a far partire il cammino da OGNI nodo presente nel grafo
        for nodo in self._graph.nodes:
            parziale = [nodo]

            # Dizionario per contare quanti avvistamenti abbiamo per ogni mese nel cammino attuale
            # Inizializzato a 0 per tutti i mesi (1-12)
            month_counts = {i: 0 for i in range(1, 13)}
            month_counts[nodo.datetime.month] = 1  # Contiamo il mese del primo nodo

            # Avviamo la ricorsione
            self._ricorsione(parziale, month_counts)

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, month_counts):
        # 1. Caso terminale "parziale": ad ogni passo valutiamo se il cammino attuale è il migliore
        punteggio_attuale = self.calcola_punteggio(parziale)
        if punteggio_attuale > self._bestScore:
            self._bestScore = punteggio_attuale
            self._bestPath = copy.deepcopy(parziale)  # Facciamo una copia della lista

        # Prendiamo l'ultimo nodo inserito nel cammino per vedere dove possiamo andare
        ultimo = parziale[-1]

        # 2. Esploriamo i successori (archi uscenti nel grafo orientato)
        for vicino in self._graph.successors(ultimo):
            # Vincolo strutturale: durata strettamente crescente
            if vicino.duration > ultimo.duration:
                mese_vicino = vicino.datetime.month

                # Vincolo globale: massimo 3 avvistamenti dello stesso mese nel cammino
                if month_counts[mese_vicino] < 3:
                    # I vincoli sono rispettati: proviamo ad aggiungere il nodo
                    parziale.append(vicino)
                    month_counts[mese_vicino] += 1

                    # Passo ricorsivo
                    self._ricorsione(parziale, month_counts)

                    # BACKTRACKING: torniamo allo stato precedente per esplorare altre strade
                    parziale.pop()
                    month_counts[mese_vicino] -= 1

    def calcola_punteggio(self, cammino):
        if not cammino:
            return 0

        # +100 punti per ogni avvistamento nel cammino
        punti = len(cammino) * 100

        # +200 punti se l'avvistamento è avvenuto nello stesso mese del precedente
        for i in range(1, len(cammino)):
            if cammino[i].datetime.month == cammino[i - 1].datetime.month:
                punti += 200

        return punti