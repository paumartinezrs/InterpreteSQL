from antlr4 import *
from sequelLexer import sequelLexer
from sequelParser import sequelParser
from sequelVisitor import sequelVisitor

import streamlit as st
import pandas as pd

#per executar amb streamlit posarho a True
web = False

def operacion(operation, num):
    if (operation == '+'): return lambda x : x + num 
    elif (operation == '-'): return lambda x : x - num
    elif (operation == '**'): return lambda x : x * num
    elif (operation == '/'): return lambda x : x / num
    elif (operation == '^'): return lambda x : pow(x, num)

class nuevoVisitor(sequelVisitor):
    def visitRoot(self, ctx):
        [statement] = list(ctx.getChildren())
        return self.visit(statement)
    
    def visitSelect_statement(self, ctx):
        self.hijos = list(ctx.getChildren())
        
        self.visit(self.hijos[3]) #visitem Table
        self.visit(self.hijos[1]) #visitem column selection

        for i in range(4, len(self.hijos)):
            self.visit(self.hijos[i]) 
            
        return self.data_frame

    

    #no cal separar all columns i some columns de moment
    def visitSome_columns(self, ctx): 
        [lista] = list(ctx.getChildren())
        return self.visit(lista)
    




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
        [nombre_columna] = list(ctx.getChildren())
        nombre_columna = self.visit(nombre_columna)
        return nombre_columna
    
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

    

   





    def visitColumns_order(self, ctx): #devuelve una lista segun el orden que se ordenaran las filas del dataset
        l = list(ctx.getChildren()) #deberiamos comprovar que sean columnas existentes
        order = ([],[])
        for i in l: 
            if i.getText() != ',' :
                columna = self.visit(i)    
                order[0].append(columna[0])
                order[1].append(columna[1])
        
        self.data_frame = self.data_frame.sort_values(by = order[0], ascending = order[1])
        #st.write(self.data_frame)
        
    def visitCol_order_asc(self, ctx): #comprovar si existe
        l = list(ctx.getChildren())
        columna = self.visit(l[0])
        ascendente = True
        return (columna, ascendente)

    def visitCol_order_especificado(self, ctx):
        l = list(ctx.getChildren())
        columna = self.visit(l[0])
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

    def visitColumn(self, ctx): #provar si existe
        [identificador] = list(ctx.getChildren())
        return identificador.getText()

    def visitTable(self, ctx):
        self.tabla = ctx.getText()
        try:
            self.data_frame = pd.read_csv(f"./data/{self.tabla}.csv")
        except:
            st.write(f"Error: la tabla '{self.tabla}' es incorrecta") # Fallo al abrir el fichero
            return -1


def ejecuta(input_stream): 
    input_stream = InputStream(input_stream)
    lexer = sequelLexer(input_stream)   
    token_stream = CommonTokenStream(lexer)
    parser = sequelParser(token_stream)
    tree = parser.root()

    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = nuevoVisitor()
        res = visitor.visit(tree)
        if (web): st.write(res)
        else: print(res)
        return res
    else:
        print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
        print(tree.toStringTree(recog=parser))
        return -1

def main():
    input_stream = ""
    if (web):
        st.text_input("Consulta:", key="query")
        input_stream = st.session_state.query
    else: 
        input_stream = input('Consulta: ')
    ejecuta(input_stream)

#descomenta main para funcionamiento normal
#while (True): main()

#sentencia para usar en una prueba
#ejecuta("select * from countries order by region_id, country_name desc")




