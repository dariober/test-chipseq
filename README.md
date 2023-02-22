<!-- vim-markdown-toc GFM -->

* [Description](#description)
* [Installation](#installation)
* [Usage](#usage)
* [Developer](#developer)

<!-- vim-markdown-toc -->

# Description

Example of a pipeline for processing ChIPseq data. 

Although this code is functional, it is only meant to showcase the use of
Python and Snakemake.

# Installation

Using [conda](https://docs.conda.io/projects/conda/en/latest/index.html) and
[mamba](https://github.com/mamba-org/mamba) configured for working with [bioconda](https://bioconda.github.io/):

```
conda create -n test-chipseq --yes
conda activate test-chipseq
mamba install -n test-chipseq --file requirements.txt --yes
```

# Usage

```
snakemake -p -n -j 4 \
    -C sample_sheet=test/data/sample_sheet.tsv \
       genome=$PWD/test/data/geome.fa \
    -d output
```

# Developer

Run tests:

```
./test/test.py
```
