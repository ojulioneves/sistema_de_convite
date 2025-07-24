import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Conexão com MongoDB Atlas (Render usa variável de ambiente)
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["evento"]
collection = db["convidados"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form.get("nome")
        acompanhantes = request.form.get("acompanhantes")
        confirmacao = request.form.get("confirmacao")

        if nome and acompanhantes is not None and confirmacao == "sim":
            collection.insert_one({
                "nome": nome.strip(),
                "acompanhantes": int(acompanhantes),
                "confirmado_em": datetime.now()
            })
            return redirect("/?confirmado=true")

    confirmado = request.args.get("confirmado")
    return render_template("index.html", confirmado=confirmado)

if __name__ == "__main__":
    app.run(debug=True)
