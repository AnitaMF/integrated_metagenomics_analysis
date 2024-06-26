import os
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy

def process_breport_files(bracken_files, selected_ranks, output_folder):
    big_dict = {}
    
    big_dict['b_report'] = [pd.read_csv(file, delimiter='\t') for file in bracken_files]
    b_names_report = [re.search(r'(SRR\d+)\.breport$', file).group(1) for file in bracken_files]
    big_dict['b_report'] = dict(zip(b_names_report, big_dict['b_report']))

    col_names = ["percent_reads", "num_reads", "no_se", "level", "taxo_id", "organism"]
    for df in big_dict['b_report'].values():
        df.columns = col_names

    for df in big_dict['b_report'].values():
        df['level'] = df['level'].astype('category')
        df['taxo_id'] = df['taxo_id'].astype('category')
        df['organism'] = df['organism'].str.strip()

    for level in selected_ranks:
        big_dict[level] = {}

    parameter = "num_reads"
    raw_df_names = []
    for level in selected_ranks:
        levels_of_interest = level
        all_organisms = []
        sums = [0] * len(big_dict['b_report'])

        for i, (key, df) in enumerate(big_dict['b_report'].items()):
            subset_df = df[df['level'] == levels_of_interest]
            total_percent_reads = subset_df[parameter].sum()
            curr_organisms = subset_df['organism'].tolist()
            all_organisms.extend(curr_organisms)
            sums[i] = total_percent_reads

        organisms_unique = list(set(all_organisms))
        zero_matrix = pd.DataFrame(0, index=organisms_unique, columns=b_names_report)
        level_name = f"{level}_raw"
        raw_df_names.append(level_name)
        big_dict[level][level_name] = zero_matrix

        for i, (key, df) in enumerate(big_dict['b_report'].items()):
            subset_df = df[df['level'] == levels_of_interest]
            for _, row in subset_df.iterrows():
                species_name = row['organism']
                value = row[parameter]
                big_dict[level][level_name].at[species_name, key] = value

        output_file = os.path.join(output_folder, f"{level}_counts_matrix.csv")
        big_dict[level][level_name].to_csv(output_file)
        print(f"Saved counts matrix for level {level} to {output_file}")

    for level in selected_ranks:
        level_name = f"{level}_raw"
        print(f"Counts matrix for level {level}:")
        print(big_dict[level][level_name].head())

def list_csv_files(directory, suffix):
    return [f for f in os.listdir(directory) if f.endswith(suffix)]

def compute_relative_abundance(input_file, output_file):
    df = pd.read_csv(input_file, index_col=0)
    relative_abundance_df = pd.DataFrame(index=df.index, columns=df.columns)
    for col in df.columns:
        total = df[col].sum()
        relative_abundance_df[col] = (df[col] / total) * 100
    relative_abundance_df.to_csv(output_file)
    print(f"Relative abundance data saved to {output_file}")

def load_relative_abundance(input_file):
    df = pd.read_csv(input_file, index_col=0)
    return df

def filter_low_abundance_species(df, threshold=0.01):
    zero_prop = (df == 0).mean(axis=1)
    df_filt = df.loc[zero_prop < 0.8]
    mean_NoZeros = pd.DataFrame()
    mean_NoZeros['sum'] = df_filt.sum(axis=1)
    mean_NoZeros['noZero'] = (df_filt != 0).sum(axis=1)
    mean_NoZeros['rowMeans'] = mean_NoZeros['sum'] / mean_NoZeros['noZero']

    df_filt = df_filt.loc[mean_NoZeros['rowMeans'] > threshold]

    print(f'Number of species/taxonomic units before filtering: {df.shape[0]}')
    print(f'Number of species/taxonomic units after filtering: {df_filt.shape[0]}')

    return df_filt, mean_NoZeros

def generate_graphs(df, df_filt, mean_NoZeros, output_folder, rank):
    graphs_folder = os.path.join(output_folder, 'graphs')
    os.makedirs(graphs_folder, exist_ok=True)

    zero_prop = (df == 0).mean(axis=1)
    zero_prop_sorted = zero_prop.sort_values()
    plt.figure(figsize=(10, 6))
    plt.bar(zero_prop_sorted.index, zero_prop_sorted.values)
    plt.xticks(rotation=90)
    plt.axhline(y=0.8, color='r', linestyle='--')
    plt.title('Proportion of Zeros in Each Row')
    plt.xlabel('Row Index')
    plt.ylabel('Proportion of Zeros')
    plt.xticks([])
    prop_zeros_barplot = os.path.join(graphs_folder, f'proportion_zeros_{rank}.png')
    plt.savefig(prop_zeros_barplot)
    plt.close()

    plt.figure(figsize=(8, 6))
    plt.hist(mean_NoZeros['rowMeans'][mean_NoZeros['rowMeans'] < 0.01], bins=30)
    plt.title('Histogram of Mean Abundance Values')
    plt.xlabel('Mean Abundance')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    hist_filename = os.path.join(graphs_folder, f'hist_mean_abundance_{rank}.png')
    plt.savefig(hist_filename)
    plt.close()

    plt.figure(figsize=(8, 6))
    plt.hist(df_filt.sum(axis=0), bins=30)
    plt.title('Histogram of Column Sums After Filtering')
    plt.xlabel('Sum of Abundance')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    hist_filt_filename = os.path.join(graphs_folder, f'hist_column_sums_filtered_{rank}.png')
    plt.savefig(hist_filt_filename)
    plt.close()

    df_log2 = np.log2(df_filt)
    df_log2 = df_log2.replace(-np.inf, 0)

    plt.figure(figsize=(8, 6))
    plt.hist(df_filt.values.flatten(), bins=30, alpha=0.5, label='Before log2')
    plt.hist(df_log2.values.flatten(), bins=30, alpha=0.5, label='After log2')
    plt.title('Histogram of Data Before and After log2 Transformation')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    log2_hist_filename = os.path.join(graphs_folder, f'hist_before_after_log2_{rank}.png')
    plt.savefig(log2_hist_filename)
    plt.close()

    return df_log2

def calculate_alpha_diversity(df):
    alpha_diversity = pd.DataFrame(index=df.columns)
    alpha_diversity['shannon'] = df.apply(lambda x: entropy(x[x > 0]), axis=0)
    alpha_diversity['richness'] = (df > 0).sum(axis=0)
    return alpha_diversity
