#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <file1.csv> <file2.csv> [output_directory]"
    echo "  file1.csv          Path to the first CSV file"
    echo "  file2.csv          Path to the second CSV file"
    echo "  output_directory   Optional: Directory for output files (default: current directory)"
    exit 1
fi

# Get arguments
FILE1="$1"
FILE2="$2"
OUTPUT_DIR="$3"

# Create output directory argument if provided
OUTPUT_ARG=""
if [ -n "$OUTPUT_DIR" ]; then
    OUTPUT_ARG="-o $OUTPUT_DIR"
fi

# Run the Python script
python3 csv_comparison.py "$FILE1" "$FILE2" $OUTPUT_ARG