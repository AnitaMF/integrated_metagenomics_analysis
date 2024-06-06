# Integrated Metagenomics Analysis 

This is a tool that integrates all steps required for taxonomic analysis of metagenomic data in an automated manner 

## For a project of interest:
1. Download metadata from [SRA Run Selector](https://0-www-ncbi-nlm-nih-gov.brum.beds.ac.uk/Traces/study/) 
2. Download all genomic files of project from [SRA](https://www.ncbi.nlm.nih.gov/sra)
3. Run QC analysis using [FastQC](https://github.com/s-andrews/FastQC) and [Seqkit](https://github.com/shenwei356/seqkit/releases) 
4. Perform host-decontamination using Bowtie 
5. Taxonomic classification using Kraken algorithm
6. Estimate relative abundances using Bracken algorithm 
7. Analysis of taxonomic results (Python-based):
    - Read counts to frequencies 
    - Rarefaction curves 
    - Data distribution visualizations and transformations
    - Diversity metrics
    - Analysis of differentially abundant bacteria
