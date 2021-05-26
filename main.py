from math import floor

class no(object):
    def __init__(self, ordem) -> None:
        self.ordem = ordem
        self.filho = []
        self.chave = []
        self.pai = None
        self.folha = self.isFolha()

    
    # def __str__(self) -> str:
    #     chave = ' - '.join([chave for chave in self.chave])

    #     if(self.isFolha()):
    #         return f"Nó folha, chaves: {chave}"
    #     else:
    #         return f"Nó não folha, chaves: {chave}, tenho {len(self.filho)} filho(s)"

    """
        isFolha: Verifica se o nó é um nó folha ou não
    """
    def isFolha(self) -> bool:
        return len(self.filho) == 0

    """
        necessarioNovoNo: Verifica se a quantidade de chaves nesse nó já está cheia (Retorna true ou false)
    """
    def necessarioNovoNo(self) -> bool:
        return len(self.chaves) >= self.ordem

    """ buscarIndice: Retorna o índicie onde se encontra a chave no nó atual"""
    def buscarIndice(self, chave) -> int:
        i = 0
        while(i < len(self.chave) and self.chave[i] and self.chave[i] < chave):
            i += 1
        
        return i

    """ adicionaElemento: Adiciona uma chave no nó e retorna o seu indice """
    def adicionaElemento(self, chave) -> int:
        
        i = self.buscarIndice(chave)

        #verificar se não vai dar bosta
        aux = self.chave[:i]
        aux.append(chave)
        aux.extend(self.chave[i:])
        self.chave = aux
    
        return i
    
    """ full: Retorna se o nó está cheio, ou se ainda podemos inserir mais chaves """
    def full(self):
        return self.ordem <= len(self.chave)

    """ buscar: Busca o nó onde a chave se encontra a partir do no atual """
    def buscar(self, chave) -> tuple((object, int)) or None:
        i = 0
        #Percorremos todas as chaves do nó atual
        while (i < len(self.chave)):
            #caso tenhamos encontrado a chave atual, retornamos uma tupla com o nó atual e o índice encontrado
            if(self.chave[i] == chave):
                return (self, i)
            
            #Caso a chave esteja em um nó anterior
            elif(self.chave[i] > chave):
                
                #Caso o nó seja um nó folha não é possível retrocedermos para buscarmos a chave, logo esse elemento não existe
                if(self.isFolha()):
                    return None
                
                #iniciamos a busca no filho predecedente à chave atual
                return self.filho[i].buscar(chave)
            
            i += 1
        
        #caso tenha sido percorrido todos as chaves, buscamos no último filho disponível
        #que está posterior à chave atual 
        self.filho[i].buscar(chave)


    """ split: Faz o split do nó atual em dois, e vincula corretamente o novo filho """
    def split(self) -> None:
        #O meio do split equivale a (t / 2)+1
        middle = floor((self.ordem / 2) + 1)

        #Criamos um novo nó auxiliar para armazenar as chaves e filhos posteriores
        posteriores = no(self.ordem)
        posteriores.chave = self.chave[middle:]
        posteriores.filho = self.filho[middle:]
        for i in posteriores.filho:
            posteriores.filho[i].pai = self #atualizamos os novos filhos, setando o pai como o nó atual
        
        #removemos o resto dos filhos e chaves da lista
        self.filho = self.filho[:middle]
        self.chave = self.chave[:middle]

        #adicionamos o novo nó nos filhos e removemos a última chave
        self.filho.append(posteriores)
        self.chave.pop()

class ArvoreB(object):

    def __init__(self, ordem) -> None:
        self.ordem = ordem
        self.root = no(ordem)

    """ findInsert: Busca por um nó folha que pode ser inserido """
    def __findFolha(self, no, chave) -> no:
        if(no.isFolha()):
            return no
        
        i = no.buscarIndice(chave)

        return self.__findFolha(no.filho[i], chave)

    """ findChave: Busca por um valor específico na árvore """
    def findChave(self, chave):
        return self.root.buscar(chave)


    """ Insere uma chave na árvore, fazendo as tratativas devidas e retorna o nó de retorno"""
    def insert(self, chave) -> no:
        folha = self.__findFolha(self.root, chave)
        folha.adicionaElemento(chave)

        while(folha.full()):
            novo_no = folha.split()
            filho_removido = folha.filho.pop()

            if(folha.pai != None):
                folha = folha.pai
                indice_adicao = folha.adicionaElemento(novo_no)
                aux = folha.filho[:indice_adicao + 2]
                aux.append(filho_removido)
                aux = folha.filho[indice_adicao + 2:]
                folha.filho = aux
                filho_removido.pai = folha
            else:
                self.root = no(self.ordem)
                self.root.adicionaElemento(novo_no)
                self.root.filho.append(folha)
                self.root.filho.append(filho_removido)
                folha.pai = self.root
                folha = folha.pai
                filho_removido.pai = self.root

        return folha

def teste():
    arvore = ArvoreB(3)

    arvore.insert(2)
    arvore.insert(8)
    arvore.insert(6)
    arvore.insert(4)
    arvore.insert(15)

teste()