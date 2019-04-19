__version__ = '0.2'
__author__ = 'Thibault Delvaux,             \
             <thibaultdelvaux@outlook.fr>,  \
             <0484381244>'

from package1 import function as fn

#if you want to modify/use that software, please mention my name in your version.

tradFilePath = "TXT/trad.txt"
nomenclatureFilePath = "TXT/ME_CS_Canalisations.txt"
nomenclatureModifiedPath = "TXT/ME_CS_test2.txt"
detailsAndErrPath = "TXT/Details_and_errors.txt"

details = ''
error = ''  

problem = 0

def main(details, error):
    #1. load tab from C3A txt file
    tabREVIT = fn.createTab(nomenclatureFilePath)
    details += '1.\tVotre nomenclature a été importée pour modification.\n'
    #2. load tab for translating
    tabTRAD = fn.createTab(tradFilePath)
    details += '2.\tLe tableau de traduction a été chargé.\n'
    #3. sum by ref_revit/system/param/zone
    tabSUM = fn.sum(tabREVIT)
    details += '3.\tLes éléments du tableau revit ont été additionnés en fonction de la reférence Revit, du paramètre, du système et de la zone\n'
    #4. apply translating
    tabXLS, dicoDetails = fn.applyTabTrad(tabSUM, tabTRAD)
    details += '4.\tLes changements ont été appliqués, voir les détails ci-dessous : \r\n\r\n'
    details += '------------------------------------------------------------------------ \r\n\r\n'
    details += fn.showDetails(dicoDetails)
    tabXLS = fn.sum2(tabXLS)


    return tabXLS, details, error

try :

    if __name__ == '__main__' :
        tabXLS, details, error = main(details, error)
        fn.writeTab(nomenclatureModifiedPath, tabXLS)

#  /!\ get the most part of errors but not all /!\
except Exception as e :
    error += "Voici les erreurs qui se sont produites :\r\n"
    error += "{} : {}\r\n".format(e.__doc__, e)
    problem = 1

finally :
    DetErr = error + '\r\n -------------------------------------------------------------------- \r\n' + details

    if problem:
        print("problem occured")
        DetErr = "le programme n\'a pas abouti, veuillez lire la doc ci-dessous pour comprendre pourquoi :\r\n\r\n" + DetErr

    else :
        print("Ok")
        DetErr = 'Le programme a abouti:\r\n\r\n' + DetErr

    fn.write(detailsAndErrPath,DetErr)