# Genome-Assembly
Using this repository you will be able to process your samples to produce a genome assembly, and get a table of top blast hits associated with your samples. 

What you will need for to be able to run this script is simply your raw files, in this case you may use the sample files provided 

It is assumed that in this script, you will use the HCMV (NCBI accession NC_006273.2) as a reference to build a database, however this can be changed within the script.

The sample data used to run this pipeline is a subset of the whole sequence, to make it more easily processable. Users might already have their data ready, but to make it easier I will show how I automated the download of my samples. I created a text file containing the accession numbers of my samples to download called accessionsList.txt, the python script download_accessions.py was run to download and split the files into forward and reverse reads. Both of these files are provided for reference.  
