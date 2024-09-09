import os
import psycopg2
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
from PIL import Image, ImageTk

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()


class Estoque:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        self.cur = self.conn.cursor()

    def adicionar_sola(self, descricao, quantidade):
        self.cur.execute(
            "INSERT INTO sola (descricao, quantidade) VALUES (%s, %s) RETURNING referencia",
            (descricao, quantidade)
        )
        referencia = self.cur.fetchone()[0]
        self.conn.commit()
        return referencia

    def buscar_sola(self, referencia):
        self.cur.execute("SELECT * FROM sola WHERE referencia = %s", (referencia,))
        return self.cur.fetchone()

    def listar_solas(self):
        self.cur.execute("SELECT * FROM sola")
        return self.cur.fetchall()

    def atualizar_quantidade(self, referencia, quantidade):
        self.cur.execute(
            "UPDATE sola SET quantidade = %s WHERE referencia = %s",
            (quantidade, referencia)
        )
        self.conn.commit()
        return self.cur.rowcount > 0

    def close(self):
        self.cur.close()
        self.conn.close()


class LoginScreen:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success

        root.title("Tela de Login")
        root.geometry("400x300")

        # Imagem opcional de fundo
        '''pil_image = Image.open("caminho/para/imagem.png")
        pil_image = pil_image.resize((400, 300), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(pil_image)
        bg_label = tk.Label(root, image=bg_image)
        bg_label.image = bg_image  # Manter referência da imagem
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)'''

        # Label e campos de entrada
        tk.Label(root, text="Usuário:").place(x=50, y=80)
        self.username_entry = tk.Entry(root)
        self.username_entry.place(x=150, y=80)

        tk.Label(root, text="Senha:").place(x=50, y=120)
        self.password_entry = tk.Entry(root, show='*')
        self.password_entry.place(x=150, y=120)

        # Botão de login
        tk.Button(root, text="Login", command=self.check_login).place(x=150, y=160)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Verificar as credenciais
        if username == "admin" and password == "1234":  # Substitua por verificação real
            messagebox.showinfo("Login bem-sucedido", "Bem-vindo!")
            self.on_login_success()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")


class MainApp:
    def __init__(self, root):
        self.estoque = Estoque()

        root.title("Gerenciamento de Estoque de Solas")
        root.geometry("800x800")

        # Configurar layout de grid com padding
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(9, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # Adicionar sola
        tk.Label(root, text="Descrição:").grid(row=1, column=1, sticky='e')
        self.desc_entry = tk.Entry(root)
        self.desc_entry.grid(row=1, column=2, padx=10, pady=10)

        tk.Label(root, text="Quantidade:").grid(row=2, column=1, sticky='e')
        self.quant_entry = tk.Entry(root)
        self.quant_entry.grid(row=2, column=2, padx=10, pady=10)

        tk.Button(root, text="Adicionar Sola", command=self.adicionar_sola).grid(row=3, column=2, pady=10)

        # Buscar sola
        tk.Label(root, text="Referência:").grid(row=4, column=1, sticky='e')
        self.ref_entry = tk.Entry(root)
        self.ref_entry.grid(row=4, column=2, padx=10, pady=10)

        tk.Button(root, text="Buscar Sola", command=self.buscar_sola).grid(row=5, column=2, pady=10)

        # Listar solas
        tk.Button(root, text="Listar Solas", command=self.listar_solas).grid(row=6, column=2, pady=10)

        # Atualizar quantidade
        tk.Label(root, text="Nova Quantidade:").grid(row=7, column=1, sticky='e')
        self.new_quant_entry = tk.Entry(root)
        self.new_quant_entry.grid(row=7, column=2, padx=10, pady=10)

        tk.Button(root, text="Atualizar Quantidade", command=self.atualizar_quantidade).grid(row=8, column=2, pady=10)

    def adicionar_sola(self):
        descricao = self.desc_entry.get()
        quantidade = int(self.quant_entry.get())
        referencia = self.estoque.adicionar_sola(descricao, quantidade)
        messagebox.showinfo("Sucesso", f"Sola cadastrada com sucesso. Referência: {referencia}")

    def buscar_sola(self):
        referencia = int(self.ref_entry.get())
        sola = self.estoque.buscar_sola(referencia)
        if sola:
            messagebox.showinfo("Resultado da Busca",
                                f"Referência: {sola[0]}, Descrição: {sola[1]}, Quantidade: {sola[2]}")
        else:
            messagebox.showwarning("Erro", "Sola não encontrada.")

    def listar_solas(self):
        solas = self.estoque.listar_solas()
        if not solas:
            messagebox.showinfo("Estoque Vazio", "Nenhuma sola cadastrada.")
        else:
            lista = "\n".join([f"Referência: {sola[0]}, Descrição: {sola[1]}, Quantidade: {sola[2]}" for sola in solas])
            messagebox.showinfo("Solas Cadastradas", lista)

    def atualizar_quantidade(self):
        referencia = int(self.ref_entry.get())
        nova_quantidade = int(self.new_quant_entry.get())
        if self.estoque.atualizar_quantidade(referencia, nova_quantidade):
            messagebox.showinfo("Sucesso", "Quantidade atualizada com sucesso.")
        else:
            messagebox.showwarning("Erro", "Sola não encontrada.")

    def on_close(self):
        self.estoque.close()
        root.destroy()


def show_main_app():
    login_window.destroy()  # Fecha a janela de login
    main_window = tk.Tk()  # Cria a janela principal
    app = MainApp(main_window)
    main_window.protocol("WM_DELETE_WINDOW", app.on_close)
    main_window.mainloop()


# Iniciar a tela de login
login_window = tk.Tk()
login_app = LoginScreen(login_window, show_main_app)
login_window.mainloop()
