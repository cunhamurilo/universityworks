#include "ManipulaMemoria.hh"

// Gera uma string aleatória
string ManipulaMemoria::random_string(std::string::size_type length){
    static auto& chrs = "0123456789"
        "abcdefghijklmnopqrstuvwxyz";

    thread_local static std::mt19937 rg{std::random_device{}()};
    thread_local static std::uniform_int_distribution<std::string::size_type> pick(0, sizeof(chrs) - 2);

    std::string s;

    s.reserve(length);

    while(length--)
        s += chrs[pick(rg)];

    return s;
}

ManipulaMemoria::ManipulaMemoria(Config conf){
    config = conf;
    cPageFault = 0;
    
    // Limpando tabelas
    memoria.clear();
    virtMem.clear();
    virtTable.clear();
    psCount.clear();
    tamProcesso.clear();
}


long long ManipulaMemoria::addrToFrame(long long addr){
    return (long long)(addr/config.pageSize);
}


// Simula um acesso ao frame dado na memória real.
bool ManipulaMemoria::acessoReal(long long frame){
    cout << "\t Acesso à memória real, frame: " << frame << endl;
    if(frame >= config.tamMaxSecundaria/config.pageSize){
        cout << "\t\t |-> Acesso impossível, memória secundária excedida." << endl;
        return false;
    }
    return true;
}


// Converte um endereço de memória virtual de um processo em um frame de memória real.
long long ManipulaMemoria::virtToReal(pair<string, long long> frameVirt){
    cout << "\t " << frameVirt.first << ": Acesso na página virtual " << frameVirt.second << endl;

    if(virtTable.find(frameVirt) == virtTable.end()){
        // memória virtual não tem essa página mapeada na real
        // insere na memória real.
        memoria.push_back(random_string(10));
        cout << "\t Inseriu Página Virtual no frame real: " << memoria.size() << endl;
        virtTable[frameVirt] = memoria.size();
    }

    // se estiver, converte
    long long frameReal = virtTable[frameVirt];
    acessoReal(frameReal);
    return frameReal;
}


void ManipulaMemoria::removeVirtual(pair<string, long long> frame){
    psCount[frame.first]--; 

    cout << "\t Apagando da memória virtual: " << frame.first << ": " << frame.second << endl;

    if(config.algorithm == "LRU"){
        auto pos = find(virtMem.begin(), virtMem.end(), frame);
        virtMem.erase(pos);
    }
}

long long ManipulaMemoria::acessaVirtual(pair<string, long long> frame){
    bool onVirtual = checkVirtual(frame);
    if(onVirtual == true){
        cout << "\t Frame " << frame.first << ":" << frame.second << " está na memória virtual" << endl;
        removeVirtual(frame);
    }else{
        cout << "\t Page Fault " << frame.first << " - Frame " << frame.second << endl;
        cPageFault++;
    }

    // Checar se processo está no máximo
    if(psCount[frame.first] >= tamProcesso[frame.first]/config.pageSize){
        cout << "\t Tamanho do Processo Excedido, removendo uma página" << endl;
        if(config.algorithm == "LRU"){
            for(auto par : virtMem){
                if(par.first == frame.first){
                    removeVirtual(par);
                }
            }
        }
        else if(config.algorithm == "MRU"){
            for(unsigned int i = virtMem.size()-1; i >= 0; i--){
                if(virtMem[i].first == frame.first){
                    removeVirtual(virtMem[i]);
                }
            }
        }
    }

    // Checar se virtual está no maximo
    long long maxPagVirt = (1 << config.tamanhoEndLogico)/config.pageSize;
    if(virtMem.size() >= maxPagVirt){
        cout << "\t Tamanho da Memória Virtual Total Excedido" << endl;
        if(config.algorithm == "LRU"){
            removeVirtual(virtMem[0]);
        }else if(config.algorithm == "MRU"){
            removeVirtual(virtMem[virtMem.size()-1]); 
        }
    }

    // Inserir em si
    virtMem.push_back(frame);

    // Aumentar Contagem do processo
    psCount[frame.first]++;

    // Realizar acesso memória real
    int realFrame = virtToReal(frame);
    return realFrame;
}

bool ManipulaMemoria::checkVirtual(pair<string, long long> frame){
    return (find(virtMem.begin(), virtMem.end(), frame) != virtMem.end());
}