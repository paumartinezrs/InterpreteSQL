grammar sequel;

options {caseInsensitive = true;}

root: select_statement ;

select_statement
    : SELECT column_selection FROM table 
    ;

column_selection
    : (ALL | column_list)
    ;

column_list
    : column_expr (',' column_expr)* ;


column_expr
    : ID OP NUM AS ID #columna_nueva 
    | ID              #columna_existente
    ;
    
table: ID ;

// Lexer rules
SELECT: 'select' ; 
ALL: '*';
FROM: 'from' ;
AS: 'as' ;
ID: [a-z_][a-z0-9_]* ;
NUM: [+-]?([0-9]*[.])?[0-9]+;   //floats e ints. match: 43, 43.65, .87
OP: '+' | '-' | '**' | '/' | '^';     //Problemes amb la multiplicacio, no em deixa ni que sigui '*' ni que sigui 'x', pk?

WS: [ \t\n\r]+ -> skip ;


