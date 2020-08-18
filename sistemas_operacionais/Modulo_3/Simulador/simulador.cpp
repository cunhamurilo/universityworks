#include "simulador.h"
#include "ManipulaMemoria.hh"


int main(int argc, char **argv){
	// definição do arquivo a ser lido
	char *caminhoArquivo = argv[1];
	
	Config *config = new Config();
	ManipulaMemoria *memoria = new ManipulaMemoria(*config);

	// abre o arquivo para leitura
	freopen(caminhoArquivo, "r", stdin);
	// percorre o arquivo
	string linha;
	while(getline(cin, linha)){
		op++;
		stringstream ss(linha);
		string processo, comando;
		ss >> processo >> comando;
		if(comando == "C"){
			long long tamanhoProcesso;
			ss >> tamanhoProcesso;
			cout << "Op. Criação Processo: " << processo << " :Tamanho: " << tamanhoProcesso << endl; 
			memoria->tamProcesso[processo] = tamanhoProcesso;
		}
		else{
			long long endereco;
			string opString;
			for(int i=0;i<linha.size();i++){
				if(linha[i] == '(' || linha[i] == ')'){
					linha[i] = ' ';
				} 
			}
			ss >> opString;
			endereco = strtoull(opString.c_str(), NULL, 2);

			// Checagem linha/endereco lidos
			#ifdef DEBUG
				cout << "Linha: " << linha;
				cout << " : " << endereco << endl;
			#endif

			if(comando == "P"){
				cout << "Op. CPU: Processo: " << processo << " : Disp.: " << endereco << endl; 
				long long endCPU;
				endCPU = (1L << 62) + config->pageSize * endereco; 
				cout << "\t Mapeado no endereço: " << endCPU << endl;

				// Converte endereço para página
				long long pagIdx = memoria->addrToFrame(endCPU);
				pair<string, long long> virtMemFrame = make_pair(processo, pagIdx);

				memoria->acessaVirtual(virtMemFrame);
			}
			else if(comando == "I"){
				cout << "Op. I/O: Processo " << processo << " : Disp.: " << endereco << endl; 

				long long endIO;
				endIO = (1L << 62) + (1L << 62)/2L + config->pageSize * endereco; 
				cout << "\t Mapeado no endereço: " << endIO << endl;

				// Converte endereço para página
				long long pagIdx = memoria->addrToFrame(endIO);
				pair<string, long long> virtMemFrame = make_pair(processo, pagIdx);

				memoria->acessaVirtual(virtMemFrame);
			}
			else if(comando == "W"){
				cout << "Op. Escrita: Processo " << processo << " :End.: " << endereco << endl; 
				escrita++;

				// Converte endereço para página
				long long pagIdx = memoria->addrToFrame(endereco);
				pair<string, long> virtMemFrame = make_pair(processo, pagIdx);

				
				memoria->acessaVirtual(virtMemFrame);
			}else if(comando == "R"){
				cout << "Op. Leitura: Processo " << processo << " :End.: " << endereco << endl; 
				leitura++;
				long long pagIdx = memoria->addrToFrame(endereco);
				pair<string, long long> virtMemFrame = make_pair(processo, pagIdx);
				
				memoria->acessaVirtual(virtMemFrame);
			}
		}
		cout << endl;	
	}
	
	// mostra no terminal algumas informacoes referentes ao simulador
	cout << "\nSimulador Memoria Virtual" << endl;
	cout << "  Quantidade total de operações: " << op << endl;
	cout << "  Quantidade de escrita: " << escrita << endl;
	cout << "  Quantidade de leitura: " << leitura << endl;
	cout << "  Quantidade de falta de pagina: " << memoria->cPageFault << endl;
	
	delete memoria;
	delete config;
	return 0;
}