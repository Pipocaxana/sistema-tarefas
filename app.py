from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Inicializa banco de dados
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT DEFAULT 'pendente',
            data_limite TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Página principal
@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if request.method == "POST":
        titulo = request.form.get("titulo")
        descricao = request.form.get("descricao")
        data_limite = request.form.get("data_limite")

        if titulo:
            c.execute(
                "INSERT INTO tarefas (titulo, descricao, data_limite) VALUES (?, ?, ?)",
                (titulo, descricao, data_limite)
            )
            conn.commit()

        return redirect("/")

    c.execute("SELECT * FROM tarefas")
    tarefas = c.fetchall()
    conn.close()

    # Contadores
    pendentes = [t for t in tarefas if t[3] == 'pendente']
    concluidas = [t for t in tarefas if t[3] == 'concluida']

    return render_template(
        "index.html",
        tarefas=tarefas,
        pendentes=len(pendentes),
        concluidas=len(concluidas)
    )

# Deletar tarefa
@app.route("/delete/<int:tarefa_id>", methods=["POST"])
def delete(tarefa_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM tarefas WHERE id=?", (tarefa_id,))
    conn.commit()
    conn.close()
    return redirect("/")

# Marcar como concluída
@app.route("/concluir/<int:tarefa_id>", methods=["POST"])
def concluir(tarefa_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE tarefas SET status='concluida' WHERE id=?", (tarefa_id,))
    conn.commit()
    conn.close()
    return redirect("/")

# Desfazer (voltar para pendente)
@app.route("/desfazer/<int:tarefa_id>", methods=["POST"])
def desfazer(tarefa_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE tarefas SET status='pendente' WHERE id=?", (tarefa_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
