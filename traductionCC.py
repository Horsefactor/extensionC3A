__version__ = '0.5'
__date__= '<15/05/2019>'
__author__ = 'Thibault Delvaux,             \
             <thibaultdelvaux@outlook.fr>,  \
             <0484381244>'

'''

if you want to use/modify that software, 
please keep mentioning my name in your version !

'''

from getpass import getuser
from datetime import datetime
from package.App import App
import sys

error = ''
userInfo = ''
#bool value to know if a problem occured for adjusting the details file
problem = 0
app = App()

try :
    if __name__ == '__main__' :
        #run the GUI
        app.mainloop()
#if some exception has been raised        
except Error as e :
    error += e.msg
    problem = 1

#/!\ catch the most part (all non-exit exception) but not all /!\
except Exception as e :
    error += "Des erreurs se sont produites :\r\n"
    error += "{} : {}\r\n".format(e.__doc__, e)
    problem = 1

#Put at the end of the program information about modif, 
#who is the user, last change, error, in the details file.
finally :
    now = datetime.today()
    userInfo = '''Date de dernière modification:\t\tLe {}/{}/{}
                  à {}h{}m{}s\nDernier utilisateur a avoir modifié le fichier par l\'application \"traduction cc\":\t{}\n'''.format(now.day,
                                                                                                                                    now.month,
                                                                                                                                    now.year,
                                                                                                                                    now.hour,
                                                                                                                                    now.minute,
                                                                                                                                    now.second,
                                                                                                                                    getuser())
    DetErr = userInfo + error + '\r\n\t ------------------------------------------------------------------------------------------\r\n' + app.details

    if problem:
        DetErr = "le programme n\'a pas abouti, veuillez lire la doc ci-dessous pour comprendre pourquoi :\r\n\r\n" + DetErr

    else:
        DetErr = 'Le programme a abouti:\r\n\r\n' + DetErr

    app.writeDetails(DetErr)