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

//2b ha de ser taula i constant o poden ser coses mes complexes?
column_expr
    : ID OP NUM ID #columna_nueva //em falla si fico l''as' nose pk. Crec q es per skipear la coma, no ho se potser si. 
    | ID           #columna_existente
    ;
    
table: ID ;

// Lexer rules
SELECT: 'select' ; 
ALL: '*';
FROM: 'from' ;
ID: [a-z_][a-z0-9_]* ;
NUM: [+-]?([0-9]*[.])?[0-9]+;   //floats e ints. match: 43, 43.65, .87
OP: '+' | '-' | '**' | '/';     //Problemes amb la multiplicacio, no em deixa ni que sigui '*' ni que sigui 'x', pk?
AS: 'as' ;
WS: [ \t\n\r]+ -> skip ;


