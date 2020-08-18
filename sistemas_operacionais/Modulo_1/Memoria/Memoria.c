#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){
	// Seta a seed do rand()
	srand(time(NULL));

	// Uma matrix
	int **M;
	int i, j;

	// Dimensão da matrix (N*N)
	const int N = 15000;

	// Aloca a memória
   	M = (int**) malloc (N * sizeof (int*));
   	for(i = 0; i < N; i++){
      		M[i] = (int*) malloc (N * sizeof (int));
   	}

	// Seta cada casa da matriz como um número de 0 a 100000
   	for(i = 0; i < N; i++){
   		for(j = 0; j < N; j++)
			M[i][j] = rand()%100000;
   	}

	// Libera a memória
   	for (i = 0; i < N; i++){
   		free(M[i]);
   	}
   	free(M);
   	return 0;
}
