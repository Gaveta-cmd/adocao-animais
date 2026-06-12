"""Interface web (Flask) para o sistema de adocao de animais.

Expoe as mesmas operacoes do CLI via HTTP e renderiza paginas HTML simples.
Usada para o deploy publico (Render/Railway).
"""
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from dotenv import load_dotenv
from src.models import SessionLocal, Animal
from src.api_client import buscar_raca, DogApiError

load_dotenv()
app = Flask(__name__)

def get_db():
    return SessionLocal()

@app.route("/", methods=["GET"])
def index():
    db = get_db()
    try:
        animais = db.query(Animal).all()
        return render_template("index.html", animais=animais)
    finally:
        db.close()

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        db = get_db()
        try:
            nome = request.form.get("nome")
            especie = request.form.get("especie")
            idade = int(request.form.get("idade", 0)) if request.form.get("idade") else None
            raca = request.form.get("raca")
            observacoes = request.form.get("observacoes")
            dados_api = {}
            if especie.lower() == "cachorro" and raca:
                try:
                    dados_api = buscar_raca(raca) or {}
                except DogApiError:
                    dados_api = {}
            novo_animal = Animal(
                nome=nome,
                especie=especie,
                idade=idade,
                raca=raca,
                observacoes=observacoes,
                temperamento=dados_api.get("temperamento"),
                life_span=dados_api.get("expectativa_vida"),
                peso=dados_api.get("peso"),
                origem=dados_api.get("origem"),
                status="Disponível"
            )
            db.add(novo_animal)
            db.commit()
            return redirect(url_for("index"))
        except Exception as e:
            db.rollback()
            return render_template("cadastrar.html", erro=str(e))
        finally:
            db.close()
    return render_template("cadastrar.html")

@app.route("/adotar/<int:animal_id>", methods=["POST"])
def adotar(animal_id):
    db = get_db()
    try:
        animal = db.query(Animal).filter(Animal.id == animal_id).first()
        if animal:
            animal.status = "Adotado"
            db.commit()
        return redirect(url_for("index"))
    finally:
        db.close()

@app.route("/raca", methods=["GET"])
def consultar_raca():
    nome_raca = request.args.get("nome")
    if nome_raca:
        dados = buscar_raca(nome_raca)
        return jsonify(dados)
    return jsonify({"erro": "Nome da raça não fornecido"}), 400

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)