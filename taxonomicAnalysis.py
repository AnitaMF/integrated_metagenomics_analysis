import os
import argparse
from functions import (
    process_breport_files,
    list_csv_files,
    compute_relative_abundance,
    load_relative_abundance,
    filter_low_abundance_species,
    generate_graphs,
    calculate_alpha_diversity
)

def main():
    parser = argparse.ArgumentParser(
        description="Process bracken files and calculate diversity metrics.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-r", "--ranks", type=str, default="S",
        help="Taxonomic ranks to process (e.g., S,G,F,O,C,P). Default is 'S'.\n"
             "Example: -r S,G will process Species and Genus levels."
    )
    parser.add_argument(
        '--path_bracken', '-path', help="Path to folder containing bracken files to be processed", required=True
    )
    args = parser.parse_args()

    # Check if path_bracken argument is provided
    if not args.path_bracken:
        parser.print_help()
        return
    
    selected_ranks = args.ranks.split(',')
    bracken_folder = args.path_bracken

    # Ensure the provided path is a directory
    if not os.path.isdir(bracken_folder):
        print(f"Error: {bracken_folder} is not a valid directory.")
        return

    # List all files in the directory
    path_bracken = [os.path.join(bracken_folder, f) for f in os.listdir(bracken_folder) if f.endswith('.breport')]

    # Debug print statements for file paths
    print("Selected Ranks:", selected_ranks)

    current_dir = os.getcwd()
    output_folder = os.path.join(current_dir, "output")
    os.makedirs(output_folder, exist_ok=True)

    process_breport_files(path_bracken, selected_ranks, output_folder)

    for rank in selected_ranks:
        csv_files = list_csv_files(output_folder, f'{rank}_counts_matrix.csv')
        if not csv_files:
            print(f"No {rank}_counts_matrix CSV files found in the directory.")
            continue

        for input_file in csv_files:
            input_path = os.path.join(output_folder, input_file)
            output_path = input_path.replace(f'{rank}_counts_matrix', f'{rank}_rela_abun_matrix')
            compute_relative_abundance(input_path, output_path)

            # Load relative abundance data
            csv_files_rela = list_csv_files(output_folder, f'{rank}_rela_abun_matrix.csv')
            if not csv_files_rela:
                print(f"No {rank}_rela_abun_matrix CSV files found in the directory.")
                continue

            for rela_file in csv_files_rela:
                rela_path = os.path.join(output_folder, rela_file)
                df = load_relative_abundance(rela_path)

                # Filter low abundance species
                df_filt, mean_NoZeros = filter_low_abundance_species(df)

                # Save the filtered matrix
                filtered_output_path = rela_path.replace(f'{rank}_rela_abun_matrix', f'{rank}_rela_abun_matrix_filtered')
                df_filt.to_csv(filtered_output_path)
                print(f"Filtered relative abundance matrix saved to {filtered_output_path}")

                # Generate graphs
                generate_graphs(df, df_filt, mean_NoZeros, output_folder, rank)

                # Save alpha diversity
                alpha_diversity = calculate_alpha_diversity(df_filt)
                alpha_diversity_path = os.path.join(output_folder, f'{rank}_alpha_diversity.csv')
                alpha_diversity.to_csv(alpha_diversity_path)
                print(f"Alpha diversity measures for rank {rank} saved to {alpha_diversity_path}")

if __name__ == "__main__":
    main()
