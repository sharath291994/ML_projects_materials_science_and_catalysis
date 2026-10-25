import argparse
from .analysis import run_analysis

def main():
    parser = argparse.ArgumentParser(description="Zacros CE Fit Analysis")
    parser.add_argument("file", help="Path to the AmcBvec Excel file")
    parser.add_argument("--correlation", action="store_true", help="Generate correlation matrices")
    parser.add_argument("--histograms", action="store_true", help="Generate frequency distributions")
    parser.add_argument("--CEfit", action="store_true", help="Generate CE fit plot")
    parser.add_argument("--ncols", type=int, default=None, help="Number of first n columns to include in correlation analysis")
    args = parser.parse_args()

    # If none of the flags are set, do everything
    do_correlation = args.correlation or not (args.correlation or args.histograms or args.CEfit)
    do_frequency = args.histograms or not (args.correlation or args.histograms or args.CEfit)
    do_ce_fit = args.CEfit or not (args.correlation or args.histograms or args.CEfit)

    run_analysis(
        file_path=args.file,
        n_cols=args.ncols,
        do_correlation=do_correlation,
        do_frequency=do_frequency,
        do_ce_fit=do_ce_fit
    )

if __name__ == "__main__":

    main()
