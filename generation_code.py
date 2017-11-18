"""
    @file generation_code.py
    @brief Implement of generator of code
    @author Alexandr Ivanov (alexandr.ivanov.1995@gmail.com)
"""

from tab import Tab


def generation_code(tree):
    list_ident = []
    code = ''
    data = ''
    tree = tree[1][0][1]
    name = Tab.identifier_tab.get(tree[0][1][0])
    code += '@' + name + ':\n'
    list_ident.append(tree[0][1][0])
    tree = tree[1][1]

    tree2 = tree[0][1]
    if tree2 != (6, 2):
        tree2 = tree2[0]
        if tree2[0] == (6, 1) and tree2[1] != (7, 2):
            tree2 = tree2[1][0]
            tree3 = tree2
            row = 3
            while 1:

                tree3 = tree3[1][0][1]

                ident = Tab.identifier_tab.get(tree3[0][1][0])
                if ident in list_ident:
                    error = "SEMANTIC ERROR in line " + str(row) + " : identifier '" \
                            + ident + "' is already being used"
                    return [error, row], 1
                list_ident.append(ident)
                data += "  " + ident
                cons = int(Tab.constant_tab.get(tree3[1][1][0]))
                if cons > 4294967295:
                    error = "SEMANTIC ERROR in line " + str(row) + " : " \
                            + str(Tab.constant_tab.get(tree3[1][1][0])) + " not unsigned integer"
                    return [error, row], 1
                if cons > 65536:
                    reg = "ebx"
                    data += " dd "
                else:
                    reg = "bx"
                    data += " db "

                tree3 = tree3[2][1]
                n1 = int(Tab.constant_tab.get(tree3[0]))
                n2 = int(Tab.constant_tab.get(tree3[1]))

                if n1 > 65536:
                    error = "SEMANTIC ERROR in line " + str(row) + " : " \
                            + str(Tab.constant_tab.get(tree3[0])) + " not unsigned integer"
                    return [error, row], 1
                if n2 > 65536:
                    error = "SEMANTIC ERROR in line " + str(row) + " : " \
                            + str(Tab.constant_tab.get(tree3[1])) + " not unsigned integer in"
                    return [error, row], 1
                if n2 < n1:
                    error = "SEMANTIC ERROR in line " + str(row) + " : " + str(Tab.constant_tab.get(tree3[1])) \
                            + " must be larger than " + str(Tab.constant_tab.get(tree3[0]))
                    return [error, row], 1
                n2 -= n1
                data += str(n2) + " dup (?)\n"
                code += "  mov cx," + str(n2) + "\n"
                code += "  mov si,0\n"
                code += "  mov " + reg + "," + str(cons) + "\n"
                code += "  @loop_" + ident + ":\n"
                code += "    mov " + ident + "[si],bx\n"
                code += "    inc si\n"
                code += "  loop @loop_" + ident + "\n"
                tree2 = tree2[1][1]
                tree3 = tree2
                row += 1
                if tree3 == (7, 2):
                    break

    code += "  nop\n"
    code += "end @" + name

    result = ".data\n" + data + "\n.code\n" + code
    return result, 0
