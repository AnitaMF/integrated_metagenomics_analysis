import os
import pandas as pd
import numpy as np
from functions import (
    process_breport_files,
    list_csv_files,
    compute_relative_abundance,
    filter_low_abundance_species,
    generate_graphs,
    calculate_alpha_diversity
)
import matplotlib.pyplot as plt

# All test results will be saved in this folder (which will be deleted at the end)
output_folder = './test_output'
os.makedirs(output_folder, exist_ok=True)

def test_process_breport_files():
    bracken_files_directory = './bracken_files'
    selected_rank = 'S'
    bracken_files = [os.path.join(bracken_files_directory, file) for file in os.listdir(bracken_files_directory) if file.endswith('.breport')]

    process_breport_files(bracken_files, [selected_rank], output_folder)

    output_file = os.path.join(output_folder, f'{selected_rank}_counts_matrix.csv')
    assert os.path.exists(output_file)

    df = pd.read_csv(output_file, index_col=0)
    assert "Ruminiclostridium cellulolyticum" in df.index
    assert df.loc["Ruminiclostridium cellulolyticum", "SRR14291145" ] ==  107

def test_list_csv_files():
    expected_files = ['S_counts_matrix.csv']  

    for file in expected_files:
        open(os.path.join(output_folder, file), 'r').close()

    csv_files = list_csv_files(output_folder, '.csv')

    assert all(file in csv_files for file in expected_files)
    assert len(csv_files) == len(expected_files)

def test_compute_relative_abundance():
    input_file = './test_output/S_counts_matrix.csv'  
    output_file = './test_output/S_relative_abundance.csv'
    
    compute_relative_abundance(input_file, output_file)

    assert os.path.exists(output_file)

    df = pd.read_csv(output_file, index_col=0)
    print("DataFrame:")
    print(df.head()) 
    assert "Ruminiclostridium cellulolyticum" in df.index
    assert df.loc["Ruminiclostridium cellulolyticum", "SRR14291145"] ==  0.0020903475564227


def test_filter_low_abundance_species():
    input_file = './test_output/S_relative_abundance.csv'
    output_folder = './test_output'
    output_file = os.path.join(output_folder, 'S_relative_abundance_filtered.csv')
    output_file_log2 = os.path.join(output_folder, 'S_relative_abundance_filteredAndLog2.csv')

    df = pd.read_csv(input_file, index_col=0)
    filter_low_abundance_species(df, threshold=0.01, output_folder=output_folder, input_file=input_file)

    assert os.path.exists(output_file), f"Expected output file {output_file} does not exist."
    assert os.path.exists(output_file_log2), f"Expected log2 output file {output_file_log2} does not exist."

    filtered_df = pd.read_csv(output_file, index_col=0)
    print("Filtered DataFrame:")
    print(filtered_df.head())  
    assert "Bacteroides intestinalis" in filtered_df.index
    assert df.loc["Bacteroides intestinalis", "SRR14291145"] == 0.2203460755971263


def test_generate_graphs():
    input_file_abun = './test_output/S_relative_abundance.csv'
    input_file_filtered = './test_output/S_relative_abundance_filtered.csv'
    output_folder = './test_output'
    rank = 'S' 
    mean_NoZeros_file = './test_output/mean_NoZeros.csv'

    mean_NoZeros = pd.read_csv(mean_NoZeros_file, index_col=0)
    df = pd.read_csv(input_file_abun, index_col=0)
    df_filt = pd.read_csv(input_file_filtered, index_col=0)

    generate_graphs(df, df_filt, mean_NoZeros, output_folder, rank)
    assert os.path.exists(os.path.join(output_folder, 'graphs', 'proportion_zeros_S.png')), "Proportion zeros graph not found"
    assert os.path.exists(os.path.join(output_folder, 'graphs', 'hist_mean_abundance_S.png')), "Histogram mean abundance graph not found"
    assert os.path.exists(os.path.join(output_folder, 'graphs', 'hist_column_sums_filtered_S.png')), "Histogram column sums filtered graph not found"
    assert os.path.exists(os.path.join(output_folder, 'graphs', 'hist_before_after_log2_S.png')), "Histogram before and after log2 graph not found"

    print("All tests passed!")

def test_calculate_alpha_diversity():
    output_folder = './test_output'
    input_file_filtered = './test_output/S_relative_abundance_filtered.csv'
    output_file = './test_output/S_alpha_diversity.csv'
    rank = 'S'

    df = pd.read_csv(input_file_filtered, index_col=0)
    alpha_diversity = calculate_alpha_diversity(df, rank, output_folder)
    assert isinstance(alpha_diversity, pd.DataFrame)

    df = pd.read_csv(output_file, index_col=0)
    assert "SRR14291145" in df.index
    assert df.loc["SRR14291145", df.columns[1]] == 228

# cleanup of test_output folder- running pytest with existing test_output results yields fail
def teardown_module(module):
    if os.path.exists(output_folder):
        for file in os.listdir(output_folder):
            file_path = os.path.join(output_folder, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error cleaning up file: {file_path}, Error: {e}")

        graphs_folder = os.path.join(output_folder, 'graphs')
        if os.path.exists(graphs_folder):
            for file in os.listdir(graphs_folder):
                file_path = os.path.join(graphs_folder, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Error cleaning up file: {file_path}, Error: {e}")
            os.rmdir(graphs_folder)
        
        os.rmdir(output_folder)