import json
import os

CAMINHO_USO_COMANDOS = "dados/uso_comandos.json"


pasta = os.path.dirname(CAMINHO_USO_COMANDOS)  # criar pasta dados
if pasta and not os.path.exists(pasta):
    os.makedirs(pasta)


if os.path.exists(CAMINHO_USO_COMANDOS):
    with open(CAMINHO_USO_COMANDOS, "r") as f:  # carregar arquivos
        uso_comandos = json.load(f)
else:
    uso_comandos = {}


def salvar_em_arquivo(caminho, dados):

    pasta = os.path.dirname(caminho)
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta)

    with open(caminho, "w") as f:
        json.dump(dados, f, indent=4)
