[![test status](https://github.com/dariober/test-chipseq/actions/workflows/main.yml/badge.svg)](https://github.com/dariober/test-chipseq/actions?query=branch%3Amaster+workflow%3Amain)
[![Language](http://img.shields.io/badge/language-python-blue.svg)](https://www.python.com/)
[![Snakemake](https://img.shields.io/badge/snakemake-brightgreen.svg?style=flat)](https://snakemake.readthedocs.io)
[![License](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/dariober/excelToCsv)

<!-- vim-markdown-toc GFM -->

* [Description](#description)
* [Setup](#setup)
* [Usage](#usage)
* [Developer](#developer)

<!-- vim-markdown-toc -->

# Description

Example of a pipeline for processing ChIPseq data going from fastq files to
binding sites (peaks). 

Although this code is fully functional, it is only meant to showcase the use of
Python and Snakemake.

# Setup

Using [conda](https://docs.conda.io/projects/conda/en/latest/index.html) and
[mamba](https://github.com/mamba-org/mamba) configured for working with [bioconda](https://bioconda.github.io/):

```
mamba create -n test-chipseq --yes
mamba activate test-chipseq
mamba install -n test-chipseq --file requirements.txt --yes
```

# Usage

```
snakemake -C sample_sheet=$PWD/test/data/sample_sheet.tsv \
             genome=$PWD/test/data/genome.fa \
    -p --dry-run -j 4 --directory output
```

Where:

* **sample_sheet**: Full path of tab-separated file of library characteristics with columns:
    * `library_id`: Unique library ID
    * `type`: Type of library: `chip` or `input`    
    * `control_id`: ID of the control library for this library or NA if library_id is an `input` library 
    * `fastq_r1`: Path to fastq file; path relative to output directory

* **genome**: Full path to fasta file of reference genome

* **--directory**: Output directory

`-p -j ...`: For this and other options see `snakemake -h`. Remove `--dry-run` for actual execution.

# Developer

Run tests:

```
./test/test.py
```

Format code:

```
snakefmt Snakefile
black lib/utils.py test/test.py
```
