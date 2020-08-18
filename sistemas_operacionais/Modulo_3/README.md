# Relatório Módulo 3

Para este módulo foi desenvolvido um simulador de gerenciamento de memória virtual com paginação. Para isso foram tomadas como base instruções de escrita/leitura em uma posição de memória, criação de um processo de tamanho especificado e operações de CPU e I/O, que também foram mapeadas na memória.


# Instruções Para a Execução dos Códigos

Foi criado um arquivo `Makefile`, que se encontra na pasta [simulador](./simulador/). Para compilar o programa basta utilizar o comando `Make` nesta mesma pasta, o que gerará um arquivo binário também de nome `simulador`.

Para executar o programa, é possível utilizar um arquivo de entrada como argumento:

```bash
./simulador arquivo_teste.txt
```

Durante a execução são impressas na tela do usuário as manipulações feitas referentes tanto à memória virtual quanto à memória real simuladas.


# Arquitetura do Código

## A tradução de endereços

Como no arquivo de entrada são dados endereços, é necessário que estes sejam traduzidos para páginas de memória. Então isso é calculado com base no tamanho de página e então inserido na respectiva página da memória virtual.

Com relação à memória real, as páginas são criadas e inseridas sequencialmente no caso de que uma página de memória virtual não tivesse sido mapeada anteriormente. Caso contrário o acesso é direto.

### CPU e I/O Bound

Para operações do tipo CPU e I/O bound foram utilizado o bit mais significativo e o segundo bit mais significativo para indicar o mapeamento de páginas para esses tipos de operações na memória virtual. Por conta dessa decisão de design, cada uma dessas operações possui uma região específica para si na memória virtual, que não será utilizada por outras operações de memória.

## Estruturas de Dados para a Memória

Para que o projeto se assimilasse à realidade, foram utilizadas algumas estruturas de dados da biblioteca STL da linguagem C++. 

As memórias virtual e real foram representadas com a estrutura `vector` do C++, devido ao seu comportamento sequencial. Essa estrutura foi escolhida também pois facilita manipulações do tipo inserção e remoção tanto no início/fim da memória como em posições intermediárias com complexidade amortizada em O(1).

No caso da memória virtual, foi necessário utilizar um vetor de `pair`, dado que esta é simulada a ser única para cada processo, então formando um par `<pid, página de memória>.`

Foi utilizada uma tabela de memória virtual para a memória real, traduzindo as informações da memória virtual para o seu respectivo frame na memória real. Isso foi feito utilizando a estrutura de dados `map`, que realiza acessos em O(1) amortizado e modificações em O(log(n)).

Também, devido às limitações impostas de um número máximo de páginas de memória mapeadas simultaneamente de um processo e ao tamanho máximo de memória de um procesos, foram criadas duas tabelas (utilizando map) para manter e controlar essas condições.

## Configuração

Conforme solicitado pela especificação, os parâmetros do simulador podem ser customizados na classe de configuração (Config.cpp), ou pode ser também criada uma nova classe de configuração com base no construtor especificado nesse mesmo arquivo.