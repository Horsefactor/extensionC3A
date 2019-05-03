import re

#revit structure
index_revit_zone = 0
index_revit_name = 1
index_revit_param = 2
index_revit_q1 = 3
index_revit_dim1 = 4
index_revit_q2 = 5
index_revit_dim2 = 6

#revit simplified structure
index_re_name = 0
index_re_q1 = 1
index_re_dim1 = 2
index_re_q2 = 3
index_re_dim2 = 4

#C3A structure
index_C3A_ref = 0
index_C3A_descr = 1
index_C3A_q = 2
index_C3A_dim = 3
index_C3A_com = 4

#trad structure
index_trad_check = 0
index_trad_name = 1
index_trad_param = 2
index_trad_ref = 3
index_trad_descr = 4
index_trad_form = 5
index_trad_dim = 6

#create a tab from a txt file that is formated with minimum a tabulation between columns   
def createTabFromRevit(path) :
     '''create tab from revit file'''
     with open(path, "r", encoding="utf-16-le") as file :

        return list(map(mktabRevit, file))

def stripgui(elem):
    '''strip guillemet from an elem'''
    return elem.strip('\"')

def mktabRevit(line):
    '''format a line in revit file'''
    elem = re.split(r'\t+', line)
    elem[0] = elem[0].lstrip('\ufeff')
    elem[-1] = elem[-1].rstrip('\n')

    return list(map(stripgui, elem))

def mktabTrad(line):
    ''' format a line in trad file'''
    elem = re.split(r'\t+', line)
    elem[0] = elem[0].lstrip('\ufeff')
    elem[-1] = elem[-1].rstrip('\n')

    return elem

def createTabFromTrad(path) :
     '''create trad file tab'''
     with open(path, "r") as file :

        return list(map(mktabTrad, file))

#write a txt file readable by the C3A excel plugin (if the tabs is well encoded)
def writeTab(path, tab):
    '''write a tab in a file'''
    with open(path, "w", encoding="utf-16-le") as file :
        counterLine=0

        while counterLine< len(tab) :
            counterColumn=0

            while counterColumn < len(tab[counterLine]) -1 :
                file.write("{}\t".format(tab[counterLine][counterColumn]))
                counterColumn +=1

            file.write("{}\n".format(tab[counterLine][counterColumn]))
            counterLine +=1

def stringToNumber(string):
    '''find a number in a string and return it in a type float'''
    return float(re.findall(r'[-+]?\d*\.\d+|\d+', string)[0])

def write(path, string):
    '''write something in a file '''
    with open(path, 'w', encoding='utf-16-le') as file:
        file.write(string)

def mkNames(tab):
    '''make all formated name'''
    return list(map(mkname, tab))

def mkname(elem):
    ''' make formated name of an elem of revit file ''' 
    return [elem[index_revit_zone] + '_' + elem[index_revit_name] + '_' + elem[index_revit_param],
            elem[index_revit_q1],
            elem[index_revit_dim1],
            elem[index_revit_q2],
            elem[index_revit_dim2]]

def applyTradFile(INPUT, TRAD):
    '''apply all the changes to send a new tab in excel'''
    OUT = []
    bitNoModified = [1]*len(INPUT)
    IN = mkNames(INPUT)
    i = 0
    stop = 0
    warningsElemMissing = ''
    warningsNoModif = ''

    for elem in TRAD :

        if stop < 2 :
            stop+=1
            continue

        #give any element which have the same param and name to apply formula and give them refC3A
        listeSameName = [j for j in range(len(INPUT)) if INPUT[j][index_revit_name] == elem[index_trad_name]]

        #elem marked as important in tradfile and missing in revit file
        if (int(elem[index_trad_check]) == 1 and listeSameName == []):
            warningsElemMissing += '[{}]\t missing\r\n'.format(elem[index_trad_name])

        listIndex = [j for j in range(len(INPUT)) if (INPUT[j][index_revit_name] == elem[index_trad_name] and
                                                      INPUT[j][index_revit_param] == elem[index_trad_param])]

        for index in listIndex:
            #0='pce'; 1='m'
            if int(elem[index_trad_dim]) in (0,1) :
                OUT.append([elem[index_trad_ref],
                            elem[index_trad_descr],
                            float(elem[index_trad_form])*stringToNumber(IN[index][index_re_q1]),
                            elem[index_trad_dim],
                            IN[index][index_re_name]])
                bitNoModified[index] = 0
                
            else :
                OUT.append([elem[index_trad_ref],
                            elem[index_trad_descr],
                            float(elem[index_trad_form])*stringToNumber(IN[index][index_re_q2]),
                            elem[index_trad_dim],
                            IN[index][index_re_name]])
                bitNoModified[index] = 0

    for elem in bitNoModified :
        #elem ignore by trad file (no modif)
        if elem:
            OUT.append(['??????????????',
                        IN[i][index_re_name],
                        IN[i][index_re_q1],
                        IN[i][index_re_dim1],
                        '/!\ aucune traduction trouvé dans le fichier de trad'])
            warningsNoModif += '[{}]\t:\tquantité 1:\t{}{};\tquantité 2:\t{}{};\r\n'.format(IN[i][index_re_name],
                                                                                            IN[i][index_re_q1],
                                                                                            IN[i][index_re_dim1],
                                                                                            IN[i][index_re_q2],
                                                                                            IN[i][index_re_dim2])
        i += 1

    return OUT, warningsElemMissing, warningsNoModif