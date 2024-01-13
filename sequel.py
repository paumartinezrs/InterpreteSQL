from antlr4 import *
from sequelLexer import sequelLexer
from sequelParser import sequelParser
from sequelVisitor import sequelVisitor

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

class myVisitor(sequelVisitor):
    def visitRoot(self, ctx):
        [accion, _] = list(ctx.getChildren())
        return self.visit(accion)
        
    def compruebaColumna(self, columna):
        if columna not in self.data_frame: st.write(f"Error: la columna '{columna}' es incorrecta!") 

    def visitIn(self, ctx):
        [columna, _, _, select, _] = list(ctx.getChildren())
        columna = columna.getText()
        self.compruebaColumna(columna)
        aux = self.data_frame
        select = self.visit(select)
        self.data_frame = aux
        self.data_frame = self.data_frame[columna].isin(select)
    
    def visitSimbol_declare(self, ctx):
        [identificador, _, consulta] = list(ctx.getChildren())
        identificador = identificador.getText()
        consulta = self.visit(consulta)
        st.session_state[identificador] = consulta
        return f"{identificador} declarado!"
        
    def visitSimbol_consult(self, ctx):
        [identificador] = list(ctx.getChildren())
        identificador = identificador.getText()
        return st.session_state[identificador]
    
    def visitSelect_statement(self, ctx):
        self.hijos = list(ctx.getChildren())
        self.data_frame = self.visit(self.hijos[3]) #visitamos Table
        for i in range(4, len(self.hijos)):
            self.visit(self.hijos[i]) 
        self.visit(self.hijos[1]) #visitamos column selection
        return self.data_frame

    def visitInner_clause(self, ctx): 
        [_, tabla, _, columna1, _, columna2] = list(ctx.getChildren())
        tabla = self.visit(tabla)
        columna1 = self.visit(columna1)
        columna2 = self.visit(columna2)
        self.compruebaColumna(columna1)
        self.compruebaColumna(columna2)
        self.data_frame =  self.data_frame.merge(tabla, left_on = columna1, right_on = columna2)

    def visitColumn_list(self, ctx):
        columnas = list(ctx.getChildren())
        visualizar_columnas = [] #columnas que se quedan en el data_frame
        for i in columnas:
            if i.getText() != ',': visualizar_columnas.append(self.visit(i))
        self.data_frame = self.data_frame[visualizar_columnas]
        
    def visitColumna_nueva(self, ctx):
        [expresion, _, nueva] = list(ctx.getChildren())
        expresion = self.visit(expresion)
        nueva = self.visit(nueva)
        self.data_frame[nueva] = expresion
        return nueva
   
    def visitColumna_existente(self, ctx):
        [columna] = list(ctx.getChildren())
        columna = self.visit(columna)
        self.compruebaColumna(columna)
        return columna
    
    def visitParentesis(self, ctx):
        [_, exprs, _] = list(ctx.getChildren())
        return self.visit(exprs)
    
    def visitPotencia(self, ctx):
        [primera, op, segona] = list(ctx.getChildren())
        op = op.getText()
        primera = self.visit(primera)
        segona = self.visit(segona)
        return pow(primera, segona)
    
    def visitMult_div(self, ctx):
        [primera, op, segona] = list(ctx.getChildren())
        op = op.getText()
        primera = self.visit(primera)
        segona = self.visit(segona)
        if op == '*': return primera*segona
        else: return primera/segona

    def visitSum_rest(self, ctx):
        [primera, op, segona] = list(ctx.getChildren())
        op = op.getText()
        primera = self.visit(primera)
        segona = self.visit(segona)
        if op == '+': return primera + segona
        else: return primera - segona

    def visitId_columna(self, ctx):
        [col] = list(ctx.getChildren())
        col = col.getText()
        return self.data_frame[col]
    
    def visitNum(self, ctx):
        [num] = list(ctx.getChildren())
        return float(num.getText())

    def visitColumns_order(self, ctx):
        l = list(ctx.getChildren())
        order = ([],[])
        for i in l: 
            if i.getText() != ',' :
                columna = self.visit(i) 
                order[0].append(columna[0])
                order[1].append(columna[1])
        self.data_frame = self.data_frame.sort_values(by = order[0], ascending = order[1])
        
    def visitCol_order_asc(self, ctx): 
        l = list(ctx.getChildren())
        columna = self.visit(l[0])
        self.compruebaColumna(columna)
        ascendente = True
        return (columna, ascendente)

    def visitCol_order_especificado(self, ctx):
        l = list(ctx.getChildren())
        columna = self.visit(l[0])
        self.compruebaColumna(columna)
        ascendente = l[1].getText().lower() == "asc"
        return (columna, ascendente) #true si es en orden ascendente, false en caso contrario  

    def visitClausula_where(self, ctx):
        [condition] = list(ctx.getChildren())
        condition = self.visit(condition)
        self.data_frame = self.data_frame[condition]
    
    def visitNot(self, ctx):
        [_, condition] = list(ctx.getChildren())
        return ~self.visit(condition) 
        
    def visitAnd(self, ctx):
        [condition1, _, condition2] = list(ctx.getChildren())
        condition1 = self.visit(condition1) 
        condition2 = self.visit(condition2)
        return condition1 & condition2

    def visitOr(self, ctx):
        [condition1, _, condition2] = list(ctx.getChildren())
        condition1 = self.visit(condition1) 
        condition2 = self.visit(condition2)
        return condition1 | condition2

    def visitSingle(self, ctx):
        [condition1] = list(ctx.getChildren())
        return self.visit(condition1) 
         
    def visitCondition(self, ctx):
        [expr1, op, expr2] = list(ctx.getChildren())
        expr1 = self.visit(expr1)
        op = op.getText()
        expr2 = self.visit(expr2)
        cumplen = -1
        if (op == "="):
            if isinstance(expr2, float): #expr2 es un numero, aplicamos un map
                condicion = lambda x: x == expr2
                cumplen = expr1.apply(condicion)
            else:  #expr2 es una columna, aplicamos un zip with
                cumplen = []
                for x, y in zip(expr1, expr2):
                    cumplen.append(x == y)
        elif (op == "<"):
            if isinstance(expr2, float): 
                condicion = lambda x: x < expr2
                cumplen = expr1.apply(condicion)
            else: 
                cumplen = []
                for x, y in zip(expr1, expr2):
                    cumplen.append(x < y)
        elif (op == ">"):
            if isinstance(expr2, float):
                condicion = lambda x: x > expr2
                cumplen = expr1.apply(condicion)
            else:  
                cumplen = []
                for x, y in zip(expr1, expr2):
                    cumplen.append(x > y)
        elif (op == "<>"):
            if isinstance(expr2, float):
                condicion = lambda x: x != expr2
                cumplen = expr1.apply(condicion)
            else:  
                cumplen = []
                for x, y in zip(expr1, expr2):
                    cumplen.append(x != y)
        elif (op == "<="):
            if isinstance(expr2, float): 
                condicion = lambda x: x <= expr2
                cumplen = expr1.apply(condicion)
            else:  
                cumplen = []
                for x, y in zip(expr1, expr2):
                    cumplen.append(x <= y)
        elif (op == ">="):
            if isinstance(expr2, float): 
                condicion = lambda x: x >= expr2
                cumplen = expr1.apply(condicion)
            else: 
                cumplen = []
                for x, y in zip(expr1, expr2):
                    cumplen.append(x >= y)
        return cumplen

    def visitColumn(self, ctx):
        [identificador] = list(ctx.getChildren())
        return identificador.getText()

    def visitTable(self, ctx):
        self.tabla = ctx.getText()
        try:
            return pd.read_csv(f"./data/{self.tabla}.csv")
        except:
            st.write(f"Error: la tabla '{self.tabla}' es incorrecta!")
            return "Vuelve a probar con una tabla correcta"

    def visitPlot(self, ctx):
        [_, identificador] = list(ctx.getChildren())
        identificador = identificador.getText()
        e = st.session_state[identificador]
        e.plot()
        st.pyplot()
        return f"Plot de {identificador}"


def ejecuta(input_stream): 
    input_stream = InputStream(input_stream)
    lexer = sequelLexer(input_stream)   
    token_stream = CommonTokenStream(lexer)
    parser = sequelParser(token_stream)
    tree = parser.root()
    
    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = myVisitor()
        res = visitor.visit(tree)
        st.write(res)         
    else:
        print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
        print(tree.toStringTree(recog=parser))
        

def main():
    input_stream = ""
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.header("PandaQ")
    st.subheader("by Pau Martinez")
    input_stream = st.text_area("Introduce tu consulta")
    ejecuta(input_stream)

main()



