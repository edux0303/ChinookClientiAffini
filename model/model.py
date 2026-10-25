import networkx as nx
from database.DAO import DAO
from itertools import combinations

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}

    # ==================== PUNTO 1 ====================

    def getGeneri(self):
        return DAO.getGeneri()

    def buildGraph(self,genere):
        self._grafo.clear()
        self._idMap = {}

        nodi = DAO.getNodi(genere)
        self._idMap = {at.id: at for at in nodi}
        self._grafo.add_nodes_from(nodi)
        for c,a in DAO.getCoppia(genere):
            if c in self._idMap:
                self._idMap[c].album.add(a)

        # arco se hanno almeno un film in comune, peso = numero di film in comune
        for a, b in combinations(nodi, 2):
            comuni = a.album & b.album
            if len(comuni) > 0:
                self._grafo.add_edge(a, b, weight=len(comuni))

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getNodiOrdinati(self):
        return sorted(self._grafo.nodes, key=lambda x: str(x))


    def getGradoMaggiore(self):
        best = None
        gradoMax = -1
        for n in self._grafo.nodes:
            grado = self._grafo.degree(n)
            if grado > gradoMax:
                gradoMax = grado
                best = n

        return best, gradoMax


    def getIncidenti(self):
        peso = -1
        cliente = None
        for n in self._grafo.nodes:
            p = self._grafo.degree(n, weight="weight")
            if p>peso:
                peso = p
                cliente = n
        return cliente,peso


    def getSpesaMax(self):
        spesaMax = -1
        cliente = None
        for n in self._grafo.nodes:
            if n.spesa > spesaMax:
                spesaMax = n.spesa
                cliente = n
        return cliente,spesaMax


    def getTop5(self):
        archi = []
        for u,v,dati in self._grafo.edges(data=True):
            nomi = sorted([str(u), str(v)])
            archi.append((nomi[0],nomi[1],dati["weight"]))
        archi.sort(key=lambda x: (-x[2],x[0],x[1]))
        return archi[:5]

    def getComponenti(self):
        componenti = list(nx.connected_components(self._grafo))
        piuGrande = max(componenti, key=len)
        return len(componenti), len(piuGrande)


    def getPaese(self):
        paesi = {}
        numero = -1

        for n in self._grafo.nodes:
            paesi[n.paese] = paesi.get(n.paese,0) +1

        best = None
        numero = -1

        for paese, conta in paesi.items():
            if conta > numero:
                numero = conta
                best = paese

        return best, numero


    def getCliente(self,idC):
        return self._idMap.get(idC)


    def getPercorso(self, film):
        self._solBest = []
        self._pesoBest = -1
        self._ricorsione([film], 0, float("inf"))
        return self._solBest, self._pesoBest


    def _ricorsione(self,parziale,peso,ultimoPeso):
        if peso > self._pesoBest:
            self._solBest = list(parziale)
            self._pesoBest = peso

        ultimo = parziale[-1]

        for v in self._grafo.neighbors(ultimo):
            pesoArco = self._grafo[ultimo][v]["weight"]
            if pesoArco < ultimoPeso and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale,peso+pesoArco,pesoArco)
                parziale.pop()


    def getPesoArco(self, u, v):
        return self._grafo[u][v]["weight"]



