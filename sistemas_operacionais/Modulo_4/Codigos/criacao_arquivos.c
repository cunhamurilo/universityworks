#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

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
	int size = 0;
	ticks t_ini, t_fim;
	struct timeval tval_ini, tval_fim, tval_answ;
	
	// criação do nome arquivo
	char path[100] = "../Arquivos/arquivo_size_";
	if(argc < 2){
		fprintf(stderr, "Passar tamanho como argumento!\n");
		return -1;
	}
	strcat(path, argv[1]);
	strcat(path, ".txt");
	
	// percorre as execuções
	// tempo inicial para cada execucao
	t_ini = getticks();
	gettimeofday(&tval_ini, NULL);
	
	// abrindo o arquivo para criação 
	arq = fopen(path, "wb");
	if (arq == NULL){
		printf("Problemas na CRIACAO do arquivo\n");
		return -2;
	}  
	
	// verifica o tamanho do tamanho
	if(strcmp(argv[1], "5kb") == 0)
		size = 500;
	else if(strcmp(argv[1], "10kb") == 0)
		size = 10000;
	else if(strcmp(argv[1], "100kb") == 0)
		size = 100000;
	else if(strcmp(argv[1], "1mb") == 0)
		size = 1000000;
	else if(strcmp(argv[1], "10mb") == 0)
		size = 10000000;
	else if(strcmp(argv[1], "100mb") == 0)
		size = 100000000;
	else if(strcmp(argv[1], "500mb") == 0)
		size = 500000000;
	
	// insere dados no arquivo
	for(unsigned int j=0; j < size/sizeof(j); j++){
		fwrite(&j, sizeof(j), 1, arq);
	}

	// fechando arquivo
	fclose(arq);
	
	// Tempo Final
	gettimeofday(&tval_fim, NULL);
	t_fim = getticks();

	timersub(&tval_fim, &tval_ini, &tval_answ);

	// verifica a diferenca do tempo inicial com o final 
	// e soma em uma variavel que armazena todos os resultaos
	tempo = (double)(t_fim - t_ini)/ CLOCKS_PER_SEC;
	printf("C: Milhões de clocks de cpu: %lf\n", tempo);
	printf("C: Tempo total %ld.%06ld\n", (long int)tval_answ.tv_sec, (long int)tval_answ.tv_usec);
	return 0;
}
