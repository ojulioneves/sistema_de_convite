import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime
from flask import Response

app = Flask(__name__)

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
    return render_template("admin.html", convidados=convidados)

if __name__ == "__main__":
    app.run(debug=True)

