==========
AftGalLoss
==========


Info
~~~~

+---------------+-----------------------------------------------------+
| Project Term: | AftGalLoss                                          |
+===============+=====================================================+
| Description:  | What Happens to yeast Genome after gal-network lost |
+---------------+-----------------------------------------------------+
| Author:       | BingWang                                            |
+---------------+-----------------------------------------------------+
| Last Modify:  | |today|                                             | 
+---------------+-----------------------------------------------------+
| Version:      | 0.02                                                |
+---------------+-----------------------------------------------------+

Goals and Hypothesis
~~~~~~~~~~~~~~~~~~~~

    The ambitious hypothesis is evolution is predictable. Short goal is to see what happens to yeast genome after gal network lost. 

    In this project, our hypothesis is "After gal net work lost, genes which evolve faster or slower should have something in common". "common" means share same groups of genes or share same gene ontology terms or even share same gene network topology.

    So before we go further, we need to know the *"evolve speed"*. Here is our solution:

    .. figure:: images/definition.png
        :height: 250

        These are two phylogeny trees of two specific genes, in (a)sp0 branch much 
        shorter than sp1 branch, so we assume this gene evolve slower in sp0 than in 
        sp1. While in (b) sp0 evolve faster. So we define **evolve speed** as **log2(sp2/sp1)**

Method
~~~~~~

Prepare 
-------

First, we need to get some species that lost its gal network.

So in this figure [1]_ :

.. figure:: images/Species_Tree.png
    :width: 300

    The symbol **x** here means species lost gal network

We have three species that lost gal network. And pick out their three
species threes. So we have three trees.

.. figure:: images/Four_three_sp_tree.png
    :height: 150

    The two C.gla trees are control tree pairs.


The genome data and orthologs files are from 
`Regev's Fungal Orthogroups v1.1 <http://www.broadinstitute.org/regev/orthogroups/>`_

.. tip::
    Here is a python script to grab the whole genome data and orthologs file(see get-data_),which need module `mechanize <http://wwwsearch.sourceforge.net/mechanize/download.html>`_

And we create a pipeline to calculte the speed rate:

.. figure:: images/pipeline.png
    :width: 300

.. note:: code(see cal-speed_)

Technical details(You may `skip this section`__)
    
    1. We use one2one orthologs, that means only those gene pairs appear in 
       both orthologs files (A-B and B-A) and appear only once([A_1,B_1] 
       not [A_1,B_1,B_2]) are considered as one2one orthologs.
       Others(include [A_1,NONE]) are ignored.

    2. We use `dialign-tx <http://dialign-tx.gobics.de/index>`_ do the mutiply
       alignment. And we have used `dialign-t <http://dialign-tx.gobics.de/
       dialign_t_results>`_ and `dialign 2.2 <http://bibiserv.techfak.uni-
       bielefeld.de/dialign/>`_, but these two seems have some bugs that several
       multiply would output nothing while dialign-tx is pretty good. We also 
       use `clustal-w <http://www.clustal.org/clustal2/>`_ It seems not suitable
       for phylogeny analysis. However, its not easy to get dialign-tx work on 
       64-bit MacOS, I have changed several int type variable to 64-bit long int, 
       or I won't pass the compile. On Linux Ubuntu-10.4 system, you can apt-get it, 
       it won't be a problem. It doesn't work on Windows unless you use cygwin or 
       other virtual tech.

    3. After alignment, we did refinement, so bad alignment won't influence our result.
       We plan to use Gblocks, However, we can't download it from its' `website
       <http://molevol.cmima.csic.es/castresana/Gblocks.html>`_ (Now it can!). So
       we refer the original paper [2]_ [3]_ and rewrite a simple python version of 
       "Gblocks" code at :ref:`alnrefine`. In this program, we judge a conserve site
       by seeing the percent of the biggest same aligned bases. Default value is 1.0,
       this means unless all the bases are same, or it is non-conserve site. And we only 
       want those alignment has more than *min_conserve* conserve site or length bigger
       than *min_flanking* and gaps no more than *gap_allow* and continues non-conserve
       site no more than *max_nonconserve*. This is an typical reference output. 

            .. figure:: images/Eg_for_refine.png

    4. We use `paml <http://abacus.gene.ucl.ac.uk/software/paml.html>`_ do the branch length 
    analysis. Here are the parameters we use. 
    
        ::
            
            noisy = 0               * 0,1,2,3,9: how much rubbish on the screen 
            verbose = 1	            * 0: concise; 1: detailed, 2: too much 
            runmode = 0	            * 0: user tree;  1: semi-automatic;  2: automatic 
                                    * 3: StepwiseAddition; (4,5):PerturbationNNI; -2: pairwise noise 
            seqtype = 2	            * 1:codons; 2:AAs; 3:codons-->AAs 
            aaRatefile = wag.dat	* only used for aa seqs with model=empirical(_F) 
            model = 8	            * models for AAs or codon-translated AAs: 
                                    * 0:poisson, 1:proportional, 2:Empirical, 3:Empirical+F 
                                    * 6:FromCodon, 7:AAClasses, 8:REVaa_0, 9:REVaa(nr=189) 
            Mgene = 0               * AA: 0:rates, 1:separate 
            clock = 0               * 0:no clock, 1:global clock; 2:local clock 
            fix_alpha = 1           * 0: estimate gamma shape parameter; 1: fix it at alpha 
            alpha = 0.0             * initial or fixed alpha, 0:infinity (constant rate) 
            Malpha = 0              * different alphas for genes 
            ncatG = 5               * of categories in dG of NSsites models 
            getSE = 1               * 0: don't want them, 1: want S.E.s of estimates 
            RateAncestor = 0        * (0,1,2): rates (alpha>0) or ancestral states (1 or 2) 
            Small_Diff = 1e-06
            cleandata = 1	        * remove sites with ambiguity data (1:yes, 0:no)? 
            fix_blength = 0	        * 0: ignore, -1: random, 1: initial, 2: fixed 
            method = 1	            * 0: simultaneous; 1: one branch at a time

    5. While calculate the evolve rate, we have a approximately, all branch length equal 
    to 0 will be give a minimal value 0.0001,and evolve rate bigger than 4 will be 
    equals to 4.(4 is quite big for evolve speed, though bigger are amplified by divide 
    a very small number like 0.0001)

__ analysis_
.. _analysis:

Analysis
--------

Till now we analysed:
    #. Histogram of evolve speed:
        .. figure:: images/Hist_log.png
            :width: 600

            it seems in most of the case, sp0 tend to evolve faster than sp1.
            There are two explanations. 1. These genes are evolve faster
            because some specific reasons. 2. The species evolve faster and
            these genes are just a tend representation. 

    #. Liner model
        We calculate all gene's tree and their evolve speed and see whether
        different liner model can explain the evolve speed difference between
        sp0(Gal-) and sp1(Gal+), and we get these figures:

        .. figure:: images/co_Cgla(Sbay)_Agos.png
            :width: 600

        This is a typical correction we get. Another "better" out put is:

        .. figure:: images/co_Kwal_Agos.png
            :width: 600

        But is still far from what we expected like the positive control:

        .. figure:: images/co_Cgla(Scer)_Cgla(Sbay).png
            :width: 600

    #. Gene Ontology
        We analysis the both tails of the histogram(log2(Sgla/Scer)>2). And We
        get an enrichment on A.gos's left tail and right tail. This means A.gos
        evolve faster in amino acid metabolism and evolve slower in signal
        transduction .Except this, we get nothing.(I will add figures and tables 
        later...)

    #. NewWork Analysis
        We collect a whole genome protein-protein(PP) network. And found a
        significant lower evolved gene g 


Problems
--------

+ Our hypothesis is gal network loss may influence some specific genes,
  but some genes evolve faster just because the species evolve faster. 
  So we should get rid of these genes)

+ The influenced genes may not that much because of the whole network
  robust. So it's hard to discover a miner signal under a strong white
  noise.

+ We use the one2one orhtologs so many genes are ignored, those may gene
  duplicates or novel genes which also can be a influenced signal. 

TODO
~~~~

+ Construct a bigger tree.
+ Learn Local GO analysis

Interests
---------

+ We found A.gos evolve faster in genes that correlated with amino acid
  metabolism

Eurekas
-------

+ We have new project :ref:`YeastNet`
+ We have new project :ref:`Scer_Spom`
+ We have next project :ref:`Gene Trees`
+ We have next project :ref:`Agos`

References
~~~~~~~~~~
.. [1] `Slot JC, Rokas A, 2010 <http://www.pnas.org/content/107/22/10136.short>`_
.. [2] `Talavera G, Castresana J, 2007 <http://molevol.cmima.csic.es/castresana/pdf/Talavera_2007.pdf>`_
.. [3] `Castresana J, 2000 <http://molevol.cmima.csic.es/castresana/pdf/Castresana_2000.pdf>`_

Source Codes
~~~~~~~~~~~~~~

.. _get-data:

download_regev.py
-----------------

.. literalinclude:: download_regev.py
    :language: python
    :encoding: utf-8

.. note::
    The more elegant code at :ref:`download-webpage`

.. _cal-speed:

AftGalLossAnalysis.py
--------------------------

.. literalinclude:: AftGalLossAnalysis_V001.py
    :language: python
    :encoding: utf-8




