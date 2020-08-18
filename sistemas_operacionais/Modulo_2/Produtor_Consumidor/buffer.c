#include "buffer.h"

// conta os itens no buffer 
int conta_buffer(const buffer *b){
	int count;

	count = b->in-b->out;
	if(b->in < b->out) 
		count += ITENS;
	return count;
}

// insere dado no buffer
int insere_buffer(int item, buffer *b){
	if(conta_buffer(b) >= ITENS-1) 
		return -1;
	b->buf[b->in] = item;
	b->in = (b->in+1) % ITENS;
	return 0;
}

// tira dados do buffer
int remove_buffer(int *item, buffer *b){
	if(b->in == b->out) 
		return -1;
	*item = b->buf[b->out];
	b->out = (b->out+1) % ITENS;
	return 0;
}

// inicializa buffer
void inicializa_buffer(buffer *b){
	b->in=0;
	b->out=0;
}
