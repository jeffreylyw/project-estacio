import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import getDatabase as getDB
from clientes_frame import ClientesFrame  # Importar a classe ClientesFrame


class MercadoApp:
    def __init__(self, window):
        self.window = window
        self.window.geometry("966x718")
        self.window.resizable(0, 0)
        self.window.title("Controle Gerencial Mercado Seguro Imoveis")
        self.objDB = getDB.PostgresDB()

        # Frame principal que ocupa toda a janela
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill="both", expand=True)

        # Carregar a imagem de fundo
        self.bg_frame = Image.open("images\\mercadosegurologo.png")
        self.photo = ImageTk.PhotoImage(self.bg_frame)

        # Adicionar a imagem como um Label
        self.bg_panel = tk.Label(self.main_frame, image=self.photo)
        self.bg_panel.pack(expand=True)

        # Texto de boas vindas e botões de navegação
        self.lblWelcome = tk.Label(
            self.main_frame,
            text="Bem vindo ao Controle Gerencial da Mercado Seguro!",
            font=("Arial", 18, "bold"),
            fg="#14243c",
        )
        self.lblWelcome.place(relx=0.5, rely=0.1, anchor="center")

        style = ttk.Style()
        style.configure(
            "TButton",
            background="#ac844c",
            foreground="black",
            font=("Arial", 12, "bold"),
            padding=10,
        )
        style.map("TButton", background=[("active", "#14243c")])  # Cor quando ativo

        self.btnVerClientes = ttk.Button(
            self.main_frame,
            text="Clientes Cadastrados",
            command=self.show_clientes_frame,
            style="TButton",
        )
        self.btnVerClientes.place(relx=0.5, rely=0.22, anchor="center")

        self.btnRelatorioDiario = ttk.Button(
            self.main_frame,
            text="Relatório Diário",
            command=self.show_alert_soon,
            style="TButton",
        )
        self.btnRelatorioDiario.place(relx=0.5, rely=0.32, anchor="center")

        # Inicializar a view dos clientes
        self.clientes_view = ClientesFrame(self, self.objDB)

    def show_clientes_frame(self):
        self.main_frame.pack_forget()
        self.clientes_view.clientes_frame.pack(
            fill="both", expand=True, padx=20, pady=20
        )

    def show_main_frame(self):
        self.clientes_view.clientes_frame.pack_forget()  # Esconde o frame de clientes
        self.main_frame.pack(fill="both", expand=True)  # Mostra o frame principal

    def show_alert_soon(self):
        messagebox.showinfo("Aviso", "Essa função ainda está em desenvolvimento")


def page():
    window = tk.Tk()
    MercadoApp(window)
    window.mainloop()


if __name__ == "__main__":
    page()
