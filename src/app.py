"""Interface web (Flask) para o sistema de adocao de animais.

Expoe as mesmas operacoes do CLI via HTTP e renderiza paginas HTML simples.
Usada para o deploy publico (Render/Railway).
"""
from flask import Flask, render_template, request, redirect, url_for, flash

from src.main import (
    cadastrar_animal,
    listar_animais,
    marcar_adotado,
    carregar_dados,
)
from src.api_client import buscar_raca, DogApiError


def create_app():
    app = Flask(__name__)
    app.secret_key = "adocao-animais-secret"

    @app.route("/")
    def index():
        animais = carregar_dados()
        return render_template("index.html", animais=animais)

    @app.route("/cadastrar", methods=["GET", "POST"])
    def cadastrar():
        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            especie = request.form.get("especie", "").strip()
            try:
                idade = int(request.form.get("idade", "0"))
            except ValueError:
                flash("Idade inválida.", "error")
                return redirect(url_for("cadastrar"))
            obs = request.form.get("observacao", "").strip()
            raca = request.form.get("raca", "").strip() or None
            if not nome or not especie:
                flash("Nome e espécie são obrigatórios.", "error")
                return redirect(url_for("cadastrar"))
            cadastrar_animal(nome, especie, idade, obs, raca)
            flash(f"Animal '{nome}' cadastrado!", "success")
            return redirect(url_for("index"))
        return render_template("cadastrar.html")

    @app.route("/adotar/<int:id_animal>", methods=["POST"])
    def adotar(id_animal):
        if marcar_adotado(id_animal):
            flash("Adoção registrada!", "success")
        else:
            flash("Animal não encontrado.", "error")
        return redirect(url_for("index"))

    @app.route("/raca", methods=["GET"])
    def consultar_raca():
        nome = request.args.get("nome", "").strip()
        info = None
        erro = None
        if nome:
            try:
                info = buscar_raca(nome)
                if not info:
                    erro = f"Raça '{nome}' não encontrada."
            except DogApiError as exc:
                erro = str(exc)
        return render_template("raca.html", nome=nome, info=info, erro=erro)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
