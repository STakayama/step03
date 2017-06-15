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


def readPar_f(line, index):#(
    token = {'type': 'PAR_F'}
    return token, index + 1

def readPar_l(line, index):#)
    token = {'type': 'PAR_L'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index]=='(':
            (token,index)=readPar_f(line,index)
        elif line[index]==')':
            (token,index)=readPar_l(line,index)


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



def evaluate_zero(tokens):# evaluate ( including its internal OK
    zero_tokens=[]
    zero_index=1
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    t_index=1
    while t_index < len(tokens):
        if tokens[t_index]['type'] == 'NUMBER':
            if tokens[t_index-1]['type'] == 'PAR_F':

                if t_index>1:#*( , /( etc use read... other def
                    (token,index)=({'type':tokens[t_index-2]['type']},zero_index)
                    zero_tokens.append(token)
                    zero_index += 1

                par_tokens=[]
                par_f_num=1
                par_l_num=0
                print 'all:',tokens
                par_check=t_index-2

                while tokens[par_check]['type']=='PAR_F':
                    par_tokens.append(tokens[par_check])
                    par_f_num+=1
                    par_check-=1

                
           #     if tokens[t_index-2]['type']=='PAR_F':
            #        par_tokens.append(tokens[t_index-1])
             #       par_f_num+=1
            #    while tokens[t_index]['type']!='PAR_L':
                while par_f_num!=par_l_num:
                    if tokens[t_index]['type']=='PAR_F':
                       par_f_num+=1
                    if tokens[t_index]['type']=='PAR_L':
                       par_l_num+=1
                    par_tokens.append(tokens[t_index])
                    t_index+=1
                par_l_index=t_index-1
                par_result=evaluate(par_tokens)#ok
                print 'par:',par_result,par_tokens
                (token,index)=({'type':'NUMBER','number':par_result},zero_index) 
                zero_index+=1
                
            elif tokens[t_index - 1]['type'] == 'MULTIPLY':
                (token,index)=readMul(tokens,zero_index-1)
                zero_tokens.append(token)
                (token,index)=({'type':'NUMBER','number':tokens[t_index]['number']},zero_index)
                zero_index += 1
            
                        
            elif tokens[t_index - 1]['type'] == 'DIVIDE':
                (token,index)=readDiv(tokens,zero_index-1)
                zero_tokens.append(token)
                (token,index)=({'type':'NUMBER','number':tokens[t_index]['number']},zero_index)
                zero_index += 1

            elif tokens[t_index - 1]['type'] == 'PLUS':
                (token,index)=readPlus(tokens,zero_index-1)
                zero_tokens.append(token)
                (token,index)=({'type':'NUMBER','number':tokens[t_index]['number']},zero_index)
                zero_index += 1
            
            elif tokens[t_index - 1]['type'] == 'MINUS':
                (token,index)=readMinus(tokens,zero_index-1)
                zero_tokens.append(token)
                (token,index)=({'type':'NUMBER','number':tokens[t_index]['number']},zero_index)
                zero_index += 1                
                
            else:
                print 'Invalid syntax'
            zero_tokens.append(token)
       #     print 'zero',zero_tokens
        t_index += 1
    zero_tokens.pop(0)#delete first +

    return zero_tokens




def evaluate_first(tokens):    # *, /, . make token
    first_tokens = []
    first_index = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    t_index = 1
    while t_index < len(tokens):
        if tokens[t_index]['type'] == 'NUMBER':
            if tokens[t_index - 1]['type'] == 'MULTIPLY':
                print 'fi2:',first_index,first_tokens
                print 't_in',t_index,tokens,tokens[t_index]['number']*first_tokens[first_index-1]['number']
                (token,index)=({'type': 'NUMBER', 'number':first_tokens[first_index-1]['number'] * tokens[t_index]['number']},first_index)  
                first_tokens.pop()

            elif tokens[t_index - 1]['type'] == 'DIVIDE':
                (token,index)=({'type': 'NUMBER', 'number':first_tokens[first_index-1]['number'] / tokens[t_index]['number']},first_index)
                first_tokens.pop()

            elif tokens[t_index - 1]['type'] == 'PLUS':
                first_index += 1
                (token,index)=readPlus(tokens,first_index)
                first_tokens.append(token)
                first_index += 1
                (token,index)=({'type':'NUMBER','number':tokens[t_index]['number']},first_index)

            elif tokens[t_index - 1]['type'] == 'MINUS':
                first_index += 1
                (token,index)=readMinus(tokens,first_index)
                first_tokens.append(token)
                first_index += 1
                (token,index)=({'type':'NUMBER','number':tokens[t_index]['number']},first_index)

            else:
                print 'Invalid syntax'
            first_tokens.append(token)
     #   print tokens
        t_index += 1
    return first_tokens


def evaluate_second(tokens):   # +, -
    answer = 0
    print 'second',tokens
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']

            else:
                print 'Invalid syntax'
        index += 1
    return answer


def evaluate(tokens):
    tokens=evaluate_zero(tokens)
    tokens=evaluate_first(tokens)
    answer=evaluate_second(tokens)
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
    print test("(1+2)*3",9)
    print test("3*(1+2)",9)
    print test("3*(1+2)*2",18)
    print test("(1+2)*3+2+1",12)
    print test("(1+2)*3+2*1",11)
    print test("(1+2)*3+2*(7*2+1)",39)  #3*3+2*15 new tokens
    print test("((1+2)+3)*2+1",13)
    print test("(((1+2)*2)+1)*2",14)
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print "answer = %f\n" % answer



'''
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
'''
