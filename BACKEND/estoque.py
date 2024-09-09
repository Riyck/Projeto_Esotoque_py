import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

class Sola:
    def __init__(self, referencia, descricao, quantidade):
        self.referencia = referencia
        self.descricao = descricao
        self.quantidade = quantidade



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
        print(f"Sola cadastrada com sucesso. Referência: {referencia}")

    def buscar_sola(self, referencia):
        self.cur.execute("SELECT * FROM sola WHERE referencia = %s", (referencia,))
        sola = self.cur.fetchone()
        if sola:
            print(f"Referência: {sola[0]}, Descrição: {sola[1]}, Quantidade: {sola[2]}")
        else:
            print("Sola não encontrada.")

    def listar_solas(self):
        self.cur.execute("SELECT * FROM sola")
        solas = self.cur.fetchall()
        if not solas:
            print("Estoque vazio.")
        else:
            for sola in solas:
                print(f"Referência: {sola[0]}, Descrição: {sola[1]}, Quantidade: {sola[2]}")

    def atualizar_quantidade(self, referencia, quantidade):
        self.cur.execute(
            "UPDATE sola SET quantidade = %s WHERE referencia = %s",
            (quantidade, referencia)
        )
        self.conn.commit()
        if self.cur.rowcount > 0:
            print("Quantidade atualizada com sucesso.")
        else:
            print("Sola não encontrada.")

    def close(self):
        self.cur.close()
        self.conn.close()



estoque = Estoque()

while True:
    print("\nMenu de interação")
    opc = int(input("Selecione a opção desejada:\n"
                    "1- Adicionar sola\n"
                    "2- Listar Solas cadastradas\n"
                    "3- Buscar sola\n"
                    "4- Atualizar quantidade de sola\n"
                    "5- Sair\n"
                    "Opção: "))
    if opc == 1:
        Desc_Sola = str(input("Descrição da sola: "))
        Quant_Sola = int(input("Defina a quantidade de sola: "))
        estoque.adicionar_sola(Desc_Sola, Quant_Sola)

    elif opc == 2:
        estoque.listar_solas()

    elif opc == 3:
        Ref_sola = int(input("Digite a referência da sola: "))
        estoque.buscar_sola(Ref_sola)

    elif opc == 4:
        Ref_sola = int(input("Digite a referência da sola: "))
        Quant_Sola = int(input("Digite a nova quantidade: "))
        estoque.atualizar_quantidade(Ref_sola, Quant_Sola)

    elif opc == 5:
        print("Saindo...")
        estoque.close()
        break

    else:
        print("Opção inválida. Tente novamente.")
