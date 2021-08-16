'''
INF01048 Inteligencia Artificial (2021/1) - UFRGS
Professor Anderson Rocha Tavares
TRABALHO 1 - Busca em Grafos
Autores:
    Eduardo Eugenio Kussler
    Gabriel Couto Domingues
    Thiago Sotoriva Lermen
'''

import queue
from dataclasses import dataclass, field
from typing import Any


class Nodo:
    '''Classe que representa um nodo no grafo.'''
    
    def __init__(self, estado, pai, acao, custo):
        self.estado = estado    # estado atual do 8-puzzle
        self.pai = pai          # nodo pai do estado atual
        self.acao = acao        # acao tomada anteriormente para 
                                # atingir o estado atual
        self.custo = custo      # custo do caminho do estado inicial 
                                # ate o no atual (custo pai + 1)
    
    def __str__(self):
        pai = self.pai.estado if self.pai is not None else None
        return "estado: " + str(self.estado) + ", pai: " + str(pai)  + ", acao: " + str(self.acao) + ", custo: " + str(self.custo)

@dataclass(order=True)
class NodoHeuristica:
    '''Classe que representa uma tupla com um nodo e sua prioridade.'''
    priority: int
    item: Any=field(compare=False)

class PriorityQueueAstar(queue.PriorityQueue):
    '''Classe para a fila de prioridade para o algoritmo A*.'''
    def __init__(self, heuristica):
        super().__init__()
        self.heuristica = heuristica

    def put(self, val):
        super().put(NodoHeuristica(priority=self.heuristica(val.estado) + val.custo, item = val))

    def get(self):
        return super().get().item

class SetNodos(set):
    '''Classe para um conjunto de nodos.'''
    def add(self, item):
        super().add(item)

class ListNodos(list):
    '''Classe para uma lista de nodos.'''
    def add(self, item):
        self.append(item)
    


def sucessor(estado: str):
    ''' Recebe um estado e retorna uma lista de tuplas (acao, estado atingido). '''
    espaco_vazio = estado.find('_')
    len_estado = 9 
    lst = []

    if espaco_vazio not in [0,3,6]: # esquerda
        index = espaco_vazio - 1
        lst.append(("esquerda", troca_pecas(estado, index, espaco_vazio)))
    if espaco_vazio not in [2,5,8]: # direita
        index = espaco_vazio + 1
        lst.append(("direita", troca_pecas(estado, index, espaco_vazio)))
    if espaco_vazio - 3 >= 0 : # acima
        index = espaco_vazio - 3
        lst.append(("acima", troca_pecas(estado, index, espaco_vazio)))
    if espaco_vazio + 3 < len_estado: # abaixo
        index = espaco_vazio + 3
        lst.append(("abaixo", troca_pecas(estado, index, espaco_vazio)))
    
    return lst

def troca_pecas(estado, index_1, index_2):
    '''Dado um estado e dois indices, troca as peças.'''
    estado_lst = list(estado)
    estado_lst[index_1], estado_lst[index_2] = estado_lst[index_2], estado_lst[index_1]
    return "".join(estado_lst)

def expande(nodo: Nodo):
    ''' Expande um nodo, retornando os nodos sucessores do nodo passado como argumento.'''
    sucessores = sucessor(nodo.estado)
    lst_sucessores = []

    for suc in sucessores:
        nodo_sucessor = Nodo(suc[1], nodo, suc[0], nodo.custo + 1)
        lst_sucessores.append(nodo_sucessor)
        
    return lst_sucessores

class ErroBusca(Exception):
    '''Exceção para erro na busca'''
    pass

def busca_grafo(start, construtor_fronteira, construtor_expandidos):
    '''Realiza a busca no grafo.'''
    if not solucionavel(start):
        return None 

    X = construtor_expandidos()
    F = construtor_fronteira()
    F.put(Nodo(start, None, None, 0))
    
    while not F.empty():
        v = F.get()

        if estado_objetivo(v.estado):
            return caminho(v)
        if v.estado not in X:
            X.add(v.estado)
            fronteira_v = expande(v)
            for nodo_de_fronteira in fronteira_v:
                F.put(nodo_de_fronteira)
    
    raise ErroBusca("Não encontrou estado final")

def solucionavel(estado):
    '''Verifica se o 8 puzzle tem solução.'''
    estado_lst = [int(char) if char != '_' else 0 for char in estado]

    inversoes = 0
    for i in range(9):
        for j in range(i+1,9):
            if estado_lst[j] != 0 and estado_lst[i] > estado_lst[j]:
                inversoes += 1

    return inversoes % 2 == 0

def estado_objetivo(v):
    '''Verifica se o estado final foi atingido.'''
    return v == "12345678_"

def caminho(end):
    '''Retorna o caminho até o nodo atual.'''
    caminho = []
    caminho.append(end.acao)
    curr = end.pai

    while curr is not None:
        caminho.append(curr.acao)
        curr = curr.pai

    del caminho[-1]
    caminho.reverse()
    return caminho

def bfs(estado):
    '''Executa o BFS.'''
    return busca_grafo(estado, queue.Queue, SetNodos)

def dfs(estado):
    '''Executa o DFS.'''
    return busca_grafo(estado, queue.LifoQueue, SetNodos)

def astar_hamming(estado):
    '''Executa o A* com a heuristica hamming.'''
    return busca_grafo(estado, lambda : PriorityQueueAstar(hamming), ListNodos)

def astar_manhattan(estado):   
    '''Executa o A* com a heuristica manhattan.'''
    return busca_grafo(estado, lambda : PriorityQueueAstar(manhattan), ListNodos)



def hamming(estado):
    '''Calculo da distancia de hamming.'''
    return sum(char1 != char2 for char1, char2 in zip("12345678", estado))

'''
Posições corretas das peças no puzzle.
'''
posicao_correta = {
    "1":(0,0),
    "2":(0,1),
    "3":(0,2),
    "4":(1,0),
    "5":(1,1),
    "6":(1,2),
    "7":(2,0),
    "8":(2,1)
}

def manhattan(estado):
    '''Calculo da distancia manhattan.'''
    vals = ["1","2","3","4","5","6","7","8"]
    
    estimativa = 0
    for val in vals:
        index = estado.find(val)
        row = index // 3
        column = index % 3
        posicao_valor = posicao_correta[val]
        estimativa += abs(posicao_valor[0] - row) + abs(posicao_valor[1] - column)
        
    return estimativa



estado = '_23541687'
astar_hamming(estado)
astar_manhattan(estado)
bfs(estado)
dfs(estado)
