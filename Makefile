all: compilar

compilar:
	antlr4 -Dlanguage=Python3 -no-listener -visitor sequel.g4

test:
	pytest -v

streamlit:
	streamlit run sequel.py
	
run:
	python3 sequel.py

