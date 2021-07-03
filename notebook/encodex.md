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
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
```

```python
import pyBigWig
```

```python
experiment_of_interest = "/experiments/ENCSR767LLP/"
```

## Retrieve and read files manifest

```python
!aws s3 cp s3://encode-public/encode_file_manifest.tsv encode_file_manifest.tsv --no-sign-request
```

```python
encodedb_files = pd.read_csv('encode_file_manifest.tsv', sep='\t')
encodedb_files.head()
```

```python
bigwigs = encodedb_files.loc[files.dataset == experiment_of_interest].loc[files.file_format == 'bigWig']
bigwigs
```

```python
example_bw = bigwigs.s3_uri.head().tolist()
example_bw = example_bw[1]
example_bw
```

```python
!aws s3 cp {example_bw} experiment.bigWig --no-sign-request
```

```python
bw = pyBigWig.open('experiment.bigWig')
```

```python
chroms = bw.chroms()
filtered_chroms = {
    k: v
    for k, v in chroms.items()
    if len(k) < 10
}
filtered_chroms
```

```python

```
