from re import findall, split
from package.Exc import*

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

def mktabRevit(line):
    ''' format a line in revit file '''
    elem = split(r'\t+', line)
    elem[0] = elem[0].lstrip('\ufeff')
    elem[-1] = elem[-1].rstrip('\n')

    if len(elem) != 7:
        raise ColumnError('''Les collones du fichier .txt sortit de revit ne sont pas complete
                           \nS.v.p verrifier que les lignes contiennent bien 7 collonne 
                           \nou que celle-ci ne sont pas séparée par des tabulations!''')

    return list(map(lambda e:e.strip('\"'), elem))

def createTabFromRevit(path) :
     ''' create tab from revit file that is formated with minimum a tabulation between columns '''
     with open(path, "r", encoding="utf-16-le") as file :

        return list(map(mktabRevit, file))

def mktabTrad(line):
    ''' format a line in trad file '''
    elem = split(r'\t+', line)
    elem[0] = elem[0].lstrip('\ufeff')
    elem[-1] = elem[-1].rstrip('\n')

    return elem

def createTabFromTrad(path):
     ''' create trad file tab '''
     with open(path, "r", encoding="utf-16-le") as file :

        return list(map(mktabTrad, file))

def writeTab(path, tab):
    ''' write a tab in a file '''
    with open(path, "w", encoding="utf-16-le") as file :

        for elem in tab[:-1]:
            file.write('\t'.join(elem) + '\n')
        
        file.write('\t'.join(tab[-1]))

def stringToNumber(string):
    ''' find a number in a string and return it in a type float '''
    return float(findall(r'[-+]?\d*\.\d+|\d+', string)[0])

def write(path, string):
    ''' write something writable in a file '''
    with open(path, 'w', encoding='utf-16-le') as file:
        file.write(string)

def mkNames(tab):
    ''' make all formated name '''
    return list(map(mkname, tab))

def mkname(elem):
    ''' make formated name of an elem of revit file ''' 
    return [elem[index_revit_zone] + '_' + elem[index_revit_name] + '_' + elem[index_revit_param],
            elem[index_revit_q1],
            elem[index_revit_dim1],
            elem[index_revit_q2],
            elem[index_revit_dim2]]

def itemNotInTab(tab, name):
    ''' Search if an item is not in the tab in function of his name '''
    for j in range(len(tab)):

        if tab[j][index_revit_name] == name:
            return False
            
    return True

def applyTradFile(INPUT, TRAD):
    '''apply all the changes to send a new tab in excel '''
    OUT = []
    bitNoModified = [1]*len(INPUT)
    IN = mkNames(INPUT)
    warningsElemMissing = ''
    warningsNoModif = ''

    for elem in TRAD[2:]:

        if len(elem) != 7:
            raise ColumnError('''Les collones du fichier de traduction.txt ne sont pas complète
                               \nS.v.p verrifier que les lignes contiennent bien 7 collonne!
                               \nou que celle-ci ne sont pas séparée par des tabulations!''')

        #elem marked as important in tradfile and missing in revit file
        if int(elem[index_trad_check]) == 1 and itemNotInTab(INPUT, elem[index_trad_name]):
            warningsElemMissing += '''[{}]\t missing\r\n'''.format(elem[index_trad_name])

        iterIndex = (j for j in range(len(INPUT)) if (INPUT[j][index_revit_name] == elem[index_trad_name] and
                                                      INPUT[j][index_revit_param] == elem[index_trad_param]))

        for index in iterIndex:
            bitNoModified[index] = 0

            #0='pce'; 1='m'
            if int(elem[index_trad_dim]) in (0,1) :
                OUT.append([elem[index_trad_ref],
                            elem[index_trad_descr],
                            str(float(elem[index_trad_form])*stringToNumber(IN[index][index_re_q1])),
                            elem[index_trad_dim],
                            IN[index][index_re_name]])
            
            #2='m²'; 3='m³'
            else :
                OUT.append([elem[index_trad_ref],
                            elem[index_trad_descr],
                            str(float(elem[index_trad_form])*stringToNumber(IN[index][index_re_q2])),
                            elem[index_trad_dim],
                            IN[index][index_re_name]])

    for index, elem in enumerate(bitNoModified) :
        #elem ignore by trad file (no modif)
        if elem:
            OUT.append(['??????????????',
                        IN[index][index_re_name],
                        IN[index][index_re_q1],
                        IN[index][index_re_dim1],
                        '/!\ aucune traduction trouvé dans le fichier de trad'])
            warningsNoModif += '''[{}]\t:\t\tquantité 1:\t\t{}{};\tquantité 2:\t\t{}{};\r\n'''.format(IN[index][index_re_name],
                                                                                                      IN[index][index_re_q1],
                                                                                                      IN[index][index_re_dim1],
                                                                                                      IN[index][index_re_q2],
                                                                                                      IN[index][index_re_dim2])

    return OUT, warningsElemMissing, warningsNoModif