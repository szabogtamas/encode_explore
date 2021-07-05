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
experiments_of_interest = ["ENCSR767LLP/"] # An eCLIP dataset with RBFOX2 as target
region_of_interest = ("chr9", 94178791, 94178963) # positions of miRNA let-7-d
```

## Retrieve and read files manifest

```python
encodedb_files = encodex.io.read_files_manifest()
encodedb_files.head()
```

```python
bigwigs =  encodex.filters.retrieve_bw_paths_by_experiment(encodedb_files, experiments_of_interest)
bigwigs
```

```python
signal_values = encodex.filters.extract_genomic_range(bigwigs.file_path.tolist(), region_of_interest)
```

```python
encodex.viz.plot_range_coverage(signal_values)
```
