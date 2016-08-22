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
# Este arquivo passa o nome da instancia Rio16.txt para outro arquivo. Este nome sera utilizado para acessar o  #
# arquivo que contem a base de dados desta instancia, que serao utilizados para a resolucao do modelo.          #
#################################################################################################################

import time
import ResolveProblema

fonte = 'Dados_PTTOR-16/Rio16/Rio16.txt'
print ("\n\n--------- INSTANCIA Rio16---------\n\n")
t1=time.time()
ResolveProblema.resProblema(fonte)
t2 =time.time()
print("\n\n--------- Tempo Gasto: %.3f segundos ---------" %(t2-t1))
