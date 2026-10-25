import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
    def _errore(self, msg):
        self._view._txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    def fillDDGeneri(self):
        for idG, nome in self._model.getGeneri():
            self._view._ddGenere.options.append(ft.dropdown.Option(key=str(idG), text=nome))


    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        genere = self._view._ddGenere.value

        self._model.buildGraph(genere)
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        # riempio il dropdown degli attori (punto 2)
        self._view._ddClienti.options.clear()
        self._view._ddClienti.value = None
        for a in self._model.getNodiOrdinati():
            self._view._ddClienti.options.append(ft.dropdown.Option(key=a.id, text=str(a)))

        self._view.update_page()

    def handleStampaInfo(self, e):
        self._view._txt_result.controls.clear()

        # il grafo deve esistere
        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # a. cliente con grado maggiore
        cliente, grado = self._model.getGradoMaggiore()
        self._view._txt_result.controls.append(
            ft.Text(f"Cliente con grado maggiore: {cliente} (grado: {grado})"))

        # b. cliente con somma pesi incidenti massima
        cliente, somma = self._model.getIncidenti()
        self._view._txt_result.controls.append(
            ft.Text(f"Cliente con somma pesi incidenti massima: {cliente} (somma: {somma})"))

        # c. cliente che ha speso di più
        cliente, spesa = self._model.getSpesaMax()
        self._view._txt_result.controls.append(
            ft.Text(f"Cliente che ha speso di più: {cliente} ({spesa:.2f} $)"))

        # d. 5 archi di peso maggiore
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(ft.Text("Top 5 archi di peso maggiore:"))
        for i, (n1, n2, peso) in enumerate(self._model.getTop5(), start=1):
            self._view._txt_result.controls.append(
                ft.Text(f"{i}. {n1} -- {n2} (album in comune: {peso})"))

        # e. componenti connesse
        numComp, dimMax = self._model.getComponenti()
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di componenti connesse: {numComp}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Dimensione della componente più grande: {dimMax}"))

        # f. paese con più clienti
        paese, numero = self._model.getPaese()
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(
            ft.Text(f"Paese con più clienti nel grafo: {paese} ({numero} clienti)"))

        self._view.update_page()

    def handleSequenza(self, e):
        self._view._txt_result.controls.clear()

        # 1. il grafo deve esistere
        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # 2. cliente di partenza
        if self._view._ddClienti.value is None:
            self._errore("Selezionare un cliente di partenza!")
            return
        partenza = self._model.getCliente(int(self._view._ddClienti.value))
        if partenza is None:
            self._errore("Cliente non presente nel grafo, ricreare il grafo!")
            return

        # 3. ricorsione
        percorso, peso = self._model.getPercorso(partenza)

        # 4. stampa
        if len(percorso) <= 1:
            self._errore(f"{partenza} non ha vicini: nessuna catena possibile")
            return

        self._view._txt_result.controls.append(
            ft.Text(f"Catena di affinità migliore partendo da {partenza}:"))
        self._view._txt_result.controls.append(ft.Text(f"1. {percorso[0]}"))
        for i in range(1, len(percorso)):
            p = self._model.getPesoArco(percorso[i - 1], percorso[i])
            self._view._txt_result.controls.append(
                ft.Text(f"{i + 1}. {percorso[i]} (album in comune con il precedente: {p})"))
        self._view._txt_result.controls.append(ft.Text(f"Peso totale: {peso}"))

        self._view.update_page()