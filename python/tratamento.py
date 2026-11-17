import pandas as pd 
 
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

df =  df.drop(columns = ["BLOCO/APTO"])
 
#calculo de consumo de media 
 
df["consumo_medio"] = (  
    df["consumo"] - df["MEDIA"] 
    ) 
 
#calculo de percentual de media 
 
df["percentual_media"] = (  
    df["consumo"] / df["MEDIA"] * 100 
    ).round(2) 
 
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

#salvar arquivo tratado 
 
df.to_excel( 
    "../Excel/consumo_medio_tratado.xlsx",
    index=False 
) 
 
#resultado final 
 
print("Tratamento Concluido!")