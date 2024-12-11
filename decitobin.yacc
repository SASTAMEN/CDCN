yacc1.l:

%{
  #include "yacc1.tab.h"
%}
%%
[0-9]+ {yylval = atoi(yytext);
                            return NUM;}
\n return 0;

. return yytext[0];

%%

yacc:

%{

#include<stdio.h>

int x, p, r, n;

void yyerror(char *s);

int yylex();

%}

%token NUM

%%

stmt: NUM{ x =$1 ;p = 1 ; n = 0;

while (x != 0 )

{

r = x%2;

n = n + r*p;

p = p * 10;

x = x / 2;

}

printf("%d\n",n);

}

%%

int main()

{

printf("\nEnter a decimal number: ");

yyparse();

return 0;

}

int yywrap() {

return 1;

}

void yyerror(char *s){

printf("\nInvalid expression");
}
