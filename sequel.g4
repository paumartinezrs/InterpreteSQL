grammar sequel;

options {caseInsensitive = true;}

root: (select_statement | simbol_declare | simbol_consult | plot)+ ';' ;

select_statement
    : SELECT column_selection FROM table inner_clause* where_clause? (ORDER columns_order)? 
    ;

simbol_declare
    : ID ':=' select_statement
    ;

simbol_consult
    : ID 
    ;

plot
    : 'plot ' ID 
    ;

inner_clause
    : INNER table ON column '=' column
    ;

column_selection
    : '*'           
    | column_list   
    ;

column_list
    : column_id (',' column_id)* 
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
    : col_order (',' col_order)*;

col_order
    : column ('asc' | 'desc') #col_order_especificado
    | column                  #col_order_asc
    ;

where_clause 
    : WHERE op_logic+
    ;

op_logic
    : column 'in' '(' select_statement ')' #in
    | 'not' op_logic                       #not 
    | op_logic 'and' op_logic              #and
    | op_logic 'or' op_logic               #or  
    | condition                            #single
    ;

condition
    : column_expr ('=' | '<' | '>' | '<=' | '>=' | '<>') column_expr
    ; 

column: ID;
    
table: ID ;

SELECT: 'select' ; 
FROM: 'from' ;
AS: 'as' ;
INNER: 'inner join ';
ON: 'ON';
WHERE: 'where' ;
ORDER: 'order by' ;
ID: [a-z_][a-z0-9_]* ;
NUM: [+-]?([0-9]*[.])?[0-9]+;
WS: [ \t\n\r]+ -> skip ;