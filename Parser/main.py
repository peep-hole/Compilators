from termcolor import colored
from copy import deepcopy

TOKENS_TABLE = {
    "comment": lambda x: x[0] == '#',
    "spaces": lambda x: True if all([True if el in [' ', '\n', '\t'] else False for el in x]) else False,
    "key_words": lambda x: x in ['if', 'for', 'in', 'while', 'None', 'not', 'return', 'else', 'then'],
    "boolean": lambda x: x in ['True', 'False'],
    "variable": lambda x: x.isalnum() and x[0].isalpha(),
    "number": lambda x: x.isdecimal(),
    "float": lambda x: len(x.split('.')) == 2 and x.split('.')[0].isdecimal() \
        and (x.split('.')[1].isdecimal() or x.split('.')[1] == ''),
    "hexadecimal": lambda x: len(x) > 1 and x[0] == '0' and x[1] == 'x' and \
        all([l.isdigit() or l in ['A', 'B', 'C', 'D', 'E', 'F'] for l in x[2:]]),
    "exponencial": lambda x: not x,
    "l_parenthesis": lambda x: x == '(',
    "r_parenthesis": lambda x: x == ')',
    "add": lambda x: x == '+',
    "multiply": lambda x: x == '*',
    "subtract": lambda x: x == '-',
    "divide": lambda x: x == '/',
    "set": lambda x: x == '=',
    "equal": lambda x: x=='==',
    "colon": lambda x: x==':',
    "less_or_equal": lambda x: x == '<=',
    "less": lambda x: x == '<',
    "more_or_equal": lambda x: x == '>=',
    "more": lambda x: x == '>',
    "plus_equal": lambda x: x == '+=',
    "minus_equal": lambda x: x == '-='

}

COLOR_TABLE = {
    "variable": 'blue',
    "number": 'green',
    "key_words": 'magenta',
    "float": 'cyan',
    "boolean": 'green',
    "hexadecimal": 'cyan',
    "comment": 'grey'
}

HTML_COLOR_TABLE = {
    "variable": '#0017FF',
    "number": '#009B46',
    "key_words": '#F501D4',
    "float": '#0AE5EC',
    "boolean": '#009B46',
    "hexadecimal": '#0AE5EC',
    "comment": '#9E9E9E'
}

def init_html(f):
    f.write('<html>')
    f.write("\n")

def close_htm(f):
    f.write("<p><p\>")
    f.write("\n")
    f.write('</html>')   

def writ_color_to_html(f, color, text):
    content = deepcopy(text)
    content = content.replace("\t", "&emsp;")
    content = content.replace(" ", "&nbsp;")
    f.write(f'<span style="color:{color}">{content}</span>')
    f.write("\n")

def check_number_and_variable_spacing(sentence, index):
    return False


def check(buffer):
    for key, value in TOKENS_TABLE.items():
        if value(buffer):
            return key
    return None


def scanner(sentence, pos):
    buffer = ""
    last_res = ""
    check_buffer = ""
    act_pos = 0
    for i in range(pos, len(sentence)):
        check_buffer += sentence[i]
        res = check(check_buffer)
        if res is None:
            return buffer, last_res, i
        last_res = res
        buffer += sentence[i]
        act_pos = i
    return buffer, last_res, act_pos + 1


def scan(sentence, debug=False, to_html=False, html_name='result.html'):
    last_len = 0
    last = 'none'
    pos = 0
    if to_html:
        f = open(html_name, "a")
        init_html(f)
    while pos < len(sentence):
        result = scanner(sentence, pos)
        if result[0] == result[1] == '':
            raise NameError(
                f"{sentence}\n{' ' * 11 + ' ' * result[2] + '^'}\nUnknown type of token in column {result[2]}")
        if result[1] == 'variable' and last == 'number':
            raise NameError(
                f"{sentence}\n{' ' * 11 + ' ' * (result[2]-len(result[0])-last_len) + '^'}\nVariable name can't start with number")
        if debug:
            print(f"{result[0]} | {result[1]}")
        elif to_html:
            color = HTML_COLOR_TABLE[result[1]] if result[1] in COLOR_TABLE else None
            if color is None:
                writ_color_to_html(f, "#000000", result[0])
            else:
                writ_color_to_html(f, color, result[0])
        else:
            color = COLOR_TABLE[result[1]] if result[1] in COLOR_TABLE else None
            if color is None:
                print(result[0], end='')
            else:
                print(colored(result[0], color), end='')    
        pos = result[2]
        last = result[1]
        last_len = len(result[0])
    if to_html:
        close_htm(f)
        f.close()


def read_file_line_by_line(file):
    f = open(file)

    lines = f.readlines()

    for line in lines:
        scan(line, to_html=True)

    print("\n")

    f.close()


read_file_line_by_line("./Parser/ex.txt")

