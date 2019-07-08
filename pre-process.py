
import re
from collections import defaultdict

INPUT_DIR = "inputData/"
OUTPUT_DIR = "outputData/"
input_data=["CDR_DevelopmentSet.PubTator.txt", "CDR_TrainingSet.PubTator.txt","CDR_TestSet.PubTator.txt"]
input_data = [ INPUT_DIR + d for d in input_data]

output=["dev.txt","train.txt","test.txt"]
output_data = [OUTPUT_DIR + d for d in output]
output_infoData = [OUTPUT_DIR +'info_' +d for d in output]

MAX_LINE = 1000000

#def makefile(data,table)
match=dict()  
trigger=True
def preprocess(index):
    print ('processing file:  input:' + input_data[index] + ' output:' + output_data[index]+ ' ' + output_infoData[index])
    outfile = open(output_data[index], "w")
    outInfoFile = open(output_infoData[index], "w")
    with open(input_data[index]) as infile:
    #    print '\n Total file length: ' + infile.size()
        idx = 0
        id =''
        tile = ''
        diseases =[]
        article = ''

        line_txt_count = 0 #count the line of input file

        for line in infile:  
            idx += 1

            if idx >= MAX_LINE: break

            '''
            read |t| 
            read |a|
            read Disease  line[4]=='Disease' , split to B-Disease, I-Disease, other O
            util blank line
            write outfile
            write outInfoFile
            
            write info for assemble:
               ID, |t|, fromline, toline
               ID, |a|, fromLine, toLine
               ID, Disease,
            
            '''
            # 'find title'
            result = re.match("^(\d+)\|t\|(.*)", line)
            if result:
                if id =='':
                    id = result.group(1)
                title =  result.group(2)

            #'find ariticle'
            result = re.match("^(\d+)\|a\|(.*)", line)
            if result:
                article =  result.group(2)

            #'find disease'
            result = re.match("^(\d+)	.*", line)
            if result:
                line = line.split("	")
                #print  'split line:', line
                if len(line) > 4 and line[4] == 'Disease':
                    disease = [(s, 'B-Disease',line[1], line[2]) if i == 0 else (s, 'I-Disease') for i, s in enumerate(line[3].split(" "))]
                    diseases.append(disease)

            #new patient
            if len(line) <=1:
                #construct txt and write for previous patient

                print ('title=', title)
                print ('article=', article)
                print('diseases=',diseases)

                disease_dic = dict()
                for disease in diseases:
                    for dis in disease:
                        disease_dic [dis[0]] = dis[1]

                # rgx = re.compile("([\w][\w']*\w)")
                # words = rgx.findall(title)
                # #write title
                words = re.findall(r"[\w']+|[.,!?;%~\&<>\-|()\[\]\{\}\]\\\*\.\+\=/]",title)
                start_line = line_txt_count
                for word in words:
                    if word in disease_dic:
                        outfile.write(word+'	'+disease_dic[word]+'\n')
                        line_txt_count += 1
                    else:
                        outfile.write(word+'	O\n')
                        line_txt_count += 1
                    if word in ['.','!','?',';']:
                        outfile.write("\n")
                        line_txt_count += 1
                outInfoFile.write(id + '	' + 'title'+ '	'+ str(start_line) + '	' + str(line_txt_count-1)+'\n')

                words = re.findall(r"[\w']+|[.,!?;%~\&<>\-|()\[\]\{\}\]\\\*\.\+\=/]", article) #write article
                start_line = line_txt_count
                for word in words:
                    if word in disease_dic:
                        outfile.write(word+'	'+disease_dic[word]+'\n')
                        line_txt_count += 1
                    else:
                        outfile.write(word+'	O\n')
                        line_txt_count += 1
                    if word in ['.','!','?',';']:
                        outfile.write("\n")
                        line_txt_count += 1
                outInfoFile.write(id + '	' + 'article'+ '	'+ str(start_line) + '	' + str(line_txt_count-1)+'\n')

                print ('diseases_dic=', disease_dic)
                for disease   in diseases:   #write diseases
                    for word in disease:
                        print ('disease={}, word={} '.format(  disease, word  ))
                        outfile.write(word[0]+'	'+ word[1] +'\n')
                        tmp = '	'+ word[2]+'	'+word[3] if word[1] =='B-Disease' else ''
                        outInfoFile.write(id + '	' + 'Disease'+ '	'+ str(line_txt_count) + '	' + str(line_txt_count) \
                                +'	' + word[0] + '	'+word[1]+ tmp +'\n')
                        line_txt_count += 1
                outfile.write('\n')
                outInfoFile.write('\n')
                line_txt_count += 1

                id = ''
                title = ''
                article = ''
                diseases =[]
    outInfoFile.close()
    outfile.close()

    
    
if __name__ == '__main__':
    for i in range(len(input_data)):
        preprocess(i)