# -*- coding:utf-8 -*-
'''
Author: Bing Wang
Last Modified: 2012.3.18
Version: V0.01
'''
WORKPATH = "/Users/bingwang/VimWork/"
#########################
#######Import#############
import os
import sys
import time
import math
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
sys.path.append("/Users/bingwang/VimWork/")
import lib.read.read_orthogroups_tab as orth
import lib.func.alnrefine as alr 
import lib.func.paml as paml
#######  Class ##########
class Species():
    def __init__(self,name):
        self.name = name
        self.gene = {}
        f = open(WORKPATH+'db/'+self.name+"AA.fasta")
        for line in f:
            line = line.strip()
            if line[0] == ">":
                name = line[1:]
            else:
                self.gene[name] = line
        f.close()

######## Function ##########
def time_left(percent):
    time_used = time.time() - TIME_START
    print percent*100,'%'
    print "Time used:\t %.2f"%((time_used)/60.),'min'
    print "Time left:\t %.2f"%((time_used)*(1-percent)/(60.*percent)),'min'

def check_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def prepare_aln(sp0,sp1,sp2,outdir):
    print "************************************"
    print "*** Prepare Alignment input Data ***"
    print "************************************"
    for item in sp0.orth_sp1:
        try:
            sp0.orth_sp2[item]
            try:
                sp0.gene[item]
                sp1.gene[sp0.orth_sp1[item]]
                sp2.gene[sp0.orth_sp2[item]]
                write_f_name = item+"_"+sp0.orth_sp1[item]+"_"+ \
                        sp0.orth_sp2[item]+".fasta"
                f = open(outdir+write_f_name,"w")
                f.write(">"+item+"\n"+sp0.gene[item]+"\n")
                f.write(">"+sp0.orth_sp1[item]+"\n"+sp1.gene[sp0.orth_sp1[item]]+"\n")
                f.write(">"+sp0.orth_sp2[item]+"\n"+sp2.gene[sp0.orth_sp2[item]]+"\n")
                f.close()
            except:
                print "WARNING: gene",item,"not write" 
                continue
        except:
            pass


def batch_run_dialign(path):
    print "************************************"
    print "***         Doing Alignment      ***"
    print "************************************"
    fsalist = []
    conf = "/Users/bingwang/VimWork/lib/conf/"
    dialign = "dialign-tx "
    for item in os.listdir(path):
        if item[item.rfind(".")+1:] == "fasta":
            fsalist.append(item)
    total = len(fsalist)
    for i,item in enumerate(fsalist):
        time_left(i*1.0/total*0.25+TOTAL_PERCENT)
        infile = path+item
        outfile = path+item[:item.rfind(".")]+".fa"
        cmd = dialign+" "+conf+" "+infile+" "+outfile
        os.system(cmd)

def batch_refine_aln(path):
    print "**************************"
    print "*** Refining Alignment ***"
    print "**************************"
    for item in os.listdir(path):
        if item[item.rfind(".")+1:] == "fa":
            alr.refine(path + item)


def batch_write_ctl(aa_path,treefile=None):
    print "*****************************"
    print "*** Writing paml ctl file ***"
    print "*****************************"
    if treefile == None:
        treefile = WORKPATH + "lib/func/3.tree"
    for item in os.listdir(aa_path):
        if item[item.rfind(".")+1:] == "aa":
            paml.write_ctl(aa_path+item,treefile)
           
def batch_codeml(ctl_path):
    print "*********************"
    print "*** Runing codeml ***"
    print "*********************"
    ctllist = []
    for item in os.listdir(ctl_path):
        if item[item.rfind(".")+1:] == "ctl":
            paml.codeml(ctl_path+item)

def batch_read_output(out_path,outfile):
    f = open(outfile,"w")
    f.write("Sp0\tSp1\tSp2\tsp1+sp0\tsp2+sp0\tsp2+sp1\t\n")
    for item in os.listdir(out_path):
        if item[item.rfind(".")+1:] == "out":
            paml_out = paml.codeml_read(out_path+item)
            f.write(paml_out.write_line())
    f.close()

def branch_calculte(filename):
    f=open(WORKPATH+filename)
    f.readline()
    paml_rate = {}
    for line in f:
        line = line.strip()
        paml_out = paml.read_line(line)
        sp0 = round(((paml_out.sp1_sp0 + paml_out.sp2_sp0) - paml_out.sp2_sp1)/2,4)
        sp1 = round(((paml_out.sp2_sp1 + paml_out.sp1_sp0) - paml_out.sp2_sp0)/2,4)
        sp2 = round(((paml_out.sp2_sp1 + paml_out.sp2_sp0) - paml_out.sp1_sp0)/2,4)
        if math.isnan(sp0) or math.isnan(sp1) or math.isnan(sp2):
            pass
        else:
            sp0 = sp0 if sp0 > 0 else 0.0001
            sp1 = sp1 if sp1 > 0 else 0.0001
            sp0_devide_sp1 = sp0/sp1
            sp0_devide_sp1 = 16 if sp0_devide_sp1 > 16 else sp0_devide_sp1
            sp0_devide_sp1 = 0.0625 if sp0_devide_sp1 < 0.0625 else sp0_devide_sp1
            paml_rate[paml_out.sp0name]=np.log2(sp0_devide_sp1)    #paml-rate structure
    '''
    f = open(branch_file,"w")
    f.write("sp0\tB_sp0\tB_sp1\tB_sp2\n")
    for name in paml_rate:
        f.write(name+"\t"+str(paml_rate[name][0])+\
                "\t"+str(paml_rate[name][1])+\
                "\t"+str(paml_rate[name][2])+"\n")
    f.close()
    '''
    return paml_rate

def check_num_of_file(outdir):
    count_fasta = 0
    count_aa = 0
    count_out = 0
    for item in os.listdir(outdir):
        a = item[item.rfind(".")+1:]
        if a == "out":
            count_out += 1
        elif a == "fasta":
            count_fasta += 1
        elif a == "aa":
            count_aa += 1
    if count_out == count_aa and count_aa == count_fasta:
        return True
    else:
        return False

def pipe(sp_name):
    #########        Calculte function           ########
    outdir = WORKPATH+"AftGalLoss/"+sp_name[0] +"_"+sp_name[1]+"_"+sp_name[2]+"/"
    check_dir(outdir)    #if not exist,creat it
    sp0 = Species(sp_name[0])
    sp1 = Species(sp_name[1])
    sp2 = Species(sp_name[2])
    sp0.orth_sp1 = orth.one(sp0.name,sp1.name)
    sp0.orth_sp2 = orth.one(sp0.name,sp2.name)
    prepare_aln(sp0,sp1,sp2,outdir)
    batch_run_dialign(outdir)
    batch_refine_aln(outdir)
    batch_write_ctl(outdir)
    batch_codeml(outdir)
    if check_num_of_file(outdir):
        outfile = WORKPATH+"AftGalLoss/"+sp_name[0] +"_"+sp_name[1]+"_"+sp_name[2]+".txt"
        batch_read_output(outdir,outfile)
    
def hist_log_sp0_sp1(paml_rate,orth):
    count_right = 0
    log_sp0_sp1 = []
    for name in Bg_Genes:
        if sp0_devide_sp1 > 1:
            count_right += 1
        log_sp0_sp1.append(paml_rate[orth[name]])
    pr = (count_right)*1.0/len(log_sp0_sp1)
    plt.hist(log_sp0_sp1,100)

def draw_hist():
    plt.subplot(221)
    hist_log_sp0_sp1(Kwal_Sklu_Klac,Scer.orth_Kwal)
    plt.ylabel("frequency")
    plt.title("Hist(log2(Kwal/Sklu))")

    plt.subplot(222)
    hist_log_sp0_sp1(Cgla_Scer_Scas,Scer.orth_Cgla)
    plt.title("Hist(log2(Cgla/Scer))")

    plt.subplot(223)
    hist_log_sp0_sp1(Cgla_Sbay_Scas,Scer.orth_Cgla)
    plt.ylabel("frequency")
    plt.xlabel("log2(sp0/sp1)")
    plt.title("Hist(log2(Cgla/Sbay))")

    plt.subplot(224)
    hist_log_sp0_sp1(Agos_Klac_Sklu,Scer.orth_Agos)
    plt.title("Hist(log2(Agos/Klac))")
    plt.xlabel("log2(sp0/sp1)")

    plt.savefig("/Users/bingwang/VimWork/AftGalLoss/Hist_log.png",dpi=200)

def draw_scatter():
    import lib.draw.scatter_hist_test as scatter
    kwal_sklu = []
    cgla_scer = []
    cgla_sbay = []
    agos_klac = []
    for name in Bg_Genes:
        kwal_sklu.append(Kwal_Sklu_Klac[Scer.orth_Kwal[name]])
        cgla_scer.append(Cgla_Scer_Scas[Scer.orth_Cgla[name]])
        cgla_sbay.append(Cgla_Sbay_Scas[Scer.orth_Cgla[name]])
        agos_klac.append(Agos_Klac_Sklu[Scer.orth_Agos[name]])
    scatter.scatter(kwal_sklu,cgla_scer,WORKPATH+"AftGalLoss/co_Kwal_Cgla(Scer).png",\
            "lg2(Kwal/Sklu) vs lg2(Cgla/Scer)")
    scatter.scatter(kwal_sklu,cgla_sbay,WORKPATH+"AftGalLoss/co_Kwal_Cgla(Sbay).png",\
            "lg2(Kwal/Sklu) vs lg2(Cgla/Sbay)")
    scatter.scatter(kwal_sklu,agos_klac,WORKPATH+"AftGalLoss/co_Kwal_Agos.png",\
            "lg2(Kwal/Sklu) vs lg2(Agos/Klac)")
    scatter.scatter(cgla_scer,cgla_sbay,WORKPATH+"AftGalLoss/co_Cgla(Scer)_Cgla(Sbay).png",\
            "lg2(Cgla/Scer) vs lg2(Cgla/Sbay)")
    scatter.scatter(cgla_scer,agos_klac,WORKPATH+"AftGalLoss/co_Cgla(Scer)_Agos.png",\
            "lg2(Cgla/Scer) vs lg2(Agos/Klac)")
    scatter.scatter(cgla_sbay,agos_klac,WORKPATH+"AftGalLoss/co_Cgla(Sbay)_Agos.png",\
            "lg2(Cgla/Sbay) vs lg2(Agos/Klac)")

def go_term_query():
    f = open(WORKPATH+"/AftGalLoss/term_query_Genes.txt","w")
    f.write("Bg_Genes\tlog2(Kwal/Sklu)\tlog2(Cgla/Scer)\tlog2(Cgla/Sbay)\tlog2(Agos/Klac)\n")
    for name in Bg_Genes:
        f.write(name+"\t"+str(Kwal_Sklu_Klac[Scer.orth_Kwal[name]])\
               +"\t"+str(Cgla_Scer_Scas[Scer.orth_Cgla[name]])  \
               +"\t"+str(Cgla_Sbay_Scas[Scer.orth_Cgla[name]]) \
               +"\t"+str(Agos_Klac_Sklu[Scer.orth_Agos[name]])+"\n")

def p_value(n_hit,n,p):
    pv = 0
    for i in range(n_hit,n+1,1):
        pv += ((math.factorial(n)/(math.factorial(i)* \
                math.factorial(n-i)))*(p**i)*((1-p)**(n-i)))
    return pv
#############             Main              ################

############################
###       Calculte      ####
############################
#TIME_START = time.time()
#TOTAL_PERCENT = 0.0001
#Kwal_Sklu_Klac = pipe(["Kwal","Sklu","Klac"])
##TOTAL_PERCENT = 0.25
#Cgla_Scer_Scas = pipe(["Cgla","Scer","Scas"])
##TOTAL_PERCENT = 0.5
#Agos_Klac_Sklu = pipe(["Agos","Klac","Sklu"])
##TOTAL_PERCENT = 0.75
#Cgla_Sbay_Scas = pipe(["Cgla","Sbay","Scas"])
#Klac_Agos_Kwal = pipe([""])
##############################
###       Analysis         ###
##############################
Kwal_Sklu_Klac = branch_calculte("AftGalLoss/Kwal_Sklu_Klac.txt")
Cgla_Scer_Scas = branch_calculte("AftGalLoss/Cgla_Scer_Scas.txt")
Cgla_Sbay_Scas = branch_calculte("AftGalLoss/Cgla_Sbay_Scas.txt")
Agos_Klac_Sklu = branch_calculte("AftGalLoss/Agos_Klac_Sklu.txt")

Scer = Species("Scer")
Scer.orth_Kwal = orth.one("Scer","Kwal")
Scer.orth_Cgla = orth.one("Scer","Cgla")
Scer.orth_Agos = orth.one("Scer","Agos")
Scer.orth_Klac = orth.one("Scer","Klac")

Bg_Genes = []
for name in Scer.gene:
    try:
        Kwal_Sklu_Klac[Scer.orth_Kwal[name]]
        Cgla_Scer_Scas[Scer.orth_Cgla[name]]
        Cgla_Sbay_Scas[Scer.orth_Cgla[name]]
        Agos_Klac_Sklu[Scer.orth_Agos[name]]
        Bg_Genes.append(name)
    except:
        continue
#draw_hist()
#draw_scatter()
#go_term_query()


#TODO involve in network
import networkx as nx
import My_Physical_engine as Phy
import read_interaction_data as Interaction

interaction_file = "/Users/bingwang/VimWork/db/interaction_data.tab"
interactions = []
PP_net = nx.Graph()

f = open(interaction_file)
for line in f:
    line = line.strip()
    interaction = Interaction.Interaction_SGD(line)
    interactions.append(interaction)
f.close()
gal_genes = ["YBR018C","YBR019C","YBR020W","YDR009W",\
        "YLR081W","YML051W","YMR105C","YPL248C"]
#gene_name = [GAL7,GAL10,GAL1,GAL3,\
#           GAL2,GAL80,GAL5,GAL4]
for name in gal_genes:
    try:
        print Scer.orth_Klac[name]
    except:
        print "No:",name

'''
pp_exp_type = ["Reconstituted Complex","Two-hybrid","Protein-peptide", \
    "PCA","FRET","Far Western","Co-purification","Co-localization", \
    "Co-fractionation","Co-crystal Structure","Affinity Capture-Western",\
    "Affinity Capture-MS","Affinity Capture-Luminescence"]

for item in Interaction.exp_gene_filter(interactions,pp_exp_type,gal_genes):
    PP_net.add_node(item.bait_name)
    PP_net.add_node(item.hit_name)
    PP_net.add_edge(item.bait_name,item.hit_name)

PP_net = Interaction.sub_by_genes(Bg_Genes,PP_net)

query_genes = [name for name in Bg_Genes if Agos_Klac_Sklu[Scer.orth_Agos[name]] < -1] 
#query_genes = [name for name in Bg_Genes if Agos_Klac_Sklu[Scer.orth_Agos[name]] > 1] 
#query_genes = [name for name in Bg_Genes if Kwal_Sklu_Klac[Scer.orth_Kwal[name]] < -1] 
#query_genes = [name for name in Bg_Genes if Kwal_Sklu_Klac[Scer.orth_Kwal[name]] > 1] 
#query_genes = [name for name in Bg_Genes if Cgla_Sbay_Scas[Scer.orth_Cgla[name]] < -1] 
#query_genes = [name for name in Bg_Genes if Cgla_Sbay_Scas[Scer.orth_Cgla[name]] > 1] 
#query_genes = [name for name in Bg_Genes if Cgla_Scer_Scas[Scer.orth_Cgla[name]] < -1] 
#query_genes = [name for name in Bg_Genes if Cgla_Scer_Scas[Scer.orth_Cgla[name]] > 1] 

hit_genes = [name for name in query_genes if name in PP_net.nodes()] 
for gene in hit_genes:
    print gene
print "p value:",p_value(len(hit_genes),len(query_genes),len(PP_net.nodes())*1./len(Bg_Genes))
'''
