#include <algorithm>
#include <iostream>
#include <deque>
#include <vector>
#include <utility>
#include <random> // random string

#include "Config.hh"
using namespace std;

class ManipulaMemoria {
    private:
    // Configuracao
    Config config;

    // Memoria Real
    vector<string> memoria;

    // Memoria Virtual
    vector<pair<string, long long>> virtMem;

    // Tabela Memoria Virtual -> Real 
    map<pair<string, long long>, long long> virtTable;
    
    // Tabela Contagem Processo
    map<string, int> psCount;

    // Remove frame da memória virtual
    void removeVirtual(pair<string, long long> frame);

    // Checa se um frame está na memória virtual
    // Retorna verdadeiro/falso
    bool checkVirtual(pair<string, long long> frame);

    public:

    // Tabela tamanho processo
    map<string, long long> tamProcesso;

    // Quantidade pageFault
    int cPageFault;

    /****************
        Funções
    *****************/

    ManipulaMemoria(Config conf);

    // Converte Endereço em um Frame
    long long addrToFrame(long long addr);

    // Simula acesso de um frame na memória real
    // Chamado automaticamente pela função de virtToReal
    bool acessoReal(long long frame);
    
    // Recebe pair <processo, endereco> e retorna frame real associada
    // Associa caso ainda não esteja mapeada
    long long virtToReal(pair<string, long long> frameVirt);

    // Checa se já não está existe
    // Insere se não existir
    // Faz todos checks e chama remoção caso necessário
    // Retorna frame real onde foi inserido
    long long acessaVirtual(pair<string, long long> frame);

    // Gera string de tamanho length
    string random_string(std::string::size_type length);
};

