from numpy import empty
import pandas as pd
import re

# Endereço do arquivo excel
src = "./beforeEdit/130_mercearia_salgada.xlsx"
# src = "./dpt_140_bebidas.xlsx"

# Nome do arquivo final a ser criado
fileName = "./afterEdit/dpt_130-mercearia_salgada.xlsx"

# Inicializando o data frame
df = pd.read_excel(src)
df["Função"] = df["Função"].fillna(0)

# Identifica o padrão de medida no final da descrição
def getPattern(list):
   # pattern = r"(\d+ml|\d+,\d+ml|\d+l|\d+,\d+l|\d+L|\d+,\d+L|\d+g|\d+,\d+g|\d+G|\d+,\d+G|\d+kg|\d+,\d+kg|\d+Kg|\d+,\d+Kg|\d+KG|\d+,\d+KG)"
   pattern = r'(\d+ml|\d+,\d+ml|\d+l|\d+,\d+l|\d+g|\d+,\d+g|\d+kg|\d+,\d+kg)'
   return re.findall(pattern, list, re.IGNORECASE)

def otherPattern(list):
   pattern = r"c[\]\/]\d+"
   # return bool(re.match(pattern, list))
   return re.findall(pattern, list, re.IGNORECASE)

def decimalNumbers(newFunc, strIndex):
   if (df.at[j, 'Função']) == 0:
         df.at[j, 'Função'] = newFunc.upper()
   elif (df.at[j, 'Função']) == "EX":
      df.at[j, 'Função'] = f"EX;{newFunc}"

   # Se for número com vírgula, faz um map e splits para mudar para um .
   if ("," in string):
      tmp = re.findall(r'\d+', string)
      # print(tmp, j, (len(tmp[1])))

      # Verifica quantos dígitos tem após a vírgula
      a = len(tmp[1])
      res = list(map(int, tmp))
      # print(res, j)
      # 
      if a == 1:
         res[1] *= 100
      elif a == 2:
         res[1] *= 10
      res = float(res[0] + (res[1]/1000))
      # print(res, j)
      df.at[j, 'Peso Liq'] = res
   else:
      df.at[j, 'Peso Liq'] = float(strIndex)

def decimalForMinor(newFunc, strIndex):
   if (df.at[j, 'Função']) == 0:
         df.at[j, 'Função'] = newFunc.upper()
   elif (df.at[j, 'Função']) == "EX":
      df.at[j, 'Função'] = f"EX;{newFunc}"
   if ("," in string):
      tmp = re.findall(r'\d+', string)
      res = list(map(int, tmp))
      res = float(f"{res[0]}{res[1]}")/10000
      df.at[j, 'Peso Liq'] = res
   else:
      df.at[j, 'Peso Liq'] = float(strIndex)/1000
# Transforma a coluna "Descrição" em uma lista python
listDescription = df["Descrição"].tolist()


# Lista que armazena os volumes
volumeList = []

# len(df) = Número de colunas do data frame
for i in range (len(df)):
   volumeList.append(getPattern(listDescription[i]))

# Lista contendo index de alguns casos específicos que requerem mais atenção
warningsList = []
for j in range (len(df)):
   index = otherPattern(listDescription[j])
   if (index != []):
      warningsList.append(j)
      # print(listDescription[j])
      # print(index)

# Manipula string para conter apenas os números
for j in range (len(volumeList)):
   string = ""
   string += str(volumeList[j])
   num = ""
   if (string[-4:-2] == "ml" or string[-4:-2] == "ML" or string[-4:-2] == "Ml"):
      # Se for Mililitro
      # print("Mililitro "+string[2:-4])
      decimalForMinor("LT", string[2:-4])

   elif (string[-3:-2] == "l" or string[-3:-2] == "L"):
      # Se for Litro
      # print("Litro "+string[2:-3])
      decimalNumbers("LT", string[2:-3])

   elif (string[-4:-2] == "kg" or string[-4:-2] == "Kg" or string[-4:-2] == "KG"):
      # Se for Quilograma
      # print("Quilos "+string[2:-4])
      decimalNumbers("KG", string[2:-4])

   elif (string[-3:-2] == "g" or string[-3:-2] == "G"):
      # Se for Gramas
      # print("Gramas "+string[2:-3])
      decimalForMinor("KG", string[2:-3])
      
with pd.option_context('display.max_rows', None):  # more options can be specified also
    print(df)

df.to_excel(fileName)

print("Alteração concluída")
print(warningsList)
