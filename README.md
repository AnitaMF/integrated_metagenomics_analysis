# Integrated Metagenomics Analysis 

This is a tool that integrates all steps required for taxonomic analysis of metagenomic data in an automated manner 

##  Project Introduction

Metagenomics is a powerful approach for studying the genetic material (DNA) recovered directly from environmental samples. Unlike traditional microbiology, which relies on culturing organisms in the lab, metagenomics allows researchers to analyze the entire community of microorganisms in a given environment. This approach provides insights into the [diversity](https://bio.libretexts.org/Bookshelves/Ecology/Biodiversity_(Bynum)/7%3A_Alpha_Beta_and_Gamma_Diversity) and [composition/taxonomy](https://www.lawinsider.com/dictionary/taxonomic-composition#:~:text=Taxonomic%20composition%20means%20the%20identity,or%20within%20a%20water%20body.) of microbial communities, which are crucial for understanding ecosystems, human health, agriculture, and biotechnology.

## Generating data 
![](/generating_data.PNG)



## Analyzing metagenomic data 

However, the process of analyzing metagenomic data involves multiple complex and time-consuming steps. These include downloading data, quality control, host decontamination, taxonomic classification, and downstream analysis. The Integrated Metagenomics Analysis Pipeline is designed to streamline these steps, offering a fully automated solution for comprehensive metagenomic analysis.


After 
## For a project of interest this pipeline will:
1. Download metadata from [SRA Run Selector](https://0-www-ncbi-nlm-nih-gov.brum.beds.ac.uk/Traces/study/) 
2. Download all genomic files of project from [SRA](https://www.ncbi.nlm.nih.gov/sra) based on metadata (step 1)
3. Run QC analysis using [FastQC](https://github.com/s-andrews/FastQC) and [Seqkit](https://github.com/shenwei356/seqkit/releases) - this step will be depedent on the needs of your files 
4. Perform host-decontamination using Bowtie 
5. Taxonomic classification using Kraken algorithm
6. Estimate relative abundances using Bracken algorithm 
7. Analysis of taxonomic results (Python-based):
    - Read counts to frequencies 
    - Rarefaction curves 
    - Data distribution visualizations and transformations
    - Diversity metrics
    - Analysis of differentially abundant bacteria

### Usage: 

1. install dependencies 
    pip install -r requirements.txt
2. download code 



## What is metagenomics data? 

> This project was originally implemented as part of the [Python programming course](https://github.com/szabgab/wis-python-course-2024-04)
> at the [Weizmann Institute of Science](https://www.weizmann.ac.il/) taught by [Gabor Szabo](https://szabgab.com/)
