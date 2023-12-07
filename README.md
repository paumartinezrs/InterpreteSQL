# InterpreteSQL
Creación de un interprete SQL utilizando antlr4 y python. Los datos son tratados con la libreria pandas y la interfície gráfica con streamlit.

Para compilar: antlr4 -Dlanguage=Python3 -no-listener -visitor sequel.g4 \n
Para ejecutar: streamlit run sequel.py
