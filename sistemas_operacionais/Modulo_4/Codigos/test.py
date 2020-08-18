import os
import statistics as stat
import matplotlib.pyplot as plt

def media(lista):
    return sum(lista)/len(lista)

sizes = ['5kb', '10kb', '100kb', '1mb', '10mb', '100mb', '500mb']
Cavgs = []
Lavgs = []
Exavgs = []
Cstdev = []
Lstdev = []
Exstdev = []

for tamanho in sizes:
    Cclocks = []
    Ctimes = []
    Lclocks = []
    Ltimes = []
    Exclocks = []
    Extimes = []

    for it in range(0, 10):
        inputstr = "./criacao_arquivos " + tamanho + " 1> output 2>/dev/null" 
        os.system(inputstr)
        f = open("output")
        currClock = float(f.readline().strip('\n').split(' ').pop())
        currTime = float(f.readline().strip('\n').split(' ').pop())
        Cclocks.append(currClock)
        Ctimes.append(currTime)
        f.close()

        inputstr = "./leitura_arquivos " + tamanho + " 1> output 2>/dev/null"
        os.system(inputstr)
        f = open("output")
        currClock = float(f.readline().strip('\n').split(' ').pop())
        currTime = float(f.readline().strip('\n').split(' ').pop())
        Lclocks.append(currClock)
        Ltimes.append(currTime)
        f.close()

        inputstr = "./exclusao_arquivos " + tamanho + " 1> output 2>/dev/null"
        os.system(inputstr)
        f = open("output")
        currClock = float(f.readline().strip('\n').split(' ').pop())
        currTime = float(f.readline().strip('\n').split(' ').pop())
        Exclocks.append(currClock)
        Extimes.append(currTime)
        f.close()

    print("\n\nTamanho", tamanho)
    print("Criacao\n Tempo medio: ", media(Ctimes))
    print(" Desvio Padrao: ", stat.stdev(Ctimes))
    print("Leitura\n Tempo medio: ", media(Ltimes))
    print(" Desvio Padrao: ", stat.stdev(Ltimes))
    print("Exclusao\n Tempo medio: ", media(Extimes))
    print(" Desvio Padrao: ", stat.stdev(Extimes))
    Cavgs.append(media(Ctimes))
    Cstdev.append(stat.stdev(Ctimes))
    Lavgs.append(media(Ltimes))
    Lstdev.append(stat.stdev(Ltimes))
    Exavgs.append(media(Extimes))
    Exstdev.append(stat.stdev(Extimes))

plt.errorbar(sizes, Cavgs, Cstdev, fmt='-o', label='Criação')
plt.errorbar(sizes, Lavgs, Lstdev, fmt='-o', label='Leitura')
plt.errorbar(sizes, Exavgs, Exstdev, fmt='-o', label='Exclusão')
plt.xlabel('Tamanho do arquivo')
plt.ylabel('Tempo (s)')
plt.legend()
plt.savefig('Graficos.png')
plt.title("Comparativo entre manipulações - NTFS")

print(Cavgs, Cstdev)
print(Lavgs, Lstdev)
print(Exavgs, Exstdev)





