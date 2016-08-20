import pulp 
import FiltraArquivo

#imprimir dados, ja ajustados em vetores e matrizes
def imprime (atvPer, escTur, cusAtv, cusFix):
    print ("Atividades\tPeriodo")
    tam = len(atvPer)
    i = 0
    while (i < tam):
        print (atvPer[i])
        i = i+1
            
    print ("\nEscolhas dos Turistas")
    str1 = '\t'.join(escTur)
    print (str1)

    print ("\nCustos das Atividades")
    tam = len(cusAtv)
    i = 0
    while (i < tam):
        print (cusAtv[i])
        i = i+1

    print ("\nCusto Fixo")
    print (cusFix)

def resProblema (arqFonte):
    #Carrega arquivo com dados e salva tudo dentro de uma unica string, que sera desmembrada posteriormente
    arq = open(arqFonte, 'r')
    #Todo o texto foi passado para caixa baixa, para padronizar todas as instancias. Na instancia Rio16 tem uma tag diferente
    #das demais instancias (<Custo Fixo> - <Custo fixo>)
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
    
    #imprime (atvPer, escTur, cusAtv, cusFix)

    # Cria a variavel modelo do pulp
    model = pulp.LpProblem('Model_PTTOR-16', pulp.LpMinimize)

    #Quantidade de atividades selecionadas
    n = len(escTurAtl)

    ########### VARIAVEIS ###########
    
    # Declaracao das variaveis x: Variavel binaria ativada se for tomada a rota da atividade i para a atividade j
    x = [[[pulp.LpVariable('x_'+str(i)+'_'+str(j)+'_'+str(k), lowBound = 0, cat='Binary') for i in range(n)] for j in range(n)] for k in range(n)]

    # Declaracao das variaveis y: Variavel binaria ativada se o carro k for utilizado
    y = [[pulp.LpVariable('y_'+str(k), lowBound = 0, cat='Binary') for k in range(n)]]

    # Declaracao das variaveis u: Variavel que representa a atividade i feita pelo carro k
    u = [[pulp.LpVariable('u_'+str(i)+'_'+str(k), lowBound = 0, cat='Integer') for i in range(n)] for k in range(n)]
    
    ########### FUNCAO OBJETIVO ###########
    
    # Declaracao da funcao objetivo 
    model += sum(((cusFix*y[0][k]) + sum([sum(cusAtv[i][j]*x[i][j][k] for i in range(n)) for j in range(n)])) for k in range(n))

    ########### RESTRICOES ###########

    #Apenas uma rota pode sair da posicao i (1)
    for i in range(n):
        model += sum([sum(x[i][j][k] for j in range(n)) for k in range(1, n)]) == 1

    #Apenas uma rota pode chegar na posicao j (2)
    for j in range(n):
        model += sum([sum(x[i][j][k] for k in range(n)) for i in range(n)]) == 1

    #Cada carro k comporta no maximo 4 pessoas (3)
    for k in range(n):
        model += sum([sum(x[i][j][k] for i in range(n)) for j in range(n)]) <= 4*y[0][k]

    #Cada veiculo nao realiza mais que uma rota
    for k in range(n):
        model += sum(x[0][j][k] for j in range(n)) <= 1

    #Garante que o veiculo nao fique parado
   # for j in range(n):
    #    for k in range(n):
     #       model += sum(x[i][j][k] - x[j][i][k] for i in range(n)) == 0
  

    #Evitar a ocorrência de subciclos no grafo formado pelo trajeto tomado pelo carro k (5)
    for k in range(n):
        for i in range(1, n):
            for j in range(1, n):
                model += (u[i][k]-u[j][k] + 4*x[i][j][k]) <= 3

    #Verifica a formação de subciclos a partir do segundo nó, desconsiderando o primeiro nó (6)
    for i in range(1, n):
        for k in range(n):
            model += u[i][k] >= 2         
    
    #print (model)

    # Resolve o modelo
    model.solve()
	
    # Escreve a versao deste modelo no formato LP
    model.writeLP("Trabalho_PTTOR-16.lp")

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


    #Imprime quais clientes estao em cada carro (variavel z)
    print ("##################################################")
    print ("Turistas Contidos em Cada Carro: ")
    tamCar = len(carro)
    for k in range(tamCar):
        print ("\nCarro %d:" % carro[k])
        print ("Cliente\t\tAtividade\tPeriodo")
        for j in range (n):
            for i in range(n):
                if (x[i][j][carro[k]].value() == 1.0):
                    print ("%d\t\t%s\t\t%s" % (i, escTurAtl[i], periodo[i]))


    print ("##################################################")
    print ("\n")

    print ("##################################################")
    print ("Rotas: ")

    for k in range(tamCar):
        print ("\nCarro %d:" % carro[k])
        for j in range(n):
            for i in range(n):
                if (x[i][j][carro[k]].value() == 1.0):
                    print ("%s \t->\t %s" %(escTurAtl[i],escTurAtl[j]))


    print ("##################################################")
    print ("\n")

    # Imprime a funcao objetivo
    print ("##################################################")
    print ('Funcao Objetivo: %.2f.' % model.objective.value())
    print ("##################################################")

    
