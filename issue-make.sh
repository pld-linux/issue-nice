#!/bin/sh
# Pawe³ ¯urowski (pzurowski@post.pl)
# License: GPL v2+
#
# wywolanie: $0 "1 2 3 0" "0 42 42 40" datadir < plik_4_liniowy
#                ^^^^^^^   ^^^^^^^^^^ 
#                |||||||   \\\\\\\\\\--- rozmiar tabulacji
#                \\\\\\\---------------- wciecie w spacjach
#
# datadir jest sciezka do danych, koncowy / musi byc
#
# plik_4_liniowy:
# ala ma kota
# kot	->mruk
# ala	.:6y     (tam jest tabulator)
# 	(: #
#
#wynik:
#  ala ma kota
#   kot-------------------------->mruk
#    ala.........................:6y
# (((((((((((((((((((((((((((((: #
#                                ^ zakladajac, ze tu jest 42 kolumna
cat|awk ' BEGIN {
	split("'"$1"'",indents);
	split("'"$2"'",tabs);
	datadir="'$3'";
}

function multichar(ch, count){
	while (count>0){
		printf("%c",ch);
		count--
	}
}
{
	gsub("@@uname-p@@","`" datadir "uname-p.sh`");
	gsub("@@random@@","`" datadir "random.sh`");
}
/\t/ {
	split($0,field1,"\t");
	f1=field1[1];
	f2=substr(field1[2],2);
	delim=substr(field1[2],1,1);
	tabstop=tabs[NR]-indents[NR]-length(f1);
	
	multichar(" ",indents[NR]);
	printf("%s",f1);
	multichar(delim,tabstop);
	printf("%s\n",f2);
	next;
}
{
	multichar(" ",indents[NR]);
	print;
}

';
