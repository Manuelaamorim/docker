from flask import Flask, jsonify
import psycopg2
import redis
import os
import time

app = Flask(__name__)

# Pausa para esperar Postgres subir
time.sleep(5)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

CACHE_HOST = os.getenv("CACHE_HOST")

# Redis
cache = redis.Redis(host=CACHE_HOST, port=6379, decode_responses=True)

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME
    )

@app.route("/")
def home():
    return "API de Alunos funcionando! Endpoints: /aluno/<id> e /todos"

@app.route("/aluno/<id>")
def aluno(id):
    # 1️⃣ Primeiro tenta no cache
    aluno_cache = cache.get(f"aluno:{id}")
    if aluno_cache:
        return jsonify({"aluno (cache)": aluno_cache})

    # 2️⃣ Se não encontrar → buscar no Postgres
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome, curso FROM alunos WHERE id = %s", (id,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if not result:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    nome, curso = result

    # 3️⃣ Salvar no cache
    cache.set(f"aluno:{id}", f"{nome} - {curso}")

    return jsonify({"aluno (db)": f"{nome} - {curso}"})


@app.route("/todos")
def todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, curso FROM alunos")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({"alunos": rows})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
