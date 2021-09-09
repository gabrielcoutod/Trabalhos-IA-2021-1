INF01048 Inteligencia Artificial (2021/1) - Turma A - UFRGS
Professor Anderson Rocha Tavares
TRABALHO 2 - Poda alfa-beta em Othello/Reversi
Autores:
    Eduardo Eugenio Kussler - 315799
    Gabriel Couto Domingues - 302229
    Thiago Sotoriva Lermen  - 313020

Descrição da função de avaliação, da estratégia de parada: Fizemos uma função de avaliação baseada na função de avaliação disponivel na bibliografia. Nossa função calcula valores relacionados a paridade, similaridade, mobilidade, dando pesos para esses valores na avaliação. O peso para esses valores foi escolhido de maneira experimental. Para a estratégia de parada consideramos uma profundidade fixa de 3, começando em 0, pois testamos essa profundidade e foi a maior profundidade que não ficava mais de 5 segundos calculando a melhor jogada.

Eventuais melhorias (quiescence search, singular extensions, etc): Nenhuma.

Decisões de projeto e dificuldades encontradas: Acho que a maior dificuldade foi que estavamos tentando resolver um problema que não sabíamos por onde começar, ou seja, a maior dificuldade foi dar o primeiro passo. Porém, depois de pensar sobre como implementar o algoritmo, conseguimos entender o funcionamento do algoritmo e implementá-lo com sucesso.

Bibliografia completa (incluindo sites): Nós baseamos na função de avaliação disponível em: https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-reversiothello/