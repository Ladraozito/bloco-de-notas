from tkinter import Menu


class BarraSuperior:
    def __init__(self, master):
        self.barraDeMenu = Menu(master, background='#FF00FF', foreground='pink',
                                activebackground='#FF00FF', activeforeground='pink')
        self.menuDeArquivo = Menu(self.barraDeMenu, background='#FF00FF',
                                  foreground='pink', activebackground='#FF00FF', activeforeground='pink')
        self.menuDeCodigo = Menu(self.barraDeMenu, background='#FF00FF',
                                 foreground='pink', activebackground='#FF00FF', activeforeground='pink')

        self.barraDeMenu.add_cascade(label='Arquivo', menu=self.menuDeArquivo)
        self.menuDeArquivo.add_command(label='Novo', command=master.novo)
        self.menuDeArquivo.add_command(label='Nova janela', command=master.novaJanela)
        self.menuDeArquivo.add_command(label='Carregar...', command=master.carregar)
        self.menuDeArquivo.add_command(label='Salvar', command=master.salvar)
        self.menuDeArquivo.add_command(label='Salvar como...', command=master.salvarComo)
        self.menuDeArquivo.add_separator()
        self.menuDeArquivo.add_command(label='Fechar', command=master.fecharJanela)

        self.barraDeMenu.add_cascade(label='Codificação', menu=self.menuDeCodigo)
        self.menuDeCodigo.add_command(label='UTF-8', command=lambda: master.mudarCodificacao('UTF-8'))
        self.menuDeCodigo.add_command(label='UTF-16', command=lambda: master.mudarCodificacao('UTF-16'))
        self.menuDeCodigo.add_command(label='UTF-32', command=lambda: master.mudarCodificacao('UTF-32'))
        self.menuDeCodigo.add_command(label='ASCII', command=lambda: master.mudarCodificacao('ASCII'))

        master.config(bg='pink', menu=self.barraDeMenu)
