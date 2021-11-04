PARSING_TABLE = {
    "variable": lambda x: x.isalnum() and x[0].isalpha(),
    "number": lambda x: x.isdecimal(),
    "l_parenthesis": lambda x: x == '(',
    "r_parenthesis": lambda x: x == ')',
    "add": lambda x: x == '+',
    "multiply": lambda x: x == '*',
    "subtract": lambda x: x == '-',
    "divide": lambda x: x == '/'
}


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
    pos = 0
    while pos < len(sentence):
        result = scanner(sentence, pos)
        print(result[0] + " | " + result[1])
        pos = result[2]


phrase = "123*z1+2*(27-y22)"

parser(phrase)


# zbudowac parser/skaner do kolorowania skladni dla wybranego formatu np. c zapisany w txt

