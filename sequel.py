from antlr4 import *
from sequelLexer import sequelLexer
from sequelParser import sequelParser
from sequelVisitor import sequelVisitor

import streamlit as st
import pandas as pd
import operator as op

def operacion(operation, num):
    if (operation == '+'): return lambda x : x + num 
    elif (operation == '-'): return lambda x : x - num
    elif (operation == '**'): return lambda x : x * num
    elif (operation == '/'): return lambda x : x / num
    elif (operation == '^'): return lambda x : pow(x, num)

class nuevoVisitor(sequelVisitor):
    def visitSelect_statement(self, ctx):
        self.hijos = list(ctx.getChildren())
        self.data_frame = self.visit(self.hijos[len(self.hijos) - 1]) #data frame con los valores de la tabla entera
        if self.hijos[1].getText() == '*': 
            st.write(self.data_frame)
        else:
            datos = self.visit(self.hijos[1]) 
            st.write(pd.DataFrame(datos))

    def visitColumn_selection(self, ctx):
        [lista] = list(ctx.getChildren())
        return self.visit(lista)
        
    def visitColumn_list(self, ctx):
        columnas = list(ctx.getChildren())
        self.datos = {} #devuelvo un diccionario con las columnas necesarias. la llave sera el nombre
        #problema      #m'agradaria passar datos com a valor com a parametre, pq no em deixa???
        for c in columnas:
            self.visit(c) #añade al diccionario los valores de la columna c. (puede ser una columna existente o una columna nueva)
        return self.datos
        
    def visitColumna_existente(self, ctx):
        [nombre_columna] = list(ctx.getChildren())
        nombre_columna = nombre_columna.getText()
        valores_columna = self.data_frame[nombre_columna]
        self.datos[nombre_columna] = valores_columna

    def visitColumna_nueva(self, ctx):
        [columna1, operation, numero, a, columna2] = list(ctx.getChildren())
        columna1 = columna1.getText()
        operation = operation.getText()
        numero = float(numero.getText())
        a = a.getText()
        columna2 = columna2.getText()
        self.datos[columna2] = list(map(operacion(operation, numero), list(self.data_frame[columna1])))

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
