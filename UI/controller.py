from datetime import datetime
import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceArrivo = None
        self._choicePartenza = None

    def handleAnalizza(self, e):
        cMinTxt = self._view._txtInCMin.value
        if cMinTxt == "":
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Inserire un valore numerico per numero minimo compagnie.", color="red"))
            self._view.update_page()
            return

        try:
            cMin = int(cMinTxt)
        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Inserire un valore intero per numero minimo compagnie.", color="red")
            )
            self._view.update_page()
            return

        if cMin <= 0:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Il filtro sul numero di compagnie deve essere un intero positivo.", color="red")
            )
            self._view.update_page()
            return

        self._model.buildGraph(cMin)
        numNodes, numEdges = self._model.getGraphDetails()
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text(f"Grafo correttamente creato: ", color="green")
        )
        self._view._txtResults.controls.append(
            ft.Text(f"Il grafo contiene {numNodes} nodi e {numEdges} archi. ", color="green")
        )
        allNodes = self._model.getAllNodes()
        self._fillDropdown(allNodes)
        self._view.update_page()

    def handleTestConnessione(self, e):
        if self._choicePartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione, per usare questo metodo occorre selezionare un aeroporto di partenza.",
                        color="red")
            )
            self._view.update_page()
            return

        if self._choiceArrivo is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione, per usare questo metodo occorre selezionare un aeroporto di partenza.",
                        color="red")
            )
            self._view.update_page()
            return

        if not self._model.hasPath(self._choicePartenza, self._choiceArrivo):
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text(f"Non ho trovato un cammino fra {self._choicePartenza} e {self._choiceArrivo}.", color="orange"))
            self._view.update_page()
            return

        path = self._model.getPath(self._choicePartenza, self._choiceArrivo)

        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(ft.Text(f"Ho trovato un cammini tra {self._choicePartenza} e {self._choiceArrivo}. Di seguito i nodi che compongono il cammino.", color="green"))
        for p in path:
            self._view._txtResults.controls.append(ft.Text(p))
        self._view.update_page()

    def handleConnessi(self, e):
        if self._choicePartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione, per usare questo metodo occorre selezionare un aeroporto di partenza.",
                        color="red")
            )
            self._view.update_page()
            return

        viciniT = self._model.getViciniOrdinati(self._choicePartenza)
        self._view._txtResults.controls.clear()
        for v in viciniT:
            self._view._txtResults.controls.append(ft.Text(f"{v[0]} - peso: {v[1]}"))
        self._view.update_page()

    def handleCerca(self, e):
        if self._choicePartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione, per usare questo metodo occorre selezionare un aeroporto di partenza.",
                        color="red")
            )
            self._view.update_page()
            return

        if self._choiceArrivo is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione, per usare questo metodo occorre selezionare un aeroporto di partenza.",
                        color="red")
            )
            self._view.update_page()
            return

        t = self._view._txtInNTratteMax.value

        try:
            tInt = int(t)
        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text(f"Il valore di t deve essere un intero positivo.", color="red")
            )
            self._view.update_page()
            return

        tic = datetime.now()
        path, score = self._model.getCamminoOttimo(self._choicePartenza, self._choiceArrivo, tInt)
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text(f"Cammino fra {self._choicePartenza} e {self._choiceArrivo} trovato.", color="green")
        )
        self._view._txtResults.controls.append(
            ft.Text(f"Il cammino ha uno score complessivo pari a {score} e contiene i seguenti nodi: ", color="green")
        )

        for p in path:
            self._view._txtResults.controls.append(ft.Text(p, color="green"))
        self._view._txtResults.controls.append(
            ft.Text(f"Cammino trovato in {datetime.now() - tic} secondi.")
        )
        self._view.update_page()

    def _fillDropdown(self, allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(
                ft.dropdown.Option(data = n, key = n.IATA_CODE, on_click=self._choiceDDPartenza)
            )
            self._view._ddAeroportoA.options.append(
                ft.dropdown.Option(data = n, key = n.IATA_CODE, on_click=self._choiceDDArrivo)
            )

    def _choiceDDPartenza(self, e):
        self._choicePartenza = e.control.data
        print(f"Hai selezionato come aeroporto di partenza {self._choicePartenza}")

    def _choiceDDArrivo(self, e):
        self._choiceArrivo = e.control.data
        print(f"Hai selezionato come aeroporto di arrivo {self._choiceArrivo}")