grammar sequel;

options {caseInsensitive = true;}

root: select_statement ;

select_statement
    : SELECT column_list FROM table 
    ;

column_list
    : '*'
    //|  column_id (COMA column_id)*
    ;

column_id: ID ;

table: ID ;

// Lexer rules
SELECT: 'select' ;
FROM: 'from' ;
ID: [a-z_][a-z0-9_]* ;
COMA: ',' ;
WS: [ \t\n\r]+ -> skip ;

