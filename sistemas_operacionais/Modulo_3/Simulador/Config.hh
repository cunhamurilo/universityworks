#include <map>
#include <utility>
#include <string>
#include <iostream>

using namespace std;

class Config {
public:
    Config();
    Config(int size, int szEndLogico, int szMemFisica, int szMaxSecundaria, int szImgProcesso, string algorithm);

    int pageSize; // tamanho página/quadro
    int tamanhoEndLogico; //tamanho em bits endereço lógico
    // maxPagVirt = (1 << tamanhoEndLogico)/pageSize;

    // Tamanhos de memória 
    int tamMemFisica; 
    int tamMaxSecundaria;

    string algorithm; // algoritmo utilizado
};
