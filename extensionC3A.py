__version__ = '0.5'
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
problem = 0
app = App()

try :
    if __name__ == '__main__' :
        app.mainloop()
        
#/!\ catch the most part (all non-exit exception) but not all /!\
except Error as e :
    error += e.msg
    problem = 1

except Exception as e :
    error += "Des erreurs se sont produites :\r\n"
    error += "{} : {}\r\n".format(e.__doc__, e)
    problem = 1

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
        print("problem occured")
        DetErr = "le programme n\'a pas abouti, veuillez lire la doc ci-dessous pour comprendre pourquoi :\r\n\r\n" + DetErr

    else:
        print("Ok")
        DetErr = 'Le programme a abouti:\r\n\r\n' + DetErr

    app.writeDetails(DetErr)