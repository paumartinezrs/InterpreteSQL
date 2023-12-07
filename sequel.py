from antlr4 import *
from sequelLexer import sequelLexer
from sequelParser import sequelParser
from sequelVisitor import sequelVisitor

import streamlit as st
import pandas as pd

def operacion(operation, num):
    if (operation == '+'): return lambda x : x + num 
    elif (operation == '-'): return lambda x : x - num
    elif (operation == '**'): return lambda x : x * num
    elif (operation == '/'): return lambda x : x / num
    elif (operation == '^'): return lambda x : pow(x, num)

class nuevoVisitor(sequelVisitor):
    def visitSelect_statement(self, ctx):
        self.hijos = list(ctx.getChildren())
        self.data_frame = self.visit(self.hijos[3]) #data frame con los valores de la tabla entera, hijo 3 del select
        
        if self.hijos[1].getText() != '*': 
            self.visit(self.hijos[1]) 
        if len(self.hijos) > 4: #tenim un order by 
            order = self.visit(self.hijos[5]) #alguna manera millor de cridar al visit del ordre??
            self.data_frame = self.data_frame.sort_values(by = order[0], ascending = order[1])

        st.write(self.data_frame)           
        
    def visitColumn_selection(self, ctx):
        [lista] = list(ctx.getChildren()) #pq [lista] i no lista??
        return self.visit(lista)
        
    def visitColumn_list(self, ctx):
        columnas = list(ctx.getChildren())
        self.visualizar_columnas = [] #columnas que se quedan en el data_frame
        for i in columnas:
            self.visit(i)
        self.data_frame = self.data_frame.filter(items = self.visualizar_columnas)

    def visitColumna_existente(self, ctx): 
        [nombre_columna] = list(ctx.getChildren())
        nombre_columna = nombre_columna.getText()
        self.visualizar_columnas.append(nombre_columna)

    def visitColumna_nueva(self, ctx):
        [columna1, operation, numero, _, columna2] = list(ctx.getChildren())
        columna1 = columna1.getText()
        operation = operation.getText()
        numero = float(numero.getText())
        columna2 = columna2.getText()
        self.data_frame[columna2] = list(map(operacion(operation, numero), list(self.data_frame[columna1])))
        self.visualizar_columnas.append(columna2)

    def visitColumns_order(self, ctx): #devuelve una lista segun el orden que se ordenaran las filas del dataset
        l = list(ctx.getChildren()) #tienen que ser columnas existentes
        res = ([],[])
        for i in range(len(l)): 
            if (l[i].getText() != ','):
                order = self.visit(l[i])
                res[0].append(order[0])
                res[1].append(order[1])
        return res
        
    def visitCol_order(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 1: 
            return (l[0].getText(), True) #Columna por la que ordenar, true si es ascendente, false en caso contrario
        else:
            columna = l[0].getText()
            asc = l[1].getText().lower() == "asc"
            return (columna, asc)

    def visitTable(self, ctx:sequelParser.TableContext):
        self.tabla = ctx.getText()
        try:
            self.data_frame = pd.read_csv(f"./data/{self.tabla}.csv")
            return self.data_frame
        except:
            st.write(f"Error: la tabla '{self.tabla}' es incorrecta") # Fallo al abrir el fichero
            return -1

st.text_input("Consulta:", key="query")
input_stream = InputStream(st.session_state.query)
lexer = sequelLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = sequelParser(token_stream)
tree = parser.root()

if parser.getNumberOfSyntaxErrors() == 0:
    visitor = nuevoVisitor()
    visitor.visit(tree)
else:
    print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
    print(tree.toStringTree(recog=parser))
