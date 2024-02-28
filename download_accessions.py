import os

# Function to run fastq-dump for a given accession number
def run_fastq_dump(accession):
    command = f"fastq-dump --split-files {accession}"
    os.system(command)

# Read accession numbers from accessionList.txt and run fastq-dump for each
with open("accessionList.txt", "r") as file:
    for line in file:
        accession = line.strip()  # Remove newline character
        run_fastq_dump(accession)
