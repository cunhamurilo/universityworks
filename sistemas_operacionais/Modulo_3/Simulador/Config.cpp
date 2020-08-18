#include "Config.hh"

Config::Config(){
    pageSize = 64; // tamanho página/quadro
    tamanhoEndLogico = 8; //tamanho em bits endereço lógico

    // Tamanhos de memória (em quantidade de páginas)
    tamMemFisica = 2048; 
    tamMaxSecundaria = 4096;

    algorithm = "LRU"; // algoritmo utilizado
    // algorithm = "MRU"; // descomentar caso queira utilizar MRU
    return;    
}
    
Config::Config(int size, int szEndLogico, int szMemFisica, int szMaxSecundaria, int szImgProcesso, string algorithm){
    pageSize = size; // tamanho página/quadro
    tamanhoEndLogico = szEndLogico; //tamanho em bits endereço lógico
    if(tamanhoEndLogico > 62){
        cout << "Tamanho do endereço lógico muito grande." << endl;
        cout << "O máximo suportado é 62 bits." << endl;
        abort();
    }

    // Tamanhos de memória (em quantidade de páginas)
    tamMemFisica = szMemFisica; 
    tamMaxSecundaria = szMaxSecundaria;

    algorithm = algorithm; // algoritmo utilizado
    return;    
}
