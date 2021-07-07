---
jupyter:
  jupytext:
    formats: md,ipynb
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.3
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Exploring ENCODE database

## Setup

```python
import sys
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
```

```python
sys.path.append("/usr/local/dev_scripts")

import encodex
```

```python
experiments_of_interest = ["ENCSR767LLP"] # An eCLIP dataset with RBFOX2 as target
region_of_interest = ("chr9", 94178791, 94178963) # positions of miRNA let-7-d
```

```python
gencode_annotation = "s3://encode-public/2019/06/04/8f6cba12-2ebe-4bec-a15d-53f498979de0/gencode.v29.primary_assembly.annotation_UCSC_names.gtf.gz"
```

## Retrieve and read files manifest

```python
encodedb_files = encodex.io.read_files_manifest()
encodedb_files.head()
```

## Show signal for experiment in region

```python
bigwigs =  encodex.filters.retrieve_bw_paths_by_experiment(encodedb_files, experiments_of_interest)
bigwigs
```

```python
signal_values = encodex.filters.combine_experiment_signals(bigwigs.s3_uri.tolist(), region_of_interest)
signal_values.head()
```

```python
genome_annotation = encodex.filters.read_genome_annotation(gencode_annotation)
genome_annotation.loc[(annotation.Chr == region_of_interest[0]) & ((annotation.Start_g < region_of_interest[2]) & (annotation.End_g > region_of_interest[1]))].head()
```

```python
encodex.viz.plot_range_coverage(signal_values, region_of_interest[0], genome_annotation)
```
