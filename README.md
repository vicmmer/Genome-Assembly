# Pipeline Overview 
Using this repository you will be able to process your samples to produce a genome assembly, and get a table of top blast hits associated with your samples.

What you will need for to be able to run this script is simply your raw files, in this case you may use the sample files provided

It is assumed that in this script, you will use the HCMV (NCBI accession NC_006273.2) as a reference to build a database, however this can be changed within the script.

## Dependencies 
You will need to have the following dependencies installed: 
1. BLAST
	Visit the [BLAST website](https://blast.ncbi.nlm.nih.gov/Blast.cgi) to download and install BLAST according to your operating system.
	Follow the installation instructions provided by the BLAST documentation.

2.  Bowtie
	Visit the [Bowtie website](http://bowtie-bio.sourceforge.net/index.shtml) to download and install Bowtie according to your operating system.
	Follow the installation instructions provided by the Bowtie documentation.

3. SPAdes
	Visit the [SPAdes GitHub repository](https://github.com/ablab/spades) to download and install SPAdes according to your operating system.
	Follow the installation instructions provided in the SPAdes documentation. 

## Data 
The sample data used to run this pipeline is a subset of the whole sequence, to make it more easily processable. Users might already have their data ready, but to make it easier I will show how I automated the download of my samples. I created a text file containing the accession numbers from NCBI of my samples to download called accessionsList.txt, the python script download_accessions.py was run to download and split the files into forward and reverse reads. Both of these files are provided for reference. File names: **accessionList.txt** and **download_accessions.py**

## How to Run the Script ## 
1. There are only two things you need to run the script: your fastq files (forward and reverse in _1.fastq and _2.fastq format
2. Now, you must run the python_wrapper script with the command: **python python_wrapper.py**
Once samples are downloaded, (one forward and reverse read file for each sample) you will have to run the python_wrapper.py script with the following command: python python_wrapper.py.  Likewise, you can clone the whole repository and you will have access too all the files needed to run the python_wrapper.py script
2. The script should run in about 2-3 minutes and will produce many output files. A description follows below:
   a) SampleName_filtered.*.fastq: these are the filtered fastq files, filtered to keep only the reads that map to the index, in this case the HCMV index.
   b) HCMV_index.*.bt2 : Bowtie2 produces multiple index files because it divides the index into multiple parts for efficient memory usage and faster alignment. Each of these index files serves a different purpose and will be used in the alignment process
   c) blast_hits.csv: Contains the top 10 blast hits to the ncbi database created.
   d) temp.log: this is just a temporary log file that will be combined with the blast_hits.csv file later to produce the final log file.
  e) PipelineProject.log: THIS IS THE MOST IMPORTANT file that reports the number of reads in each sample before and after filtering, the numver of contigs in the assembly that are larger than 1000 bp, the number of base pairs in the assembly, and a table with information for the top 10 blast hits. 
>>>>>>> 7dedfc28a197838178c37d4f8f640040f265e028
