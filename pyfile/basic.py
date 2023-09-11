
import os
from sys import *

# Creating an interpretor for the language

# creating a token list
tokens=[]
#creatinga a list for handling all the expressions
num_stack=[]
#For symbol table creating a dictionary
symbols = {}

errors=["Error: Bhaii iss naam se koi variable nhi hai (●´⌓`●)"]


def open_file(filename):
    data = open(filename,"r").read()
    # /* Eof here is used to represend End  of file*/
    data +="<EOF>" 
    return data

def lex(filecontents):
    tok=""
    #expr for checking if it is number or not
    isexpr= 0
    state = 0
    string = ""
    expr=""
    n=""
    #now creating a variable for storing a value 
    varStarted = 0
    var =""
    #For hindi text bolo doing encoding
    unicode_str = "U+092C U+094B U+0932 U+094B"
    string_value = ''.join(chr(int(code_point[2:], 16)) for code_point in unicode_str.split())
    filecontents = list(filecontents)
    for char in filecontents: 
        tok+=char
        if tok ==" ":
            if state ==0:
                tok=""
            else:
                tok=" "  
        elif tok=="\n" or tok=="<EOF>":
            if expr !="" and isexpr==1:
                tokens.append("EXPR:"+expr)
                expr="" 
            elif expr!="" and isexpr==0:
                tokens.append("NUM:"+expr)
                expr=""  
            elif var !="":
                #Can cause error so keep monetering $=naam
                tokens.append("VAR:"+var[4:])
                var =""
                varStarted =0      
            tok=""
        elif tok == "=" and state==0:
            if expr!="" and isexpr==0:
                tokens.append("NUM:"+expr)
                expr=""
            if var!="":
                tokens.append("VAR:"+var[4:])
                var =""
                varStarted = 0
            if tokens[-1] == "EQUALS":
                tokens[-1] = "EQEQ"
            else:
                tokens.append("EQUALS")
            tok=""    
        elif tok=="naam" and state ==0:
            varStarted = 1
            var +=tok
            tok ="" 
        elif varStarted ==1:
            if tok =="<" or tok==">":
                if var!="":
                    tokens.append("VAR:"+var[4:])
                    var =""
                    varStarted = 0
            var +=tok
            tok=""               
        elif tok == "bolo" or tok == "BOLO" or tok ==string_value:
            tokens.append("bolo")
            tok =""
        elif tok == "likho" or tok == "LIKHO":
            tokens.append("likho")
            tok =""
        elif tok == "nhito" or tok == "NHITO":
            tokens.append("nhito")
            tok =""    
        elif tok == "agar" or tok == "AGAR":
            tokens.append("agar")
            tok =""
        elif tok == "to" or tok == "TO":
            if expr!="" and isexpr==0:
                tokens.append("NUM:"+expr)
                expr=""
            tokens.append("to")
            tok =""                
        elif tok=="0" or tok=="1" or tok=="2" or tok=="3" or tok=="4"or tok=="5"or tok=="6"or tok=="7"or tok=="8"or tok=="9":
            expr +=tok
            tok=""
        elif tok=="+" or tok=="-"or tok=="*"or tok=="/"or tok=="("or tok==")"or tok=="%":
            isexpr = 1
            expr +=tok
            tok=""
            # Expecting error in decting " as "/" " is not working but fixed by '"'
        elif tok=="\t":
            tok=""
        elif tok =='"' or tok == " \"":  
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append("STRING:"+string+'"')
                string =""
                state = 0
                tok=""
        elif state == 1:
            string += tok
            tok = ""
    # print(tokens)
    # print(expr) 
    # return '' 
    return(tokens)
#Creating a function for evaluating the expression
def evalExpression(expr):    
    return eval(expr)


#To remove quotes before and after string in the terminal we are creating a function
def doPrint(toPrint):
    if(toPrint[0:6]=="STRING"):
        toPrint = toPrint[8:]
        toPrint = toPrint[:-1]
    if(toPrint[0:3]=="NUM"):
        toPrint = toPrint[4:]  
    if(toPrint[0:4]=="EXPR"):
        toPrint = evalExpression(toPrint[5:])      
    print(toPrint)    
#Creating a function that will take care of assigning a variable
def doAssign(varname,varvalue):
    #kyuki hame sirf variable name store karna hai naa ki 'var:' poora so start with 4 index
    symbols[varname[4:]] = varvalue
#Creating a function jo ki symbol dictionary se uss variable ka ans nikal kar dega
def getVariable(varname):
    varname = varname[4:]
    if varname in symbols:
        return symbols[varname]
    else:
        
        return errors[0]
        exit() 
#Creating a function to take input
def getInput(string,varname):
    i = input(string[1:-1]+" ")
    symbols[varname] = "STRING:\""+i+"\""         
# Creating a parser function 
def parse(toks):
    i= 0
    while(i < len(toks)):
        # if toks[i]=="nhito":
        #     # if toks[i+9][0:6] == "STRING":
        #     #     doPrint(toks[i+9])
        #     # elif toks[i+9][0:3] == "NUM":
        #     #     doPrint(toks[i+9])
        #     # elif toks[i+9][0:4] == "EXPR":
        #     #     doPrint(toks[i+9])
        #     # elif toks[i+9][0:3] == "VAR":
        #     #     doPrint(getVariable(toks[i+9])) 
        #     i+=1
        if toks[i]+" "+toks[i+1][0:6]=="bolo STRING" or toks[i]+" "+toks[i+1][0:3]=="bolo NUM"or toks[i]+" "+toks[i+1][0:4]=="bolo EXPR"or toks[i]+" "+toks[i+1][0:3]=="bolo VAR":
            if toks[i+1][0:6] == "STRING":
                doPrint(toks[i+1])
            elif toks[i+1][0:3] == "NUM":
                doPrint(toks[i+1])
            elif toks[i+1][0:4] == "EXPR":
                doPrint(toks[i+1])
            elif toks[i+1][0:3] == "VAR":
                doPrint(getVariable(toks[i+1]))            
            i+=2
        elif toks[i][0:3] + " "+ toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " "+ toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " "+ toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR"or toks[i][0:3] + " "+ toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " "+ toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
            if toks[i+2][0:6] == "STRING":
                doAssign(toks[i],toks[i+2])
            elif toks[i+2][0:3] == "NUM":
                doAssign(toks[i],toks[i+2])
            elif toks[i+2][0:4] == "EXPR":
                doAssign(toks[i],"NUM:"+str(evalExpression(toks[i+2][5:])))
            elif toks[i+2][0:3] == "VAR":
                doAssign(toks[i],getVariable(toks[i+2]))     
            i+=3
        elif toks[i]+" "+toks[i+1][0:6]+" "+ toks[i+2][0:3]=="likho STRING VAR" :     
            #['likho', 'STRING:"Enter your name:"', 'VAR:a']  
            getInput(toks[i+1][7:],toks[i+2][4:])
            i+=3
        # elif toks[i]+" "+toks[i+1][0:3]+" "+ toks[i+2]+" "+ toks[i+3][0:3]+" "+ toks[i+4]=="agar NUM EQEQ NUM to" :     
        #     # ['agar', 'NUM:1', 'EQEQ', 'NUM:1', 'to', 'bolo', 'STRING:"Jai Hind"', 'nhito'] 
        #     if toks[i+1][4:]== toks[i+3][4:]:
        #         print("Diya gaya condition sahi hai ʘ‿ʘ>")   
        #         if toks[i+6][0:6] == "STRING":
        #             doPrint(toks[i+6])
        #         elif toks[i+6][0:3] == "NUM":
        #             doPrint(toks[i+6])
        #         elif toks[i+6][0:4] == "EXPR":
        #             doPrint(toks[i+6])
        #         elif toks[i+6][0:3] == "VAR":
        #             doPrint(getVariable(toks[i+6])) 
        #         exit()    
        #     else:
        #         print("Diya gaya condition sahi nhi hai ( •_•)")   
        #     #Here we are taking 5 tokens here increase it by 5
        #     i+=5
    # print(symbols)  


folder_path = "./temp/"
files = os.listdir(folder_path)

if files:
    # get the first file in the list
    first_file = files[0]
    print("File name: "+first_file)
    print("-----------------------")
       
def run():
    data = open_file(folder_path+first_file)
    toks = lex(data)  
    parse(toks)  
run();    