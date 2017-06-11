def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
        if index < len(line) and line[index] == '.':
            index += 1
            keta = 0.1
            while index < len(line) and line[index].isdigit():
                number += int(line[index]) * keta
                keta *= 0.1
                index += 1
        token = {'type': 'NUMBER', 'number': number}
        return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def readMul(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1


def readDiv(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1




def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMul(line, index)
        elif line[index] == '/':
            (token, index) = readDiv(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens


def evaluate_first(tokens):    # *, /, . make token
    first_tokens = []
    first_index = 1
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    t_index = 1
 #   print tokens
    while t_index < len(tokens):
       # print 'type'+tokens[t_index-1]['type']
        if tokens[t_index]['type'] == 'NUMBER':
            if tokens[t_index - 1]['type'] == 'MULTIPLY':
                first_tokens.pop()
                (token,index)=({'type': 'NUMBER', 'number':tokens[t_index-2]['number'] * tokens[t_index]['number']},first_index-1)  
            elif tokens[t_index - 1]['type'] == 'DIVIDE':
                first_tokens.pop()
                (token,index)=({'type': 'NUMBER', 'number':tokens[t_index-2]['number'] / tokens[t_index]['number']},first_index-1)
            elif tokens[t_index - 1]['type'] == 'PLUS':
                (token,index)=({'type':'PLUS'},first_index-1)
                first_tokens.append(token)
                (token,index)=({'type':'NUMBER','number':tokens[t_index]['number']},first_index)
                first_index += 1
            elif tokens[t_index - 1]['type'] == 'MINUS':
                (token,index)=readMinus(tokens,first_index-1)
                first_tokens.append(token)
                (token,index)=({'type':'NUMBER','number':tokens[t_index]['number']},first_index)
                first_index += 1
            else:
                print 'Invalid syntax'
            first_tokens.append(token)
     #   print first_tokens
        t_index += 1
                        #    first_index += 1
    return first_tokens


def evaluate_second(tokens):   # +, -
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
#    print len(tokens)
    while index < len(tokens):
 #       print tokens[index]
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
               # print tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']

            else:
                print 'Invalid syntax'
        index += 1
    return answer


def evaluate(tokens):
    first_result=evaluate_first(tokens)
    answer=evaluate_second(first_result)
    return answer


def test(line, expectedAnswer):
    tokens = tokenize(line)
    actualAnswer = evaluate(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1",1)
    test("2+1", 3)
    test("2-1",1)
    test("2*1",2)
    test("2/1",2)

    test("2.0+1", 3)
    test("2.0-1",1)
    test("2.0*1",2)
    test("2.0/1",2)

    test("2.0+1.0", 3)
    test("2.0-1.0",1)
    test("2.0*1.0",2)
    test("2.0/1.0",2)

    test("2.2+1",3.2)
    test("2.2-1",1.2)
    test("2.2*1",2.2)
    test("2.2/1",2.2)

    test("2.2+1.0",3.2)
    test("2.2-1.0",1.2)
    test("2.2*1.0",2.2)
    test("2.2/1.0",2.2)

#    test("1.0+2.1-3", 0.1)
    test("1.0+2.1*3", 7.3)
    test("1.0-2.1*3",-5.3)
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print "answer = %f\n" % answer
