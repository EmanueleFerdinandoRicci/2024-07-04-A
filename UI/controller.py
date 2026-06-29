import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillYears(self):
        years = self._model.getAllYears()
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(year))
        self._view.update_page()

    def fillShapes(self,e):
        year = self._view.ddyear.value
        shapes = self._model.getAllShapes(year)
        for s in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.update_page()

    def handle_graph(self, e):
        self._model.creaGrafo(self._view.ddshape.value, self._view.ddyear.value)
        n, e = self._model.getGraphDetails()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(
            ft.Text(f"Grafo correttamente creato:")
        )
        self._view.txt_result1.controls.append(
            ft.Text(f"Numero di vertici: {n}")
        )
        self._view.txt_result1.controls.append(
            ft.Text(f"Numero di archi: {e}")
        )
        num, comp_max = self._model.getCompConnessa()
        self._view.txt_result1.controls.append(
            ft.Text(f"Il grafo ha: {num} componenti connesse.")
        )
        self._view.txt_result1.controls.append(
            ft.Text(f"La componente connessa più grande è composta da {len(comp_max)} nodi:")
        )
        for i in comp_max:
            self._view.txt_result1.controls.append(
                ft.Text(f"{i}")
            )
        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result2.controls.clear()

        # Avviamo l'algoritmo
        path, score = self._model.getBestPath()

        if not path:
            self._view.txt_result2.controls.append(
                ft.Text("Nessun cammino trovato con i criteri specificati.", color="red")
            )
            self._view.update_page()
            return

        # a. Stampiamo il punteggio totale del percorso ottenuto
        self._view.txt_result2.controls.append(
            ft.Text(f"Cammino ottimo trovato!")
        )
        self._view.txt_result2.controls.append(
            ft.Text(f"Punteggio Totale: {score} punti")
        )
        self._view.txt_result2.controls.append(
            ft.Text(f"Numero di tappe: {len(path)}")
        )

        for i in path:
            self._view.txt_result2.controls.append(
                ft.Text(f"{i}")
            )

        # Aggiorniamo la pagina Flet per mostrare i dati a video
        self._view.update_page()
