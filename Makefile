all: compilar ejecutar

compilar:
	antlr4 -Dlanguage=Python3 -no-listener -visitor sequel.g4

ejecutar:
	streamlit run sequel.py

