from antlr4 import *
from sequelLexer import sequelLexer
from sequelParser import sequelParser
from sequelVisitor import sequelVisitor

import streamlit as st
import pandas as pd

#Devuelve un maybe dataFrame, si la tabla existe
def existe_tabla(tabla): 
    try:
        #,index_col=0 
        df = pd.read_csv(f"./data/{tabla}.csv")
        return (True, df)
    except:
        # Fallo al abrir el fichero
        return (False, 0)

class nuevoVisitor(sequelVisitor):
    def visitTable(self, ctx:sequelParser.TableContext):
        tabla = ctx.getText()
        (res, data_frame) = existe_tabla(tabla)
        if not res:
            st.write(f"No existe la tabla {tabla}.")
        else:
            st.write(data_frame)
        return self.visitChildren(ctx)

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
