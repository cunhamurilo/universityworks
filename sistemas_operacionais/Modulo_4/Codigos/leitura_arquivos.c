#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
#include <sys/time.h>

typedef unsigned long long ticks;

static __inline__ ticks getticks(void){
     unsigned a, d;
     asm("cpuid");
     asm volatile("rdtsc" : "=a" (a), "=d" (d));

     return (((ticks)a) | (((ticks)d) << 32));
}

int main(int argc, char*argv[]){
	FILE *arq;
	double tempo = 0;
	ticks t_ini, t_fim;
	struct timeval tval_ini, tval_fim, tval_answ;

	unsigned int readVar;
	
	// Pegando caminho do arquivo
	char path[100] = "../Arquivos/arquivo_size_";
	if(argc < 2){
		printf("Passar argumento com arquivo!\n");
		return -1;
	}
	strcat(path, argv[1]);
	strcat(path, ".txt");


	// Tempo Inicial
	t_ini = getticks();
	gettimeofday(&tval_ini, NULL);

	// Checa se arquivo existe
	if (access(path, F_OK) != -1){
		// checa se existe
		arq = fopen(path, "rb");

		fseek(arq, 0L, SEEK_END);
		long sz = ftell(arq);
		fprintf(stderr, "Arquivo de tamanho %ld\n", sz);
		fclose(arq);
	}else{
		// Arquivo não existe
		fprintf(stderr, "Arquivo %s não existe!\n", path);
		return -1;
	}

	arq = fopen(path, "rb");
	while(!feof(arq)){
		fread(&readVar, sizeof(readVar), 1, arq);
	}
	fclose(arq);

	// Tempo Final
	gettimeofday(&tval_fim, NULL);
	t_fim = getticks();
	//t_fim = time(NULL);

	timersub(&tval_fim, &tval_ini, &tval_answ);

	// verifica a diferenca do tempo inicial com o final 
	// e soma em uma variavel que armazena todos os resultaos
	tempo = (double)(t_fim - t_ini)/ CLOCKS_PER_SEC;
	printf("L: Milhões de clocks de cpu: %lf\n", tempo);
	printf("L: Tempo total %ld.%06ld\n", (long int)tval_answ.tv_sec, (long int)tval_answ.tv_usec);
	return 0;
}
