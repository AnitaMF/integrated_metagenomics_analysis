#!/bin/bash

cd ~/integrated_analysis/kraken
mkdir k2.reports 
mkdir kraken_outputs

cd ~/integrated_analysis


for x in $(ls *_1_.fastq.gz); do     y=${x%_1_trim.fastq.gz}_2_.fastq;     z=${x%_1_.fastq.gz};     kraken2 --db /integrated_analysis/kraken/k2_standard_20240112 --threads 8  --report /integrated_analysis/kraken/k2.reports/$z.k2report  --paired /integrated_analysis/fastq/$x /integrated_analysis/fastq/$y > /integrated_analysis/kraken/kraken_outputs/$z.kraken2; done


