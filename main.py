#Eletric GYM Puzzle - @augustovmedeiros
#Projeto feito para melhorar a ideia do meu amigo https://github.com/ntn-ss/Pokemon-Electric-Gym
from random import randint

class Lixeira(): #Definimos a lixeira como um objetos
    def __init__(self):#Inicializamos o objeto da lixeira dando algumas caracteristicas a ele.
        self.isFirst = False#Definindo alguns estados iniciais importantes.
        self.isSecond = False
        self.modo = None
    def setFirst(self):#Definimos as funções de setar no objeto.
        self.isFirst = True
    def setSecond(self):
        self.isSecond = True
    def setModo(self, modo):
        self.modo = modo
    def checkFirst(self):#Definimos as funções de checar no objeto.
        return self.isFirst
    def checkSecond(self):
        return self.isSecond
    def checkModo(self):
        return self.modo
    def render(self):#Receber o emoji a ser printado pelo script.
        if(self.modo == "certo"):
            return " O "
        elif(self.modo == "errado"):
            return " X "
        else:
            return "🗑️ "
        
        
def getLixeiraAdjacente(num, lixeiraColuna, qtdLixeiras): #Escolhendo um numero para ser nossa segunda lixeira.
    lixeirasAdj = []#Lista de lixeiras adjacentes
    num += 1#Para termos exatamente qual a mesa e não o indice da lista.
    lixeirasAdj.append(int(num - lixeiraColuna))#Lixeira de cima
    esquerdaInvalida = []#Guardar numeros em que os lados não são validos.
    direitaInvalida = []
    for x in range(int(qtdLixeiras/lixeiraColuna)):
        esquerdaInvalida.append(int(lixeiraColuna*(x)))
        direitaInvalida.append(int(lixeiraColuna*(x+1))+1)
    esquerda = int(num - 1)
    direita = int(num + 1)
    if(esquerda not in esquerdaInvalida):#Verificar os lados.
        lixeirasAdj.append(esquerda)#Lixeira da esquerda
    if(direita not in direitaInvalida):
        lixeirasAdj.append(direita)#Lixeira da direita
    lixeirasAdj.append(int(num + lixeiraColuna))#Lixeira de baixo
    lixeirasRemovidas = 0#Para manter o contador do laço repeticional precisamos saber quantas lixeiras já foram removidas.
    for lixeira in range(len(lixeirasAdj)):#Iremos itinerar pelas lixeiras para verificar se todas existem.
        lixeiraVal = lixeirasAdj[lixeira-lixeirasRemovidas]
        if(lixeiraVal < 0 or lixeiraVal > qtdLixeiras):#Se a lixeira for menor que 0 ou maior que as lixeiras, não existe.
            lixeirasAdj.pop(lixeira-lixeirasRemovidas)#Removemos ela da lista.
            lixeirasRemovidas += 1#Adicionamos ao contador de lixeiras removidas.

    lixeiraEscolhida = randint(0, len(lixeirasAdj)-1)#Escolher uma lixeira com randint.
    return lixeirasAdj[lixeiraEscolhida]-1, lixeirasAdj#Retornamos uma lixeira aleatoria da lista e removemos um para ser um indice.
    #Também retornamos a lista de opções possiveis para o jogador.

def renderizarJogo(lixeiras, lixeiraColuna):
    contador = 1 #Contando pra fazer a quebra de coluna do jogo.
    for lixeira in lixeiras:
        print(lixeira.render(), end="")
        if(contador % lixeiraColuna == 0):
            print("")
        contador += 1

def palpite(lixeira, primeira=False):#Função para receber o palpite e verificar se a primeira ou segunda lixeira.
    if(primeira):
        if(lixeira.checkFirst()):#Verificamos se esta é a primeira lixeira.
            lixeira.setModo("certo")#Atualizamos o modo de renderização.
            return True#Retornamos o palpite como Verdadeiro.
        else:
            lixeira.setModo("errado")
            return False
    else:
        if(lixeira.checkSecond()):#Verificamos se esta é a segunda lixeira.
            lixeira.setModo("certo")
            return True
        else:
            lixeira.setModo("errado")
            return False

def gerarPartida(qtdLixeiras=15, colunas=3):
    lixeiras = []#Definimos a lista das lixeiras que iremos usar na partida.
    lixeiraColuna = qtdLixeiras/colunas#Calculamos o numero de lixeiras por coluna.

    for x in range(qtdLixeiras):#Com esse laço repeticional para gerar uma lixeira (objeto) para quantidade necessaria.
        lixeiras.append(Lixeira())#Adicionando a lista.
    
    numPrimaria = randint(0,qtdLixeiras-1)
    lixeiraPrimaria = lixeiras[numPrimaria]#Escolhendo lixeira primaria.
    lixeiraPrimaria.setFirst()
    lixeirasAdj = getLixeiraAdjacente(numPrimaria, lixeiraColuna, qtdLixeiras)#Recebendo informações da lixeiras adjacentes.
    numSecundaria = lixeirasAdj[0]#Escolhendo lixeira secundaria.
    lixeiraSecundaria = lixeiras[numSecundaria]
    lixeiraSecundaria.setSecond()

    encontradoPrimeiro = False
    while(encontradoPrimeiro != True):#Laço pra manter o jogo rodando até encontrar primeira lixeira.
        renderizarJogo(lixeiras, lixeiraColuna)
        numJogador = int(input("Digite o número da primeira lixeira: "))
        encontradoPrimeiro = palpite(lixeiras[numJogador-1], True)#Atualizar estado do jogo apartir do palpite.

    for lixeira in lixeiras:#Limpar o jogo para a procura da segunda lixeira.
        if(lixeira.checkModo() == "errado"):
            lixeira.setModo(None)
    
    #Procura da segunda lixeira sem repetição para garantir apenas uma chance ao jogador de acertar.
    renderizarJogo(lixeiras, lixeiraColuna)
    numJogador = int(input(f"Digite o número da segunda lixeira {lixeirasAdj[1]}: "))
    encontradoSegundo = palpite(lixeiras[numJogador-1])
    renderizarJogo(lixeiras, lixeiraColuna)
    if(encontradoSegundo == True):
        print("Correto.")
        return True
    else:
        print("Errado. Tente Novamente!")
        return False

jogando = False#Manter jogo em loop até o jogador encontrar as duas lixeiras.
while(jogando != True):
    jogando = gerarPartida()