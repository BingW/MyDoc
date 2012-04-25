#coding: utf-8
'''
Author: Bing Wang
Last Modified: 2012.3.19
useage:
    import sys
    sys.path.append("/Users/bingwang/VimWork/")
    import lib.func.alnrefine as alr 

    alr.refine(                   # alnfile -> refined alnfile
        alnfile,
        [gap_sign="-",            #in alnfile,"-"means gap
        outfile=alnfile.aa,       #default ourput alnfile.aa
        reffile=alnfile.ref,      #reference and alinment printing
        gap_allow=0,              #all how many gaps
        min_conserve=5,           #the minimal conserved number
        min_flanking=10,          #the minimal flanking number
        max_nonconserve=6,        #the max countinue nonconserve
        judge_conserve=1.0]       #(0,1]:conservity = count(base)/count(species) 
                                   > judge_conserve
        )
'''

def read_aln(alnfile):
    gene = {}
    f = open(alnfile)
    for line in f:
        line = line.strip()
        if len(line)>0 and line[0] == ">":
            genename = line[1:]
            gene[genename] = ""
        else:
            gene[genename]+=line
    f.close()
    error = False
    for name in gene:
        if len(gene[name]) != len(gene[genename]):
            error = True
            break
    if not error:
        return gene
    else:
        print "alignment not at same length"
        return gene 

def aln_mark(gene,judge_conserve,gap_sign):
    geneseq_mark = ""
    geneseq = []
    for name in gene:
        geneseq.append(gene[name])
    if len(geneseq)==0:
        print gene
    for i in range(len(geneseq[0])):
        alnment = ""
        mark = False
        for sequence in geneseq:
            alnment += sequence[i]
        if alnment.find(gap_sign) != -1:
            geneseq_mark += "X"    #X means gap
            mark = True
            continue
        else:
            for base in alnment:
                if alnment.count(base)*1./len(alnment) >= judge_conserve:
                    geneseq_mark += "C"    #C means conserve
                    mark = True
                    break
            if mark == False:
                geneseq_mark += "N"    #N means non-conserve
    if len(geneseq_mark) == len(geneseq[0]):
        return geneseq_mark

def gene_refine(geneseq_mark,gap_allow,min_conserve,min_flanking,max_nonconserve):
    keep = ""
    count_conserve = 0
    count_gap = 0
    continue_nonconserve = 0
    start = False
    keeptemp = ""
    for i,mark in enumerate(geneseq_mark):
        if start == True:
            if mark == "X":
                count_gap += 1
                continue_nonconserve += 1
                keeptemp += " "
                if count_gap>gap_allow or continue_nonconserve>=max_nonconserve:
                    if count_conserve>=min_conserve or \
                      len(keeptemp[:keeptemp.rfind("T")+1])>=min_flanking:
                        for base in range(len(keeptemp[:keeptemp.rfind("T")+1])):
                            keep += "T"
                        for base in range(len(keeptemp[keeptemp.rfind("T")+1:])):
                            keep += "F"
                    else: 
                        for base in range(len(keeptemp)):
                            keep += "F"
                    count_conserve = 0
                    continue_nonconserve = 0
                    count_gap = 0
                    start = False
                    keeptemp = ""
            elif mark == "C":
                count_conserve += 1
                continue_nonconserve = 0
                keeptemp += "T"
            elif mark == "N":
                continue_nonconserve += 1
                keeptemp += " "
                if continue_nonconserve>=max_nonconserve:
                    if count_conserve>=min_conserve or \
                      len(keeptemp[:keeptemp.rfind("T")+1])>=min_flanking:
                        for base in range(len(keeptemp[:keeptemp.rfind("T")+1])):
                            keep += "T"
                        for base in range(len(keeptemp[keeptemp.rfind("T")+1:])):
                            keep += "F"
                    else:
                        for base in range(len(keeptemp)):
                            keep += "F"
                    count_conserve = 0
                    continue_nonconserve = 0
                    count_gap = 0
                    start = False
                    keeptemp = ""
            else:
                print"Something unnormal happen"
                print mark
        elif mark == "C": 
            start = True
            keeptemp += "T"
            count_conserve += 1
            continue_nonconserved = 0
        elif mark == "X" or mark == "N":
            keep += "F"
        else:
            print "Something unnormal happen"
            print mark
    if count_conserve>=min_conserve or \
      len(keeptemp[:keeptemp.rfind("T")+1])>=min_flanking:
        for base in range(len(keeptemp[:keeptemp.rfind("T")+1])):
            keep += "T"
        for base in range(len(keeptemp[keeptemp.rfind("T")+1:])):
            keep += "F"
    else:                    
        for base in range(len(keeptemp)):
            keep += "F"
    if len(keep) != len(geneseq_mark):
        print "Bug @ gene_refine"
        return None
    return keep

def write_aa(gene,name_index_order,keep,outfile):
    gene_new = {} 
    for name in gene:
        gene_new[name] = ""
        for i,mark in enumerate(keep):
            if mark == "T":
                gene_new[name] += gene[name][i]
    f = open(outfile,"w")
    f.write("\t"+str(len(gene))+"\t"+str(len(gene_new[name]))+"\n")
    for name in name_index_order:
        f.write(">"+name+"\n")
        f.write(gene_new[name] + "\n")
    f.close()

def write_ref(gene,name_index_order,mark,keep,outfile,gap_allow,min_conserve,\
        min_flanking,max_nonconserve,judge_conserve,perline = None):
    if perline == None:
        perline = 60
    max_genename = 20
    for name in name_index_order:
        if max_genename < len(name):
            max_genename = len(name)+5
    f = open(outfile,"w")
    if len(gene[name]) <= perline:
        for name in gene:
            f.write(name+(max_genename-len(name))*" "+gene[name]+"\n")
        f.write("gene_mark"+(max_genename-9)*" "+mark+"\n")  # len("gene_mark")=9
        f.write("gene_keep"+(max_genename-9)*" "+keep+"\n")
    
    else:
        for name in name_index_order:
            f.write(name+(max_genename-len(name))*" "+gene[name][:perline]+"\n")
        f.write("gene_mark"+(max_genename-9)*" "+mark[:perline]+"\n")
        f.write("gene_keep"+(max_genename-9)*" "+keep[:perline]+"\n")
        f.write("\n")
        j=0
        for i in range(len(gene[name])/perline-1):
            for name in name_index_order:
                f.write(name+(max_genename-len(name))*" "+gene[name][(i+1)*perline:(i+2)*perline]+"\n")
            f.write("gene_mark"+(max_genename-9)*" "+mark[(i+1)*perline:(i+2)*perline]+"\n")
            f.write("gene_keep"+(max_genename-9)*" "+keep[(i+1)*perline:(i+2)*perline]+"\n")
            f.write("\n")
            j=i
        for name in name_index_order:
            f.write(name+(max_genename-len(name))*" "+gene[name][(j+1)*perline:]+"\n")
        f.write("gene_mark"+(max_genename-9)*" "+mark[(j+1)*perline:]+"\n")
        f.write("gene_keep"+(max_genename-9)*" "+keep[(j+1)*perline:]+"\n")
    f.write("\n\n\n")
    f.write("*******************************\n")
    f.write("*        Argument             *\n")
    f.write("*******************************\n")
    f.write("#gap_allow:\t"+str(gap_allow)+"\n")
    f.write("#min_conserve:\t"+str(min_conserve)+"\n")
    f.write("#min_flanking:\t"+str(min_flanking)+"\n")
    f.write("#max_nonconserve:\t"+str(max_nonconserve)+"\n")
    f.write("#judge_conserve:\t"+str(judge_conserve)+"\n")
    f.close()

###########input#############
def refine(alnfile,gap_sign=None,outfile=None,reffile=None,gap_allow=None,
        min_conserve=None,min_flanking=None,max_nonconserve=None,
        judge_conserve=None):

    if gap_sign==None:
        gap_sign="-"    #In alnfile,the gap_sign should be "-", or modidy this
    if outfile==None:
        outfile = alnfile[:alnfile.rfind(".")]+".aa"
    if reffile==None:
        reffile = alnfile[:alnfile.rfind(".")]+".ref"
    if gap_allow==None:
        gap_allow = 0    #can be any int >= 0
    if min_conserve==None:
        min_conserve = 5
    if min_flanking==None:
        min_flanking = 10    #should be biger than min_conserve or won't work
    if max_nonconserve==None:
        max_nonconserve = 6
    if judge_conserve==None:
        judge_conserve = 1.0    #any float between (0,1)

    name_index_order = alnfile[alnfile.rfind("/")+1:alnfile.rfind(".")].split("_")
    gene = read_aln(alnfile)
    mark = aln_mark(gene,judge_conserve,gap_sign)
    keep = gene_refine(mark,gap_allow,min_conserve,min_flanking,max_nonconserve)
    write_aa(gene,name_index_order,keep,outfile)

    mark = mark.replace("C",":") #: means conserved
    mark = mark.replace("N"," ") #. means noncenserved 
    mark = mark.replace("X"," ") # means gap
    keep = keep.replace("F"," ") # means not good aliment
    keep = keep.replace("T","=") #_ means good alinment 
    write_ref(gene,name_index_order,mark,keep,reffile,gap_allow,min_conserve,\
            min_flanking,max_nonconserve,judge_conserve)

##########run_test###########
if __name__ == '__main__':
    refine("/Users/bingwang/VimWork/lib/test/Kwal0.3_SAKL0D07062g_KLLA0F01793g.fa")
    #filename = "Kwal0.3_SAKL0D07062g_KLLA0F01793g"
    #name_index_order = filename.split("_")
    #alnfile = "/Users/bingwang/VimWork/lib/test/"+filename+".fa"
    #outfile = "/Users/bingwang/VimWork/lib/test/"+filename+".aa"
    #reffile = "/Users/bingwang/VimWork/lib/test/"+filename+".ref"
    ##Arguments
    #gap_sign = "-"
    #gap_allow = 0    #can be any int >= 0 
    #min_conserve = 5    
    #min_flanking = 10    #should be biger than min_conserve or won't work
    #max_nonconserve = 6    
    #judge_conserve = 1.0    #any float between (0,1)
    ##Mianfun
    #gene = read_aln(alnfile)
    #mark = aln_mark(gene,judge_conserve,gap_sign)
    #keep = gene_refine(mark,gap_allow,min_conserve,min_flanking,max_nonconserve)
    #write_aa(gene,name_index_order,keep,outfile)
    #
    ##for more beautiful printing 
    #mark = mark.replace("C",":") #: means conserved
    #mark = mark.replace("N"," ") #. means noncenserved 
    #mark = mark.replace("X"," ") # means gap

    #keep = keep.replace("F"," ") # means not good aliment
    #keep = keep.replace("T","=") #_ means good alinment 
    #
    #write_ref(gene,name_index_order,mark,keep,reffile,gap_allow,min_conserve,\
    #        min_flanking,max_nonconserve,judge_conserve)


