# coding: utf-8 
# recite GRE words
# version: 0.01
# author: bing wang
import json
import time
import numpy as np

def initial():
    def blast(w1,w2):
        w_match = 2
        w_mismatch = -1
        w_gap = -1
        score_matrix = np.zeros((len(w1)+1,len(w2)+1))
        for i in range(len(w1)):
            for j in range(len(w2)):
                s = w_match if w1[i] == w2[j] else w_mismatch
                score_matrix[i+1,j+1] = max(0,score_matrix[i,j]+s,\
                                            score_matrix[i+1,j]+s+w_gap,\
                                            score_matrix[i,j+1]+s+w_gap)
        return score_matrix[len(w1),len(w2)]

    GRE_book = {}
    f = open("/Users/bingwang/VimWork/GRE.txt")
    for i,line in enumerate(f):
        line = line.strip()
        word = line[:line.find("[")-1]
        GRE_book[word] = {}
        GRE_book[word]["meaning"] = line[line.find("]")+2:]
        GRE_book[word]["recite_count"] = 0
        GRE_book[word]["remember_rate"] = 0.
        GRE_book[word]["last_recite_time"] = 0.
        GRE_book[word]["strength"] = 0
        GRE_book[word]["difficulty"] = 0
        GRE_book[word]["time_used"] = 0
        GRE_book[word]["group_words"] = []
        group_words = [a for a in GRE_book if blast(a,word) > 7 and (a != word)]
        for a in group_words:
            if word not in GRE_book[a]["group_words"]:
                GRE_book[a]["group_words"].append(word)
            if a not in GRE_book[word]["group_words"]:
                GRE_book[word]["group_words"].append(a)
        print i*1.0/8395
    encode = json.dumps(GRE_book)
    f = open("/Users/bingwang/VimWork/GRE_book","w")
    f.write(encode)
    f.close()

def word_handle(word,stastus,t):
    GRE_book[word]["time_used"] += t
    GRE_book["_this_time"] += t
    if (int(GRE_book["_this_time"])*1.0/60)%1 == 0:
        if save():
            print "**auto saved**"
    if stastus == False:
        GRE_book[word]["difficulty"] += 1
    elif stastus == True:
        GRE_book[word]["recite_count"] += 1
        GRE_book[word]["strength"] += 0.5 
        GRE_book[word]["remember_rate"] = 1.0
        GRE_book[word]["last_recite_time"] = time.time()

def show_stastus():
    word_reviewed = len([word for word in review_list if GRE_book[word]["remember_rate"] == 1])
    word_newed = len([word for word in new_list if GRE_book[word]["remember_rate"] == 1])
    word_total = len([word for word in GRE_book if word[0] != "_" and
        GRE_book[word]["remember_rate"] > remember_threshold])
    print "#########################"
    print "you sepend:\t\t",GRE_book["_this_time"]/3600,"h"
    print "words reviewed:\t\t",word_reviewed,"words"
    print "review speed:\t\t",word_reviewed*1./((review_time+1)*1./3600),"words/h"
    print "words newed:\t\t",word_newed,"words"
    print "new word speed:\t\t",word_newed*1.0/((GRE_book["_this_time"]-review_time+1)*1./3600),"words/h"
    print "total percent:\t\t",round(word_total*100.0/len(GRE_book),2),"%"

def save():
    from datetime import date
    day = str(date.today().day)
    month = str(date.today().month)
    year = str(date.today().year)
    filetime = year + "_" + month + "_" + day
    encode = json.dumps(GRE_book)
    f = open("/Users/bingwang/VimWork/GRE/GRE_book_"+filetime,"w")
    f.write(encode)
    f.close()
    f = open("/Users/bingwang/VimWork/GRE/GRE_book","w")
    f.write(encode)
    f.close()
    return True

def recite(word):
    print word
    word_start = time.time()
    cmd = getch()

    if cmd.upper() == "N":
        print GRE_book[word]["meaning"]
        print "........................press any to continue"
        if getch():
            word_time_used = int(time.time()-word_start)
            word_handle(word,False,word_time_used)
            return False

    elif cmd.upper() == "Y":
        word_time_used = int(time.time()-word_start)
        print GRE_book[word]["meaning"]
        print "........................press \"y\" if right"
        if getch().upper() == "Y":
            word_handle(word,True,word_time_used)
            return True
        else:
            word_handle(word,False,word_time_used)
            return False

    elif cmd.upper() == "X":
        GRE_book[word]["strength"] = 10

    elif cmd.upper() == "S":
        if save():
            print "saved!"
        print "press any to continue:"
        if getch():
            return None

    elif cmd.upper() == "P":
        show_stastus()
        print "press any to continue:"
        if getch():
            return None

    elif cmd.upper() == "Q":
        show_stastus()
        save()
        return "Q"

    else:
        print "#########################"
        print "y\t\t\tI remember"
        print "n\t\t\tI forget"
        print "h\t\t\tshow this message"
        print "p\t\t\tshow stastus"
        print "s\t\t\tsave"
        print "x\t\t\tnever appear again"
        print "q\t\t\tquit"
        print "press any to continue:"
        if getch():
            return None

def calculte_remember_rate():
    import math
    for word in GRE_book:
        if word[0] != "_" and GRE_book[word]["recite_count"] > 0:
            t = int((time.time()-GRE_book[word]["last_recite_time"])/3600)*1.0/24
            GRE_book[word]["remember_rate"] = math.e ** \
            (-t*1.0*(GRE_book[word]["difficulty"]+1)\GRE_book[word]["strength"])
        else:
            continue

def review(review_list):
    count = len(review_list)
    while count > 0:
        for i,word in enumerate(review_list):
            if GRE_book[word]["remember_rate"] == 1 and \
                GRE_book[word]["strength"] % 1 == 0:
                count -= 1
            else:
                cmd = recite(word)
                if cmd == "Q":
                    return "Q"

def check_redundance():
    for word in GRE_book:
        if word[0] != "_":
            for group in GRE_book[word]["group_words"]:
                if group == word:
                    GRE_book[word]["group_words"].remove(group)
                    print "remove\t",group,"\tfrom\t",word
                elif GRE_book[word]["group_words"].count(group) > 1:
                    GRE_book[word]["group_words"].remove(group)
                    print "remove\t",group,"\tfrom\t",word

def getch():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

####################  main  ######################
remember_threshold = 0.37
unit_length = 30

f = open("/Users/bingwang/VimWork/GRE/GRE_book")
encode = f.read()
GRE_book = json.loads(encode)
review_time = 0.0
GRE_book["_this_time"] = 0

print "calculaing remember rate"
calculte_remember_rate()

print "prepare review list"
review_list = [word for word in GRE_book if word[0] != "_" \
        and GRE_book[word]["recite_count"] > 0 \
        and (GRE_book[word]["remember_rate"] < remember_threshold \
            or GRE_book[word]["strength"]%1 != 0)]

new_list = []
print "#############################"
print "#           Review          #"
print "#############################"
if review(review_list) != "Q":
    print "#############################"
    print "#           New Word        #"
    print "#############################"
    review_time = GRE_book["_this_time"]
    temp_list = []
    new_list = []
    cmd = ""
    for word in GRE_book:
        if word[0] != "_" and GRE_book[word]["recite_count"] == 0:
            temp_list.append(word)
            new_list.append(word)
            for group in GRE_book[word]["group_words"]:
                if GRE_book[group]["recite_count"] == 0 and group not in new_list:
                    temp_list.append(group)
                    new_list.append(group)
                    if len(temp_list) > unit_length:
                        cmd = review(temp_list)
                        if cmd != "Q":
                            temp_list = []
                        else:
                            break
            if cmd != "Q":
                continue
            else:
                break
