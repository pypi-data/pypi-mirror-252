**Install:** `pip install hicrepcm`

The `hicrepcm` package generates mean SCC scores from [hicrep](https://github.com/dejunlin/hicrep) for an arbitrary number of input .mcool contact matrices and outputs a [clustermap](https://seaborn.pydata.org/generated/seaborn.clustermap.html).

All input arguments to `hicrepm` are identical to those for `hicrep` and are passed to it directly, with the exception of the input and output specification.
+ Inputs are specified with `--fmcool`, a list of space-separated .mcool filenames.
+ The output directory is specified with `--fout_dir`. All SCC score files and the output clustermap will be saved here.
+ The image filename can be specified with `--img_out` and is `hicrepfig.png` by default.
+ `--skipIfExists`: do not recalculate SCC score files that already exist in the output directory.
+ '--processes': Number of cores to use

A number of other parameters control aspects of the figure format:
+ '--captionFile': If provided with a file with tab-delimited lines structured as '{filename prefix}\t{caption}', recaptions the filenames.
+ '--colorMap': Select the colormap to use from [ColorCET](https://colorcet.com/gallery.html). By default, chooses a perceptually-accurate, colorblind-friendly colormap.
+ '--vMin': Minimum of colormap
+ '--vMax': Maximum of colormap
+ '--bottomWhitespace': Fraction of y axis (below figure) reserved for whitespace
+ '--rightWhitespace': Fraction of y axis (to right of figure) reserved for whitespace
+ '--xCaptionRotation': Degrees to rotate x caption
+ '--yCaptionRotation': Degrees to rotate y caption
+ '--xCaptionHa': Choose from 'left', 'right', 'center'. Controls label position relative to column.
+ '--fontScale': Multiplier for the font size
+ '--scaleW': Figure width multiplier
+ '--scaleH': Figure height multiplier

All two-way comparisons will be generated, including self-comparisons.
No title or legend is generated for the clustermap.
