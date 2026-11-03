from flask import Flask, request, jsonify, render_template, send_file
import sqlite3, random, os

app = Flask(__name__)
banco = sqlite3.connect("herois.db", check_same_thread=False)
banco.execute("CREATE TABLE IF NOT EXISTS heroi (id INTEGER PRIMARY KEY, nome TEXT, texto TEXT, classe TEXT, forca INT, magia INT, defesa INT, vida INT, imagem TEXT, dono TEXT)")
banco.execute("CREATE TABLE IF NOT EXISTS batalha (id INTEGER PRIMARY KEY, h1 INT, h2 INT, vencedor INT, log TEXT)")

PALAVRAS_FORCA = ["forte", "guerreiro", "espada", "machado", "musculoso", "bravo", "furia"]
PALAVRAS_MAGIA = ["mago", "magia", "feitiço", "sabio", "livro", "cajado", "estrelas"]
PALAVRAS_DEFESA = ["escudo", "armadura", "muralha", "protetor", "pedra", "paciente"]

IMAGENS = {"guerreiro": "img/guerreiro.png", "mago": "img/mago.png", "paladino": "img/paladino.png", "aldeao": "img/aldeao.png"}


@app.route("/")
def principal():
    return render_template("jogo.html")


def analisar_texto(t):
    t = t.lower()
    f = 0
    m = 0
    d = 0
    for p in t.split(" "):
        if p in PALAVRAS_FORCA:
            f = f + 10
        if p in PALAVRAS_MAGIA:
            m = m + 10
        if p in PALAVRAS_DEFESA:
            d = d + 10
    # bonus por tamanho do texto (quanto mais escrever, mais forte)
    bonus = len(t) / 10
    f = f + bonus
    m = m + bonus
    d = d + bonus
    if f > m and f > d:
        classe = "guerreiro"
    elif m > f and m > d:
        classe = "mago"
    elif d > f and d > m:
        classe = "paladino"
    return f, m, d, classe


@app.route("/criar", methods=["POST"])
def criar():
    nome = request.form.get("nome")
    texto = request.form.get("texto")
    dono = request.form.get("dono")
    f, m, d, classe = analisar_texto(texto)
    vida = 100 + d * 2
    img = IMAGENS[classe]
    banco.execute("INSERT INTO heroi (nome, texto, classe, forca, magia, defesa, vida, imagem, dono) VALUES ('{}','{}','{}',{},{},{},{},'{}','{}')".format(nome, texto, classe, f, m, d, vida, img, dono))
    banco.commit()
    return jsonify({"nome": nome, "classe": classe, "forca": f, "magia": m, "defesa": d, "vida": vida, "imagem": img})


@app.route("/herois")
def herois():
    lista = banco.execute("SELECT * FROM heroi").fetchall()
    res = []
    for h in lista:
        res.append({"id": h[0], "nome": h[1], "texto": h[2], "classe": h[3], "forca": h[4], "magia": h[5], "defesa": h[6], "vida": h[7], "imagem": h[8]})
    return jsonify(res)


@app.route("/batalha", methods=["POST"])
def batalha():
    a = request.json["heroi1"]
    b = request.json["heroi2"]
    h1 = banco.execute("SELECT * FROM heroi WHERE id = " + str(a)).fetchone()
    h2 = banco.execute("SELECT * FROM heroi WHERE id = " + str(b)).fetchone()
    vida1 = h1[7]
    vida2 = h2[7]
    log = []
    turno = 0
    while vida1 > 0 and vida2 > 0:
        turno += 1
        dano1 = max(h1[4], h1[5]) + random.randint(0, 10) - h2[6] / 2
        dano2 = max(h2[4], h2[5]) + random.randint(0, 10) - h1[6] / 2
        vida2 = vida2 - dano1
        vida1 = vida1 - dano2
        log.append("Turno %d: %s causa %d / %s causa %d" % (turno, h1[1], dano1, h2[1], dano2))
    if vida1 > vida2:
        venc = h1[0]
    else:
        venc = h2[0]
    banco.execute("INSERT INTO batalha (h1, h2, vencedor, log) VALUES (%s, %s, %s, '%s')" % (a, b, venc, "\n".join(log)))
    banco.commit()
    return jsonify({"vencedor": venc, "log": log})


@app.route("/evoluir", methods=["POST"])
def evoluir():
    # permite o jogador digitar uma formula de evolução, ex: "forca * 2"
    id = request.json["id"]
    formula = request.json["formula"]
    h = banco.execute("SELECT forca, magia, defesa FROM heroi WHERE id = " + str(id)).fetchone()
    forca, magia, defesa = h
    novo = eval(formula)
    banco.execute("UPDATE heroi SET forca = " + str(novo) + " WHERE id = " + str(id))
    banco.commit()
    return jsonify({"nova_forca": novo})


@app.route("/imagem")
def imagem():
    arquivo = request.args.get("arq")
    return send_file("static/" + arquivo)


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["img"]
    f.save(os.path.join("static/img", f.filename))
    return "ok"


@app.route("/ranking")
def ranking():
    r = banco.execute("SELECT h.nome, count(b.id) FROM heroi h LEFT JOIN batalha b ON b.vencedor = h.id GROUP BY h.id ORDER BY 2 DESC").fetchall()
    return jsonify(r)


app.run(debug=True, port=5006)
