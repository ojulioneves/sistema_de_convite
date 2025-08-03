import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime
from flask import Response

app = Flask(__name__)

# Conexão com o MongoDB
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["evento"]
collection = db["convidados"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form.get("nome")
        confirmacao = request.form.get("confirmacao")

        # Verifica se o nome foi enviado e se a caixa de confirmação está marcada
        if nome and confirmacao == "sim":
            collection.insert_one({
                "nome": nome.strip(),
                "confirmado_em": datetime.now()
            })
            return redirect("/confirmado")

    return render_template("index.html")

@app.route("/confirmado")
def confirmado():
    return render_template("confirmado.html")

@app.route("/admin")
def admin():
    senha = request.args.get("senha")
    if senha != os.environ.get("ADMIN_PASS", "admin123"):
        return Response("Acesso negado", status=401)

    convidados = list(collection.find({}, {"_id": 0}))
    total_confirmados = len(convidados)

    return render_template("admin.html", convidados=convidados, total=total_confirmados)

if __name__ == "__main__":
    app.run(debug=True)

