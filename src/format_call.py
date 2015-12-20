import re
import os

def find_all_index(arr,item):
    return [i for i,a in enumerate(arr) if a==item]

#-----------------------------------Function Format-----------------------------------
#filenameIn--------input testSample
#filenameOut1------output formatted codes
#filenameOut2------output grammer analysis result
def format_called(filenameIn, *tuple_arg):
    filenameOut1 = tuple_arg[0]
    if len(tuple_arg) == 2:
        filenameOut2 = tuple_arg[1]

    fileReadObj = open(filenameIn)
    fileBeforeFormater = []
    match1_1_list = []
    match1_2_list = []
    match2_list = []
    match4_list = []
    match5_list = []
    match7_list = []
    for fileString in fileReadObj.readlines():
        fileBeforeFormater.append(fileString)

        #-------------------------rule 1-------------------------
        match1_1 = re.match(r'void.*|int.*|long.*', fileString)
        if match1_1:
            match1_1_list.append(fileString)
        else:
            match1_1_list.append('flag')
        match1_2 = re.match(r'void.*\(.*\)|int.*\(.*\)|long.*\(.*\)', fileString)
        if match1_2:
            match1_2_list.append(fileString)
        else:
            match1_2_list.append('flag')

        #-------------------------rule 2-------------------------
        match2 = re.match(r'.+(\(.+\)).+|.+(\(.+\))|(\(.+\)).+|(\(.+\))', fileString)
        if match2:
            match2_list.append(fileString)
        else:
            match2_list.append('flag')

        #-------------------------rule 4-------------------------
        match4 = re.match(r'.+,.+|.+;.+', fileString)
        if match4:
            match4_list.append(fileString)
        else:
            match4_list.append('flag')

        #-------------------------rule 5-------------------------
        match5 = re.match(r'.+do.+|.+else.+|.+if.+|.+for.+|.+while.+|.+else|for.+|int.+{|long.+{|void.+{', fileString)
        if match5:
            match5_list.append(fileString)
        else:
            match5_list.append('flag')

        #-------------------------rule 7-------------------------
        match7 = re.split(r';',fileString)
        if match7:
            match7_list.append(match7)
        else:
            match7_list.append('flag')

    fileReadObj.close()

    #-------------------------rule2-------------------------
    for i in range(len(match2_list)):
        if match2_list[i] != 'flag':
            string = fileBeforeFormater[i]
            j = 0
            while j < len(string):
                if string[j] == '(':
                    k = j+1
                    while string[k] == ' ' or string[k] == '\t' and k < len(string):
                        k = k+1
                    fileBeforeFormater[i] = string[0:j+1] + ' ' + string[k:len(string)]
                elif string[j] == ')':
                    l = j-1
                    while string[l] == ' ' or string[l] == '\t' and k < len(string):
                        l = l-1
                    fileBeforeFormater[i] = string[0:l+1] + ' ' + string[j:len(string)]
                string = fileBeforeFormater[i]
                j = j + 1

    #-------------------------rule 1-------------------------
    for i in range(len(match1_1_list)):
        #make funcName and left bucket in the same line
        if match1_1_list[i] != 'flag' and match1_2_list[i] == 'flag':
            if len(fileBeforeFormater[i]) > 1:
                if (fileBeforeFormater[i])[-2] != ';':#not the declaration of function
                    fileBeforeFormater[i] = (fileBeforeFormater[i])[0:-1] + ' ' + fileBeforeFormater[i+1]
                    fileBeforeFormater[i+1] = ''
        #make a blank between funcName and left bucket
        if match1_1_list[i] != 'flag':
            string = fileBeforeFormater[i]
            k = 0
            for j in range(len(string)):
                if string[j].isalpha():
                    k = j
                if string[j] == '(':
                    fileBeforeFormater[i] = string[0:k+1] + ' ' + string[j:len(string)]

    #-------------------------rule 4-------------------------
    for i in range(len(match4_list)):
        if match4_list[i] != 'flag':
            string = fileBeforeFormater[i]
            j = 0
            while j < len(string)-1:
                if string[j] == ',' or string[j] == ';':
                    k = j + 1
                    while string[k] == ' ':
                        k = k+1
                    fileBeforeFormater[i] = string[0:j+1] + ' ' + string[k:len(string)]
                    string = fileBeforeFormater[i]
                j = j + 1


    #-------------------------rule 6-------------------------
    for i in range(len(fileBeforeFormater)):
        if len(fileBeforeFormater[i]) > 0:
            #delete front-blank
            string = fileBeforeFormater[i]
            j = 0
            while string[j] == ' ' or string[j] == '\t':
                j = j+1;
            if string[j] == ';':
                fileBeforeFormater[i] = ''
            #delete back-blank
            string = fileBeforeFormater[i]
            if len(string) > 1:
                j = len(string)-1
                while string[j] == ' ' or string[j] == '\n' or string[j] == '\t':
                    j = j-1
                k = j-1
                if string[j] == ';':
                    while string[k] == ' ' or string[k] == '\t' or string[k] == ';':
                        k = k-1
                    fileBeforeFormater[i] = string[0:k+1] + ';\n'


    #-------------------------rule 7-------------------------
    for i in range(len(fileBeforeFormater)):
        string = fileBeforeFormater[i]
        if len(match7_list[i]) > 2 and match5_list[i] == 'flag':
            blank_string = '';
            for j in range(len(match7_list[i])-1):
                tmp = (match7_list[i])[j]
                blank_string = blank_string + tmp + ';\n'
            fileBeforeFormater[i] = blank_string

    #-------------------------rule 5-------------------------
    for i in range(len(fileBeforeFormater)):
        if match5_list[i] != 'flag' and len(fileBeforeFormater[i]) > 0:
            string = fileBeforeFormater[i]
            j = 0
            while string[j] != '(' and j < len(string)-1:
                j += 1
            if j != len(string)-1:
                cnt = 1
                while cnt != 0:
                    j += 1
                    if string[j] == '(':
                        cnt += 1
                    if string[j] == ')':
                        cnt -= 1
                #next line
                if string[j+1] == '\n':
                    string2 = fileBeforeFormater[i+1]
                    k = 0
                    if string2 != '' or string2 != '\n':
                        while string2[k] == ' ' or string2[k] == '\t':
                            k = k+1
                        if string2[k] != '{':
                            fileBeforeFormater[i+1] = string2[0:k-1-3] + '{\n' + string2[0:len(string2)] + string2[0:k-1-3] + '}\n'
                #same line
                else:
                    k = j+1
                    while string[k] == ' ' or string[k] == '\t':
                        k = k+1
                    if string[k] == '{':
                        fileBeforeFormater[i] = string[0:k-1] + '\n' + string[k:len(string)]
                    else:
                        fileBeforeFormater[i] = string[0:k-1] + '\n{\n' + string[k:len(string)] + '}\n'
            else:
                #next line
                if string[len(string)-5:len(string)-1] == 'else':
                    string2 = fileBeforeFormater[i+1]
                    k = 0
                    if string2 != '' or string2 != '\n':
                        while string2[k] == ' ' or string2[k] == '\t':
                            k = k+1
                        if string2[k] != '{':
                            fileBeforeFormater[i+1] = string2[0:k-1-3] + '{\n' + string2[0:len(string2)] + string2[0:k-1-3] + '}\n'
                #same line
                else:
                    j = 4
                    while string[j-4:j] != 'else':
                        j = j+1
                    k = j+1
                    while string[k] == ' ' or string[k] == '\t':
                        k = k+1
                    if string[k] == '{':
                        fileBeforeFormater[i] = string[0:k-1] + '\n' + string[k:len(string)]
                    else:
                        fileBeforeFormater[i] = string[0:k-1] + '\n{\n' + string[k:len(string)] + '}\n'



    fileWriteObj = open("../tmp.c", 'w')
    for i in fileBeforeFormater:
        fileWriteObj.write(i)
    fileWriteObj.close()

    match3_1_list = []
    match3_2_list = []
    fileReadObj = open('../tmp.c')
    fileBeforeFormater = []
    for fileString in fileReadObj.readlines():
        fileBeforeFormater.append(fileString)
        #-------------------------rule 3-------------------------
        match3_1 = re.match(r'{.*|.*{|.*{.*', fileString)
        if match3_1:
            match3_1_list.append(fileString)
        else:
            match3_1_list.append('flag')
        match3_2 = re.match(r'}.*|.*}|.*}.*', fileString)
        if match3_2:
            match3_2_list.append(fileString)
        else:
            match3_2_list.append('flag')

    fileReadObj.close()
    os.remove("../tmp.c")
    #delete all-blank
    for i in range(len(fileBeforeFormater)):
        string = fileBeforeFormater[i]
        if len(string) > 0:
            flag = 0
            for j in range(len(string)-1):
                if string[j] != ' ' and string[j] != '\t' and string[j] != ';':
                    flag = 1
            if flag == 0:
                fileBeforeFormater[i] = '\n'

    cntList = []#layer structure
    cnt = 0
    for i in range(len(fileBeforeFormater)):
        if match3_1_list[i] != 'flag':#if left bucket
            cntList.append(cnt)
            cnt += 1
        elif match3_2_list[i] != 'flag':#if right bucket
            cnt -= 1
            cntList.append(cnt)
        else:
            cntList.append(cnt)

    cnt_lines = 0
    for i in range(len(fileBeforeFormater)):
        string = fileBeforeFormater[i]
        if string != '\n':
            cnt_lines += 1#count the lines
        #-------------------------rule 3-------------------------
        #code indent
        if string != '\n' and string != '' and string != '\t':#not blank line
            j = 0
            while string[j] == ' ' or string[j] == '\t':
                j = j+1
            blank_string = ''
            cnt = cntList[i]
            while cnt != 0:
                blank_string = blank_string + '    '
                cnt -= 1
            fileBeforeFormater[i] = blank_string + string[j:len(string)]

    fileWriteObj = open(filenameOut1, 'w')
    for i in fileBeforeFormater:
        fileWriteObj.write(i)
    fileWriteObj.close()

    # ---------------------------------------------
    if len(tuple_arg) == 1:
        return
    # ---------------------------------------------

    #------------------------------output analysis-result to txt------------------------------
    output = 'Lines=' + str(cnt_lines) + '\n\n'

    outputList = []
    outputList.append(output)

    #find func_name
    func_name_list = []#func_name_list
    func_name_list.append('main')
    for i in range(len(fileBeforeFormater)):
        fileString = fileBeforeFormater[i]
        for reg in [r'long (.*)\(.*\);', r'int (.*)\(.*\);', r'void (.*)\(.*\);']:
            reg = re.compile(reg)
            match_func = reg.findall(fileString)
            if match_func:
                for j in match_func:
                    j = j.replace(' ','')
                    func_name_list.append(j)

    relationMap = [([0] * len(func_name_list)) for i in range(len(func_name_list))]

    for i in range(len(func_name_list)):#for every func
        func_name = func_name_list[i]
        j = 0
        while j < len(fileBeforeFormater):#line num
            fileString = fileBeforeFormater[j]
            if fileString.find(' '+func_name+' ') != -1 and fileString[len(fileString)-2] != ';':#find where is func_name
                k = j+2
                while cntList[k] != cntList[j] and k < len(fileBeforeFormater)-1:
                    fileString2 = fileBeforeFormater[k]
                    for ii in range(len(func_name_list)):
                        func_name2 = func_name_list[ii]
                        if fileString2.find(' '+func_name2+'(') != -1:
                            if i == ii:#self invoking
                                relationMap[i][ii] = 2
                                relationMap[ii][i] = 2
                            else:
                                relationMap[i][ii] = 1
                                relationMap[ii][i] = -1
                    k += 1
                break
            j += 1

    for i in range(len(func_name_list)):
        func_name = func_name_list[i]
        string1 = 'FunctionName:' + func_name
        string2 = 'Caller:'
        cnt = 0
        for j in range(len(func_name_list)):
            func_name2 = func_name_list[j]
            #if self-invoking is not considerated, delete condition relationMap[i][j] == 2
            if relationMap[i][j] == -1 or relationMap[i][j] == 2:
                if cnt == 0:
                    string2 = string2 + func_name2
                else:
                    string2 = string2 + ',' + func_name2
                cnt += 1
        string3 = 'Called:'
        cnt = 0
        for j in range(len(func_name_list)):
            func_name3 = func_name_list[j]
            #if self-invoking is not considerated, delete condition relationMap[i][j] == 2
            if relationMap[i][j] == 1 or relationMap[i][j] == 2:
                if cnt == 0:
                    string3 = string3 + func_name3
                else:
                    string3 = string3 + ',' + func_name3
                cnt += 1
        output = string1 + '\n' + string2 + '\n' + string3 + '\n\n'
        outputList.append(output)
        # print output2

    #------------------------------output result to txt------------------------------
    fileWriteObj = open(filenameOut2, 'w')
    for i in outputList:
        fileWriteObj.write(i)
    fileWriteObj.close()

#-----------------------------------Function Simplify-----------------------------------
#filenameIn--------input testSample
#filenameOut------output simplified codes
def simplify(filenameIn, filenameOut):
    variable_name_list = []
    match3_1_list = []
    match3_2_list = []
    fileReadObj = open(filenameIn)
    fileBeforeFormater = []
    lineNum = -1
    for fileString in fileReadObj.readlines():
        lineNum += 1
        fileBeforeFormater.append(fileString)
        #for variable
        for reg in [r'long (\w*) =.*', r'int (\w*) =.*', r'void (\w*) =.*', r'.*long (\w*) =.*', r'.*int (\w*) =.*', r'.*void (\w*) =.*',
        r'long (\w*);', r'int (\w*);', r'void (\w*);', r'.*long (\w*);', r'.*int (\w*);', r'.*void (\w*);']:
            reg = re.compile(reg)
            match_vari = reg.findall(fileString)
            if match_vari:
                for j in match_vari:
                    j.replace(' ','')
                    if j not in variable_name_list:
                        variable_name_list.append(j)
                break

        #for function
        match3_1 = re.match(r'{.*|.*{|.*{.*', fileString)
        if match3_1:
            match3_1_list.append(fileString)
        else:
            match3_1_list.append('flag')
        match3_2 = re.match(r'}.*|.*}|.*}.*', fileString)
        if match3_2:
            match3_2_list.append(fileString)
        else:
            match3_2_list.append('flag')

    fileReadObj.close()
    for i in range(len(fileBeforeFormater)):
        string = fileBeforeFormater[i]
        if len(string) > 0:
            flag = 0
            for j in range(len(string)-1):
                if string[j] != ' ' and string[j] != '\t' and string[j] != ';':
                    flag = 1
            if flag == 0:
                fileBeforeFormater[i] = '\n'

    cntList = []#layer structure
    cnt = 0
    for i in range(len(fileBeforeFormater)):
        if match3_1_list[i] != 'flag':#if left bucket
            cntList.append(cnt)
            cnt += 1
        elif match3_2_list[i] != 'flag':#if right bucket
            cnt -= 1
            cntList.append(cnt)
        else:
            cntList.append(cnt)

    #find func_name
    func_name_list = []#func_name_list
    func_declare_num_list = []#func_declare_lineNum
    func_work_num_list = []#func_work_lineNum, which factor include two num
    func_name_list.append('main')
    func_declare_num_list.append(0)
    for i in range(len(fileBeforeFormater)):
        fileString = fileBeforeFormater[i]
        for reg in [r'long (.*)\(.*\);', r'int (.*)\(.*\);', r'void (.*)\(.*\);']:
            reg = re.compile(reg)
            match_func = reg.findall(fileString)
            if match_func:
                for j in match_func:
                    j = j.replace(' ','')
                    func_name_list.append(j)
                    func_declare_num_list.append(i)

    relationMap = [([0] * len(func_name_list)) for i in range(len(func_name_list))]

    for i in range(len(func_name_list)):#for every func
        func_name = func_name_list[i]
        j = 0
        while j < len(fileBeforeFormater):#line num
            fileString = fileBeforeFormater[j]
            if fileString.find(' '+func_name+' ') != -1 and fileString[len(fileString)-2] != ';':#find where is func_name
                k = j+2
                while cntList[k] != cntList[j] and k < len(fileBeforeFormater)-1:
                    fileString2 = fileBeforeFormater[k]
                    for ii in range(len(func_name_list)):
                        func_name2 = func_name_list[ii]
                        if fileString2.find(' '+func_name2+'(') != -1:
                            if i == ii:#self invoking
                                relationMap[i][ii] = 2
                                relationMap[ii][i] = 2
                            else:
                                relationMap[i][ii] = 1
                                relationMap[ii][i] = -1
                    k += 1
                func_work_num_list.append([j,k])
                break
            j += 1

    for i in range(len(func_name_list)):
        flag = 0;
        for j in range(len(func_name_list)):
            if relationMap[i][j] == -1 or relationMap[i][j] == 1 or relationMap[i][j] == 2:
                flag = 1;
        if flag == 0:
            func_declare_num = func_declare_num_list[i];
            func_work_num = func_work_num_list[i];
            fileBeforeFormater[func_declare_num] = '';
            for j in range(func_work_num[1]-func_work_num[0]+1):
                fileBeforeFormater[j+func_work_num[0]] = '';

    #delete useless varible
    lineNum = -1
    variable_list = []
    variable_num_list = []
    for fileString in fileBeforeFormater:
        lineNum += 1
        #for variable
        for regVar in variable_name_list:
            reg = '.*'+regVar+'.*'
            reg = re.compile(reg)
            match_vari = reg.findall(fileString)
            if match_vari:
                variable_list.append(regVar)
                variable_num_list.append(lineNum)

    for variableName in variable_name_list:
        if len(find_all_index(variable_list, variableName)) == 1:
            lineNum = variable_num_list[variable_list.index(variableName)]
            fileBeforeFormater[lineNum] = ''

    #------------------------------output the codes------------------------------
    fileWriteObj = open(filenameOut, 'w')
    for i in fileBeforeFormater:
        fileWriteObj.write(i)
    fileWriteObj.close()

    #print variable_name_list,variable_num_list
    #print func_name_list,func_declare_num_list,func_work_num_list


#-----------------------------------Function Style-----------------------------------
#filenameIn--------input testSample
#filenameOut-------output style codes
def style(filenameIn, filenameOut):
    fileReadObj = open(filenameIn)
    fileBeforeFormater = []
    leftBucket_line_list = []
    lineNum = -1
    for fileString in fileReadObj.readlines():
        lineNum += 1
        fileBeforeFormater.append(fileString)
        match3_1 = re.match(r'{.*|.*{|.*{.*', fileString)
        if match3_1:
            leftBucket_line_list.append(lineNum)
    for i in leftBucket_line_list:
        tmp_string = fileBeforeFormater[i-1]
        tmp_string = tmp_string[0:len(tmp_string)-1]+'{'+tmp_string[len(tmp_string)-1]
        fileBeforeFormater[i-1] = tmp_string
        fileBeforeFormater[i] = ''
    #------------------------------output the codes------------------------------
    fileWriteObj = open(filenameOut, 'w')
    for i in fileBeforeFormater:
        fileWriteObj.write(i)
    fileWriteObj.close()
