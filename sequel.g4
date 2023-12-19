grammar sequel;

options {caseInsensitive = true;}

root: select_statement ;

select_statement
    : SELECT column_selection FROM table (ORDER columns_order)?
    ;

column_selection
    : '*'           #all_columns
    | column_list   #some_columns
    ;

column_list
    : column_id (',' column_id)*  //perque aqui sense coma salta error, pero en columns_order sense coma no?
    ;

column_id
    : column_expr AS column #columna_nueva
    | column                #columna_existente
    ;

column_expr
    : '('column_expr')'                         #parentesis
    | <assoc=right> column_expr '^' column_expr #potencia
    | column_expr ('*' | '/') column_expr       #mult_div
    | column_expr ('+' | '-') column_expr       #sum_rest
    | column                                    #id_columna
    | NUM                                       #num
    ;

columns_order
    : col_order (',' col_order)*; // perque no salta error si tinc em deixo la coma?

col_order
    : column ('asc' | 'desc') #col_order_especificado
    | column                  #col_order_asc
    ;

condition
    : column COMPARE NUM;

column: ID;
    
table: ID ;

// Lexer rules
SELECT: 'select' ; 
ALL: '*';
FROM: 'from' ;
AS: 'as' ;
ORDER: 'order by' ;
ASC: 'asc' ;
DESC: 'desc' ;
WHERE: 'where' ;
COMA : ',' ;
ID: [a-z_][a-z0-9_]* ;
NUM: [+-]?([0-9]*[.])?[0-9]+;      //floats e ints. matches: 43, 43.65, .87
OP_NUM: '+' | '-' | '*' | '/' | '^';  //Problemes amb la multiplicacio, no em deixa ni que sigui '*' ni que sigui 'x', pk?
//LOGIC_BIN: 'and' | 'or' ;
//LOGIC_
COMPARE: '=' ;
WS: [ \t\n\r]+ -> skip ;


//Si faig un append en una llista amb ',', hi ha alguna manera millor de ignorarles que if != ','


