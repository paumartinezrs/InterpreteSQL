# PandaQ
Bienvenidos a PandaQ. Un interprete de SQL creado con ANTLR4 y con la interfície grafica por streamlit. 

## Compilar
Para compilar el proyecto: antlr4 -Dlanguage=Python3 -no-listener -visitor sequel.g4 

## Ejecutar
Para ejecutar el programa: streamlit run sequel.py
Una vez iniciado streamlit como localhost se pueden hacer consultas utilizando la sintaxi de SQL. 

## Apreciaciones
Es importante tener en el directorio del proyecto, una carpeta llamada data con las tablas con las que se trabajara, en formato csv. 
