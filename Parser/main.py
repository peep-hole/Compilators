PARSING_TABLE = {
    "spaces": lambda x: True if all([True if el in [' ', '\n', '\t'] else False for el in x]) else False,
    "variable": lambda x: x.isalnum() and x[0].isalpha(),
    "number": lambda x: x.isdecimal(),
    "l_parenthesis": lambda x: x == '(',
    "r_parenthesis": lambda x: x == ')',
    "add": lambda x: x == '+',
    "multiply": lambda x: x == '*',
    "subtract": lambda x: x == '-',
    "divide": lambda x: x == '/'
}


def check_number_and_variable_spacing(sentence, index):
    return False


def check(buffer):
    for key, value in PARSING_TABLE.items():
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


def parser(sentence):
    last_len = 0
    last = 'none'
    pos = 0
    while pos < len(sentence):
        result = scanner(sentence, pos)
        if result[0] == result[1] == '':
            raise NameError(
                f"{sentence}\n{' ' * 11 + ' ' * result[2] + '^'}\nUnknown type of token in column {result[2]}")
        if result[1] == 'variable' and last == 'number':
            raise NameError(
                f"{sentence}\n{' ' * 11 + ' ' * (result[2]-len(result[0])-last_len) + '^'}\nVariable name can't start with number")
        print(result[0] + " | " + result[1])
        pos = result[2]
        last = result[1]
        last_len = len(result[0])


phrase = "123 * 12z1 + 2 * (27 - y22)"


parser(phrase)





# zbudowac parser/skaner do kolorowania skladni dla wybranego formatu np. c zapisany w txt

