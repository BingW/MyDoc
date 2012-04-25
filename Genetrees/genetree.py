#coding: utf-8
import os
from Bio.Seq import Seq

pillar_tab_file = "/Users/bingwang/VimWork/db/Pillars.tab"
f = open(pillar_tab_file)
gene_tree = {}
aln_groups = {}
for i,line in enumerate(f):
    line = line.strip()
    genename = line.split("\t")
    aln_groups[i] = [name for name in genename if name != "---" and name[:3] != "Anc"]
    evolve_pattern = ""
    for a in genename:
        has = "F" if a == "---" else "T"
        evolve_pattern += has
    try:
        gene_tree[evolve_pattern].append(i)
    except:
        gene_tree[evolve_pattern] = [i]

genome_tab_path = "/Users/bingwang/VimWork/db/genome_tab/"
gene2sp = {}
tab_files = [a for a in os.listdir(genome_tab_path) if a.endswith(".tab")]
for tab_file in tab_files:
    sp_name = tab_file[:tab_file.find("_")]
    f = open(genome_tab_path + tab_file)
    for line in f:
        elements = line.split("\t")
        gene2sp[elements[0]] = sp_name

f = open("/Users/bingwang/VimWork/db/YGOB_data.fsa")

gene2sq = {}
for line in f:
    if line[0] == ">":
        name = line[1:line.find(" ")]
        gene2sq[name] = ""
    else:
        gene2sq[name] += line.strip()

f = open("/Users/bingwang/VimWork/db/AA.fsa")
for line in f:
    if line[0] == ">":
        name = line[1:line.find(" ")]
        gene2sq[name] = ""
    else:
        gene2sq[name] += line.strip()

#write aln_group_files
for index in aln_groups:
    if len(aln_groups[index]) > 1:
        f = open("/Users/bingwang/VimWork/GeneTree/Aln/"+str(index)+".fsa","w")
        for name in aln_groups[index]:
            f.write(">"+gene2sp[name]+"|"+name+"\n")
            f.write(gene2sq[name]+"\n") 


def batch_run_dialign(path):
    print "************************************"
    print "***         Doing Alignment      ***"
    print "************************************"
    conf = "/Users/bingwang/VimWork/lib/conf/"
    dialign = "dialign-tx "
    fsalist = [a for a in os.listdir(path) if a.endswith(".fsa")]
    for i,item in enumerate(fsalist):
        print i*1.0/len(fsalist)
        infile = path+item
        outfile = path+item[:item.rfind(".")]+".aln"
        cmd = dialign+" "+conf+" "+infile+" "+outfile
        os.system(cmd)

def batch_run_Gblocks(path):
    alnlist = [a for a in os.listdir(path) if a.endswith(".aln")]
    for i,item in enumerate(alnlist):
        print i*1.0/len(alnlist)
        infile = path+item
        cmd = "Gblocks "+infile+" -t=p -e=.gb -b4=5 -a=y"
        os.system(cmd)

batch_run_Gblocks("/Users/bingwang/VimWork/GeneTree/Aln/")
