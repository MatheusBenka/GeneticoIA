import random as rnd
from PIL import Image
from numpy import random as rnd
import copy
import matplotlib.pyplot as plt
import sys
import time

class auxCriacaoGene(object):
    def __init__(self):
        self.fitness = 0
        # [cima, direita, baixo, esquerda,tipo,visitado]
        self.geneUm = [1, 0, 0, 0, 0, False]
        self.geneDois = [1, 1, 0, 0, 4, False]
        self.geneTres = [1, 1, 1, 0, 8,False]
        self.geneQuatro = [1, 1, 1, 1, 12,False]
        self.geneCinco = [1, 0, 1, 0, 13,False]
        #lista com todos tipos de pecas
        self.lista = [self.geneUm, self.geneDois, self.geneTres, self.geneQuatro, self.geneCinco]

    def rodar(self, gene, graus):
        if gene[4] != 12:# se peca for toda aberta, pula
            auxIndice = 0 #auxilia no nome da peca
            while graus > 0: #enquanto nao girar tds graus sorteados
                gene[0], gene[3], gene[2], gene[1] = gene[1], gene[0], gene[3], gene[2]
                graus = graus - 90
                auxIndice += 1 #aumenta auxiliar para nome da peca a cada 90 graus girados
            # muda o nome da peca para mais a qtd d vezes (90 graus) q ela girou
            gene[4] = int(gene[4]) + int(auxIndice)
            if gene[4] == 13 and auxIndice % 2 != 0: # se for a 13, vira 14 se girou vezes impar
                gene[4] == 14

    def gerar(self):
        indice = [0, 1, 2, 3] # nomes de pecas possiveis
        novo = copy.deepcopy(self.lista[rnd.choice(indice)]) # escolhe uma aleatoria
        graus = [0, 90, 180, 270]
        graus = rnd.choice(graus) # escolhe graus aleatorios
        self.rodar(novo, graus) # roda peca geradas
        return copy.deepcopy(novo) # retorna peca gerada

    def matriz(self,n_linhas, n_colunas):
        matriz = []
        linha = []

        while len(matriz) != n_linhas:
            n = self.gerar()
            linha.append(n)

            if len(linha) == n_colunas:
                matriz.append(linha)
                linha = []
        return matriz # retorna matriz de pecas geradas

    def fecharLados(self,individuo):
        #fecha parte de cima das pecas do labirinto na primeira linha
        for i in range(0, 40):
            individuo.labirinto[0][i][0] = 0
        # fecha parte de cima das pecas do labirinto na ultima linha
        for i in range(0, 40):
            individuo.labirinto[39][i][2] = 0
        # fecha parte da esquerda das pecas do labirinto na primeira coluna
        for i in range(1, 40):
            individuo.labirinto[i][0][3] = 0
        # fecha parte da esquerda das pecas do labirinto na ultima coluna
        for i in range(0, 39):
            individuo.labirinto[i][39][1] = 0

    def gerarPopulacao(self):
        populacao = [] # nova populacao
        for i in range(0,100):# numero de individuo da populacao
            novo = individuo() # novo individuo
            novo.fitness = self.calcFitnessCaminhosCima(novo) + self.calcularFitnessBaixo(novo) # calcula fitness do novo
            populacao.append(copy.deepcopy(novo)) #adiciona a populacao
        return populacao # retorna populacao gerada

    def limparDescobertas(self,individuo):
        for i in range(0,individuo.linhas):
            for j in range(0, individuo.colunas):
                individuo.labirinto[i][j][5] = False

    # funcao para primeira chamada
    def calcFitnessCaminhosCima(self, individuo):#algoritmo para calcular os caminhos do labirinto
        #self.telinha(individuo.labirinto,'testes')
        maiorCaminhoDireita = 0
        maiorCaminhoBaixo = 0
        if individuo.labirinto[0][0][3] == 1: #entrada aberta na entrada do labirinto
            maiorCaminhoDireita = 1
            maiorCaminhoBaixo = 1
            ## mudar linha e coluna para nove para testes
            individuo.labirinto[0][0][5] = True #marca como visitado
            if individuo.labirinto[0][0][1] == 1: #se a saida da direita estiver aberda
                maiorCaminhoDireita = maiorCaminhoDireita + self.buscaProfundidade(individuo.labirinto, 0, 1, 3, individuo.labirinto[0][1][4])
            if individuo.labirinto[0][0][2] == 1: # se a saida para baixo estiver aberta
                maiorCaminhoBaixo = maiorCaminhoBaixo + self.buscaProfundidade(individuo.labirinto, 1, 0, 0,individuo.labirinto[1][0][4])
        else:
            return 0

        if individuo.labirinto[39][39][5] is True: #se apos a busca visitou a ultima peca == percorreu o percurso
            individuo.caminhoValido = True #marca como tem caminho valido
        self.limparDescobertas(individuo)
        if maiorCaminhoBaixo > maiorCaminhoDireita:
            return copy.deepcopy(maiorCaminhoBaixo)
        else:
            return copy.deepcopy(maiorCaminhoDireita)

    def calcularFitnessBaixo(self,individuo):
        maiorCaminhoEsquerda = 0
        maiorCaminhoCima = 0
        if individuo.labirinto[39][39][1] == 1:  # saida aberta na saida do labirinto
            maiorCaminhoEsquerda = 1
            maiorCaminhoCima = 1
            ## mudar linha e coluna para nove para testes
            individuo.labirinto[39][39][5] = True  # marca como visitado
            if individuo.labirinto[39][39][3] == 1:  # se a saida da esquerda estiver aberda
                maiorCaminhoEsquerda = maiorCaminhoEsquerda + self.buscaProfundidade(individuo.labirinto, 39, 38, 1,individuo.labirinto[39][38][4])
            if individuo.labirinto[39][39][0] == 1:  # se a saida para cima estiver aberta
                maiorCaminhoCima = maiorCaminhoCima + self.buscaProfundidade(individuo.labirinto, 38, 39, 2, individuo.labirinto[38][39][4])
        else:
            return 0

        if individuo.labirinto[0][0][5] is True:  # se apos a busca visitou a ultima peca == percorreu o percurso
            individuo.caminhoValido = True  # marca como tem caminho valido
        self.limparDescobertas(individuo)
        if maiorCaminhoCima > maiorCaminhoEsquerda:
            return copy.deepcopy(maiorCaminhoCima)
        else:
            return copy.deepcopy(maiorCaminhoEsquerda)

    def buscaProfundidade(self,labirinto,linha,coluna,entrada,tipo):
        valorCaminho = 0
        valorCaminhoDireita = 0
        valorCaminhoBaixo = 0
        valorCaminhoCima = 0
        valorCaminhoEsquerda = 0
        if labirinto[linha][coluna][entrada] == 1: # se tiver entrada por onde a peca anterior saiu
            valorCaminhoDireita = 2
            valorCaminhoBaixo = 2
            valorCaminhoCima = 2
            valorCaminhoEsquerda = 2
            if tipo == 12:
                valorCaminhoDireita = 0.5
                valorCaminhoBaixo = 0.5
                valorCaminhoCima = 0.5
                valorCaminhoEsquerda = 0.5
            if tipo >= 8 and tipo <= 11:
                valorCaminhoDireita = 1
                valorCaminhoBaixo = 1
                valorCaminhoCima = 1
                valorCaminhoEsquerda = 1
            if tipo >=0 and tipo <=3:
                valorCaminhoDireita = 0.5
                valorCaminhoBaixo = 0.5
                valorCaminhoCima = 0.5
                valorCaminhoEsquerda = 0.5
            if linha in range(0, 40) and coluna in range(0, 40):
                if labirinto[linha][coluna][5] is False: # nao foi visitado
                    labirinto[linha][coluna][5] = True  #marca como visitado
                    if labirinto[linha][coluna][0] == 1 and linha-1 > 0:  # se estiver aberto a face de cima da peca
                        if labirinto[linha-1][coluna][5] is False: #se peca a cima nao foi visitada
                            valorCaminhoCima = valorCaminhoCima + self.buscaProfundidade(labirinto,linha-1,coluna,2,labirinto[linha-1][coluna][4]) #visitar

                    if labirinto[linha][coluna][1] == 1 and coluna +1 < 40:  # se estiver aberto a face da direita da peca
                        if labirinto[linha][coluna+1][5] is False:#se peca a direita nao foi visitada
                             valorCaminhoDireita = valorCaminhoDireita + self.buscaProfundidade(labirinto, linha, coluna+1,3,labirinto[linha][coluna+1][4])

                    if labirinto[linha][coluna][2] == 1 and linha+1 < 40:  # se estiver aberto a face de baixo da peca
                        if labirinto[linha+1][coluna][5] is False:#se peca a baixo nao foi visitada
                            valorCaminhoBaixo = valorCaminhoBaixo + self.buscaProfundidade(labirinto, linha+1, coluna,0,labirinto[linha+1][coluna][4])

                    if labirinto[linha][coluna][3] == 1 and coluna-1 > 0:  # se estiver aberto a face da esquerda da peca
                        if labirinto[linha][coluna-1][5] is False:#se peca a esquerda nao foi visitada
                            valorCaminhoEsquerda = valorCaminhoEsquerda + self.buscaProfundidade(labirinto, linha, coluna-1,1,labirinto[linha][coluna-1][4])

        return max(valorCaminhoCima,valorCaminhoBaixo,valorCaminhoDireita,valorCaminhoEsquerda)


    def telinha(self,labirinto,nomeImage):
        image = Image.open('novoFundo.png')
        for i in range (0,40):
            LINHAFundo = i * 100
            LINHAImagem = (i+1)*100
            for j in range (0,40):
                COLUNAFundo = j * 100
                COLUNAImagem = (j+1)*100
                area = (COLUNAFundo, LINHAFundo, COLUNAImagem, LINHAImagem)
                #area = (cantoCima,cantoBaixo, (i+2)* xImagem, (i+2)* yImagem)
                imageAppend = Image.open('tile' + str(labirinto[i][j][4]) + '.png')
                image.paste(imageAppend, area)
        image.save("saidas/"+str(nomeImage)+".png")
        image.close()



class individuo(object):

    def __init__(self):
        aux = auxCriacaoGene()
        self.caminhoValido = False
        self.colunas = 40
        self.linhas = 40
        self.labirinto = aux.matriz(self.colunas, self.linhas)
        self.labirinto[0][0][0] = 0 # fechada parte de cima da primeira peca
        aux.fecharLados(self)
        self.pais = []
        self.fitness = 0
        self.taxaMutacao = 0.1

    def __len__(self):
        return len(self.labirinto)

    def printar(self,nome):
        arq = open("saida"+str(nome)+".txt", "w")
        for i in range(0, self.colunas):
            for j in range(0, self.linhas):                
                if self.labirinto[i][j][4] < 10:
                    arq.write(' '+str(self.labirinto[i][j][4]))
                else:
                    arq.write(str(self.labirinto[i][j][4]))
                arq.write('|')
        #   print('\n')
            arq.write('\n')
        arq.close()

class ambiente(object):

    def __init__(self):
        self.aux = auxCriacaoGene()
        self.populacao = self.aux.gerarPopulacao()
        self.geracao = 0
        self.melhor = self.populacao[rnd.randint(0, len(self.populacao))]
        self.iteracaoSemMelhora = 0
        self.fitness = 0
        self.taxaCruzamento = 0.2
        self.taxaMutacao = 0.02
        self.pai1 = ''
        self.pai2 = ''
        self.listaFitnessPop = []
        self.listaFitnessIndividuos = []
        self.listaGeracoes = []


    def cruzamento(self):
        novosIndividuos = [] # lista com novos individuos
        qtdCruzamentos = len(self.populacao) * self.taxaCruzamento # qtd de cruzamentos baseado na taxa
        retirar = copy.deepcopy(qtdCruzamentos) # aux para retiradas da qtd de gerados
        while qtdCruzamentos > 0:
            self.pai1 = self.selecao() # seleciona pais
            self.pai2 = self.selecao() # seleciona pais
            pontoCorteLinha = rnd.randint(0,40) #seleciona ponto de corte aleatorio
            #pontoCorteColuna = rnd.randint(0,40) #seleciona ponto de corte aleatorio
            filho1 = individuo() # gera novo individuo
            filho2 = individuo() # gera novo individuo
            for i in range(0, pontoCorteLinha):
                for j in range(0,len(filho1)):
                    filho1.labirinto[i][j] = self.pai1.labirinto[i][j]
                    filho2.labirinto[i][j] = self.pai2.labirinto[i][j]
            for i in range(pontoCorteLinha, len(filho1)):
                for j in range(0,len(filho1)):
                    filho1.labirinto[i][j] = self.pai2.labirinto[i][j]
                    filho2.labirinto[i][j] = self.pai1.labirinto[i][j]

            self.mutacao(filho1)
            self.mutacao(filho2)

            # calcula fitness dos filhos gerados pelo cruzamento
            filho1.fitness = self.aux.calcFitnessCaminhosCima(filho1) + self.aux.calcularFitnessBaixo(filho1)
            filho2.fitness = self.aux.calcFitnessCaminhosCima(filho2) + self.aux.calcularFitnessBaixo(filho2)
            # add na lista de novos individuos da populacao
            novosIndividuos.append(copy.deepcopy(filho1))
            novosIndividuos.append(copy.deepcopy(filho2))
            qtdCruzamentos -= 1



        for i in novosIndividuos:
            self.populacao.append(copy.deepcopy(i))
        # limpa lista
        novosIndividuos.clear()
        # retira da populacao a msm quantidade de filhos gerados
        self.limparMenosAptos(retirar*2)
        self.listaFitnessPop.append(self.mediaPop())

    def mediaPop(self):
        media = 0
        for i in range (0,len(self.populacao)):
            media += self.populacao[i].fitness
        print("Media Pop {}".format(media/len(self.populacao)))
        return media/len(self.populacao)

    def mutacao(self,novo):
        mutacoes = self.taxaMutacao * (len(novo.labirinto)*2)
        # gera mutacoes
        while mutacoes > 0:
            linha = rnd.randint(0, 40)
            coluna = rnd.randint(0, 40)
            novoGene = self.aux.gerar()

            #fechar lados para mutacao
            if linha == 0 and coluna != 0:
                novoGene[0] = 0
            elif linha == 39 and coluna != 39:
                novoGene[2] = 0
            elif coluna == 0 and linha != 0:
                novoGene[3] = 0
            elif coluna == 39 and linha != 39:
                novoGene[1] = 0
            # individuo aleatorio, e indices aleatorios
            novo.labirinto[linha][coluna] = novoGene
            mutacoes -= 1

    def selecao(self):
        fitness = lambda populacao:populacao.fitness
        self.populacao.sort(key=fitness, reverse=True)
        candidato1 = rnd.choice(self.populacao)
        candidato2 = rnd.choice(self.populacao)
        if candidato1.fitness > candidato2.fitness: # sorteio
            return candidato1
        else:
            return candidato2

    def limparMenosAptos(self,qtdRetirar):
        qtdRetirar = int(qtdRetirar)
        fitness = lambda populacao: populacao.fitness
        # ordena por maior fitness
        self.populacao.sort(key=fitness, reverse=True)
        # retira da populacao os piores
        self.populacao = self.populacao[:-qtdRetirar]

    def mostrarResultados(self):
        print('fitness do melhor = '+str(self.melhor.fitness))
        print('num geracao = '+str(self.geracao))


    def rodar(self, maximoSemMelhora):
        self.geracao = 0
        while self.iteracaoSemMelhora < maximoSemMelhora :
            #if self.populacao[0].caminhoValido is False: #DESCOMENTAR PARA PARAR QUANDO HOUVER UM CAMINHO VALIDO
                self.cruzamento()
                if self.populacao[0].fitness > self.melhor.fitness:
                    self.melhor = copy.deepcopy(self.populacao[0])
                    self.iteracaoSemMelhora = 0
                    self.fitness = self.melhor.fitness
                    # IMPRIMIR O LABIRINTO EM UMA IMAGEM QUANDO HOUVER MELHORA
					#self.aux.telinha(self.melhor.labirinto, str(self.melhor.fitness))
                else:
                    self.iteracaoSemMelhora += 1
                self.geracao += 1
                self.listaGeracoes.append(self.geracao)
                self.listaFitnessIndividuos.append(self.melhor.fitness)
                self.mostrarResultados()
            #else:
            #    break
        self.aux.telinha(self.populacao[0].labirinto,'ficoAssim')
        plt.xlabel('Geracoes')
        plt.ylabel('Fitness Pop(Verm)/Ind(Azul)')
        plt.plot(self.listaGeracoes, self.listaFitnessPop, linestyle='--', color='r', marker='s',
                 linewidth=3.0)
        plt.plot(self.listaGeracoes, self.listaFitnessIndividuos, linestyle='-', color='b', marker='s',
                 linewidth=2.0)

        plt.axis([0, len(self.listaGeracoes)*1.2, 0, max(self.listaFitnessIndividuos)*1.2])
        plt.show()
        #plt.savefig("saidas/grafiquinho.png")




novoAmbiente = ambiente()
inicio = time.time()
novoAmbiente.rodar(100)
fim = time.time()
print("tempo de execucao : {}".format((fim - inicio)/60))
