#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <errno.h>
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
	double tempo = 0;
	ticks t_ini, t_fim;
	struct timeval tval_ini, tval_fim, tval_answ;
	
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
	//t_ini = time(NULL);

	// Checa se arquivo existe
	if (access(path, F_OK) != -1){
		// remove arquivo
		if(remove(path) == -1){
			fprintf(stderr, "Erro ao remover arquivo!\n");
		}else{
			fprintf(stderr, "Arquivo %s removido com sucesso!\n", path);
		}	
	}else{
		// Arquivo não existe
		fprintf(stderr, "Arquivo %s não existe!\n", path);
	}

	// Tempo Final
	gettimeofday(&tval_fim, NULL);
	t_fim = getticks();
	//t_fim = time(NULL);

	timersub(&tval_fim, &tval_ini, &tval_answ);

	// verifica a diferenca do tempo inicial com o final 
	// e soma em uma variavel que armazena todos os resultaos
	tempo = (double)(t_fim - t_ini)/ CLOCKS_PER_SEC;
	printf("Milhões de clocks de cpu: %lf\n", tempo);
	printf("Tempo total %ld.%06ld\n", (long int)tval_answ.tv_sec, (long int)tval_answ.tv_usec);

	return 0;
}
