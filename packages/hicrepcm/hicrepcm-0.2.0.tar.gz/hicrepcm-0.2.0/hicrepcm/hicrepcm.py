import os, argparse, subprocess
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations_with_replacement
import colorcet as cc

def main():
    # Parser code copied or adapted from:
    # https://github.com/dejunlin/hicrep
    # Python implementation of the HiCRep: a stratum-adjusted correlation coefficient (SCC) for Hi-C data with support for Cooler sparse contact matrices
    parser = argparse.ArgumentParser(description='Run hicrep with multiple cooler files and generate heatmap.')
    parser.add_argument("--fmcool", nargs='+', required=True,
                        help="List of cooler multiple-binsize contact files to compare")
    parser.add_argument("--fout_dir", type=str, required=True,
                        help="Output heatmap of mean non-NaN hicrep SCC scores for all pairs of files to this directory. \
                        Individual files will be named {input_stem1}_{input_stem2}.txt. Output format would be \
                        one column of scc scores for each chromosome")
    parser.add_argument("--img_out", type=str, default="hicrepfig.png", \
                        help="Filename of output heatmap image to output in {fout_dir} (defaults to hicrepfig.png)")
    parser.add_argument("--binSize", type=int, default=-1,
                        help="Use this to select the bin size from the input mcool\
                        file. Default to -1, meaning that the inputs are treated as\
                        single-binsize .cool files")
    parser.add_argument("--h", type=int, required=True,
                        help="Smooth the input contact matrices using a 2d mean\
                        filter with window size of 1 + 2 * value. This should\
                        be set according to the bin size. For example, you can try the\
                        following settings: --binSize=10000 --h=20,\
                        --binSize=25000 --h=10, --binSize=40000 --h5. Beware that\
                        these examples might not work in all cases and the user\
                        should adjust them according to the specific application")
    parser.add_argument("--dBPMax", type=int, required=True,
                        help="Only consider contacts at most this number of bp away\
                        from the diagonal. For human genome, the value of\
                        5000000 was used in the original HiCRep paper.")
    parser.add_argument("--bDownSample", action='store_true', default=False,
                        help="Down sample the input with more contact counts to\
                        the the same number of counts as the other input with less\
                        contact counts. If turned off, the input matrices will be\
                        normalized by dividing the counts by their respective total\
                        number of contacts.")
    parser.add_argument("--chrNames", type=str, nargs='*', default=[],
                        help="Only compute the SCC scores on this subset of\
                        chromosomes whose names are provided. The output SCC\
                        scores will be ordered as the input chromosome names\
                        here")
    parser.add_argument("--excludeChr", type=str, nargs='*', default=['M'],
                        help="Exclude chromosomes from the SCC score calculations.\
                        Mitochondrial chromosomes named \"M\" are excluded by\
                        default. The output SCC scores will be ordered as the\
                        chromosomes in the input Cooler files by removing those\
                        chromosomes provided here")
    parser.add_argument("--skipIfExists", action='store_true', default=False, help="Skip rerunning hicrep if scores file already exists")
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(args.fout_dir, exist_ok=True)

    # Generate combinations of fmcool files
    for fmcool1, fmcool2 in combinations_with_replacement(args.fmcool, 2):
        # Extract stems for fout
        stem1 = os.path.splitext(os.path.basename(fmcool1))[0]
        stem2 = os.path.splitext(os.path.basename(fmcool2))[0]
        fout_filepath = os.path.join(args.fout_dir, f"{stem1}_{stem2}.txt")

        # Prepare the hicrep command
        hicrep_command = [
            "hicrep", 
            fmcool1, 
            fmcool2, 
            fout_filepath,
            "--binSize", str(args.binSize),
            "--h", str(args.h),
            "--dBPMax", str(args.dBPMax)
        ]

        # Add optional arguments if specified
        if args.bDownSample:
            hicrep_command.append("--bDownSample")
        if args.chrNames:
            hicrep_command.extend(["--chrNames"] + args.chrNames)
        if args.excludeChr:
            hicrep_command.extend(["--excludeChr"] + args.excludeChr)

        # Run hicrep
        if not args.skipIfExists or not os.path.exists(fout_filepath):
            subprocess.run(hicrep_command)

    # Dictionary to store scores
    scores = {}

    # Process each generated file
    for fmcool1, fmcool2 in combinations_with_replacement(args.fmcool, 2):
        stem1 = os.path.splitext(os.path.basename(fmcool1))[0]
        stem2 = os.path.splitext(os.path.basename(fmcool2))[0]
        file_path = os.path.join(args.fout_dir, f"{stem1}_{stem2}.txt")

        with open(file_path, 'r') as file:
            values = []
            for line in file:
                if not line.startswith('#'):
                    try:
                        score = float(line.strip())
                        if not np.isnan(score):
                            values.append(score)
                    except ValueError:
                        continue
            if values:
                scores[(stem1, stem2)] = np.mean(values)

    # Create a matrix for the heatmap
    stems = list(set([item for pair in scores.keys() for item in pair]))
    matrix = np.full((len(stems), len(stems)), np.nan)
    for i, stem1 in enumerate(stems):
        for j, stem2 in enumerate(stems):
            score = scores.get((stem1, stem2)) or scores.get((stem2, stem1))
            if score is not None:
                matrix[i, j] = score
    
    # Create and save the heatmap
    plt.figure(figsize=(len(stems), len(stems)*2))
    sns.set(font_scale=1)  # Keep a reasonable font scale for readability
    clustergrid = sns.clustermap(matrix, annot=True, fmt=".3f", cmap=cc.cm.CET_CBL1, vmin=0, vmax=1, xticklabels=stems, yticklabels=stems)
    clustergrid.cax.set_visible(False)
    plt.setp(clustergrid.ax_heatmap.get_xticklabels(), rotation=60)

    # Save the heatmap
    plt.savefig(os.path.join(args.fout_dir, args.img_out))

if __name__ == "__main__":
    main()