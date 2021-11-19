from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import banco

class Tela:
    cor_fundo = "#812"
    cor_botao = "#512"
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
        lb_nome.place(x=180, y=5)
        self.tb_nome = Entry(fr_principal, font="Arial 12", relief="solid")
        self.tb_nome.place(x=90, y=40, width=250, height=25)

        lb_tipo = Label(fr_principal, text="Tipo", font="Arial 18 bold", bg=self.cor_fundo)
        lb_tipo.place(x=760, y=5)
        self.selecionado = StringVar()
        opcoes = ["Série", "Filme", "Documentário"]
        cb_tipo = ttk.Combobox(fr_principal, values=opcoes, textvariable=self.selecionado, state="readonly", font="Arial 12")
        cb_tipo.set(opcoes[0])
        cb_tipo.place(x=660, y=40, width=250, height=25)

        self.tv = ttk.Treeview(fr_principal, columns=("nome", "tipo", "visto", "favorito"), show="headings")
        self.tv.column("nome", minwidth=0, width=250)
        self.tv.column("tipo", minwidth=0, width=250)
        self.tv.column("visto", minwidth=0, width=150)
        self.tv.column("favorito", minwidth=0, width=150)
        self.tv.heading("nome", text="NOME")
        self.tv.heading("tipo", text="TIPO")
        self.tv.heading("visto", text="VISTO")
        self.tv.heading("favorito", text="FAVORITO")

        self.tv.place(x=50, y=80, width=900, height=300)

        btn_inserir = Button(fr_principal, text="Inserir", command=self.inserir, bg=self.cor_botao)
        btn_inserir.place(x=50, y=400, width=180, height=50)

        btn_visto = Button(fr_principal, text="Visto", command=self.marcar_visto, bg=self.cor_botao)
        btn_visto.place(x=290, y=400, width=180, height=50)

        btn_favorito = Button(fr_principal, text="Favoritar", command=self.marcar_favorito, bg=self.cor_botao)
        btn_favorito.place(x=530, y=400, width=180, height=50)

        btn_deletar = Button(fr_principal, text="Deletar", command=self.deletar, bg=self.cor_botao)
        btn_deletar.place(x=770, y=400, width=180, height=50)


    def inserir(self):
        confirmacao_inserir = ""
        if self.tb_nome.get() == "":
            messagebox.showinfo(title="ERRO", message="Digite o nome do filme")
            return
        if self.selecionado.get() == "Série":
            confirmacao_inserir = messagebox.askyesno(title="CONFIRMAÇÃO", message=f'Deseja adicionar a série "{self.tb_nome.get()}"?')
        else:
            confirmacao_inserir = messagebox.askyesno(title="CONFIRMAÇÃO", message=f'Deseja adicionar o {self.selecionado.get().lower()} "{self.tb_nome.get()}"?')

        if confirmacao_inserir:
            self.tv.insert("", "end", values=(self.tb_nome.get(), self.selecionado.get()))
            banco.adicionar(self.tb_nome.get(), self.selecionado.get())
            self.tb_nome.delete(0, END)

    def marcar_visto(self):
        try:
            itemSelecionado = self.tv.selection()[0]
            confirmacao = messagebox.askyesno(title="CONFIRMAÇÃO", message="Deseja marcar como já visto?")
        except:
            messagebox.showinfo(title="ERRO", message="Selecione um elemento a ser marcado como visto")
        if confirmacao:
            itens = self.tv.focus()
            valores = self.tv.item(itens)["values"]
            nome = valores[0]
            tipo = valores[1]
            if len(valores) >= 3:
                favorito = valores[3]
                self.tv.insert("", "end", values=(nome, tipo, "X", favorito))
                itens2 = self.tv.focus()
                valores2 = self.tv.item(itens2)["values"]
                print("Valor 2", valores2)
            else:
                self.tv.insert("", "end", values=(nome, tipo, "X"))
            self.tv.delete(itemSelecionado)
            print("Valor 1", valores)
            
    def marcar_favorito(self):
        try:
            itemSelecionado = self.tv.selection()[0]
            confirmacao = messagebox.askyesno(title="CONFIRMAÇÃO", message="Deseja marcar como favorito?")
        except:
            messagebox.showinfo(title="ERRO", message="Selecione um elemento a ser marcado como favorito")
        if confirmacao:
            itens = self.tv.focus()
            valores = self.tv.item(itens)["values"]
            nome = valores[0]
            tipo = valores[1]
            if len(valores) == 3:
                visto = valores[2]
                self.tv.insert("", "end", values=(nome, tipo, visto, "X"))
            else:
                self.tv.insert("", "end", values=(nome, tipo, "", "X"))
            self.tv.delete(itemSelecionado)
            print(valores)

    def deletar(self):
        try:
            itemSelecionado = self.tv.selection()[0]
            self.tv.delete(itemSelecionado)
        except:
            messagebox.showinfo(title="ERRO", message="Selecione um elemento a ser deletado")

root = Tk()
Tela()