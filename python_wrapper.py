from Bio import SeqIO
import os
import subprocess 
import pandas as pd

# Define the list of k-mer sizes
k_mer_sizes = "77,99,127"

# Define the number of threads to use
num_threads = 2

''' Thispart may change depending on the user's chosen database /reference, if different, user must change the 
link for download for their specific reference as well as the index_base name for their database''' 

#Download the HCMV reference 
wget_command = 'wget -O HCMV_reference.fasta "https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id=NC_006273.2&report=fasta&retmode=text"'
subprocess.run(wget_command, shell=True, check=True)

#Create bowtie index: 
bowtie_command = 'bowtie2-build HCMV_reference.fasta HCMV_index'
subprocess.run(bowtie_command, shell = True, check = True)

# Define the HCMV index base name
index_base = "HCMV_index"
'''Changes stop here for the user '''

# Define function to count reads in a fastq file
def count_reads(file_path):
    with open(file_path, 'r') as file:
        return sum(1 for line in file) // 4

# Store filtered fastq files
filtered_files = []

# List to store input files for SPAdes
spades_input_files = []

# Iterate over each sample pair
for file1 in os.listdir('.'):
    if file1.endswith('_1.fastq'):
        file2 = file1.replace('_1.fastq', '_2.fastq')
        sample_name = file1.split('_')[0]

        # Align reads using Bowtie2
        output_prefix = f"{sample_name}_filtered"
        command = f"bowtie2 -x {index_base} -1 {file1} -2 {file2} --al-conc {output_prefix}.fastq"
        subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE)

        # Count reads before and after filtering
        before_count = count_reads(file1)
        after_count = count_reads(f"{output_prefix}.1.fastq")  # Assuming Bowtie2 outputs filtered reads as *_1.fastq
        with open('temp.log', 'a') as log_file:
            log_file.write(f"{sample_name} had {before_count} read pairs before Bowtie2 filtering and {after_count} read pairs after.\n")
            log_file.write("\n")
        # Store filtered files
        filtered_files.extend([f"{output_prefix}.1.fastq", f"{output_prefix}.2.fastq"])

        # Add filtered files to SPAdes input
        spades_input_files.extend([f"{output_prefix}.1.fastq", f"{output_prefix}.2.fastq"])

# Assemble all transcriptomes together using SPAdes
output_folder = "combined_assembly"
spades_command = f"spades.py -k {k_mer_sizes} -t {num_threads} --only-assembler"
for i in range(0, len(spades_input_files), 2):
    spades_command += f" -1 {spades_input_files[i]} -2 {spades_input_files[i + 1]}"
spades_command += f" -o {output_folder}"

subprocess.run(spades_command, shell=True, check=True)

# Write SPAdes command to log file
with open('temp.log', 'a') as log_file:
    log_file.write(f"SPAdes assembly command: {spades_command}\n")
    log_file.write("\n")

# Count contigs > 1000 bp
contigs_count = 0
total_bp_count = 0

# Read SPAdes assembly contig lengths
assembly_folder = os.path.join(output_folder, "contigs.fasta")
with open(assembly_folder, 'r') as assembly_file:
    contig_length = 0
    for line in assembly_file:
        if line.startswith(">"):
            if contig_length > 1000:
                contigs_count += 1
                total_bp_count += contig_length
            contig_length = 0
        else:
            contig_length += len(line.strip())

# Write results to log file
with open('temp.log', 'a') as log_file:
    log_file.write(f"There are {contigs_count} contigs > 1000 bp in the assembly.\n")
    log_file.write(f"There are {total_bp_count} bp in the assembly.\n")
    log_file.write("\n")

# Define the directory containing the contigs.fasta file
assembly_folder = "combined_assembly"

# Define the path to the contigs.fasta file
contigs_file = os.path.join(assembly_folder, "contigs.fasta")

# Check if the contigs.fasta file exists
if os.path.exists(contigs_file):
    # Parse the contigs.fasta file
    with open(contigs_file, 'r') as f:
        contig_records = SeqIO.parse(f, "fasta")

        # Find the longest contig
        longest_contig = max(contig_records, key=lambda x: len(x.seq))

        # Write the longest contig to a file
        longest_contig_file = "longest_contig.fasta"
        with open(longest_contig_file, 'w') as output_f:
            SeqIO.write([longest_contig], output_f, "fasta")



#Download sequences to populate the database just created
download_command = "datasets download virus genome taxon Betaherpesvirinae --include genome"
subprocess.run(download_command, shell=True, check=True)
unzip_command = "unzip -o ncbi_dataset.zip"
subprocess.run(unzip_command, shell=True, check=True)  

# Making database locally to BLAST against
output_db = "Betaherpesvirinae_db"
makeblastdb_command = f"makeblastdb -in ncbi_dataset/data/genomic.fna -out {output_db} -title {output_db} -dbtype nucl"
subprocess.run(makeblastdb_command, shell=True, check=True)

#Blast
query_seqfile = "longest_contig.fasta"
output_file = "blast_hits.csv"
with open(output_file, 'w') as f:
    f.write("qseqid\tsseqid\tpident\tlength\tqstart\tqend\tsstart\tsend\tbitscore\tevalue\tstitle\n")

# Run BLAST command
import subprocess

# Define the blast command
blast_command = f'blastn -query {query_seqfile} -db Betaherpesvirinae_db -out {output_file} -outfmt 6 -max_target_seqs 10'
subprocess.run(blast_command, shell=True, check=True)

# Add headers using sed command through subprocess
import subprocess

# Define the blast command
blast_command = f'blastn -query {query_seqfile} -db Betaherpesvirinae_db -out {output_file} -outfmt 6 -max_target_seqs 10'

# Execute the blast command
subprocess.run(blast_command, shell=True, check=True)

# Add headers using sed command through subprocess
sed_command = f"sed -i '1s/^/# sacc\tpident\tlength\tqstart\tqend\tsstart\tsend\tbitscore\tevalue\tstitle\\n/' {output_file}"
subprocess.run(sed_command, shell=True, check=True)

# Load data from the log file
with open('temp.log', 'r') as log_file:
    log_data = log_file.read()

# Load data from the CSV file
csv_data = pd.read_csv('blast_hits.csv')

# Write log text to the new log file
with open('PipelineProject.log', 'w') as combined_log:
    combined_log.write(log_data)

    # Write separator between log text and table
    combined_log.write("\n\n==== Table from blast_hits.csv ====\n\n")

    # Write CSV data to the log file
    csv_data_string = csv_data.to_csv(index=False, sep='\t')
    combined_log.write(csv_data_string)
