import pandas as pd
from json import load

with open("config.json", "r") as f:
    config = load(f)
    etapa = config["etapa"]
    is_complete = config["gabarito_completo"]

with open("gabarito.txt", "r") as f:
    gabarito = f.read().split("\n")

questoes_index = []
questoes = []
respostas = []
nota = 0.0

for line in range(len(gabarito)):
    if line % 2 == 0:
        for c in gabarito[line].split(" "):
            questoes_index.append(c)
    else:
        for c in gabarito[line].split(" "):
                questoes.append(c)

#! tirando os espaços vazios
_ = lambda x: x != ""
questoes = list(filter(_, questoes))
questoes_index = list(filter(_, questoes_index))

#! Verificando se o gabarito está errado
#...

data = pd.DataFrame(index = questoes_index, data = questoes, columns = ["Gabarito"])

questoes.clear()

#! alocando os tipos
for c in data["Gabarito"]:
    if c in ["C", "E"]:
        questoes.append("A")
    elif c.isnumeric():
        questoes.append("B")
    elif c in ["A", "B", "C", "D"]:
        questoes.append("C")
    elif c == "X":
        questoes.append("X")
    else:
        questoes.append("D")

data["Tipo"] = questoes

for c in range(100):
    respostas.append(input(f"Questão {c+1}: ").upper()[0])

#! corrigindo
data["Resposta"] = respostas
data["Acertou"] = data["Gabarito"] == respostas

notas = {"A" : [1, -1], "B" : [2, 0], "C" : [2, -0.667], "D" : [1.5, 0], "X" : [0, 0]}

data = data[["Gabarito", "Resposta", "Tipo", "Acertou"]] # pra ficar mais organizado

#! aplicando nota aproximada
for i in range(data.shape[0]):
    if data.iloc[i].Acertou:
        nota += notas.get(data.iloc[i].Tipo)[0]
    elif not data.iloc[i].Acertou:
        nota += notas.get(data.iloc[i].Tipo)[1]

print(data)
print(abs(nota))