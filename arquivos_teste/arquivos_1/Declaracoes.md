# Declaraçãoes (Statements)

Uma _declaração_ é um texto que o banco de dados reconhece como comando válido. Sempre terminam com ( ; )

```sql 
CREATE TABLE table_name (  
	column_1 data_type,  
 	column_2 data_type,  
 	column_3 data_type  
);
```

1. 'CREATE TABLE' é uma Cláusula. Estar perfoma específicas tarefas em SQL, por convesão são escritas em letras maiúsculas. Poedm ser referidas como comandos.

2. 'table_name' é o nome da tabela a que o comando se refere.


3. (column_1 data_type, column_2 data_type, column_3 data_type) é um _parâmetro_. Um parâmetro é uma lista de colunas, tipos de dados ou valores que são passados para uma cláusula como argumento. Neste exemplo, é uma lista de nomes de coluna e o tipo de dados associado a cada coluna.

A estrutura do SQL varia bastante. O número de linhas usadas não é relevante. Uma declaração pode ser escrita em uma única linha ou quebrada em diversas linhas, se for mais fácil de compreender.

Também é importante entender o conceito de [[Constantes SQL]], pois estar permitem alizar ações específicas