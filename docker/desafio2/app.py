import sqlite3
import os
import random

DB_PATH = "/data/data.db"

nomes = ["Ana", "Pedro", "Lucas", "Marina", "João"]
cursos = ["CC", "SI", "Design", "ADS", "Engenharia"]

os.makedirs("/data", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    curso TEXT
)
""")

nome = random.choice(nomes)
curso = random.choice(cursos)

cursor.execute("INSERT INTO alunos (nome, curso) VALUES (?, ?)", (nome, curso))
conn.commit()

cursor.execute("SELECT * FROM alunos")
infos = cursor.fetchall()
print("Alunos:", infos)

conn.close()
