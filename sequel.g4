grammar sequel;

//Falten trys excepts

options {caseInsensitive = true;}

root: select_statement ;

select_statement
    : SELECT column_selection FROM table (WHERE clausula_where)? (ORDER columns_order)? 
    ;

column_selection
    : '*'           #all_columns
    | column_list   #some_columns
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
    : col_order (',' col_order)*; // perque no salta error si tinc em deixo la coma?

col_order
    : column ('asc' | 'desc') #col_order_especificado
    | column                  #col_order_asc
    ;

//fer un per sobre de op_logic per poder aplicar el resultat final

clausula_where
    : op_logic
    ;

op_logic
    : 'not' op_logic            #not 
    | op_logic 'and' op_logic   #and
    | op_logic 'or' op_logic    #or  
    | condition                 #single
    ;

condition
    : column ('=' | '<' | '>' | '<=' | '>=' | '<>') column_expr
    ; 

column: ID;
    
table: ID ;

// Lexer rules
SELECT: 'select' ; 
FROM: 'from' ;
AS: 'as' ;
ORDER: 'order by' ;
WHERE: 'where' ;
ID: [a-z_][a-z0-9_]* ;
NUM: [+-]?([0-9]*[.])?[0-9]+;      //floats e ints. matches: 43, 43.65, .87
WS: [ \t\n\r]+ -> skip ;


