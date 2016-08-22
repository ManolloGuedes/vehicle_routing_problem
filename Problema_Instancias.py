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
# Este arquivo passa o nome das 40 instancias, uma a uma, para outro arquivo. Este nome sera utilizado para     #
# acessar o arquivo que contem a base de dados desta instancia, que serao utilizados para a resolucao do modelo.#
#################################################################################################################

import pulp
import time
import ResolveProblema

i = 1
tmpTot = 0
qtdOtm = 0

while (i <= 40):
    fonte = 'Dados_PTTOR-16/Instancias_1_40/I' + str(i) + '.PTTOR-16'
    print ("\n\n--------- INSTANCIA %d---------\n\n"%i)
    t1=time.time()
    status = ResolveProblema.resProblema(fonte)
    t2 =time.time()
    t = t2-t1
    tmpTot = tmpTot + t
    print("\n\n--------- Tempo Gasto: %.3f segundos ---------" %(t))
    if (status == pulp.LpStatusOptimal):
        qtdOtm = qtdOtm + 1
    i = i + 1

tmpTot = tmpTot/40
print ("\nTempo medio gasto na execucao de todas as instancias: %.3f segundos" % tmpTot)
print ("Quantidade de solucoes otimas obtidas: %d" % qtdOtm)

