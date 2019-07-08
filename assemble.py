# coding:utf-8
from collections import defaultdict
outFile = open("outputData/result.txt", "w")

outInfoFile = open("outputData/info_test.txt", "r")
outInfo = outInfoFile.readlines()
outInfoFile.close()


rawOutFile = open('outputData/raw.out')
rawouts = rawOutFile.readlines()

def handle_punctuation(data):
    if '/' in data: data=data.replace(" /", "/")
    if '/' in data: data=data.replace("/ ", "/")
    if '-' in data: data=data.replace(" -", "-")
    if '-' in data: data=data.replace("- ", "-")
    if '?' in data: data=data.replace(" ?", "?")
    if '.' in data: data=data.replace(" .", ".")
    if ')' in data: data=data.replace(" )", ")")
    if '(' in data: data=data.replace("( ", "(")
    if '[' in data: data=data.replace("[ ", "[")
    if ']' in data: data=data.replace(" ]", "]")
    if '{' in data: data=data.replace("{ ", "{")
    if '}' in data: data=data.replace(" }", "}")
    if ',' in data: data=data.replace(" ,", ",")
    if '?' in data: data=data.replace(" ?", "?")
    if '+' in data: data=data.replace(" +", "+")
    if '+' in data: data=data.replace("+ ", "+")
    if '<' in data: data=data.replace(" <", "<")
    if '<' in data: data=data.replace("< ", "<")
    if '>' in data: data=data.replace(" >", ">")
    if '>' in data: data=data.replace("> ", ">")
    if ':' in data: data=data.replace(" :", ":")
    if ';' in data: data=data.replace(" ;", ";")
    if "'" in data: data=data.replace(" '", "'")
    if '"' in data: data=data.replace(' "', '"')
    if '=' in data: data=data.replace(' =', '=')
    if '=' in data: data=data.replace('= ', '=')
    if '%' in data: data=data.replace('%', ' % ')
    return data

def handleDisease(start, end):
    currLine =  start
    dis = []
    text = ''
    while currLine < end:
        # print ' tile -- ', s
        s = rawouts[currLine].rstrip().split(" ")
        if len(s) < 2:
            currLine += 1
            continue
        pos_start = len(text)
        if s[1] == 'B-Disease':
            tmp1 = s[0]
            text += s[0]
            while currLine+1 < end and len(rawouts[currLine + 1].rstrip().split(" ")) > 1 and \
                    rawouts[currLine + 1].rstrip().split(" ")[1] == 'I-Disease':
                currLine += 1
                s = rawouts[currLine].rstrip().split(" ")
                tmp1 += " " + s[0] if s[0]  not in ['-',] else s[0]
                text += s[0] + ' '
            text = handle_punctuation(text)
            disease =  id + "	" + str(pos_start) + "	" + str(len(text)) + "	" + tmp1+  "	Disease	-1" + '\n'
            # disease =  id + t  + "	" + tmp1+  "	Disease	-1" + '\n'
            dis.append(disease)
        elif s[0] in ['.', '!', '?']:
            text = text.rstrip() +s[0] +' '
        else:
            text += s[0] + ' '
        currLine += 1
    return (text.rstrip(), dis)

count = -1
id = titile =  article = ''
diseases = []
disease = []
t =[]
while count < len(outInfo)-1:
    count += 1

    words = outInfo[count].split("	")
    if len(words) > 1:
        if words[1] == 'title':
            id = words[0]
            title = id + "|t|"
            tmp, dis   = handleDisease(int(words[2]), int(words[3]) )
            title += tmp
            diseases.extend(dis)

            outFile.write(title+'\n')

        elif words[1] == 'article':
            id = words[0]
            article = id + "|a|"
            tmp, dis   = handleDisease(int(words[2]), int(words[3]))
            article += tmp
            diseases.extend(dis)
            outFile.write(article +'\n')
        elif len(words) >7 and words[5]=='B-Disease':
            t.append((words[6],words[7].rstrip()))
    else:#write Diseases
        # print 'diseases',len(diseases), diseases
        # print 't=',len(t), t
        for i, disease in enumerate(diseases):
            # print ('i={},disease={}\n t[i]={}'.format(i,disease,t[i]))
            disease = disease.split("	")
            #if i < len(t):disease[1], disease[2] = t[i][0], t[i][1]
            outFile.write("	".join(disease))
        outFile.write('\n')
        id = title = article = ''
        diseases = []
        t=[]

outFile.close()