"""
    @file main.py
    @brief Translator from Signal to Assembler
    @author Alexandr Ivanov (alexandr.ivanov.1995@gmail.com)
"""

import lex_analyzer as la
import syntax_analyzer as sa
import generation_code as gc
from tab import Tab

file_name = "example/program"


def create_listing(file_name, error = 0):
    source_file = open(file_name, 'r')
    listing_file = open(file_name + ".lst", 'w')
    listing_file.write("       LISTING\n\n")
    if error == 0:
        row = 1
        while 1:
            line = source_file.readline()
            if not line:
                break
            listing_file.write(str(row) + ")  " +line)
            row += 1
    else:
        row = 1
        while 1:
            line = source_file.readline()
            if not line:
                break
            listing_file.write(str(row) + ")  " +line)
            if row == error[1]:
                listing_file.write(error[0] + '\n')
            row += 1

    listing_file.write("-----------------------------------------------------------------------\n")
    listing_file.write("IDENTIFICATORS:\n")
    listing_file.write("IDENTIFICATOR\t\tCODE\n")
    for key, value in Tab.identifier_tab.items():
        listing_file.write(str(value) + "\t\t|\t\t" + str(key) + '\n')

    listing_file.write("-----------------------------------------------------------------------\n")
    listing_file.write("CONSTANTS:\n")
    listing_file.write("NUMBER\t\t\tCODE\n")
    for key, value in Tab.constant_tab.items():
        listing_file.write(str(value) + "\t\t|\t\t" + str(key) + '\n')


    listing_file.close()
    source_file.close()


def main():
    row_lexem, code = la.lex_analyzer(file_name)
    if code == 0:
        tree, code = sa.syntax_analyzer(row_lexem)
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


if __name__ == "__main__":
    main()
