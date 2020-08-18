#!/bin/bash

## Compilando os 3 programas
echo "##################"
echo "# Compilando ... #"
echo "##################"
gcc Arquivos/Arquivos.c -o Arquivos/Arquivos
gcc Memoria/Memoria.c -o Memoria/Memoria
gcc Processos/Processos.c -o Processos/Processos

# Rodando Strace
echo "    ###################"
echo "    # Strace Arquivos #"
echo "    ###################"
cd Arquivos
strace -c ./Arquivos
cd ..

echo "    ##################"
echo "    # Strace Memoria #"
echo "    ##################"
strace -c ./Memoria/Memoria

echo "    ####################"
echo "    # Strace Processos #"
echo "    ####################"
strace -c ./Processos/Processos

echo "    Tempo Arquivos"
cd Arquivos
/usr/bin/time -f "Tempo total: %e
Percentual de uso de CPU: %P
Tempo em modo de Kernel: %S
Tempo em modo de usuário: %U
Trocas de contexto involuntárias: %c
Trocas de contexto voluntárias: %w" ./Arquivos
cd ..

echo "    Tempo Memoria"
/usr/bin/time -f "Tempo total: %e
Percentual de uso de CPU: %P
Tempo em modo de Kernel: %S
Tempo em modo de usuário: %U
Trocas de contexto involuntárias: %c
Trocas de contexto voluntárias: %w" ./Memoria/Memoria

echo "    Tempo Processos"
/usr/bin/time -f "Tempo total: %e
Percentual de uso de CPU: %P
Tempo em modo de Kernel: %S
Tempo em modo de usuário: %U
Trocas de contexto involuntárias: %c
Trocas de contexto voluntárias: %w" ./Processos/Processos

