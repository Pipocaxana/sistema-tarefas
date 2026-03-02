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
            descricao TEXT
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
        if titulo:
            c.execute("INSERT INTO tarefas (titulo, descricao) VALUES (?, ?)", (titulo, descricao))
            conn.commit()
        return redirect("/")
    
   

    c.execute("SELECT * FROM tarefas")
    tarefas = c.fetchall()
    conn.close()
    return render_template("index.html", tarefas=tarefas)

@app.route("/delete/<int:tarefa_id>", methods=["POST"])
def delete(tarefa_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM tarefas WHERE id=?", (tarefa_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)