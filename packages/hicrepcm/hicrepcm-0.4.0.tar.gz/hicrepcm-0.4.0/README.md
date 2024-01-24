**Install:** `pip install hicrepcm`

**Example:** See code and image below

The `hicrepcm` package generates mean SCC scores from [hicrep](https://github.com/dejunlin/hicrep) for an arbitrary number of input .mcool contact matrices and outputs a [clustermap](https://seaborn.pydata.org/generated/seaborn.clustermap.html).

For details on hicrep, see HiCRep: assessing the reproducibility of Hi-C data using a stratum-adjusted correlation coefficient. Tao Yang Feipeng Zhang Galip Gürkan Yardımcı Fan Song Ross C. Hardison William Stafford Noble Feng Yue and Qunhua Li, Genome Res. 2017 Nov;27(11):1939-1949. doi: 10.1101/gr.220640.117.

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

Example:

Data from Xu, J., Song, F., Lyu, H., Kobayashi, M., Zhang, B., Zhao, Z., ... & Yue, F. (2022). Subtype-specific 3D genome alteration in acute myeloid leukaemia. _Nature_, _611_(7935), 387-398.

```
pip install hicrepcm
mkdir hicrepcm_demo; cd hicrepcm_demo
wget https://raw.githubusercontent.com/yardimcilab/hicrepcm/main/demo/samples.txt
wget https://raw.githubusercontent.com/yardimcilab/hicrepcm/main/demo/wget_demo_mcools_20gb.sh
chmod +x wget_demo_mcools_20gb.sh
./wget_demo_mcools_20gb.sh
hicrepcm --fmcool *.mcool --fout_dir hicrepcm --binSize 100000 --dBPMax 5000000 --h 1 --processes 8 --skipIfExists --bottomWhitespace .1 --rightWhitespace .1 --xCaptionHa right --captionFile samples.txt
```

![Example Image](demo/hicrepcm_demo.png)
