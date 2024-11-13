import sqlite3
from datetime import datetime

class Agenda:
    def __init__(self):
        self.conn = sqlite3.connect('agenda.db')
        self.criar_tabelas()

    def criar_tabelas(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contatos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compromissos (
                id INTEGER PRIMARY KEY,
                descricao TEXT NOT NULL,
                data TEXT NOT NULL,
                contato_id INTEGER,
                FOREIGN KEY (contato_id) REFERENCES contatos (id)
            )
        ''')
        self.conn.commit()

    def adicionar_contato(self, nome, telefone, email=None):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO contatos (nome, telefone, email) VALUES (?, ?, ?)', (nome, telefone, email))
        self.conn.commit()
        return cursor.lastrowid

    def adicionar_compromisso(self, descricao, data, contato_id=None):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO compromissos (descricao, data, contato_id) VALUES (?, ?, ?)', (descricao, data, contato_id))
        self.conn.commit()
        return cursor.lastrowid

    def listar_contatos(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, nome, telefone, email FROM contatos')
        return cursor.fetchall()

    def listar_compromissos(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT c.descricao, c.data, co.nome
            FROM compromissos c
            LEFT JOIN contatos co ON c.contato_id = co.id
        ''')
        return cursor.fetchall()

    def pesquisar_compromissos(self, data_inicio, data_fim):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT descricao, data, contato_id 
            FROM compromissos 
            WHERE data BETWEEN ? AND ?
        ''', (data_inicio, data_fim))
        return cursor.fetchall()

def main():
    agenda = Agenda()

    while True:
        print("\n1. Adicionar Contato")
        print("2. Adicionar Compromisso")
        print("3. Listar Contatos")
        print("4. Listar Compromissos")
        print("5. Pesquisar Compromissos por intervalo de datas")
        print("6. Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            email = input("Email (opcional): ")
            agenda.adicionar_contato(nome, telefone, email)
            print("Contato adicionado com sucesso!")
        
        elif choice == "2":
            descricao = input("Descrição do Compromisso: ")
            data = input("Data (AAAA-MM-DD): ")
            contato_id = input("ID do Contato (opcional): ")
            contato_id = int(contato_id) if contato_id else None
            agenda.adicionar_compromisso(descricao, data, contato_id)
            print("Compromisso adicionado com sucesso!")
        
        elif choice == "3":
            contatos = agenda.listar_contatos()
            for contato in contatos:
                print(contato)

        elif choice == "4":
            compromissos = agenda.listar_compromissos()
            for compromisso in compromissos:
                print(compromisso)

        elif choice == "5":
            data_inicio = input("Data de início (AAAA-MM-DD): ")
            data_fim = input("Data de fim (AAAA-MM-DD): ")
            compromissos = agenda.pesquisar_compromissos(data_inicio, data_fim)
            for compromisso in compromissos:
                print(compromisso)

        elif choice == "6":
            print("Finalizando o programa...")
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()

