#!/bin/bash

cd ~/integrated_analysis/bracken
mkdir bracken_outputs
mkdir bracken_reports

cd ~/integrated_analysis

for x  in $(ls *_1_trim.fastq); do     z=${x%_1_trim.fastq};  -d /integrated_analysis/kraken/k2_standard_20240112/ -i /integrated_analysis/kraken/k2.reports/$z.k2report -r 75 -l S -t 10 -o /integrated_analysis/bracken/bracken_outputs/$z.bracken -w  /integrated_analysis/bracken/breports/$z.breport;done
