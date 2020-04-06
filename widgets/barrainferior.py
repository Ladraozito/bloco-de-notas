from tkinter import EW, W, Label


class BarraInferior:
    def __init__(self, master):
        self.barraInferior = Label(master, bg='pink')
        self.status = Label(self.barraInferior, text=master.chaveAtual, bg='pink')

        self.barraInferior.grid(row=3, column=1, columnspan=2, sticky=EW)
        self.status.grid(row=1, column=1, sticky=W)
