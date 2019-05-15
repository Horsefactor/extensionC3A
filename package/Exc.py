__date__= '<15/05/2019>'
__author__ = 'Thibault Delvaux,             \
             <thibaultdelvaux@outlook.fr>,  \
             <0484381244>'

class Error(Exception):
    '''error to raise a msg'''
    def __init__(self, msg):
        self.msg = msg

    def handle(self):
        print(self.msg)




