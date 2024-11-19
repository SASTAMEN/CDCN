%{
   #include <stdio.h>
   int word_count = 0;
   int number_count = 0;
   int line_count = 0;
%}

%%
[a-zA-Z]+    { word_count++; }
[0-9]+       { number_count++; }
\n           { line_count++; }
.            { /* Ignore any other character */ }
%%

int main() {
   yylex();
   printf("Words: %d\n", word_count);
   printf("Numbers: %d\n", number_count);
   printf("Lines: %d\n", line_count);
   return 0;
}
