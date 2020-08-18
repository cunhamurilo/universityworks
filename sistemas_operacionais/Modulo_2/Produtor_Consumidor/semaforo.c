#include "semaforo.h"
#include "buffer.h"

// Módulo 2 - Problema do Produtor-Consumidor
// SSC - GPSO4
// https://github.com/Es7evam/SSC5723-gpso4/
// Estevam F Arantes
// Murilo C. dos Santos

// Função Produtor
void* produtor(void *p){
	int data=0;
  	// região critica
	for(int i = 0; i < ITENS; i++){
		printf("Produtor esperando processo %d\n", i);

		// Espera a liberação da região crítica
		sem_wait(&vazio_slot);
		sem_wait(&exclusao);

		// Realiza as operações
		printf("Produtor - Produziu -> %d.\n", i);
		data++;
		insere_buffer(data,p);

		// Libera a região crítica
		sem_post(&exclusao);
		sem_post(&cheio_slot);

    	sleep(random() % 3);
	}
}

// Função Consumidor
void* consumidor(void *p){
	int data;
  	// região critica
	for(int i = 0; i < ITENS; i++){
		printf("Consumidor - Esperando %d\n", i);

		// Espera a região crítica
		sem_wait(&cheio_slot);
		sem_wait(&exclusao);

		// Realiza as ações
		remove_buffer(&data,p);
		printf("Consumidor - Consumiu -> %d.\n", data);

		// Libera a região crítica
		sem_post(&exclusao);
		sem_post(&vazio_slot);

		sleep(random() % 3);
	}
}


int main(int argc, char*argv[]){
	// Inicializa a seed do random
	srandom(time(NULL));

	// cria o buffer
	buffer *buf = (buffer*)malloc(sizeof(buffer));
	inicializa_buffer(buf);
	
  	// Inicializa os semáforos com as posições do buffer
	sem_init(&exclusao,0,1);
	sem_init(&cheio_slot,0,0);
	sem_init(&vazio_slot,0,ITENS);
	
  	// Cria as threads de produtor e consumidor
	pthread_create(&thr_produtor,NULL,produtor,buf);
	pthread_create(&thr_consumidor,NULL,consumidor,buf);

  	// Thread principal espera a thread produtor e consumidor acabarem 
	pthread_join(thr_produtor, NULL);
  	pthread_join(thr_consumidor, NULL);

	// destroy os semáforos
	sem_destroy(&exclusao);
	sem_destroy(&cheio_slot);
	sem_destroy(&vazio_slot);

	// Libera a memória do buffer
	free(buf);	
	return 0;
}