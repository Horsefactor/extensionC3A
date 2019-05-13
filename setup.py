from cx_Freeze import setup, Executable

setup(
    name='TraductionCC',
    version = '0.6',
    description="GUI for the software traductionCC wich provides a translating of a Revit file and manage data's"
    executables=[Executable("extensionC3A.py")]
)