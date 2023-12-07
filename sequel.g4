grammar sequel;

options {caseInsensitive = true;}

root: select_statement ;

select_statement
    : SELECT column_selection FROM table (ORDER columns_order)?
    ;

column_selection
    : (ALL | column_list)
    ;

column_list
    : column_expr (',' column_expr)*  //Esta be aquesta coma o seria millor ficar una lexer rule?
    ;

column_expr
    : ID OP NUM AS ID #columna_nueva 
    | ID              #columna_existente
    ;

columns_order
    : col_order (',' col_order)*; 

col_order
    : ID (ASC | DESC)? ;
    
table: ID ;

// Lexer rules
SELECT: 'select' ; 
ALL: '*';
FROM: 'from' ;
AS: 'as' ;
ORDER: 'order by' ;
ASC: 'asc' ;
DESC: 'desc' ;
ID: [a-z_][a-z0-9_]* ;
NUM: [+-]?([0-9]*[.])?[0-9]+;      //floats e ints. matches: 43, 43.65, .87
OP: '+' | '-' | '**' | '/' | '^';  //Problemes amb la multiplicacio, no em deixa ni que sigui '*' ni que sigui 'x', pk?
WS: [ \t\n\r]+ -> skip ;


