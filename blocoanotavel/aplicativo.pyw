from tkinter import *
from tkinter import filedialog

import chardet
import os

from blocoanotavel.barrasuperior import BarraSuperior


class Aplicativo:
    def __init__(self, master=None):
        self.arquivoSalvo = False
        self.chaveAtual = 'UTF-8'
        self.diretorio = 'Arquivo novo'
        self.atual = master

        self.barraDeMenu = Menu(master)
        self.menuDeArquivo = Menu(self.barraDeMenu, tearoff=0)
        self.menuDeCodigo = Menu(self.barraDeMenu, tearoff=0)

        self.barraVertical = Scrollbar(master, orient=VERTICAL)
        self.barraHorizontal = Scrollbar(master, orient=HORIZONTAL)
        self.conteudo = Text(master, height=0, width=0, wrap=NONE,
                             xscrollcommand=self.barraHorizontal.set,
                             yscrollcommand=self.barraVertical.set)

        self.barraInferior = Label(master)
        self.status = Label(self.barraInferior, text=self.chaveAtual)

        self.janelaDeSalvar = None
        self.mensagem = self.conteudo.get(1.0, END)

        self.criarBarraSuperior()
        self.criarConteudo()
        self.criarBarraInferior()
        self.novo()

        master.after(0, self.verificarSalvamento)
        master.after(0, self.verificarStatus)
        master.protocol('WM_DELETE_WINDOW', self.fecharJanela)

    # Widgets
    def criarBarraSuperior(self):
        pass

    def criarConteudo(self):
        self.barraHorizontal.grid(row=2, column=1, sticky=EW)
        self.barraVertical.grid(row=1, column=2, sticky=NS)
        self.conteudo.grid(row=1, column=1, sticky=NSEW)

        self.barraHorizontal.config(command=self.conteudo.xview)
        self.barraVertical.config(command=self.conteudo.yview)

    def criarBarraInferior(self):
        self.barraInferior.grid(row=3, column=1, columnspan=2, sticky=EW)

        self.status.grid(row=1, column=1, sticky=W)

    # Funções
    def verificarSalvamento(self):
        if self.mensagem == self.conteudo.get(0.0, END):
            self.atual.title(f'{self.diretorio}   -   Bloco de Notas')
            self.arquivoSalvo = True
        else:
            self.atual.title(f'{self.diretorio} * -   Bloco de Notas')
            self.arquivoSalvo = False
        self.atual.after(10, self.verificarSalvamento)

    def verificarStatus(self):
        self.status['text'] = self.chaveAtual
        self.status.grid(row=1, column=2)
        self.atual.after(10, self.verificarStatus)

    def tentarAbrir(self):
        try:
            arquivo = open(self.diretorio, 'r', encoding=self.chaveAtual)
            self.mensagem = arquivo.read()
        except (UnicodeDecodeError, UnicodeError):
            arquivo = open(self.diretorio, 'br')
            self.mensagem = arquivo.read()
            chute = chardet.detect(self.mensagem)
            arquivo.close()
            arquivo = open(self.diretorio, 'r', encoding=chute['encoding'])
            self.mensagem = arquivo.read()
            arquivo.close()
            self.chaveAtual = chute['encoding']
        finally:
            arquivo.close()
            self.status['text'] = self.chaveAtual

    def novo(self):
        self.diretorio = 'Arquivo novo'
        self.conteudo.delete(1.0, END)
        self.mensagem = self.conteudo.get(1.0, END)

    def carregar(self):
        copia = self.diretorio
        self.diretorio = filedialog.askopenfilename(defaultextension='.txt',
                                                    filetypes=[('Arquivos de texto', '.txt'),
                                                               ('Todos arquivos', '.*')])
        if not self.diretorio:
            self.diretorio = copia
        else:
            self.tentarAbrir()
            self.conteudo.delete(1.0, END)
            self.conteudo.insert(END, self.mensagem)
            self.conteudo.delete(float(self.conteudo.index(END)) - 1.0)

    def salvar(self):
        if self.diretorio == 'Arquivo novo':
            self.salvarComo()
        else:
            self.salvarArquivo()

    def salvarComo(self):
        copia = self.diretorio
        self.diretorio = filedialog.asksaveasfilename(defaultextension='.txt',
                                                      filetypes=[('Arquivos de texto', '.txt'),
                                                                 ('Todos arquivos', '.*')],
                                                      initialfile='*.txt')
        if not self.diretorio:
            self.diretorio = copia
        else:
            self.salvarArquivo()

    def salvarArquivo(self):
        arquivo = open(self.diretorio, 'w', encoding=self.chaveAtual)
        texto = self.conteudo.get(1.0, END)
        arquivo.write(texto)
        arquivo.close()
        arquivo = open(self.diretorio, 'r', encoding=self.chaveAtual)
        self.mensagem = arquivo.read()
        arquivo.close()

    def mudarCodificacao(self, norma):
        self.chaveAtual = norma

    def fecharJanela(self):
        if self.janelaDeSalvar:
            self.janelaDeSalvar.lift()
        elif not self.arquivoSalvo:
            self.janelaDeSalvar = Toplevel()
            self.janelaDeSalvar.geometry('250x100+500+500')
            self.janelaDeSalvar.title(self.diretorio)
            self.janelaDeSalvar.grid_columnconfigure(0, weight=1)
            self.janelaDeSalvar.grid_columnconfigure(1, weight=1)
            self.janelaDeSalvar.grid_columnconfigure(2, weight=1)
            self.janelaDeSalvar.grid_rowconfigure(0, weight=3)
            self.janelaDeSalvar.grid_rowconfigure(1, weight=1)

            pergunta = Label(self.janelaDeSalvar, text='Deseja salvar?')
            pergunta.grid(column=0, row=0, columnspan=3, sticky=NSEW)
            pergunta['font'] = ('Arial', 20)

            botaoSalvar = Button(self.janelaDeSalvar, text='Salvar', width=6, command=self.sairSalvando)
            botaoSalvar.grid(column=0, row=1, sticky=W)

            botaoNaoSalvar = Button(self.janelaDeSalvar, text='Não salvar', width=6, command=self.sairSemSalvar)
            botaoNaoSalvar.grid(column=1, row=1, sticky=EW)

            botaoCancelar = Button(self.janelaDeSalvar, text='Cancelar', width=6, command=self.cancelar)
            botaoCancelar.grid(column=2, row=1, sticky=E)

            self.janelaDeSalvar.resizable(False, False)
            self.janelaDeSalvar.transient(self.atual)
            self.janelaDeSalvar.focus_force()
            self.janelaDeSalvar.grab_set()
            self.janelaDeSalvar.protocol('WM_DELETE_WINDOW', self.cancelar)
        else:
            self.atual.destroy()

    def sairSalvando(self):
        self.salvar()
        self.janelaDeSalvar.destroy()
        self.atual.destroy()
    
    def sairSemSalvar(self):
        self.janelaDeSalvar.destroy()
        self.atual.destroy()
    
    def cancelar(self):
        self.janelaDeSalvar.destroy()
        self.janelaDeSalvar = None


class Aspecto:
    def __init__(self, master=None):
        master.geometry('600x400')
        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(1, weight=1)
        if os.name == 'nt':
            master.iconbitmap('arquivos/icone.ico')


def novaJanela():
    janela = Tk()
    Aplicativo(janela)
    BarraSuperior(Aplicativo(janela))
    Aspecto(janela)
    janela.mainloop()


novaJanela()