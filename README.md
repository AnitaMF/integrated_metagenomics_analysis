# Integrated Metagenomics Analysis 

This is a tool that integrates all steps required for taxonomic analysis of metagenomic data in an automated manner 

##  Project Introduction

[Metagenomics](https://en.wikipedia.org/wiki/Metagenomics) is a powerful approach for studying the genetic material (DNA) recovered directly from environmental samples. Unlike traditional microbiology, which relies on culturing organisms in the lab, metagenomics allows researchers to analyze the entire community of microorganisms in a given environment. This approach provides insights into the [diversity](https://bio.libretexts.org/Bookshelves/Ecology/Biodiversity_(Bynum)/7%3A_Alpha_Beta_and_Gamma_Diversity) and [composition/taxonomy](https://www.lawinsider.com/dictionary/taxonomic-composition#:~:text=Taxonomic%20composition%20means%20the%20identity,or%20within%20a%20water%20body.) of microbial communities, which are crucial for understanding ecosystems, human health, agriculture, and biotechnology.

However, the process of analyzing metagenomic data involves multiple complex and time-consuming steps. These include downloading data, quality control, host decontamination, taxonomic classification, and downstream analysis. The Integrated Metagenomics Analysis Pipeline is designed to streamline these steps, offering a fully automated solution for comprehensive metagenomic analysis.


## Generating Data
![Generating Data](/generating_data.PNG)

To generate metagenomic data:
1. **DNA Extraction**: DNA is isolated from the sample.
2. **DNA Fragmentation**: The DNA is broken into smaller pieces, called reads.
3. **Sequencing**: The reads are sequenced using Next-Generation Sequencing (NGS) techniques, producing a large volume of sequence data that represents the sample's genetic diversity.

**Next-Generation Sequencing (NGS)** technologies enable high-throughput sequencing, allowing millions of DNA fragments to be sequenced simultaneously. This capability is essential for metagenomic studies, which aim to analyze the vast and diverse microbial populations in complex samples.

**Note**: This pipeline includes a step for downloading publicly available data from SRA, but it can also be used with your own data.

## Analyzing Metagenomic Data

###  (1) pre-processing 
Once we have the sequences, the goal is to identify the microorganisms present in the community and determine the proportions of each organism within the sample, approximating their abundances in the community. Before this analysis, pre-processing of the sequencing reads is necessary:

0. **Download Data/Produce Your Own Data**
1. **Quality Control**: Ensuring data integrity and suitability for analysis.
2. **Host Decontamination**: Removing any host DNA contamination to focus on microbial sequences.

**Note**: Host decontamination depends on the source of the sample. For example, if the samples are from the human gut microbiome (stool samples representing the gut community), we will remove all human sequences found in the sequencing data, as the human DNA represents the "host" of the microbial community.

### (2) Taxonomic Classification: What Microorganisms Are Present?

**Note**: We can assess the presence of species, genus, families, and other taxonomic levels. For simplicity, we will focus on species.

To determine the species present, we will use the [Kraken algorithm](https://ccb.jhu.edu/software/kraken/MANUAL.html), a highly accurate and efficient tool for assigning taxonomic labels to metagenomic DNA sequences. 

**Kraken Output**: Kraken generates a detailed report of the taxonomic composition of the sample by counting the number of reads that match each species in a provided database. The main output is a table/matrix for each sample, listing the number of reads corresponding to each identified microorganism.

[View sample.k2report kraken output example](SRR14291145.k2report)

Using the **sample.k2report output from Kraken**, we will run the [Bracken algorithm](https://github.com/jenniferlu717/Bracken), which uses Bayes' theorem to re-estimate the number of reads that match a species. This step is necessary because some reads will match more than one species.

[View bracken output example]()
### (3) Analysis of Taxonomic Results (Python-based)

Once the taxonomic classification is complete, we will perform a comprehensive analysis of the results using Python. This analysis includes:

- **Read Counts to Frequencies**: Converting raw read counts into relative frequencies to account for differences in sequencing depth across samples. This normalization allows for more accurate comparisons between samples.
- **Rarefaction Curves**: Generating rarefaction curves to assess the adequacy of sequencing depth. These curves help determine if the sampling effort has been sufficient to capture the diversity present in the samples.
- **Data Distribution Visualizations and Transformations**: Visualizing the distribution of taxa across samples using various plots (e.g., bar plots, heatmaps). Transformations (e.g., log transformation) may be applied to stabilize variance and meet the assumptions of statistical tests.
- **Diversity Metrics**: Calculating diversity metrics such as alpha diversity (within-sample diversity) and beta diversity (between-sample diversity). These metrics provide insights into the complexity and variation of microbial communities.

# USAGE
## For a project of interest this pipeline will:
1. Download metadata from [SRA Run Selector](https://0-www-ncbi-nlm-nih-gov.brum.beds.ac.uk/Traces/study/) 
2. Download all genomic files of project from [SRA](https://www.ncbi.nlm.nih.gov/sra) based on metadata (step 1)
3. Run QC analysis using [FastQC](https://github.com/s-andrews/FastQC) and [Seqkit](https://github.com/shenwei356/seqkit/releases) - this step will be depedent on the needs of your files 
4. Perform host-decontamination using Bowtie 
5. Taxonomic classification using [Kraken algorithm](https://ccb.jhu.edu/software/kraken/MANUAL.html)
6. Re-estimate read counts using [Bracken algorithm](https://github.com/jenniferlu717/Bracken) 
7. Analysis of taxonomic results (Python-based):
    - Read counts to frequencies 
    - Rarefaction curves 
    - Data distribution visualizations and transformations
    - Diversity metrics

###  Instructions
1. install dependencies 
    pip install -r requirements.txt
2. download code

3. Run tests with pytest: 
    pytest 



> This project was originally implemented as part of the [Python programming course](https://github.com/szabgab/wis-python-course-2024-04)
> at the [Weizmann Institute of Science](https://www.weizmann.ac.il/) taught by [Gabor Szabo](https://szabgab.com/)
