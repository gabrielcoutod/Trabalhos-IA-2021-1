# INF01048 Inteligencia Artificial (2021/1) - UFRGS
# Professor Anderson Rocha Tavares
# TRABALHO 1 - Busca em Grafos
# Autores:
#   Eduardo Eugenio Kussler
#   Gabriel Couto Domingues
#   Thiago Sotoriva Lermen


class Nodo:
    ''' Classe que representa um nodo no grafo.'''
    
    def __init__(self, estado, pai, acao, custo):
        self.estado = estado    # estado atual do 8-puzzle
        self.pai = pai          # nodo pai do estado atual
        self.acao = acao        # acao tomada anteriormente para 
                                # atingir o estado atual
        self.custo = custo      # custo do caminho do estado inicial 
                                # ate o no atual (custo pai + 1)
    
    def __str__(self):
        return "estado: " + str(self.estado) + ", pai: " + str(self.pai) + ", acao: " + str(self.acao) + ", custo: " + str(self.custo)
    

def sucessor(estado: str):
    ''' Recebe um estado e retorna uma lista de tuplas (acao, estado atingido). '''
    espaco_vazio = estado.find('_')
    len_estado = 9 
    lst = []

    if espaco_vazio - 1 >= 0: # esquerda
        index = espaco_vazio - 1
        estado_lst = list(estado)
        estado_lst[index], estado_lst[espaco_vazio] = estado_lst[espaco_vazio], estado_lst[index]
        lst.append(("esquerda","".join(estado_lst)))
    if espaco_vazio + 1 < len_estado: # direita
        index = espaco_vazio + 1
        estado_lst = list(estado)
        estado_lst[index], estado_lst[espaco_vazio] = estado_lst[espaco_vazio], estado_lst[index]
        lst.append(("direita","".join(estado_lst)))
    if espaco_vazio - 3 >= 0 : # acima
        index = espaco_vazio - 3
        estado_lst = list(estado)
        estado_lst[index], estado_lst[espaco_vazio] = estado_lst[espaco_vazio], estado_lst[index]
        lst.append(("acima","".join(estado_lst)))
    if espaco_vazio + 3 < len_estado: # abaixo
        index = espaco_vazio + 3
        estado_lst = list(estado)
        estado_lst[index], estado_lst[espaco_vazio] = estado_lst[espaco_vazio], estado_lst[index]
        lst.append(("abaixo","".join(estado_lst)))
    
    return lst

def expande(nodo: Nodo):
    ''' Expande um nodo, retornando os nodos sucessores do nodo passado como argumento.'''
    sucessores = sucessor(nodo.estado)
    lst_sucessores = []
    for suc in sucessores:
        nodo_sucessor = Nodo(suc[1], nodo.estado, suc[0], nodo.custo + 1)
        lst_sucessores.append(nodo_sucessor)
    return lst_sucessores
