from tab import Tab
__author__ = 'alexandr'

error_list = []
result = []
row = 1
tab_row = {}
flag_row = False
flag_comment = False


def error(type_error, char=0):
    if type_error is 6:
        error_list.append(["Error: Unknown character '" + chr(char) + "' in row " + str(row), row])
    if type_error is 4:
        error_list.append(["Error: a comment is not closed", -1])


def type_chr(char, file_program):
    if char in (32, 9, 10):

        return 0
    elif char in range(65, 91) or char in range(97, 123):
        return 1
    elif char in range(48, 58):
        return 2
    elif char in (59, 46, 61, 92, 44):
        return 3
    elif char is 40:
        if ord(file_program.read(1)) is 42:
            return 4
        else:
            if not flag_comment:
                error(6, char)
            return 6
    elif char is 42:
        if ord(file_program.read(1)) is 41:
            return 5
        else:
            if not flag_comment:
                error(6, char)
            return 6
    else:
        if not flag_comment:
            error(6, char)
        return 6


def identificator(lex):
    global result
    if lex in Tab.direction_tab.keys():
        result.append(Tab.direction_tab.get(lex))
    elif lex in Tab.identificator_tab.keys():
        result.append(Tab.identificator_tab[lex])
    else:
        code = 1001 + len(Tab.identificator_tab)
        Tab.identificator_tab[lex] = code
        result.append(code)



def number(lex):
    global result
    if lex in Tab.constant_tab.keys():
        result.append(Tab.constant_tab.get(lex))
    else:
        code = 501 + len(Tab.constant_tab)
        Tab.constant_tab[lex] = code
        result.append(code)


def delimiter(lex):
    global result
    result.append(ord(lex))


def get_identificator(lex, file_program):
    next_char = ' '
    global flag_row
    while 1:
        char = file_program.read(1)
        type_char = type_chr(ord(char), file_program)
        if char == '\n':
            flag_row = True
        if type_char in (1, 2):
            lex += char
        elif type_char is 4:
            comment(file_program)
        else:
            next_char = char
            break
    return lex, next_char


def get_number(lex, file_program):
    next_char = ' '
    global flag_row
    while 1:
        char = file_program.read(1)
        type_char = type_chr(ord(char), file_program)
        if char == '\n':
            flag_row = True
        if type_char is 2:
            lex += char
        elif type_char is 4:
            comment(file_program)
        else:
            next_char = char
            break
    return lex, next_char


def comment(file_program):
    global flag_comment, row
    flag_comment = True
    while flag_comment:
        char = file_program.read(1)
        if char == '\n':
            result.append('\n')
            row += 1
        if not char:
            error(4)
            break
        if type_chr(ord(char), file_program) is 5:
            flag_comment = False
            break


def get_lexem(type_lex, let, file_program):
    lex = let
    next_char = ' '
    if type_lex is 1:
        lex, next_char = get_identificator(lex, file_program)
    elif type_lex is 2:
        lex, next_char = get_number(lex, file_program)
    elif type_lex is 4:
        comment(file_program)
    elif type_lex is 0:
        lex = ''
    return lex.upper(), next_char


def add_lexem(lex, type_lex):
    if type_lex is 1:
        identificator(lex)
    elif type_lex is 2:
        number(lex)
    elif type_lex is 3:
        delimiter(lex)


def lex_analyzer(file_name):
    file_program = open(file_name)
    global row, flag_row
    while 1:
        character = file_program.read(1)
        if not character:
            break

        if character == '\n':
            result.append('\n')
            row += 1
        type_lexem = type_chr(ord(character), file_program)
        lexem, next_character = get_lexem(type_lexem, character, file_program)

        if lexem is not '':
            add_lexem(lexem, type_lexem)
        if ord(next_character) in Tab.delimiter_tab:
            add_lexem(next_character, 3)

        if flag_row == True:
            flag_row = False
            result.append('\n')
            row += 1

    file_program.close()
    result.append('#')
    if len(error_list) is 0:
        print("Direction: ", Tab.direction_tab)
        print("Identificator: ", Tab.identificator_tab)
        print("Number: ", Tab.constant_tab)
        print("Result: ", result)
    else:
        for err in error_list:
            return err, 1

    sub_dict = {}
    for key, value in Tab.identificator_tab.items():
        sub_dict[value] = key
    Tab.identificator_tab = sub_dict

    sub_dict = {}
    for key, value in Tab.constant_tab.items():
        sub_dict[value] = key
    Tab.constant_tab = sub_dict

    return result, 0
