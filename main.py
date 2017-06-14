import lex_analyzer as la
import sintax_analyzer as sa
import generation_code as gc
from tab import Tab
__author__ = 'alexandr'

file_name = "program"


def create_listing(file_name, error = 0):
    f1 = open(file_name, 'r')
    f = open(file_name + ".lst", 'w')
    f.write("       LISTING\n\n")
    if error == 0:
        row = 1
        while 1:
            line = f1.readline()
            if not line:
                break
            f.write(str(row) + ")  " +line)
            row += 1
    else:
        row = 1
        while 1:
            line = f1.readline()
            if not line:
                break
            f.write(str(row) + ")  " +line)
            if row == error[1]:
                f.write(error[0] + '\n')
            row += 1

    f.write("-----------------------------------------------------------------------\n")
    f.write("IDENTIFICATORS:\n")
    f.write("IDENTIFICATOR\t\tCODE\n")
    for key, value in Tab.identificator_tab.items():
        f.write(str(value) + "\t\t|\t\t" + str(key) + '\n')

    f.write("-----------------------------------------------------------------------\n")
    f.write("CONSTANTS:\n")
    f.write("NUMBER\t\t\tCODE\n")
    for key, value in Tab.constant_tab.items():
        f.write(str(value) + "\t\t|\t\t" + str(key) + '\n')


    f.close()
    f1.close()



if __name__ == "__main__":
    row_lexem, code = la.lex_analyzer(file_name)
    if code == 0:
        tree, code = sa.sintax_analyzer(row_lexem)
        if code == 0:
            print('\nTree')
            print(tree)
            print('\n')
            asm, code = gc.generation_code(tree)
            if code == 0:
                f = open(file_name + ".asm", 'w')
                f.write(asm)
                f.close()
                create_listing(file_name)
                print("SUCCESSFUL!")
            else:
                print("ERROR")
                print(asm[0])
                create_listing(file_name, asm)

        else:
            print("ERROR")
            print(tree[0])
            create_listing(file_name, tree)
    else:
        print("ERROR")
        print(row_lexem[0])
        create_listing(file_name, row_lexem)



