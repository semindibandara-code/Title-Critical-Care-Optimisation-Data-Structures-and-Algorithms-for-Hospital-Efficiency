# This script is the command-line interface (CLI) to run the
# sorting benchmark (Module 4).
# It compares Merge Sort and Quick Sort across multiple dataset
# sizes and prints a timing table.


import sys                       # allows reading command-line arguments
from benchmarking import _print_table  # function to format and print results
from sorting import benchmark            # function that runs the timing tests

# MAIN 
if __name__ == "__main__":
    # Check if the user typed an extra argument "--plot"
    write_csv = (len(sys.argv) > 1 and sys.argv[1] == "--plot")

    # Run the benchmark (Merge Sort & Quick Sort on random, nearly-sorted, reversed)
    rows = benchmark()

    # Print the results in a nice table format
    _print_table(rows)

    # If user asked for --plot, confirm that the CSV file was written
    if write_csv:
        print("\nCSV written to sorting_results.csv")
