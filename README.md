# Integrated Metagenomics Analysis 

This is a tool that integrates all steps required for taxonomic analysis of metagenomic data in an automated manner.

**Input**: taxonomy tables from kraken&braken taxonomy classifier algorithms 

##  Project Introduction

[Metagenomics](https://en.wikipedia.org/wiki/Metagenomics) is a powerful approach for studying the genetic material (DNA) recovered directly from environmental samples. Unlike traditional microbiology, which relies on culturing organisms in the lab, metagenomics allows researchers to analyze the entire community of microorganisms in a given environment. This approach provides insights into the [composition/taxonomy](https://www.lawinsider.com/dictionary/taxonomic-composition#:~:text=Taxonomic%20composition%20means%20the%20identity,or%20within%20a%20water%20body.) and [diversity](https://bio.libretexts.org/Bookshelves/Ecology/Biodiversity_(Bynum)/7%3A_Alpha_Beta_and_Gamma_Diversity) of microbial communities, which are crucial for understanding ecosystems, human health, agriculture, and biotechnology.

However, the process of analyzing taxonomic data involves multiple complex and time-consuming steps and there is currently no standard protocol. **The Integrated Metagenomics Analysis Pipeline** is designed to streamline downstream analysis of taxonomy offering a solution for comprehensive metagenomic analysis. 

**Note**: There is a section at the end that explains in detail how to get taxonomy tables from metagenomic data. It includes all steps from downloading publicly available data from SRA & classifying reads into taxonomic profiles.

## Up-stream steps
### (1) Generating Data: Produce Your Own Data/Download Data

![Generating Data](/generating_data.PNG)

To generate metagenomic data:
1. **DNA Extraction**: DNA is isolated from the sample.
2. **DNA Fragmentation**: The DNA is broken into smaller pieces, called reads.
3. **Sequencing**: The reads are sequenced using Next-Generation Sequencing (NGS) techniques, producing a large volume of sequence data that represents the sample's genetic diversity.

**Next-Generation Sequencing (NGS)** technologies enable high-throughput sequencing, allowing millions of DNA fragments to be sequenced simultaneously. This capability is essential for metagenomic studies, which aim to analyze the vast and diverse microbial populations in complex samples.

![Workflow](Workflow.png)


### (2) Taxonomic Classification: What Microorganisms Are Present?
Once we have the sequences, the goal is to identify the microorganisms present in the community and determine the proportions of each organism within the sample, approximating their abundances in the community. 

a. **Taxonomic classification using** [Kraken algorithm](https://ccb.jhu.edu/software/kraken/MANUAL.html): To determine the species present the *Kraken algorithm* is a highly accurate and efficient tool for assigning taxonomic labels to metagenomic DNA sequences. 

**Kraken Output**: Kraken generates a detailed report of the taxonomic composition of the sample by counting the number of reads that match each species in a provided database. The main output is a table/matrix for each sample, listing the number of reads corresponding to each identified microorganism.
![kraken output](kraken_output.png)
View a complete kraken output file: [sample.k2report](SRR14291145.k2report)

b. **Re-estimate read counts using** [Bracken algorithm](https://github.com/jenniferlu717/Bracken): Using the **sample.k2report output from Kraken**, *Bracken algorithm*, which uses Bayes' theorem to re-estimate the number of reads that match a species. This step is necessary because some reads will match more than one species.
![braken output](bracken_output.png)
View complete braken output file: [sample.breport](SRR14291145.breport)


## Down-stream steps
## **Integrated Metagenomics Analysis Pipeline**

### Analysis of Taxonomic Results 

Once the taxonomic classification is complete, we will perform a comprehensive analysis of the results using Python based tool. This analysis includes:

- **Merge all samples into one matrix**: Using the **sample.bracken output files from bracken** we will create one table/matrix that contains the taxonomic classification results of all samples in the project for all downstream analysis. The table dimensions are species x # of samples
![matrix](matrix.png)
View complete matrix output file: [matrix.txt](readCount.txt)
- **Read Counts to Frequencies**: Converting matrix of read counts into relative frequencies to account for differences in sequencing depth across samples. This normalization allows for more accurate comparisons between samples.
- **Data Distribution Visualizations, filter low abundant taxa and Transformations**: Visualizing the distribution of taxa across samples using various plots (e.g., bar plots, heatmaps). Transformations (e.g., log transformation) may be applied to stabilize variance and meet the assumptions of statistical tests.
- **Diversity Metrics**: Calculating diversity metrics such as [alpha](https://docs.onecodex.com/en/articles/4136553-alpha-diversity) diversity (within-sample diversity) and [beta](https://www.statisticshowto.com/bray-curtis-dissimilarity/) diversity (between-sample diversity). These metrics provide insights into the complexity and variation of microbial communities.

# Pipeline Summary 
Analysis of taxonomic results:

- Merge results files 

- Read counts to frequencies 

- Filter low abundant bacteria 

- Data distribution visualizations and transformations

- Diversity metrics

#### This pipeline provides the option to run all of these steps at one or multiple taxonomic ranks (species, genus, family, etc.).

#### After running this pipeline, all files & graphs created will be saved inside *output* folder
## USAGE:

**Note**: make sure you have python installed 

#### 1. Clone the Repository

Using Git Bash/Terminal, run:
```sh
git clone https://github.com/AnitaMF/integrated_metagenomics_analysis.git
```
Alternatively, download the following files:

1. **Requirements.txt** # Contains the necessary libraries to run the program.
2. **functions.py** # Contains the functions used in the program.
3. **taxonomicAnalysis.py** # The main script that runs the program.

**Note**: To run this program, you will need breport files from the Bracken algorithm. Example files are provided in the bracken_files folder for testing the program.

#### 2. Ensure you are working from the folder of the cloned repository:

```sh
cd integrated_metagenomics_analysis
```
#### 3. Install Dependencies

Run:
```sh
pip install -r requirements.txt
``` 
#### 4. Run tests 

To verify everything is set up correctly, run:

```sh
pytest 
```
**Note**: For each function pytest verifies that the file is created and that the information inside is correct (and displayed). 

#### 5. Run program: 

a. Get Help and Available Options

To see how to correctly run the program and explore available options, run:

```sh 
python taxonomicAnalysis.py -h 
```

    Usage: taxonomicAnalysis.py [-h] [-r RANKS] --path_bracken PATH_BRACKEN

    Process bracken files and calculate diversity metrics.

    options:
      -h, --help            show this help message and exit
      -r RANKS, --ranks RANKS
                            Taxonomic ranks to process (e.g., S,G,F,O,C,P). Default is 'S'.
                            Example: -r S,G will process Species and Genus levels.
      --path_bracken PATH_BRACKEN, -path PATH_BRACKEN
                            Path to folder containing bracken files to be processed

b. Test pipeline with Provided Files

To test the program using the files provided in this repository, specifying the desired taxonomic rank(s) with the -r option, run:

```sh
python taxonomicAnalysis.py -path .\bracken_files -r S,G
```

c. Run the Program on Your Own Files

To run the program on your own breport files, provide the path to the directory containing those files. Specify the desired taxonomic rank(s) with the -r option, run:

Run: 
```sh
python taxonomicAnalysis.py -path .\PATH_TO_YOUR_BREPORT_FILES [-r S,G]
```
Replace PATH_TO_YOUR_BREPORT_FILES with the actual path to your breport files.



# Instructions for up-stream steps: 

## Detailed instructions for steps previous to the utilization of this pipeline: 
### Example of Running instructions: 

To examplify we will run all the steps for the following project: 

    PRJNA664754

Create a directory to store all files and code 
```sh
mkdir integrated_analysis    
```

#### Step 0: download data 
**OPTIONAL**: This step is optional and not automated- If you have your own data already proceed to step 1

1. Download accesion list from [SRA Run Selector](https://0-www-ncbi-nlm-nih-gov.brum.beds.ac.uk/Traces/study/)

a. Search for accesion list of project: Write project name and click on **search** 
![search](searchAccesion.PNG)
b. Click on "Acession list" to download a txt file containing the names of all the files in the project ![click](clickAcession.PNG) 
c. Move file into "integrated_analysis" folder and change file-name to "accession_list.txt"

View [accession list](SRR_Acc_List.txt) file

2. Download all fastq files of project 

a. Download [**SRA-toolkit**](https://github.com/ncbi/sra-tools/wiki/02.-Installing-SRA-Toolki)

b. Download files: 
```sh
prefetch --option-file accession_list.txt
```
#### Step 1: taxonomic classification 

0. Create a new folder "fastq" (Inside integrated_analysis folder) and move all fastq files 

```sh
mkdir fastq 
mv *.fastq.gz fastq
```

1. Kraken

**Note**: We can assess the presence of species, genus, families, and other taxonomic levels. For simplicity, we will focus on species.

a. Download kraken to integrated_analysis folder: [link](https://github.com/DerrickWood/kraken2/blob/master/docs/MANUAL.markdown) 

Or use: 
```sh
mkdir kraken
cd kraken 
./install_kraken2.sh 
```

b. Download database & unpack (inside kraken folder): this one has been updated in 2024
```sh
wget https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20240112.tar.gz 

tar -xzvf k2_standard_20240112.tar.gz
```
c. Run kraken on all samples: 

**Note**: Make sure the names of R1 and R2 have the following format: name_1_.fastq.gz and  name_2_.fastq.gz

```sh
./kraken_loop_paired.sh 
```
2. Bracken

a. Install bracken 
 ```sh
 mkdir bracken
 cd bracken 
  ./install_bracken.sh 
 ```
b. Run braken on all samples:

```sh
./bracken_loop.sh

```


> This project was originally implemented as part of the [Python programming course](https://github.com/szabgab/wis-python-course-2024-04)
> at the [Weizmann Institute of Science](https://www.weizmann.ac.il/) taught by [Gabor Szabo](https://szabgab.com/)
