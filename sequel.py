from antlr4 import *
from sequelLexer import sequelLexer
from sequelParser import sequelParser
from sequelVisitor import sequelVisitor

import streamlit as st
import pandas as pd

class nuevoVisitor(sequelVisitor):
    def visitSelect_statement(self, ctx):
        self.hijos = list(ctx.getChildren())
        self.data_frame = self.visit(self.hijos[len(self.hijos) - 1])
        if self.hijos[1].getText() == '*': 
            st.write(self.data_frame)
        else:
            try:
                lista_columnas = self.visit(self.hijos[1])
                st.write(self.data_frame[lista_columnas])
            except:
                st.write("Error: columna/s incorrecta/s")
            

    def visitColumn_selection(self, ctx):
        [lista] = list(ctx.getChildren())
        return self.visit(lista)
        
    def visitColumn_list(self, ctx):
        l = list(ctx.getChildren())
        lista_columnas = []
        for i in l:
            lista_columnas.append(i.getText())
        return lista_columnas
        
    def visitTable(self, ctx:sequelParser.TableContext):
        self.tabla = ctx.getText()
        try:
            self.data_frame = pd.read_csv(f"./data/{self.tabla}.csv")
            return self.data_frame
        except:
            # Fallo al abrir el fichero
            st.write(f"Error: la tabla '{self.tabla}' es incorrecta")
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
