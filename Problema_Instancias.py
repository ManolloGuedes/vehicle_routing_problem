import ResolveProblema

i = 1

while (i <= 40):
    fonte = 'Dados_PTTOR-16/Instancias_1_40/I' + str(i) + '.PTTOR-16'
    print ("\n\n--------- INSTANCIA %d---------\n\n"%i)
    ResolveProblema.resProblema(fonte)
    i = i + 1
