import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from getDatabase import PostgresDB


class ClientesFrame:
    def __init__(self, master, objDB):
        self.master = master
        self.objDB = objDB

        # Frame para mostrar os clientes
        self.clientes_frame = tk.Frame(self.master.window)
        self.clientes_frame.grid_rowconfigure(1, weight=1)
        self.clientes_frame.grid_columnconfigure(0, weight=1)

        # Frame para os botões
        self.btnFrame = tk.Frame(self.clientes_frame)
        self.btnFrame.grid(row=0, column=0, pady=(10, 0))

        # Carregar ícones e manter referências
        self.add_icon = ImageTk.PhotoImage(
            Image.open("icons\\add-icon.png").resize((30, 30), Image.LANCZOS)
        )
        self.edit_icon = ImageTk.PhotoImage(
            Image.open("icons\\edit-icon.png").resize((30, 30), Image.LANCZOS)
        )
        self.remove_icon = ImageTk.PhotoImage(
            Image.open("icons\\remove-icon.png").resize((30, 30), Image.LANCZOS)
        )

        # Botões com ícones
        self.btnAdd = tk.Button(
            self.btnFrame, image=self.add_icon, command=self.add_client, bd=1
        )
        self.btnEdit = tk.Button(
            self.btnFrame, image=self.edit_icon, command=self.edit_client, bd=1
        )
        self.btnRemove = tk.Button(
            self.btnFrame, image=self.remove_icon, command=self.remove_client, bd=1
        )

        self.btnAdd.grid(row=0, column=0, padx=5)
        self.btnEdit.grid(row=0, column=1, padx=5)
        self.btnRemove.grid(row=0, column=2, padx=5)

        # Frame para a Treeview
        self.treeFrame = tk.Frame(self.clientes_frame)
        self.treeFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Centralizar a treeview
        self.treeFrame.grid_rowconfigure(0, weight=1)
        self.treeFrame.grid_columnconfigure(0, weight=1)

        # Colunas da tabela
        self.dataColumn = (
            "Código do Cliente",
            "Nome",
            "CPF",
            "Data de Nascimento",
            "Email",
            "Telefone",
        )

        # Treeview para mostrar os clientes cadastrados
        self.treeClientes = ttk.Treeview(
            self.treeFrame,
            columns=self.dataColumn,
            show="headings",
            selectmode="extended",
        )
        self.treeClientes.grid(row=0, column=0, sticky="nsew")

        # Scrollbar vertical
        self.verscrlbar = ttk.Scrollbar(
            self.treeFrame, orient="vertical", command=self.treeClientes.yview
        )
        self.verscrlbar.grid(row=0, column=1, sticky="ns")
        self.treeClientes.configure(yscrollcommand=self.verscrlbar.set)

        # Cabeçalhos das colunas
        for col in self.dataColumn:
            self.treeClientes.heading(col, text=col)
            self.treeClientes.column(col, anchor="center", width=120, stretch=True)

        # Botões abaixo da Treeview
        self.btnBack = tk.Button(
            self.clientes_frame,
            text="Voltar",
            width=20,
            command=self.master.show_main_frame,
        )
        self.btnCopyEmail = tk.Button(
            self.clientes_frame,
            text="Copiar Emails",
            width=20,
            command=self.copy_selected_emails,
        )
        self.btnCopyPhone = tk.Button(
            self.clientes_frame,
            text="Copiar Telefones",
            width=20,
            command=self.copy_selected_phones,
        )

        # Posicionar os botões de ação abaixo da Treeview
        self.btnBack.grid(row=2, column=0, sticky="w", padx=10, pady=(5, 10))
        self.btnCopyEmail.grid(row=2, column=0, padx=150, pady=(5, 10))
        self.btnCopyPhone.grid(row=2, column=0, sticky="e", padx=10, pady=(5, 10))

        self.show_clientes_Treeview()

    def show_clientes_Treeview(self):
        # Limpar a Treeview antes de repopular
        for item in self.treeClientes.get_children():
            self.treeClientes.delete(item)

        # Recuperar todos os clientes do banco de dados
        clients = (
            self.objDB.selectAllData()
        )  # Suponha que você tenha uma função que retorna todos os clientes

        # Inserir os clientes na Treeview
        for client in clients:
            self.treeClientes.insert(
                "",
                "end",
                values=(
                    client["id"],
                    client["nome"],
                    client["cpf"],
                    client["dt_nascimento"],
                    client["email"],
                    client["telefone"],
                ),
            )

    # Funções para copiar dados selecionados
    def copy_selected_emails(self):
        selected_items = self.treeClientes.selection()
        if not selected_items:
            print("Nenhum cliente selecionado!")
            return

        emails = [self.treeClientes.item(item, "values")[4] for item in selected_items]
        self.master.window.clipboard_clear()
        self.master.window.clipboard_append(";".join(emails))
        print("Emails copiados para a área de transferência.")

    def copy_selected_phones(self):
        selected_items = self.treeClientes.selection()
        if not selected_items:
            print("Nenhum cliente selecionado!")
            return

        phones = [self.treeClientes.item(item, "values")[5] for item in selected_items]
        self.master.window.clipboard_clear()
        self.master.window.clipboard_append(" ".join(phones))
        print("Telefones copiados para a área de transferência.")

    def add_client(self):
        # Criar uma nova janela
        add_window = tk.Toplevel()
        add_window.title("Adicionar Cliente")

        # Campos para entrada
        tk.Label(add_window, text="Nome").grid(row=0, column=0, padx=10, pady=5)
        nome_entry = tk.Entry(add_window)
        nome_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="CPF").grid(row=1, column=0, padx=10, pady=5)
        cpf_entry = tk.Entry(add_window)
        cpf_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Data de Nascimento").grid(
            row=2, column=0, padx=10, pady=5
        )
        dt_nascimento_entry = tk.Entry(add_window)
        dt_nascimento_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Email").grid(row=3, column=0, padx=10, pady=5)
        email_entry = tk.Entry(add_window)
        email_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Telefone").grid(row=4, column=0, padx=10, pady=5)
        telefone_entry = tk.Entry(add_window)
        telefone_entry.grid(row=4, column=1, padx=10, pady=5)

        # Botão para adicionar cliente
        add_button = tk.Button(
            add_window,
            text="Adicionar",
            command=lambda: self.add_new_client(
                nome_entry.get(),
                cpf_entry.get(),
                dt_nascimento_entry.get(),
                email_entry.get(),
                telefone_entry.get(),
                add_window,
            ),
        )
        add_button.grid(row=5, columnspan=2, pady=10)

    def add_new_client(self, nome, cpf, dt_nascimento, email, telefone, window):
        try:
            self.objDB.insertData(nome, cpf, dt_nascimento, email, telefone)
            print("Cliente adicionado com sucesso.")
            self.show_clientes_Treeview()  # Atualiza a Treeview
            window.destroy()

        except Exception as e:
            print(f"Erro ao adicionar cliente: {e}")

    def edit_client(self):
        selected_item = self.treeClientes.selection()
        if not selected_item:
            messagebox.showwarning(
                "Edição de Cliente", "Selecione um cliente para editar."
            )
            return

        # Obter os dados do cliente selecionado
        item_values = self.treeClientes.item(selected_item)["values"]
        cliente_id = item_values[0]  # O ID do cliente pode estar na primeira coluna

        # Criar uma nova janela
        edit_window = tk.Toplevel()
        edit_window.title("Editar Cliente")

        # Campos para entrada
        tk.Label(edit_window, text="Nome").grid(row=0, column=0, padx=10, pady=5)
        nome_entry = tk.Entry(edit_window)
        nome_entry.insert(0, item_values[1])  # Preencher com o valor atual
        nome_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(edit_window, text="CPF").grid(row=1, column=0, padx=10, pady=5)
        cpf_entry = tk.Entry(edit_window)
        cpf_entry.insert(0, item_values[2])
        cpf_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(edit_window, text="Data de Nascimento").grid(
            row=2, column=0, padx=10, pady=5
        )
        dt_nascimento_entry = tk.Entry(edit_window)
        dt_nascimento_entry.insert(0, item_values[3])
        dt_nascimento_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(edit_window, text="Email").grid(row=3, column=0, padx=10, pady=5)
        email_entry = tk.Entry(edit_window)
        email_entry.insert(0, item_values[4])
        email_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(edit_window, text="Telefone").grid(row=4, column=0, padx=10, pady=5)
        telefone_entry = tk.Entry(edit_window)
        telefone_entry.insert(0, item_values[5])
        telefone_entry.grid(row=4, column=1, padx=10, pady=5)

        # Botão para salvar alterações
        save_button = tk.Button(
            edit_window,
            text="Salvar",
            command=lambda: self.save_edited_client(
                cliente_id,
                nome_entry.get(),
                cpf_entry.get(),
                dt_nascimento_entry.get(),
                email_entry.get(),
                telefone_entry.get(),
                edit_window,
            ),
        )
        save_button.grid(row=5, columnspan=2, pady=10)

    def save_edited_client(
        self, client_id, nome, cpf, dt_nascimento, email, telefone, window
    ):
        try:
            self.objDB.updateData(client_id, nome, cpf, dt_nascimento, email, telefone)
            print("Cliente editado com sucesso.")
            self.show_clientes_Treeview()  # Atualiza a Treeview

        except Exception as e:
            print(f"Erro ao editar cliente: {e}")

        # Fechar a janela de edição
        window.destroy()

    def remove_client(self):
        selected_item = self.treeClientes.selection()
        if not selected_item:
            messagebox.showwarning(
                "Remoção de Cliente", "Selecione um cliente para remover."
            )
            return

        # Confirmar remoção
        confirm = messagebox.askyesno(
            "Confirmar", "Tem certeza que deseja remover este cliente?"
        )
        if confirm:
            cliente_id = self.treeClientes.item(selected_item)["values"][
                0
            ]  # ID do cliente
            # Lógica para remover o cliente do banco de dados
            self.objDB.deleteData(cliente_id)

            # Remover da Treeview
            self.treeClientes.delete(selected_item)
