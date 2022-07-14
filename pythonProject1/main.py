import copy
import math
import random

#functia de maximizat, coeficientii fiind cititi la input
def myF(x, c):
    return c[0]*(x**2) + c[1]*x + c[2]

n = int(input("dimensiunea populatiei = "))
print("Domeniul functiei:")
a = int(input("a = "))
b = int(input("b = "))
print("Parametrii functiei de maximizat: ", end=" ")
coef = [int(x) for x in input().split()]
precizie = int(input("precizia = "))
pr = float(input("probabilitatea de incrucisare = "))
pm = float(input("probabilitatea de mutatie = "))
etape = int(input("numarul de etape = "))

g = open("Evolutie.txt", "w")

#discretizarea intervalului + cromozomii generati random
dimC = math.ceil(math.log2((b-a)*(10**precizie)))
cromozomi = [[random.randint(0, 1) for j in range(dimC)] for i in range(n)]

################ populatia initiala ####################
for etapa in range(1, etape+1):
    if etapa == 1:
        g.write("Populatia initiala\n")
    sumF = 0
    X = []
    Maxfittest = float('-inf')
    fittest = 0
    for i in range(n):
        b2string = ''.join([str(x) for x in cromozomi[i]])
        x = int(b2string, 2) #transform sirul de biti in baza 10
        interpolateX = ((b-a) / (2**dimC - 1))*x + a #valoarea codificata a cromozomilor
        X.append(interpolateX)
        if etapa == 1:
            g.write(str(i+1) + " : " + b2string + " x= " + str(round(interpolateX, precizie)) + " f= " + str(myF(round(interpolateX, precizie), coef)))
            g.write('\n')
        sumF += myF(interpolateX, coef)  # suma din formula -> F  performanta totala a populatiei
        if myF(round(interpolateX, precizie), coef) > Maxfittest: #de asemenea calculez si cel mai fittest cromozom sa-l trec direct in etapa urmatoare
            Maxfittest = myF(round(interpolateX, precizie), coef)
            fittest = i

    fittestch = cromozomi[fittest].copy()

####################### PROBABILITATILE PT CROMOZOMI - metoda ruletei ####################
    if etapa == 1:
        g.write("\nProbabilitati selectie\n")
    probSelection = []
    for i in range(n):
        probSelection.append(myF(X[i], coef) / sumF)
        if etapa == 1:
            g.write("cromozom " + str(i+1) + " probabilitate " + str(myF(X[i], coef) / sumF))
            g.write('\n')

 ##################### INTERVALELE PROBABILITATE SELECTIE ########################
    if etapa == 1:
        g.write("\nIntervale probabilitate selectie\n")
    intervalsProbSel = [0]
    sumI = probSelection[0]
    intervalsProbSel.append(sumI)
    if etapa == 1:
        g.write("0 " + str(sumI) + " ")
    for i in range(1, n):
        sumI += probSelection[i]
        intervalsProbSel.append(sumI)
        if etapa == 1:
            g.write(str(sumI) + " ")


    def findI(u, v, st, dr): #cautarea binara pentru a gasi intervalul potrivit pentru un u dat
        global last
        while st <= dr:
            mij = (st + dr) // 2
            if v[mij] <= u:
                last = mij
                st = mij+1
            elif v[mij] > u:
                dr = mij-1
        return last+1

# evidenţierea procesul de selecţie, care constă în generarea unui număr aleator u uniform pe
# [0,1) şi determinarea intervalului [qi , qi+1) căruia aparține acest număr; corespunzător acestui
# interval se va selecta cromozomul i+1.

    if etapa == 1:
        g.write("\n\n")
    selected = [0 for _ in range(n)]
    for i in range(n):
        u = random.random()    #genereazaz u variabila uniforma pe [0,1)
        cr = findI(u, intervalsProbSel, 0, n) - 1
        if etapa == 1:
            g.write("u= " + str(u) + " selectam cromozomul " + str(cr+1))
            g.write('\n')
        selected[i] = cr #cromozomii ce trec de selectie sunt adaugati in selected

############# DUPA SELECTIE ###########
    if etapa == 1:
        g.write("\nDupa selectie\n")
    cc = []
    for i in range(n):
        if etapa == 1:
            g.write(str(i+1) + ": " + ''.join([str(x) for x in cromozomi[selected[i]]]) + " x= " + str(round(X[selected[i]], precizie)) + " f= " + str(myF(X[selected[i]], coef)))
            g.write('\n')
        cc.append(cromozomi[selected[i]])
    cromozomi = copy.deepcopy(cc) #copiez toti cromozomii care au trecut de selectie in lista initiala cromozomi si trec mai departe

######### PROBABILITATE INCRUCISARE ################
    if etapa == 1:
        g.write("\nProbabilitatea de incrucisare " + str(pr) + "\n")
    recomb = []
    for i in range(n):
        u = random.random()
        if u < pr:   #daca u este mai mic decat probabilitatea de incrucisare adaug indicele cromozomului in vect recomb
            if etapa == 1:
                g.write(str(i+1) + ": " + ''.join([str(x) for x in cromozomi[i]]) + " u= " + str(u) + "<" + str(pr) + " participa\n")
            recomb.append(i)
        else:
            if etapa == 1:
                g.write(str(i+1) + ": " + ''.join([str(x) for x in cromozomi[i]]) + " u= " + str(u) + "\n")

##################### RECOMBINARE ############
    if etapa == 1:
        g.write('\n')
    while len(recomb) > 1: #recomb = lista de indici
        i = random.randrange(len(recomb)) #se alege un i si un j random si incrucisez cromozomii recomb[i] recomb[j]
        j = len(recomb)-i-1
        if i == j:
            continue
        if etapa == 1:
            g.write("Recombinare dintre cromozomul " + str(recomb[i]+1) + " cu cromozomul " + str(recomb[j]+1) + "\n")
        pct = random.randrange(dimC) #punctul random ales pentru incrucisare
        if etapa == 1:
            g.write(''.join([str(x) for x in cromozomi[recomb[i]]]) + " " + ''.join([str(x) for x in cromozomi[recomb[j]]]) + " punct " + str(pct) + "\n")
        chcopy = cromozomi[recomb[i]][:pct+1].copy() #incrucisarea
        cromozomi[recomb[i]][:pct+1] = cromozomi[recomb[j]][:pct+1].copy()
        cromozomi[recomb[j]][:pct+1] = chcopy.copy()
        if etapa == 1:
            g.write("Rezultat " + ''.join([str(x) for x in cromozomi[recomb[i]]]) + " " + ''.join([str(x) for x in cromozomi[recomb[j]]]) + "\n")

        aux = [recomb[k] for k in range(len(recomb)) if k != i and k != j] #elimin indicii i si j din recomb
        recomb = aux.copy()

#####DUPA RECOMBINARE ##########
    if etapa == 1:
        g.write("\nDupa recombinare\n")
    for i in range(n):
        b2string = ''.join([str(x) for x in cromozomi[i]])
        x = int(b2string, 2)
        interpolateX = ((b - a) / (2 ** dimC - 1)) * x + a #calculez valorile x pentru noii cromozomi
        X[i] = interpolateX
        if etapa == 1:
            g.write(str(i + 1) + " : " + b2string + " x= " + str(round(interpolateX, precizie)) + " f= " + str(myF(round(interpolateX, precizie), coef)))
            g.write('\n')

    if etapa == 1:
        g.write("\nProbabilitate de mutatie pentru fiecare gena 0.01\n")
        g.write("Au fost modificati cromozomii:\n")
    for i in range(n):
        u = random.random() #generez un u random si pentru cromozomii cu u<probabilitatea de mutatie, schimb un bit de pe pozitia poz care e si ea generata random
        if u < pm:
            poz = random.randrange(dimC)
            cromozomi[i][poz] = 1-cromozomi[i][poz]
            if etapa == 1:
                g.write(str(i+1) + "\n")

###################### DUPA MUTATIE ##################
    if etapa == 1:
        g.write("\nDupa mutatie:\n")
    Max = float('-inf')
    worstVal = float('inf')
    worst = 0
    medValSum = 0
    for i in range(n):
        b2string = ''.join([str(x) for x in cromozomi[i]])
        x = int(b2string, 2)
        interpolateX = ((b - a) / (2 ** dimC - 1)) * x + a #la final recalculez din nou valorile x dupa mutatii
        X[i] = interpolateX
        if etapa == 1:
            g.write(str(i + 1) + " : " + b2string + " x= " + str(round(interpolateX, precizie)) + " f= " + str(myF(round(interpolateX, precizie), coef)))
            g.write('\n')
        Max = max(Max, myF(round(interpolateX, precizie), coef)) #valoarea maximizata a functiei
        medValSum += myF(round(interpolateX, precizie), coef) #ajuta la calculul valorii medii a performantei
        if myF(round(interpolateX, precizie), coef) < worstVal: #totodata vreau sa vad cromozomul cu worst performance pentru a-l inlocui cu cel mai fittest pe care l-am ales la inceput
            worstVal = myF(round(interpolateX, precizie), coef) #deoarece folosim selectia de tip elitist, cel mai fittest trece automat mai departe
            worst = i

    cromozomi[worst] = fittestch.copy()
    Max = max(Max, Maxfittest)
    medValSum = medValSum - worstVal + Maxfittest

    if etapa == 1:
        g.write("\n\nEvolutia maximului\n")
    g.write("Population " + str(etapa+1) + " maxValue= " + str(Max) + " medium performance: " + str(medValSum/n) + "\n")

g.close()