# No arquivo: database.py
import mysql.connector
from mysql.connector import errorcode
from config import DB_PASSWORD

def conectar():
    """Função para conectar ao servidor MySQL"""
    try:
        # Substitua os dados abaixo pelos seus
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password=DB_PASSWORD, 
            database="mydb"
        )
        return conexao
    except mysql.connector.Error as err:
        print(f"Erro de conexão com o banco de dados: {err}")
        return None