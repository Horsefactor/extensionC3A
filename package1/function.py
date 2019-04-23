import re
from decimal import Decimal

#revit structure
index_ref = 0
index_descr = 1
index_quantity = 2
index_dim = 3
index_quantity2 = 4
index_dim2 = 5
index_sys = 6
index_param = 7
index_zone = 8

#trad structure
ind_trad_ref = 0
ind_trad_descr = 1
ind_trad_dim = 2
ind_trad_sys = 3
ind_trad_param = 4
ind_trad_form = 5 
ind_trad_ref2 = 6
ind_trad_descr2 = 7
ind_trad_dim2 = 8

#create a tab from a txt file that is formated with minimum a tabulation between columns   
def createTab(path) :
     
     with open(path, "r", encoding="utf-16-le") as file :
        tab = []
        counterLine = 0

        for line in file :
            tab.append([])
            elem = re.split(r'\t+', line)
            elem[0] = elem[0].lstrip('\ufeff')
            elem[-1] = elem[-1].rstrip('\n')
            tab[counterLine] = [elem[counterColumn] for counterColumn in range(len(elem))]
            counterLine +=1

        return tab

#return an index list of ref, which could be use to manipulate tabs
def search(tab, ref, system, param) :

    return [i for i in range(len(tab)) if (tab[i][index_ref] == ref and 
                                           tab[i][index_sys] == system and 
                                           tab[i][index_param] == param)]

#write a txt file readable by the C3A excel plugin (if the tabs is well encoded)
def writeTab(path, tab):

    with open(path, "w", encoding="utf-16-le") as file :
        counterLine =0

        while counterLine< len(tab) :
            counterColumn = 0

            while counterColumn < len(tab[counterLine]) -1 :
                file.write("{}\t".format(tab[counterLine][counterColumn]))
                counterColumn +=1

            file.write("{}\n".format(tab[counterLine][counterColumn]))
            counterLine +=1

def stringToNumber(string):

    return float(re.findall(r'[-+]?\d*\.\d+|\d+', string)[0])

def write(path, string):

    with open(path, 'w', encoding='utf-16-le') as file:
        file.write(string)

def wrapped(arg):

    return '\"{}\"'.format(arg)

def sum(tab):
    counter=0

    while counter < len(tab):
        tab[counter][index_quantity] = stringToNumber(tab[counter][index_quantity]) 
        tab[counter][index_quantity2] = stringToNumber(tab[counter][index_quantity2]) 
        i=1

        while i < len(tab):

            if (tab[i][index_ref] == tab[counter][index_ref] and 
                tab[i][index_sys] == tab[counter][index_sys] and 
                tab[i][index_param] == tab[counter][index_param] and 
                tab[i][index_zone] == tab[counter][index_zone] and
                i != counter):

                tab[counter][index_quantity] += stringToNumber(tab[i][index_quantity])
                tab[counter][index_quantity2] += stringToNumber(tab[i][index_quantity2])
                del(tab[i])

            else :
                i +=1

        counter += 1

    return tab

def applyTabTrad(tabSUM, tabTRAD):
    tabXLS = []
    #key : zone,    value : ["[REFC3A] nom : formula * quantity = finalQuantity","...","..."]
    dico = dict()
    listeIndexNoModif = [1]*(len(tabSUM))

    for elem in tabTRAD :
        ref = wrapped(elem[ind_trad_ref])
        system = wrapped(elem[ind_trad_sys])
        param = wrapped(elem[ind_trad_param])
        listeIndex = search(tabSUM, ref, system, param)

        for index in listeIndex:
            tmp =[]
            tmp = list(tabSUM[index])
            quantity = '%.2f' % tabSUM[index][index_quantity]
            tmp[index_ref] = wrapped(elem[ind_trad_ref2])
            tmp[index_descr] = wrapped(elem[ind_trad_descr2])
            tmp[index_quantity] *= float(elem[ind_trad_form])
            tmp[index_quantity2] *= float(elem[ind_trad_form])
            tmp[index_quantity] = '\"%.2f\"' % tmp[index_quantity]
            tmp[index_quantity2] = '\"%.2f\"' % tmp[index_quantity2]
            listeIndexNoModif[index] = 0
            tabXLS.append(tmp)

            if tmp[index_zone] not in dico :
                dico[tmp[index_zone]] = []
                
            dico[tmp[index_zone]].append('[\"{}\"]\t{}\t:\t{}\tx\t{}\t=\t{}\n'.format(elem[ind_trad_ref2], 
                                                                                      elem[ind_trad_descr2],
                                                                                      elem[ind_trad_form], 
                                                                                      quantity,
                                                                                      tmp[index_quantity]))

    i = 0
    for elem in listeIndexNoModif :

        if elem:
            tmp = list(tabSUM[i])
            tmp[index_quantity] = '\"%.2f\"' % tmp[index_quantity]
            tmp[index_quantity2] = '\"%.2f\"' % tmp[index_quantity2]
            tabXLS.append(tmp)

            if tmp[index_zone] not in dico :
                dico[tmp[index_zone]] = []
            
            dico[tmp[index_zone]].append('[{}]\t{}\t:\tnon-modifié,\tquantité\t=\t{}\n'.format(tmp[index_ref], 
                                                                                               tmp[index_descr],
                                                                                               tmp[index_quantity]))

        i+=1
        
    return tabXLS, dico

def showDetails(dico):
    string = ''

    for key in dico :
        string2 = ''

        for elem in dico[key]:
            string2 += elem

        string += '\r\n\r\nZone :\t{}\r\n\r\n{}'.format(key, string2)

    return string

def sum2(tab):
    counter=0

    while counter < len(tab):
        tab[counter][index_quantity] = stringToNumber(tab[counter][index_quantity]) 
        tab[counter][index_quantity2] = stringToNumber(tab[counter][index_quantity2]) 
        i=1

        while i < len(tab):

            if (tab[i][index_ref] == tab[counter][index_ref] and 
                tab[i][index_sys] == tab[counter][index_sys] and 
                tab[i][index_param] == tab[counter][index_param] and 
                tab[i][index_zone] == tab[counter][index_zone] and
                i != counter):

                tab[counter][index_quantity] += stringToNumber(tab[i][index_quantity])
                tab[counter][index_quantity2] += stringToNumber(tab[i][index_quantity2])
                del(tab[i])

            else :
                i +=1

        tab[counter][index_quantity] = '\"%.2f\"' % tab[counter][index_quantity]
        tab[counter][index_quantity2] = '\"%.2f\"' % tab[counter][index_quantity2]
        counter += 1

    return tab