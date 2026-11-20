import pandas as pd 
import random as rd
 
#arquivo excel a ser tratado 
 
arquivo = "../Excel/consumo_medio.xlsx"
 
#ler arquivo excel 
df = pd.read_excel(arquivo) 
 
print("Planilha Carregada com sucesso!") 
 
print("\nColunas Originais: ") 
print(df.columns.tolist()) 
 
print("\nQuantidade de Registros: ") 
print(len(df)) 
 
#correção de nomes das colunas 
 
df.columns = [ 
    "BLOCO/APTO", 
    "Leitura Inicial", 
    "Leitura Final", 
    "consumo", 
    "MEDIA", 
] 
 
print("\nColunas Corrigidas: ") 
print(df.columns.tolist()) 
 
#mostrar primeiros dados da planilha 
 
print("\nPrimeiros Registros: ") 
print(df.head()) 

#Separa os Apartamentos dos Blocos

df[["BLOCO","APARTAMENTO"]] = df["BLOCO/APTO"].str.split("/", expand = True)

df = df.drop(columns = ["BLOCO/APTO"])
 
#calculo de consumo de media 
 
df["consumo_medio"] = (  
    df["consumo"] - df["MEDIA"] 
    ) 
 
#classificação de consumo 
 
def classificar(row): 
 
    if row["consumo"] == 0: 
        return "Sem consumo" 
     
    elif row["consumo"] > row["MEDIA"] * 1.5: 
        return "Muito acima da média" 
 
    elif row["consumo"] > row["MEDIA"]: 
        return "Acima da média" 
 
    elif row["consumo"] < row["MEDIA"] * 0.5: 
        return "Abaixo da média" 
 
    else: 
        return "Dentro da média" 
 
df["classificacao"] = df.apply( 
     classificar, 
     axis=1 
) 

#dado simulado de conta de água no fim do mês 
dias = 31

def calcular_conta(consumo):
    faixas = [
        (15, 7.41),
        (30, 18.69),
        (45, 25.48),
        (60, 50.97),
        (float("inf"), 67.96)
    ]

    valor_agua = 0
    consumo_anterior = 0

    for limite, tarifa in faixas:
        quantidade = max(0, min(consumo, limite) - consumo_anterior)

        if quantidade > 0:
            valor_agua += quantidade * tarifa

        consumo_anterior = limite

        if consumo <= limite:
            break

    valor_esgoto = 34.41
    valor_total = valor_agua + valor_esgoto

    return round(valor_agua, 2), round(valor_esgoto, 2), round(valor_total, 2)

consumos = []
valores_agua = []
valores_esgoto = []
valores = []

for _, apartamento in df.iterrows():

    consumo_diario = []

    media_diaria = apartamento["consumo"] / dias

    for dia in range(1, dias + 1):

        consumo = rd.uniform(
            media_diaria * 0.7,
            media_diaria * 1.3
        )

        consumo_diario.append(round(consumo, 2))

    consumo_total = round(sum(consumo_diario), 2)

    valor_agua, valor_esgoto, valor_conta = calcular_conta(consumo_total)

    consumos.append(consumo_total)
    valores_agua.append(valor_agua)
    valores_esgoto.append(valor_esgoto)
    valores.append(valor_conta)

df["consumo_simulado"] = consumos
df["valor_agua"] = valores_agua
df["valor_esgoto"] = valores_esgoto
df["valor_conta"] = valores

#salvar arquivo tratado 
 
df.to_excel( 
    "../Excel/consumo_medio_tratado.xlsx",
    index=False 
) 
 
#resultado final 

print("Tratamento Concluido!")