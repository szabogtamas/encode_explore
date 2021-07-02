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
#TODO set up mounting of S3 here
```

```python
files = pd.read_csv('encode-public/encode_file_manifest.tsv', sep='\t')
```

```python

```
