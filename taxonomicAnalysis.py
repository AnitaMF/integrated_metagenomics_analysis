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
        help="Taxonomic ranks to process (e.g., S,G,F,O,C,P)-no spaces. Default is 'S'.\n"
             "Example: -r S,G will process Species and Genus levels."
    )
    parser.add_argument(
        '--path_bracken', '-path', help="Path to folder containing bracken files to be processed", required=True
    )
    args = parser.parse_args()

    if not args.path_bracken:
        parser.print_help()
        return
    
    selected_ranks = args.ranks.split(',')
    bracken_folder = args.path_bracken

    if not os.path.isdir(bracken_folder):
        print(f"Error: {bracken_folder} is not a valid directory.")
        return

    path_bracken = [os.path.join(bracken_folder, f) for f in os.listdir(bracken_folder) if f.endswith('.breport')]

    print("Selected Ranks:", selected_ranks)

    current_dir = os.getcwd()
    output_folder = os.path.join(current_dir, "output")
    os.makedirs(output_folder, exist_ok=True)

    #RUN PIPELINE
    # Process bracken files
    process_breport_files(path_bracken, selected_ranks, output_folder)

    # Iterate over selected ranks
    for rank in selected_ranks:
        csv_files = list_csv_files(output_folder, f'{rank}_counts_matrix.csv')
        if not csv_files:
            print(f"No {rank}_counts_matrix CSV files found in the directory.")
            continue

        # Iterate over each CSV file found
        for input_file in csv_files:
            input_path = os.path.join(output_folder, input_file)
            output_path = input_path.replace(f'{rank}_counts_matrix', f'{rank}_rela_abun_matrix')

            # Compute relative abundance
            compute_relative_abundance(input_path, output_path)

            # Load relative abundance data
            df, _ = load_relative_abundance(output_path) 

            # Filter low abundance species
            df_filt, mean_NoZeros = filter_low_abundance_species(df, output_folder=output_folder, input_file=output_path)

            # Generate graphs
            generate_graphs(df, df_filt, mean_NoZeros, output_folder, rank)

            # Calculate alpha diversity
            calculate_alpha_diversity(df_filt, rank, output_folder)

if __name__ == "__main__":
    main()
