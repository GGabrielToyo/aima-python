from collections import deque
import sys


class Problem:
    def __init__(self, initial, goal, grafo):
        self.initial = initial
        self.goal = goal
        self.grafo = grafo

    def acoesDoEstado(self, state):
        return self.grafo[state]
    
    def testeDeObjetivo(self, state):
        return state == self.goal
      
class Node:
    def __init__(self, state, parent = None, action = None):
        self.state = state
        self.parent = parent
        self.action = action
    
    def expandirNo(self, problem):
        novos_nos = []
        for estado in problem.acoesDoEstado(self.state):
            novo_estado = Node(estado, self, problem.acoesDoEstado(estado))
            novos_nos.append(novo_estado)
        return novos_nos
    
    def caminho(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))
    
    def __repr__(self) -> str:
        return f"Node {self.state}\nParent: {self.parent.state if self.parent else None}\nAction: {self.action}\n"
    
    def __str__(self) -> str:
        return f"{self.state}"
    

#busca em profundidade
def busca_em_profundidade(problem):
    nodeInitial = Node(problem.initial, None, problem.acoesDoEstado(problem.initial))
    frontier = [] #stack
    frontier.append(nodeInitial)
    explored = set()
    count = 0

    while frontier:
        count += 1
        node = frontier.pop()
        if problem.testeDeObjetivo(node.state):
            print(f"Quantidade de movimentos: {count}")
            return node.caminho()
        explored.add(node.state)
        frontier.extend(child for child in node.expandirNo(problem)
                     if child.state not in explored and child not in frontier)
    return None

#busca em largura
def busca_em_largura(problem):
    nodeInitial = Node(problem.initial, None, problem.acoesDoEstado(problem.initial))
    frontier = deque([nodeInitial]) #queue
    explored = set()
    count = 0

    if problem.testeDeObjetivo(nodeInitial.state):
            return node.caminho()

    while frontier:
        count += 1
        node = frontier.popleft()
        explored.add(node.state)
        for child in node.expandirNo(problem):
            if child.state not in explored and child not in frontier:
                if problem.testeDeObjetivo(child.state):
                    print(f"Quantidade de movimentos: {count}")
                    return child.caminho()
                frontier.append(child)
    return None

#busca em profundidade limitada
def busca_em_profundidade_limitada(problem, limit = 50):
    def recursive_dls(node, problem, limit):
        count = 0
        if problem.testeDeObjetivo(node.state):
            return node.caminho()
        elif limit == 0:
            return 'Limite não atingiu objetivo'
        else:
            cutoff_occurred = False
            for child in node.expandirNo(problem):
                count += 1
                result = recursive_dls(child, problem, limit - 1)
                if result == 'Limite não atingiu objetivo':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'Limite não atingiu objetivo' if cutoff_occurred else None

    return recursive_dls(Node(problem.initial, None, problem.acoesDoEstado(problem.initial)), problem, limit)

#busca em profundidade limitada interativa
def busca_em_profundidade_limitada_interativa(problem):
    for profundidade in range(sys.maxsize):
        result = busca_em_profundidade_limitada(problem, profundidade)
        if result != 'Limite não atingiu objetivo':
            return result
