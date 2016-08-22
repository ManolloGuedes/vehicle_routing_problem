#################################################################################################################
# Problema_Rio.py												#
# Implementacao do modelo de roteamento de veiculos, com restrições de custo, periodo da atividade e limite do  #
# carro.                                                                                                        #
# GCC118 - Programacao Matematica 									   	#
# Exemplo de modelagem de problema linear utilizando a biblioteca PuLP, na linguagem Pyton, com o solver CLP    #
# Alunos: Cezar Jr, Herlon Manollo, Tulio Silva, Caio Freitas e Rodolpho                                        #
# Professor: Mayron C. O. Moreira.										#
# 2016/01													#
# Turma: 10A													#
# DCC/UFLA													#														#		                                                        #                                                                                                               #
#################################################################################################################
# Este arquivo carrega o arquivo que contem a base de dados de determinada instancia, salva tudo em uma String e#
# passa para outro arquivo, que separa esta String em estruturas de dados, que sao retornadas. Tendo as         #
# estruturas de dados, eh resolvido o modelo matematico programado nesta mesma classe. A maioria das impressoes #
# de dados resultantes para o usuario sao feitas aqui tambem.                                                   #
#################################################################################################################

import pulp
import time
#Importa arquivo que contem funcao que ira filtrar e desmembrar o arquivo de entrada (Rio16 e 40 instancias)
import FiltraArquivo

#Recebe o nome do arquivo que contem a fonte de dados
def resProblema (arqFonte):
    #Carrega arquivo com dados e salva tudo dentro de uma unica string, que sera desmembrada posteriormente
    arq = open(arqFonte, 'r')
    #Todo o texto foi passado para caixa baixa, para padronizar todas as instancias. Na instancia Rio16 tem uma
    #tag diferente das demais instancias (<Custo Fixo> - <Custo fixo>)
    text = arq.read().lower()
    text = text.split('\n')
    arq.close()

    #Passa a string com todos os dados obtidos do arquivo de texto para uma funcao em outro arquivo.
    #Estes dados serao analisados e separados corretamente em vetores, que serao retornados e utilizados aqui
    dados = FiltraArquivo.fltArq(text)

    atvPer = dados[0] #Atividades e Periodos
    escTur = dados[1] #Escolhas dos Turistas
    cusAtv = dados[2] #Custos das Atividades
    cusFix = int(dados[3]) #Custo Fixo
    escTurAtl = dados[4]   #Escolhas dos turistas odenada de acordo com a tabela de custos das atividades (para fins de impressao)
    periodo = dados[5] #Periodos de cada atividade selecionada pelo cliente
    perDiv = dados[6]  #Contem tres vetores, cada um guardando as posicoes de atividades de acordo com seu periodo

    vMat = perDiv[0]
    vVes = perDiv[1]
    vNot = perDiv[2]
    # Cria a variavel modelo do pulp
    model = pulp.LpProblem('Model_PTTOR-16', pulp.LpMinimize)

    #Tamanho dos vetores que armazenam as atividades de acordo com seu periodo
    ma = len(vMat)
    ve = len(vVes)
    no = len(vNot)

    #Quantidade de atividades selecionadas
    n = len(escTurAtl)

    ########### VARIAVEIS ###########
    
    # Declaracao das variaveis x: Variavel binaria ativada se for tomada a rota da atividade i para a atividade j
    x = [[[pulp.LpVariable('x_'+str(i)+'_'+str(j)+'_'+str(k), lowBound = 0, cat='Binary') for i in range(n)] for j in range(n)] for k in range(n)]

    # Declaracao das variaveis y: Variavel binaria ativada se o carro k for utilizado
    y = [[pulp.LpVariable('y_'+str(k), lowBound = 0, cat='Binary') for k in range(n)]]

    # Declaracao das variaveis u: Variavel que representa a atividade i feita pelo carro k
    u = [[pulp.LpVariable('u_'+str(i)+'_'+str(k), lowBound = 0, cat='Integer') for i in range(n)] for k in range(n)]

    # Declaracao das variaveis tipo z: Variavel binaria ativada se o carro k tem uma rota noturna
    z = [[pulp.LpVariable('z_'+str(k), lowBound = 0, cat='Binary') for k in range(n)]]
    
    ########### FUNCAO OBJETIVO ###########
    
    # Declaracao da funcao objetivo 
    model += sum(((cusFix*y[0][k]) + sum([sum(cusAtv[i][j]*x[i][j][k] for i in range(n)) for j in range(n)])) for k in range(n))

    ########### RESTRICOES ###########

    #Apenas uma rota pode sair da posicao i (1)
    for i in range(1, n):
        model += sum([sum(x[i][j][k] for j in range(n)) for k in range(1, n)]) == 1

    #Apenas uma rota pode chegar na posicao j (2)
    for j in range(1, n):
        model += sum([sum(x[i][j][k] for k in range(n)) for i in range(n)]) == 1

    #Cada carro k comporta no maximo 4 pessoas + 1 empresa (5 rotas) (3)
    for k in range(n):
        model += sum([sum(x[i][j][k] for i in range(n)) for j in range(n)]) <= 5*y[0][k]

    #Todos os carros devem sair do ponto 0 (4)
    model += sum(x[0][j][k] for j in range(n) for k in range(n)) == sum(y[0][k] for k in range(n))

    #Todos os carros devem chegar no ponto 0 (5)
    model += sum(x[i][0][k] for i in range(n) for k in range(n)) == sum(y[0][k] for k in range(n))

    #Garante que o veiculo nao fique parado (6)
    for j in range(n):
        for k in range(n):
            model += sum(x[i][j][k] - x[j][i][k] for i in range(n)) == 0


    #Se a rota ij e pegada nao pode pegar a rota ji (voltar) (7)
    for i in range(n):
        for j in range(n):
            model += sum(x[i][j][k] + x[j][i][k] for k in range(n)) <= 1

    #Cada veiculo nao realiza mais que uma rota (8)
    for k in range(n):
        model += sum(x[0][j][k] for j in range(n)) <= 1
  

    #Evitar a ocorrência de subciclos no grafo formado pelo trajeto tomado pelo carro k (9)
    for k in range(n):
        for i in range(1, n):
            for j in range(1, n):
                model += (u[i][k]-u[j][k] + 4*x[i][j][k]) <= 3

    #Verifica a formação de subciclos a partir do segundo nó, desconsiderando o primeiro nó (10)
    for i in range(1, n):
        for k in range(n):
            model += u[i][k] >= 2

    #Limita que uma rota entre matutino e noturno nao sejam tomados (rota i para j) (11)
    for k in range(n):
        model += sum([sum(x[vMat[i]][vNot[j]][k] for i in range(ma)) for j in range(no)]) == 0

    #Limita que uma rota entre matutino e noturno nao sejam tomados (rota j para i) (12)
    for k in range(n):
        model += sum([sum(x[vNot[j]][vMat[i]][k] for i in range(ma)) for j in range(no)]) == 0

    #Impede que se uma atividade vespertina receba de uma matutina, ela va para outra atividade noturna (13)
    for i in range (ve):
        for j in range (ma):
            model += sum(sum(x[vMat[j]][vVes[i]][k] + x[vVes[i]][vNot[l]][k]) for l in range(no) for k in range(n)) <= 1

    #Impede que se uma atividade vespertina receba de uma noturna, ela va para outra atividade matutina (14)
    for i in range (ve):
        for j in range (no):
            model += sum(sum(x[vNot[j]][vVes[i]][k] + x[vVes[i]][vMat[l]][k]) for l in range(ma) for k in range(n)) <= 1
    
    #Resolve o modelo e armazena o valor retornada na variavel status
    status = model.solve()
    
    #Escreve a versao deste modelo no formato LP 
    nomeA = arqFonte.split('/')
    nomeA = nomeA[len(nomeA)-1].split('.')
    nomeA = str(nomeA[0])    
    model.writeLP("Solucao_%s.lp" % nomeA)

    #Verifica resolucao do problema
    if (status == pulp.LpStatusInfeasible):
        print ('MODELO INFACTIVEL\n')

    elif (status == pulp.LpStatusUnbounded):
        print ('MODELO ILIMITADO\n')

    elif (status == pulp.LpStatusOptimal):
        print ('SOLUÇÃO OTIMA ENCONTRADA\n')
        
    #Imprime os carros utilizados (variavel y)
    print ("##################################################")
    print ("Carros Utilizados:\n ")
    carro = []
    for k in range(n):
        if (y[0][k].value() == 1.0):
            carro.append(k)
            print ("Carro %d"% k)

    print ("##################################################")
    print ("\n")


    #Imprime quais clientes estao em cada carro
    print ("##################################################")
    print ("Turistas Contidos em Cada Carro: ")
    tamCar = len(carro)
    for k in range(tamCar):
        print ("\nCarro %d:" % carro[k])
        print ("Cliente\t\tAtividade\tPeriodo")
        for j in range (0, n):
            for i in range(1, n):
                if (x[i][j][carro[k]].value() == 1.0):
                    prd = ''
                    if (periodo[i-1] == 1):
                        prd = 'M'
                    elif (periodo[i-1] == 2):
                        prd = 'V'
                    elif (periodo[i-1] == 3):
                        prd = 'N'
                    print ("%d\t\t%s\t\t%s" % (i, escTurAtl[i], prd))


    print ("##################################################")
    print ("\n")

    #Imprime as rotas tomadas por cada carro. Todos saem do ponto 0 e retornam ao mesmo
    print ("##################################################")
    print ("Rotas: ")

    for k in range(tamCar):
        print ("\nCarro %d:" % carro[k])
        print ("Rotas\t\t\t\tCusto")
        for j in range(n):
            for i in range(n):
                if (x[i][j][carro[k]].value() == 1.0):
                    print ("%s \t->\t %s\t\t%d" %(escTurAtl[i],escTurAtl[j],cusAtv[i][j]))


    print ("##################################################")
    print ("\n")

    # Imprime a funcao objetivo
    print ("##################################################")
    print ('Funcao Objetivo: %.2f.' % model.objective.value())
    print ("##################################################")

    #Para contabilizar solucoes otimas no teste das 40 instancias
    return status
    
