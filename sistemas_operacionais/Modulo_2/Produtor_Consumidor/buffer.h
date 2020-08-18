#ifndef BUFFER_H
#define BUFFER_H

#define ITENS 30

// estrutura do buffer
typedef struct{
	int in;
	int out;
	int buf[ITENS];
} buffer;

// funções do buffer 
extern void inicializa_buffer(buffer *b);
extern int conta_buffer(const buffer *b);
extern int insere_buffer(int item, buffer *b);
extern int remove_buffer(int *item, buffer *b);
#endif
