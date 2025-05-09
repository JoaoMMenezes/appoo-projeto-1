import json

# 1. Carrega dados da base (JSON)
with open('dados.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

print("Dados originais carregados:")
print(dados)

# 2. Operação: calcular média de nota da turma
media = sum(item['nota'] for item in dados) / len(dados)
print(f"Média da turma: {media:.2f}")

# 3. Anexa a média em cada registro
for item in dados:
    item['media_turma'] = round(media, 2)

# 4. Grava dados atualizados em novo arquivo JSON
with open('dados_atualizados.json', 'w', encoding='utf-8') as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print("Dados atualizados salvos em 'dados_atualizados.json'.")
