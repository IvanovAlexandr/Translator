"""
    @file tab.py
    @brief Structure containing the tokens of the language
    @author Alexandr Ivanov (alexandr.ivanov.1995@gmail.com)
"""


class Tab:
    direction_tab = {"PROGRAM": 401, "BEGIN": 402, "END": 403, "DEFFUNC": 404, "PROCEDURE": 405}
    identifier_tab = {}
    constant_tab = {}
    delimiter_tab = (59, 46, 61, 92, 44)
