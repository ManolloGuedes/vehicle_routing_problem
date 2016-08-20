def fltArq (text):
    atvPer = []         #Atividades e Periodos
    escTur = []         #Escolhas dos Turistas
    cusAtv = []         #Custos das Atividades
    escTurAtl = []      #Escolhas dos Turistas, MAS ORDENADA DE ACORDO COM O CABECALHO DOS CUSTOS DAS ATIVIDADES (Esta diferente a ordem)
    periodo = []        #Vetor com apenas os periodos de cada atividade (1 = matutino, 2 = vespertino, 3 = noturno)
    
    cusFix = 0          #Custo Fixo
    atvPerC = 0         #Controle do arquivo - Atividades e Periodos
    escTurC = 0         #Controle do arquivo - Escolhas dos Turistas
    cusAtvC = 0         #Controle do arquivo - Custos das Atividades

    i = 0
    #Retira dados da string e armazena em vetores 
    while (text[i] != "<fim>"):

        #Caso ache essa tag no arquivo texto, sera ativado o controlador para que os dados sejam salvos no vetor correto
        if (text[i] == "<atividades\tperiodo>"):
            atvPerC = 1

        if (text[i] == "<escolha turistas>"):
            atvPerC = 0
            escTurC = 1

        if (text[i] == "<custos das atividades>"):
            escTurC = 0
            cusAtvC = 1

        if (text[i] == "<custo fixo>"):
            cusAtvC = 0
            cusFix = text[i+1]
        

        #Verifica se o controlador esta ativado, se sim, armazena dado no respectivo vetor
        if (atvPerC == 1):
            atvPer.append (text[i])

        if (escTurC == 1):
            escTur.append (text[i])

        if (cusAtvC == 1):
           cusAtv.append (text[i])
            
        i = i+1

    atvPer.pop(0) # Retira posicao inutil (armazena o titulo do arquivo de texto)
    escTur.pop(0) # Retira posicao inutil (armazena o titulo do arquivo de texto)
    cusAtv.pop(0) # Retira posicao inutil (armazena o titulo do arquivo de texto)

    escTur = escTur[0].split('\t') #Coloca cada escolha de turistas em uma posicao do vetor (inicialmente estava toda a linha salva em uma so posicao)

    #Por algum motivo, ao ler uma instancia que nao seja a Rio16, salva um vazio '' na ultima posicao
    t = len(escTur) - 1
    if (escTur[t] == ''):
        escTur.pop(t)

    #Arrumando matriz de custo de atividades (cada dado em uma posicao). Inicialmente cada linha do arquivo era uma posicao
    auxCusAtv = []
    tamCusAtv = len(cusAtv)
    i = 0
    
    while (i < tamCusAtv):
        auxCusAtv.append(cusAtv[i].split('\t'))
        i = i+1

    cusAtv = auxCusAtv

    #Retira linha e coluna 0 da matriz de custos das atividades, que servem como especies de cabecalho. Desta forma, fica apenas os dados que serao utilizados
    cusAtv.pop(0)
    tamCusAtv = len(cusAtv)

    i = 0
    while (i < tamCusAtv):
        escTurAtl.append(cusAtv[i].pop(0))
        i = i+1

    #Converter matriz de custos das atividades para tipo inteiro. As distancias infinitas (INF), de uma posicao para ela mesma, serao transformadas
    #em um numero suficientemente grande, que nao interfira na resolução do problema de minimizacao
    i = 0
    j = 0

    tamCusAtv = len(cusAtv)
    
    while (i < tamCusAtv):
        while (j < tamCusAtv):
            if (i == j):
                cusAtv[i][j] = int(1000)
            else:
                cusAtv[i][j] = int(cusAtv[i][j])
            j = j+1
        j = 0
        i = i+1

    #Vetor de periodos das atividades escolhidas por cada cliente
    tamPer = len(atvPer)
    i = 0
    while (i < tamPer):
        str1 = atvPer[i].split('\t')
        if (str1[1] == 'm'):
            periodo.append(1)
        elif (str1[1] == 'v'):
            periodo.append(2)
        elif (str1[1] == 'n'):
            periodo.append(3)
        i = i+1

    #Tendo obtido os periodos, agora sera invibializadas as rotas de periodos nao consequentes.
    #Para isso sera adicionada a rota que os liga um valor suficientemente grande para que a mesma nao seja acionada.
    tamCus = len(atvPer)
    for i in range(tamCus):
        for j in range(tamCus):
            tamPer = int(periodo[i]) - int(periodo[j])
            if (tamPer == 2 or tamPer == -2):
                cusAtv[i][j] = 1000

    
    #Retorna todos os vetores obtidos a partir da filtragem do texto
    retornoDados = []
    retornoDados.append(atvPer)
    retornoDados.append(escTur)
    retornoDados.append(cusAtv)
    retornoDados.append(cusFix)
    retornoDados.append(escTurAtl)
    retornoDados.append(periodo)

    return retornoDados
