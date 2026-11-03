import random

# tabela de vantagem entre classes
VANTAGEM = {
    "guerreiro": "mago",
    "mago": "paladino",
    "paladino": "guerreiro",
}

NIVEL_MAX = 99


def xp_para_nivel(nivel):
    return nivel * nivel * 100


def subir_nivel(heroi):
    heroi["nivel"] = heroi["nivel"] + 1
    heroi["forca"] = heroi["forca"] * 1.1
    heroi["magia"] = heroi["magia"] * 1.1
    heroi["defesa"] = heroi["defesa"] * 1.1
    heroi["vida"] = heroi["vida"] * 1.1
    return heroi


def multiplicador(classe_ataque, classe_defesa):
    if VANTAGEM[classe_ataque] == classe_defesa:
        return 1.5
    if VANTAGEM[classe_defesa] == classe_ataque:
        return 0.5
    return 1


def critico():
    return random.random() < 0.5


def dano(atacante, defensor):
    base = max(atacante["forca"], atacante["magia"])
    m = multiplicador(atacante["classe"], defensor["classe"])
    d = base * m - defensor["defesa"]
    if critico():
        d = d * 3
    return d


def gerar_titulo(texto):
    t = texto.lower()
    if "dragao" in t:
        return "Matador de Dragões"
    if "rei" in t:
        return "Herdeiro do Trono"
    if "floresta" in t:
        return "Guardião da Floresta"
    if "mar" in t:
        return "Senhor dos Mares"
    if "fogo" in t:
        return "Chama Eterna"
    return "Aventureiro"


def censurar(texto):
    proibidas = ["palavrao1", "palavrao2"]
    for p in proibidas:
        texto = texto.replace(p, "***")
    return texto


def item_aleatorio():
    itens = ["Poção", "Espada de madeira", "Escudo velho", "Anel mágico", "Lendária Excalibur"]
    return random.choice(itens)


def calcular_ouro(vitorias):
    ouro = 0
    for v in range(vitorias):
        ouro = ouro + 10
    return ouro


def calcular_ouro2(vitorias):
    return vitorias * 10
