# PandaQ
Bienvenidos a PandaQ, un interprete de SQL. La gramatica se ha hecho con ANTLR4 y la interfície gráfica con streamlit. 

## Compilar
Para compilar el proyecto: antlr4 -Dlanguage=Python3 -no-listener -visitor sequel.g4 

## Ejecutar
Para ejecutar el programa: streamlit run sequel.py  
Una vez iniciado streamlit como localhost se pueden hacer consultas utilizando la sintaxi de SQL.

## Apreciaciones
Es importante tener en el directorio del proyecto, una carpeta llamada data con las tablas con las que se trabajara, en formato csv.  

