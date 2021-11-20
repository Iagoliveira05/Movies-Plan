from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from random import choice
import banco

class Tela:
    cor_fundo = "#D00000"
    cor_botao = "#E85D04"
    cor_botao_pressionado = "#BB3E03"
    def __init__(self):
        self.root = root
        self.configura_tela()
        self.tela_principal()
        root.mainloop()
    
    def configura_tela(self):
        self.root.title("Movies Plan")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)
        self.root.configure(bg=self.cor_fundo)

    def tela_principal(self):
        lb_titulo = Label(self.root, text="Movies Plan", font="Arial 80 bold", bg=self.cor_fundo)
        lb_titulo.pack(ipady=10)

        fr_principal = Frame(self.root, bg=self.cor_fundo)
        fr_principal.place(x=0, y=150, width=1000, height=500)

        lb_nome = Label(fr_principal, text="Nome", font="Arial 18 bold", bg=self.cor_fundo)
        lb_nome.place(x=140, y=5)
        self.tb_nome = Entry(fr_principal, font="Arial 12", relief="solid")
        self.tb_nome.place(x=50, y=40, width=250, height=25)

        lb_ordenar = Label(fr_principal, text="Ordenar por", font="Arial 18 bold", bg=self.cor_fundo)
        lb_ordenar.place(x=380, y=5)
        self.selecionado_ordem = StringVar()
        opcoes_ordem = ["Inclusão", "Nome", "Tipo", "Favoritos", "Vistos"]
        cb_tipo_ordem = ttk.Combobox(fr_principal, values=opcoes_ordem, textvariable=self.selecionado_ordem, state="readonly", font="Arial 12")
        cb_tipo_ordem.set(opcoes_ordem[0])
        cb_tipo_ordem.place(x=330, y=40, width=250, height=25)
        cb_tipo_ordem.bind("<<ComboboxSelected>>", self.ordenar)

        lb_tipo = Label(fr_principal, text="Tipo", font="Arial 18 bold", bg=self.cor_fundo)
        lb_tipo.place(x=720, y=5)
        self.selecionado = StringVar()
        opcoes = ["Série", "Filme", "Documentário"]
        cb_tipo = ttk.Combobox(fr_principal, values=opcoes, textvariable=self.selecionado, state="readonly", font="Arial 12")
        cb_tipo.set(opcoes[0])
        cb_tipo.place(x=620, y=40, width=250, height=25)

        imagem = PhotoImage(file="roleta.png")
        self.botao = Button(fr_principal, image=imagem, command=self.sortear, borderwidth=0)
        self.botao.imagem = imagem
        self.botao.place(x=900, y=12, width=50, height=54)

        scroll = Scrollbar(fr_principal)
        scroll.place(x=953, y=80, height=300)

        self.tv = ttk.Treeview(fr_principal, columns=("numero", "nome", "tipo", "visto", "favorito"), show="headings", yscrollcommand=scroll.set, selectmode="browse")
        style = ttk.Style()
        style.configure("Treeview.Heading", font="Arial 15 bold")
        self.tv.column("numero", anchor=N, minwidth=0, width=30)
        self.tv.column("nome", anchor=N, minwidth=0, width=250)
        self.tv.column("tipo", anchor=N, minwidth=0, width=250)
        self.tv.column("visto", anchor=N, minwidth=0, width=150)
        self.tv.column("favorito", anchor=N, minwidth=0, width=150)
        self.tv.heading("numero", text="N°")
        self.tv.heading("nome", text="NOME")
        self.tv.heading("tipo", text="TIPO")
        self.tv.heading("visto", text="VISTO")
        self.tv.heading("favorito", text="FAVORITO")

        self.tv.place(x=50, y=80, width=900, height=300)
        self.mostrar_dados()

        scroll.config(command=self.tv.yview)

        btn_inserir = Button(fr_principal, text="Inserir", font="Arial 14 bold", fg="black", relief="raised", borderwidth=4, command=self.inserir, bg=self.cor_botao, activebackground=self.cor_botao_pressionado)
        btn_inserir.place(x=50, y=400, width=180, height=50)
        self.root.bind("<Return>", self.inserir)

        btn_visto = Button(fr_principal, text="Visto", font="Arial 14 bold", fg="black", relief="raised", borderwidth=4, command=self.marcar_visto, bg=self.cor_botao, activebackground=self.cor_botao_pressionado)
        btn_visto.place(x=290, y=400, width=180, height=50)

        btn_favorito = Button(fr_principal, text="Favoritar", font="Arial 14 bold", fg="black", relief="raised", borderwidth=4, command=self.marcar_favorito, bg=self.cor_botao, activebackground=self.cor_botao_pressionado)
        btn_favorito.place(x=530, y=400, width=180, height=50)

        btn_deletar = Button(fr_principal, text="Deletar", font="Arial 14 bold", fg="black", relief="raised", borderwidth=4, command=self.deletar, bg=self.cor_botao, activebackground=self.cor_botao_pressionado)
        btn_deletar.place(x=770, y=400, width=180, height=50)
        self.root.bind("<Delete>", self.deletar)

    def sortear(self):
        vquery = "SELECT nome FROM dados"
        linhas = banco.dql(vquery)
        opcoes = []
        for i in linhas:
            for nome in i:
                opcoes.append(nome)
        escolha = choice(opcoes)
        messagebox.showinfo(title="RECOMENDAÇÃO", message=f'Eu recomendo que você assista "{escolha}"')

    def mostrar_dados(self):
        self.tv.delete(*self.tv.get_children())
        vquery = "SELECT * FROM dados order by numero"
        linhas = banco.dql(vquery)
        for i in linhas:
            self.tv.insert("", "end", values=i)

    def inserir(self, event=None):
        confirmacao_inserir = ""
        if self.tb_nome.get() == "":
            messagebox.showinfo(title="ERRO", message="Digite o nome do filme")
            return
        if self.selecionado.get() == "Série":
            confirmacao_inserir = messagebox.askyesno(title="CONFIRMAÇÃO", message=f'Deseja adicionar a série "{self.tb_nome.get()}"?')
        else:
            confirmacao_inserir = messagebox.askyesno(title="CONFIRMAÇÃO", message=f'Deseja adicionar o {self.selecionado.get().lower()} "{self.tb_nome.get()}"?')

        if confirmacao_inserir:
            vnome = self.tb_nome.get()
            vtipo = self.selecionado.get()
            self.tv.insert("", "end", values=(self.tb_nome.get(), self.selecionado.get()))
            try:
                vquery = "INSERT INTO dados (nome, tipo, visto, favorito) VALUES ('"+vnome+"', '"+vtipo+"', '', '')"
                banco.dml(vquery)
            except:
                messagebox.showinfo(title="ERRO", message="Erro ao inserir")
                return
            self.mostrar_dados()
            self.tb_nome.delete(0, END)

    def marcar_visto(self):
        confirmacao = ""
        try:
            itemSelecionado = self.tv.selection()[0]
            confirmacao = messagebox.askyesno(title="CONFIRMAÇÃO", message="Deseja marcar como já visto?")
        except:
            messagebox.showinfo(title="ERRO", message="Selecione um elemento a ser marcado como visto")
        if confirmacao:
            itens = self.tv.focus()
            valores = self.tv.item(itens)["values"]
            vnome = str(valores[1])
            try:
                vquery = "UPDATE dados SET visto='X' WHERE nome='"+vnome+"'"
                banco.dml(vquery)
            except:
                messagebox.showinfo(title="ERRO", message="Erro ao marcar como visto")
                return
            self.mostrar_dados()
            
    def marcar_favorito(self):
        confirmacao = ""
        try:
            itemSelecionado = self.tv.selection()[0]
            confirmacao = messagebox.askyesno(title="CONFIRMAÇÃO", message="Deseja marcar como favorito?")
        except:
            messagebox.showinfo(title="ERRO", message="Selecione um elemento a ser marcado como favorito")
        if confirmacao:
            itens = self.tv.focus()
            valores = self.tv.item(itens)["values"]
            vnome = str(valores[1])
            try:
                vquery = "UPDATE dados SET favorito='X' WHERE nome='"+vnome+"'"
                banco.dml(vquery)
            except:
                messagebox.showinfo(title="ERRO", message="Erro ao marcar como favorito")
                return
            self.mostrar_dados()

    def deletar(self, event=None):
        confirmacao = ""
        try:
            itemSelecionado = self.tv.selection()[0]
            confirmacao = messagebox.askyesno(title="CONFIRMAÇÃO", message="Deseja excluir?")
        except:
            messagebox.showinfo(title="ERRO", message="Selecione um elemento a ser deletado")
        if confirmacao:
            itens = self.tv.focus()
            vnome = str(self.tv.item(itens)["values"][1])
            senha = simpledialog.askstring("Senha", "Digite a senha de Admin para excluir", show="•")
            if senha == "admin123":
                try:
                    vquery = "DELETE FROM dados WHERE nome='"+vnome+"'"
                    banco.dml(vquery)
                except:
                    messagebox.showinfo(title="ERRO", message="Erro ao deletar dado")
                    return
                self.tv.delete(itemSelecionado)
            else:
                messagebox.showinfo(title="ERRO", message="Senha de admin incorreta")
        
    def ordenar(self, event=None):
        ordem = self.selecionado_ordem.get().lower()
        if ordem == "inclusão":
            vquery = "SELECT * FROM dados order by numero"
        elif ordem == "nome":
            vquery = "SELECT * FROM dados order by nome"
        elif ordem == "tipo":
            vquery = "SELECT * FROM dados order by tipo"
        elif ordem == "vistos":
            vquery = "SELECT * FROM dados order by visto DESC"
        elif ordem == "favoritos":
            vquery = "SELECT * FROM dados order by favorito DESC"
        self.tv.delete(*self.tv.get_children())
        linhas = banco.dql(vquery)
        for i in linhas:
            self.tv.insert("", "end", values=i)
                

root = Tk()
Tela()