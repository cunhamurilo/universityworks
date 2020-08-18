#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

// threads produtor e consumidor
pthread_t thr_produtor;
pthread_t thr_consumidor;

// semaforos
static sem_t exclusao;
static sem_t vazio_slot;
static sem_t cheio_slot;

//funções produtor x consumidor
void* produtor(void *p);
void* consumidor(void *p);