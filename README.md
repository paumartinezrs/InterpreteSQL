# PandaQ
Welcome to PandaQ, an SQL interpreter. The grammar was created with ANTLR4, and the graphical interface is built with Streamlit.

## Compile
To compile the project:  
`antlr4 -Dlanguage=Python3 -no-listener -visitor sequel.g4`

## Run
To run the program:  
`streamlit run sequel.py`  
Once Streamlit is running as localhost, SQL queries can be executed using SQL syntax.

## Notes
It is important to have a folder named `data` in the project directory, containing the tables to work with, in CSV format.

