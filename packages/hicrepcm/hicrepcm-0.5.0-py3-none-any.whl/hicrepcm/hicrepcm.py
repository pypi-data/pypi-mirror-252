import os, argparse, subprocess
import numpy as np
import matplotlib.transforms

import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations_with_replacement
import colorcet as cc
from multiprocessing import Pool
import glob

def process_filepaths(filepaths):
    # Expand wildcards and flatten the list
    expanded_filepaths = [globbed_file for pattern in filepaths for globbed_file in glob.glob(pattern)]
    return expanded_filepaths

def get_captions(caption_file, data_filenames):
    if caption_file == "":
        d = {}
        for f in data_filenames:
            stem = os.path.splitext(os.path.basename(f))[0]
            d[stem] = stem
        return d
    else:
        captions = {}
        lines = open(caption_file).readlines()
        for line in lines:
            s = line.split('\t')
            captions[s[0]] = s[1]
        return captions

def run_hicrep(args_tuple):
    fmcool1, fmcool2, args = args_tuple

    # Extract stems for fout
    stem1 = os.path.splitext(os.path.basename(fmcool1))[0]
    stem2 = os.path.splitext(os.path.basename(fmcool2))[0]
    fout_filepath = os.path.join(args.foutDir, f"{stem1}_{stem2}.txt")

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

def main():
    # Parser code copied or adapted from:
    # https://github.com/dejunlin/hicrep
    # Python implementation of the HiCRep: a stratum-adjusted correlation coefficient (SCC) for Hi-C data with support for Cooler sparse contact matrices
    parser = argparse.ArgumentParser(description='Run hicrep with multiple cooler files and generate heatmap.')
    parser.add_argument("--version", action='version', version='%(prog)s 0.5.0')
    parser.add_argument("--fmcool", nargs='+', required=True,
                        help="List of cooler multiple-binsize contact files to compare")
    parser.add_argument("--foutDir", type=str, required=True,
                        help="Output heatmap of mean non-NaN hicrep SCC scores for all pairs of files to this directory. \
                        Individual files will be named {input_stem1}_{input_stem2}.txt. Output format would be \
                        one column of scc scores for each chromosome")
    parser.add_argument("--imgOut", type=str, default="hicrepfig.png", \
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
    parser.add_argument("--processes", type=int, default=1, help="Number of processes to use running hicrep")
    parser.add_argument("--captionFile", type=str, default="", help="File associating filenames with captions with lines in the format {filename}\t{caption}")
    parser.add_argument("--colorMap", type=str, default='CET_CBL1')
    parser.add_argument("--vMin", type=float, default=0, help="SCC score corresponding to colormap minimum")
    parser.add_argument("--vMax", type=float, default=1, help="SCC score corresponding to colormap maximum")
    parser.add_argument("--bottomWhitespace", type=float, default=.2, help="Fraction of figure bottom whitespace (y axis)")
    parser.add_argument("--rightWhitespace", type=float, default=.8, help="Fraction of figure right hand side whitespace (x axis)")
    parser.add_argument("--yCaptionRotation", type=int, default=0, help="Angle of bottom captions (degrees)")
    parser.add_argument("--xCaptionRotation", type=int, default=60, help="Angle of right captions (degrees)")
    parser.add_argument("--xCaptionHa", type=str, default="center", help="Position of x axis")
    parser.add_argument("--fontScale", type=int, default=1, help="Font scale, increase to enlarge caption")
    parser.add_argument("--scaleW", type=float, default=1, help="Figure width adjustment, increase to enlarge")
    parser.add_argument("--scaleH", type=float, default=1, help="Figure height adjustment, increase to enlarge")

    args = parser.parse_args()
    

    fmcool = process_filepaths(args.fmcool)
    print(f"Running hicrepcm on {' '.join(fmcool)}")

    # Ensure output directory exists
    os.makedirs(args.foutDir, exist_ok=True)

    # Assuming 'args' and 'fmcool' are already defined
    args_list = [(fmcool1, fmcool2, args) for fmcool1, fmcool2 in combinations_with_replacement(fmcool, 2)]

    # Create a pool of worker processes
    with Pool(args.processes) as pool:
        pool.map(run_hicrep, args_list)

    # Generate combinations of fmcool files
    for fmcool1, fmcool2 in combinations_with_replacement(fmcool, 2):
        # Extract stems for fout
        stem1 = os.path.splitext(os.path.basename(fmcool1))[0]
        stem2 = os.path.splitext(os.path.basename(fmcool2))[0]
        fout_filepath = os.path.join(args.foutDir, f"{stem1}_{stem2}.txt")

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
    for fmcool1, fmcool2 in combinations_with_replacement(fmcool, 2):
        stem1 = os.path.splitext(os.path.basename(fmcool1))[0]
        stem2 = os.path.splitext(os.path.basename(fmcool2))[0]
        file_path = os.path.join(args.foutDir, f"{stem1}_{stem2}.txt")

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
    
    # Get captions associated with filenames
    captions_dict = get_captions(args.captionFile, fmcool)
    
    captions = [captions_dict[stem] for stem in stems]

    matrix = np.full((len(stems), len(stems)), np.nan)
    for i, stem1 in enumerate(stems):
        for j, stem2 in enumerate(stems):
            score = scores.get((stem1, stem2)) or scores.get((stem2, stem1))
            if score is not None:
                matrix[i, j] = score

    # Set font scale for readability
    sns.set(font_scale=args.fontScale)

    # Create the clustermap
    clustergrid = sns.clustermap(matrix, annot=True, fmt=".3f", cmap=cc.cm[args.colorMap], vmin=args.vMin, vmax=args.vMax,
                                xticklabels=captions, yticklabels=captions, figsize=(len(stems)*args.scaleW, len(stems)*args.scaleH))  # Adjust figsize as needed

    # Hide colorbar
    clustergrid.cax.set_visible(False)

    clustergrid.ax_heatmap.yaxis.set_label_position("right")
    clustergrid.ax_heatmap.yaxis.tick_right()

    # Adjust the layout and whitespace
    plt.subplots_adjust(right=1-args.rightWhitespace, bottom=args.bottomWhitespace)

    # Rotate xtick labels
    plt.setp(clustergrid.ax_heatmap.get_xticklabels(), rotation=args.xCaptionRotation, ha=args.xCaptionHa)
    plt.setp(clustergrid.ax_heatmap.get_yticklabels(), rotation=args.yCaptionRotation)

    # Save the clustermap
    plt.savefig(os.path.join(args.foutDir, args.imgOut))

if __name__ == "__main__":
    main()
