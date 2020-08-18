#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>

int main(void){
	// Número de processos a serem criados
    	const int N = 1000;

	// Ids de cada processo
	pid_t child[N];
	pid_t parent;

	// Pega id do processo pai.
	parent = getpid();

	int i;
	for(i=0; i<N;i++){
		// Se não for o pai
		if(!(child[i] = fork())){
			//printf("In child\n");
			sleep(5);
			//printf("Exit child\n");
		}
	}

	// Termina os processos filhos
	for(i=0; i<N;i++){
		kill(child[i], SIGKILL);
	}

	// Sai do processo
	exit(0);

	// Mata o processo pai
	kill(parent, SIGKILL);

}
