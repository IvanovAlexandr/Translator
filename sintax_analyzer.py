from tab import Tab

__author__ = 'alexandr'

START = 0
SIGNAL_PROGRAM = 1
PROGRAM = 2
BLOCK = 3
STATEMENTS_LIST = 4
DECLARATIONS = 5
MATH_FUNCTION_DECLARATIONS = 6
FUNCTION_LIST = 7
FUNCTION = 8
FUNCTION_CHARACTERISTIC = 9
CONSTANT = 10
PROCEDURE_IDENTIFIER = 11
FUNCTION_IDENTIFIER = 12
IDENTIFIER = 13
UNSIGNED_INTEGER = 14


EMPTY = -1
amk = {START: [[SIGNAL_PROGRAM, 1, False],
               ['#', True, False]],
       SIGNAL_PROGRAM: [[PROGRAM, True, False]],
       PROGRAM: [[401, 1, False],
                 [PROCEDURE_IDENTIFIER, 2, False],
                 [59, 3, False],

                 [BLOCK, 4, False],
                 [46, True, False]],
       BLOCK: [[DECLARATIONS, 1, False],
               [402, 2, False],
               [STATEMENTS_LIST, 3, False],
               [403, True, False]],
       STATEMENTS_LIST: [[EMPTY, True, True]],
       DECLARATIONS: [[MATH_FUNCTION_DECLARATIONS, True, False]],
       MATH_FUNCTION_DECLARATIONS: [[404, 1, 2],
                                    [FUNCTION_LIST, True, False],
                                    [EMPTY, True, True]],
       FUNCTION_LIST: [[FUNCTION, 1, 2],
                       [FUNCTION_LIST, True, False],
                       [EMPTY, True, True]],
       FUNCTION: [[FUNCTION_IDENTIFIER, 1, False],
                  [61, 2, False],
                  [CONSTANT, 3, False],
                  [FUNCTION_CHARACTERISTIC, 4, False],
                  [59, True, False]],
       FUNCTION_CHARACTERISTIC: [[92, 1, False],
                                 [UNSIGNED_INTEGER, 2, False],
                                 [44, 3, False],
                                 [UNSIGNED_INTEGER, True, False]],
       CONSTANT: [[UNSIGNED_INTEGER, True, False]],
       PROCEDURE_IDENTIFIER: [[IDENTIFIER, True, False]],
       FUNCTION_IDENTIFIER: [[IDENTIFIER, True, False]]
       }

dg_to_w = {(1, 0): "<SIGNAL_PROGRAM>",
           (2, 4): "<PROGRAM> PROGRAM",
           (3, 3): "<BLOCK> .",
           (4, 0): ["BEGIN <STATEMENTS_LIST> END .", ["EMPTY"]],
           (5, 0): "<DECLARATIONS> ",
           (5, 1):"<DECLARATIONS>",
           (6, 1): "<MATH_FUNCTION_DECLARATIONS> DEFFUNC",
           (6, 2): ["<MATH_FUNCTION_DECLARATIONS>", ["EMPTY"]],
           (7, 1): "<FUNCTION_LIST>",
           (7, 2): ["<FUNCTION_LIST>", ["EMPTY"]],
           (8, 4): "<FUNCTION> ",
           (9, 3): "<FUNCTION_CHARACTERISTIC> ;",
           (10, 0): "<CONSTANT>",
           (11, 0): "<PROCEDURE_IDENTIFIER>  ",
           (12, 0): "<FUNCTION_IDENTIFIER> = ",
           (15, 3): ["<PROCEDURE>", ["PROCEDURE <procedure-ident>"]],
           (16, 0): ["<PARAMETER-LIST> ;", ["EMPTY"]]}
error_text = ''


def error(lexem, row):
    global error_text
    error_text = ["Syntax error line(" + str(row) + "): invalid syntax -> " + str(lexem), row]


def sintax_analyzer(list_lexem):
    stack_index = []
    result = -1
    sub_tree = {}
    second_tree = {}
    row = 1
    list_lexem.reverse()

    index = START
    last_index = index
    lexem = len(list_lexem) - 1
    i = 0
    while list_lexem[lexem] == '\n':
        list_lexem.pop()
        lexem -= 1
    while 1:
        if result == True:
            if isinstance(amk[index][i][1], bool):
                l = len(stack_index) - 1

                if l in sub_tree:
                    st = sub_tree.pop(l)
                    st2 = second_tree.pop(l)
                    if l < last_index:
                        st.append([dg_to_w[(index, i)], sub_tree.pop(last_index)])
                        st2.append([(index, i), second_tree.pop(last_index)])
                    else:
                        st.append(dg_to_w[(index, i)])
                        st2.append((index, i))
                else:
                    if l < last_index:
                        st = [[dg_to_w[(index, i)], sub_tree.pop(last_index)]]
                        st2 = [[(index, i), second_tree.pop(last_index)]]
                    else:
                        st = dg_to_w[(index, i)]
                        st2 = (index, i)

                sub_tree[l] = st
                second_tree[l] = st2
                last_index = l
                index, i = stack_index.pop()
                result = True
                continue
            else:
                i = amk[index][i][1]

        elif result == False:
            if isinstance(amk[index][i][2], bool):
                if amk[index][i][2] == True:
                    result = True
                    l = len(stack_index) - 1
                    if l in sub_tree:
                        st = sub_tree.pop(l)
                        st2 = second_tree.pop(l)
                        st.append(dg_to_w[(index, i)])
                        st2.append((index, i))
                    else:
                        st = [[dg_to_w[(index, i)], sub_tree.pop(last_index)]]
                        st2 = [[(index, i), second_tree.pop(last_index)]]
                    sub_tree[l] = st
                    second_tree[l] = st2
                else:
                  #  pass
                    error(list_lexem[lexem], row)
                    result = False

                if len(stack_index) != 0:
                    index, i = stack_index.pop()
                else:
                    break
                continue
            else:
                i = amk[index][i][2]

        result = -1

        if index == EMPTY:
            result = True
            index, i = stack_index.pop()
            continue

        if index == IDENTIFIER:
            if list_lexem[lexem] in Tab.identificator_tab:
                lex = list_lexem.pop()
                l = len(stack_index) - 1
                if l in sub_tree:
                    st = sub_tree.pop(l)
                    st2 = second_tree.pop(l)
                    st.append(Tab.identificator_tab[lex])
                    st2.append(lex)
                else:
                    st = [Tab.identificator_tab[lex]]
                    st2 = [lex]
                last_index = l
                sub_tree[l] = st
                second_tree[l] = st2
                lexem -= 1
                while list_lexem[lexem] == '\n':
                    row += 1
                    list_lexem.pop()
                    lexem -= 1
                result = True
            else:
                error(list_lexem[lexem], row)
                result = False

            index, i = stack_index.pop()
            continue

        if index == UNSIGNED_INTEGER:
            if list_lexem[lexem] in Tab.constant_tab:
                lex = list_lexem.pop()
                l = len(stack_index) - 1
                if l in sub_tree:
                    st = sub_tree.pop(l)
                    st2 = second_tree.pop(l)
                    st.append(Tab.constant_tab[lex])
                    st2.append(lex)
                else:
                    st = [Tab.constant_tab[lex]]
                    st2 = [lex]
                sub_tree[l] = st
                second_tree[l] = st2
                last_index = l
                lexem -= 1
                while list_lexem[lexem] == '\n':
                    row += 1
                    list_lexem.pop()
                    lexem -= 1
                result = True
            else:
                error(list_lexem[lexem], row)
                result = False

            index, i = stack_index.pop()
            continue

        if amk[index][i][0] == '#':
            if amk[index][i][0] == list_lexem[lexem]:
                result = True
            else:
                error(list_lexem[lexem], row)
                result = False
            break

        if amk[index][i][0] < 15:
            stack_index.append([index, i])
            index = amk[index][i][0]
            i = 0
            continue

        if amk[index][i][0] == list_lexem[lexem]:
            list_lexem.pop()
            lexem -= 1
            while list_lexem[lexem] == '\n':
                row += 1
                list_lexem.pop()
                lexem -= 1
            if isinstance(amk[index][i][1], bool):
                l = len(stack_index) - 1
                if l in sub_tree:
                    st = sub_tree.pop(l)
                    st2 = second_tree.pop(l)
                    st.append([dg_to_w[(index, i)], sub_tree.pop(last_index)])
                    st2.append([(index, i), second_tree.pop(last_index)])
                else:
                    st = [[dg_to_w[(index, i)], sub_tree.pop(last_index)]]
                    st2 = [[(index, i), second_tree.pop(last_index)]]
                sub_tree[l] = st
                second_tree[l] = st2
                last_index = l
                index, i = stack_index.pop()
                result = True
                continue
            else:
                i = amk[index][i][1]
                continue
        else:
            if isinstance(amk[index][i][2], bool):
                if amk[index][i][2] == True:
                    result = True
                    l = len(stack_index) - 1
                    if l in sub_tree:
                        st = sub_tree.pop(l)
                        st2 = second_tree.pop(l)
                        st.append([dg_to_w[(index, i)], sub_tree.pop(last_index)])
                        st2.append([(index, i), second_tree.pop(last_index)])
                    else:
                        st = [[dg_to_w[(index, i)], sub_tree.pop(last_index)]]
                        st2 = [[(index, i), second_tree.pop(last_index)]]
                    sub_tree[l] = st
                    second_tree[l] = st2
                    last_index = l
                else:
                    error(list_lexem[lexem], row)
                    result = False

                index, i = stack_index.pop()
                continue
            else:
                i = amk[index][i][2]
                continue
    """
    print(result)
    print("\n")
    if result == True:
        tree = sub_tree[0][0]
        print("<START>")
        print_tree(tree)
    else:
        print(error_text)
   """
    if result:
        return second_tree[0][0], 0
    else:
        return error_text, 1


















def print_tree(tree, t=0):

    if isinstance(tree, list):
        for i in tree:
            print_tree(i, t+1)
    else:
        st = ''
        for i in range(t):
            st += "  "

        st1 = st + str(tree)
        print(st + "↓")
        print(st1)
        st += "   "

