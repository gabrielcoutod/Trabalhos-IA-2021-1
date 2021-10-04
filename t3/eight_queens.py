import numpy as np
import random

def evaluate(individual):
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 9.
    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """
    count = 0
    for i in range(8):
        for j in range(i+1, 8):
            k = j - i
            if individual[i] == individual[j] or individual[i] == individual[j] + k or individual[i] == individual[j] - k:
                count += 1
    return count



def tournament(participants):
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """
    return min(participants, key = evaluate)

def top(participants):
    return tournament(participants)
        


def crossover(parent1, parent2, index):
    """
    Realiza o crossover de um ponto: recebe dois indivíduos e o ponto de
    cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
    dois indivíduos com o material genético trocado.
    Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
    deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
    A ordem dos dois indivíduos retornados não é importante
    (o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
    :param parent1:list
    :param parent2:list
    :param index:int
    :return:list,list
    """
    return parent1[:index] + parent2[index:], parent2[:index] + parent1[index:]


def mutate(individual, m):
    """
    Recebe um indivíduo e a probabilidade de mutação (m).
    Caso random() < m, sorteia uma posição aleatória do indivíduo e
    coloca nela um número aleatório entre 1 e 8 (inclusive).
    :param individual:list
    :param m:int - probabilidade de mutacao
    :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
    """
    individual = individual[:]
    if  np.random.uniform(low=0, high=1) < m:
        pos = np.random.randint(low=0, high=8)
        val = np.random.randint(low=1, high=9)
        individual[pos] = val
    return individual

def run_ga(g, n, k, m, e):
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:bool - se vai haver elitismo
    :return:list - melhor individuo encontrado
    """
    #inicialização
    p = [list(i) for i in np.random.randint(1, 9, size=(n, 8))]

    for gen in range(g):
        if e:
            new_p = [top(p)]
        else:
            new_p = []

        while len(new_p) < n:
            part_k1 = random.sample(p, k)
            part_k2 = random.sample(p, k)
            p1, p2 = tournament(part_k1), tournament(part_k2)
            o1, o2 = crossover(p1, p2, np.random.randint(low=0, high=8))
            o1, o2 = mutate(o1, m), mutate(o2, m)
            new_p.extend([o1,o2])
        p = new_p

    return top(p)