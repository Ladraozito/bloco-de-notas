from tkinter import EW, NS, NSEW, Scrollbar, VERTICAL, HORIZONTAL, NONE, Text


class Conteudo:
    def __init__(self, master):
        self.barraVertical = Scrollbar(master, orient=VERTICAL)
        self.barraHorizontal = Scrollbar(master, orient=HORIZONTAL)
        self.conteudo = Text(master, height=0, width=0, wrap=NONE,
                             xscrollcommand=self.barraHorizontal.set,
                             yscrollcommand=self.barraVertical.set,
                             bg='pink')

        self.barraHorizontal.grid(row=2, column=1, sticky=EW)
        self.barraVertical.grid(row=1, column=2, sticky=NS)
        self.conteudo.grid(row=1, column=1, sticky=NSEW)

        self.barraHorizontal.config(command=self.conteudo.xview)
        self.barraVertical.config(command=self.conteudo.yview)
