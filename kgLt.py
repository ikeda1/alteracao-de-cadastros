"""
Script feito para modificar alguns campos de um banco de dados específico de uma forma mais prática
"""

from numpy import empty
import pandas as pd
import re

# Endereço do arquivo excel
src = "./120_mercearia_doce.xlsx"
# src = "./dpt_140_bebidas.xlsx"

# Nome do arquivo final a ser criado
fileName = "120-mercearia_doce.xlsx"

# Inicializando o data frame
df = pd.read_excel(src)
df["Função"] = df["Função"].fillna(0)
print(df.info())
# Identifica o padrão de medida no final da descrição
def getPattern(list):
   # pattern = r"(\d+ml|\d+,\d+ml|\d+l|\d+,\d+l|\d+L|\d+,\d+L|\d+g|\d+,\d+g|\d+G|\d+,\d+G|\d+kg|\d+,\d+kg|\d+Kg|\d+,\d+Kg|\d+KG|\d+,\d+KG)"
   pattern = r'(\d+ml|\d+,\d+ml|\d+l|\d+,\d+l|\d+g|\d+,\d+g|\d+kg|\d+,\d+kg)'
   return re.findall(pattern, list, re.IGNORECASE)

def otherPattern(list):
   pattern = r"c[\]\/]\d+"
   # return bool(re.match(pattern, list))
   return re.findall(pattern, list, re.IGNORECASE)

# Transforma a coluna "Descrição" em uma lista python
listDescription = df["Descrição"].tolist()


# Lista que armazena os volumes
volumeList = []

# len(df) = Número de colunas do data frame
for i in range (len(df)):
   volumeList.append(getPattern(listDescription[i]))

warningsList = []
for j in range (len(df)):
   index = otherPattern(listDescription[j])
   if (index != []):
      warningsList.append(j)
      # print(listDescription[j])
      # print(index)

# print(warningsList)
# Manipula string para conter apenas os números
for j in range (len(volumeList)):
   string = ""
   string += str(volumeList[j])
   num = ""
   if (string[-4:-2] == "ml" or string[-4:-2] == "ML" or string[-4:-2] == "Ml"):
      # Se for Mililitro
      # print("Mililitro "+string[2:-4])
      # Modificando a coluna "Função"
      if (df.at[j, 'Função']) == 0:
         df.at[j, 'Função'] = "LT"
      elif (df.at[j, 'Função']) == "EX":
         df.at[j, 'Função'] = "EX;LT"

      # Se for número com vírgula, faz um map e splits para mudar para um .
      if ("," in string):
         tmp = re.findall(r'\d+', string)
         res = list(map(int, tmp))
         res = float(f"{res[0]}.{res[1]}")
         df.at[j, 'Peso Liq'] = res
      else:
         df.at[j, 'Peso Liq'] = float(string[2:-4])/1000

   elif (string[-3:-2] == "l" or string[-3:-2] == "L"):
      # Se for Litro
      # print("Litro "+string[2:-3])
      if (df.at[j, 'Função']) == 0:
         df.at[j, 'Função'] = "LT"
      elif (df.at[j, 'Função']) == "EX":
         df.at[j, 'Função'] = "EX;LT"
      if ("," in string):
         tmp = re.findall(r'\d+', string)
         res = list(map(int, tmp))
         res = float(f"{res[0]}.{res[1]}")
         df.at[j, 'Peso Liq'] = res
      else:
         df.at[j, 'Peso Liq'] = string[2:-3]

   elif (string[-4:-2] == "kg" or string[-4:-2] == "Kg" or string[-4:-2] == "KG"):
         # Se for Quilograma
         # print("Quilos "+string[2:-4])
         if (df.at[j, 'Função']) == 0:
            df.at[j, 'Função'] = "KG"
         elif (df.at[j, 'Função']) == "EX":
            df.at[j, 'Função'] = "EX;KG"
         if ("," in string):
            tmp = re.findall(r'\d+', string)
            print(tmp, j)
            res = list(map(int, tmp))
            # print(res, j)
            # res = float(f"{res[0]}.{res[1]}")
            res = float(res[0] + (res[1]/1000))
            print(res, j)
            df.at[j, 'Peso Liq'] = res
         else:
            df.at[j, 'Peso Liq'] = float(string[2:-4])

   elif (string[-3:-2] == "g" or string[-3:-2] == "G"):
      # Se for Gramas
      # print("Gramas "+string[2:-3])
      if (df.at[j, 'Função']) == 0:
         df.at[j, 'Função'] = "KG"
      elif (df.at[j, 'Função']) == "EX":
         df.at[j, 'Função'] = "EX;KG"
      if ("," in string):
         tmp = re.findall(r'\d+', string)
         res = list(map(int, tmp))
         res = float(f"{res[0]}.{res[1]}")
         df.at[j, 'Peso Liq'] = res
      else:
         df.at[j, 'Peso Liq'] = float(string[2:-3])/1000
      
# with pd.option_context('display.max_rows', None):  # more options can be specified also
#     print(df)

df.to_excel(fileName)   
