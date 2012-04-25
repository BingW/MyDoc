##Download whole genomes and orthologs from Regev's orthogroups
import mechanize
from time import sleep

br = mechanize.Browser()
_temp = mechanize.Browser()
##Download aa and nt
br.open('http://www.broadinstitute.org/regev/orthogroups/sources.html')
for l in br.links():
    if l.url.startswith("nt") and l.url.endswith(".fasta"):
        fasta_file = l.url[l.url.rfind("/")+1:]
        sleep(1)
        print fasta_file
        _temp.open('http://www.broadinstitute.org/regev/orthogroups/aa/'+fasta_file)
        f = open("aa/"+fasta_file,"w")
        f.write(_temp.response().read())
        f.close()
        sleep(1)
        _temp.open('http://www.broadinstitute.org/regev/orthogroups/nt/'+fasta_file)
        f = open("nt/"+fasta_file,"w")
        f.write(_temp.response().read())
        f.close()

##Download orthologs
br.open('http://www.broadinstitute.org/regev/orthogroups/orthologs.html')
for l in br.links():
    if l.url.endswith(".txt"):
        ortholog_file = l.url[l.url.rfind("/")+1:].replace("%0A","")
        sleep(1)
       _temp.open('http://www.broadinstitute.org/regev/orthogroups/orthologs/'+ortholog_file)
        f = open("orthologs/"+ortholog_file,"w")
        f.write(_temp.response().read())
        f.close()


