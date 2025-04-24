import pandas as pd
import argparse
import os
from datetime import datetime

def compare_csv_files(file1_path, file2_path, output_dir=None):
    """
    Compare two CSV files and identify identical and missing rows.
    Generate two files with missing records from each file.
    Keeps data as raw as possible without type inference.
    
    Args:
        file1_path (str): Path to the first CSV file
        file2_path (str): Path to the second CSV file
        output_dir (str, optional): Directory for output files. Defaults to current directory.
    """
    # Create timestamp for output files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Set output directory
    if output_dir is None:
        output_dir = os.getcwd()
        output_dir = os.path.join(output_dir, timestamp[:4], timestamp[4:6], timestamp[6:8])  # Add year, month, and date as subfolders
    os.makedirs(output_dir, exist_ok=True)
    # Get file names without extension for reporting
    file1_name = os.path.basename(file1_path).split('.')[0]
    file2_name = os.path.basename(file2_path).split('.')[0]
    
    # Output file paths
    missing_in_file2_path = os.path.join(output_dir, f"{file1_name}_missing_in_{file2_name}_{timestamp}.csv")
    missing_in_file1_path = os.path.join(output_dir, f"{file2_name}_missing_in_{file1_name}_{timestamp}.csv")
    
    print(f"Comparing {file1_path} and {file2_path}...")
    
    # Read CSV files with dtype=str to keep all data as strings (raw)
    # Also disable index inference to preserve all data as-is
    try:
        df1 = pd.read_csv(
            file1_path, 
            dtype=str,  # Keep all data as strings
            keep_default_na=False,  # Don't convert missing values to NaN
            na_filter=False  # Don't interpret NA values
        )
        
        df2 = pd.read_csv(
            file2_path, 
            dtype=str,  # Keep all data as strings
            keep_default_na=False,  # Don't convert missing values to NaN
            na_filter=False  # Don't interpret NA values
        )
    except Exception as e:
        print(f"Error reading CSV files: {e}")
        return
    
    # Check if column names match
    if set(df1.columns) != set(df2.columns):
        print("Warning: Column names don't match between files.")
        print(f"Columns in {file1_name}: {list(df1.columns)}")
        print(f"Columns in {file2_name}: {list(df2.columns)}")
        proceed = input("Do you want to proceed with comparison anyway? (y/n): ")
        if proceed.lower() != 'y':
            print("Comparison aborted.")
            return
    
    # Convert dataframes to sets of tuples for comparison
    # This allows for comparing entire rows
    df1_rows = set(df1.astype(str).itertuples(index=False, name=None))
    df2_rows = set(df2.astype(str).itertuples(index=False, name=None))
    
    # Find common rows and differences
    common_rows = df1_rows.intersection(df2_rows)
    missing_in_file2 = df1_rows - df2_rows
    missing_in_file1 = df2_rows - df1_rows
    
    # Calculate statistics
    total_rows_file1 = len(df1)
    total_rows_file2 = len(df2)
    identical_rows = len(common_rows)
    rows_missing_in_file2 = len(missing_in_file2)
    rows_missing_in_file1 = len(missing_in_file1)
    
    # Display comparison results
    print("\nComparison Results:")
    print(f"Total rows in {file1_name}: {total_rows_file1}")
    print(f"Total rows in {file2_name}: {total_rows_file2}")
    print(f"Identical rows found in both files: {identical_rows}")
    print(f"Rows in {file1_name} missing from {file2_name}: {rows_missing_in_file2}")
    print(f"Rows in {file2_name} missing from {file1_name}: {rows_missing_in_file1}")
    
    # Generate output files for missing records - maintain original column order
    if rows_missing_in_file2 > 0:
        # Convert missing records back to DataFrame
        missing_records = list(missing_in_file2)
        missing_in_file2_df = pd.DataFrame(missing_records, columns=df1.columns)
        # Write to CSV without index and with the same data formatting
        missing_in_file2_df.to_csv(missing_in_file2_path, index=False)
        print(f"\nRecords in {file1_name} missing from {file2_name} saved to: {missing_in_file2_path}")
    else:
        print(f"\nNo records in {file1_name} are missing from {file2_name}")
    
    if rows_missing_in_file1 > 0:
        # Convert missing records back to DataFrame
        missing_records = list(missing_in_file1)
        missing_in_file1_df = pd.DataFrame(missing_records, columns=df2.columns)
        # Write to CSV without index and with the same data formatting
        missing_in_file1_df.to_csv(missing_in_file1_path, index=False)
        print(f"Records in {file2_name} missing from {file1_name} saved to: {missing_in_file1_path}")
    else:
        print(f"No records in {file2_name} are missing from {file1_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare two CSV files and identify identical and missing rows')
    parser.add_argument('file1', help='Path to the first CSV file')
    parser.add_argument('file2', help='Path to the second CSV file')
    parser.add_argument('-o', '--output', help='Directory for output files (default: current directory)')
    
    args = parser.parse_args()
    compare_csv_files(args.file1, args.file2, args.output)