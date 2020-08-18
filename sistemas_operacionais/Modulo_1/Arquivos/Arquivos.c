#include <stdio.h>
#include <stdlib.h>

int main(){
	FILE *f1, *f2;
	// Nro de váriaveis escritas
    	const int N = 100;
	int i = 0, a;
	while (i < N){
		// Abre arquivo txt no modo append
		f1 = (FILE*)fopen("txt.txt","a");
		// Abre o arquivo txt2 no modo leitura
		f2 = (FILE*)fopen("txt2.txt","r");

		// Lê do arquivo txt2 e escreve a iteração no txt1
		fscanf(f2,"%d\n", &a);
		fprintf(f1,"%d\n", i);
		i++;

		// Fecha os arquivos
		fclose(f1);
		fclose(f2);
	}

	return 0;
}
