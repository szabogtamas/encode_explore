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
experiments_of_interest = ["/experiments/ENCSR767LLP/"] # An eCLIP dataset with RBFOX2 as target
region_of_interest = ("chr9", 94178791, 94178963) # positions of miRNA let-7-d
```

## Retrieve and read files manifest

```python
encodedb_files = encodex.io.read_files_manifest()
encodedb_files.head()
```

```python
bigwigs = encodedb_files.loc[(encodedb_files.dataset.isin(experiments_of_interest)) & (encodedb_files.file_format == "bigWig") & (encodedb_files.output_type == "plus strand signal of unique reads")]
bigwigs
```

```python
fig, ax = plt.subplots()
for bwf in bigwigs.s3_uri.tolist():
    bw = encodex.io.read_experiment_bw(example_bw, force_download=True)
    signal_values = bw.values(region_of_interest[0], region_of_interest[1], region_of_interest[2], numpy=True)
    ax.plot(range(len(signal_values)), signal_values)
    ax.set_ylim(0, 3)
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
def sort_by_chromosome(x):
    chrom_number = x.replace('chr', '')
    try:
        return int(chrom_number)
    except:
        return np.inf
```

```python
sorted_chroms = sorted(
    ((k, v) for k, v in filtered_chroms.items()),
    key=lambda x: sort_by_chromosome(x[0])
)
sorted_chroms
```

```python
def make_bar_chart(data, xlab=None, ylab=None, title=None, rot=45, figsize=[14, 10]):
    plt.figure(figsize=figsize)
    df = pd.DataFrame(data)
    ax = sns.barplot(
        x=0,
        y=1,
        data=df,
        color='black',
        linewidth=2.5,
        facecolor=(1, 1, 1, 0),
        edgecolor=".2"
    )
    if xlab:
        ax.set_xlabel(xlab)
    if ylab:
        ax.set_ylabel(ylab)
    if title:
        plt.title(title)
    plt.xticks(rotation=rot)
    return ax
```

```python
sns.set_style('whitegrid')
make_bar_chart(
    sorted_chroms,
    xlab='chromosome',
    ylab='number of bases',
    title='Number of bases by chromosome'
);
```

```python
avg_signal_by_chrom = []
for c in sorted_chroms:
    avg_signal_by_chrom.append((c[0], bw.stats(c[0], 0, c[1])[0]))
avg_signal_by_chrom
```

```python
make_bar_chart(
    avg_signal_by_chrom,
    xlab='chromosome',
    ylab='mean(-log(p-value))',
    title='Average signal by chromosome'
);
```

```python
max_signal_by_chrom = []
for c in sorted_chroms:
    max_signal_by_chrom.append((c[0], bw.stats(c[0], 0, c[1], type='max')[0]))
max_signal_by_chrom
```

```python
make_bar_chart(
    max_signal_by_chrom,
    xlab='chromosome',
    ylab='max(-log(p-value))',
    title='Max signal by chromosome'
)
```

```python
signal_values = bw.values('chr13', 91351000, 91351800, numpy=True)
signal_values
```

```python
plt.figure(figsize=[16, 5])
plt.fill_between(range(len(signal_values)), 0, signal_values, color='black')
```

```python

```
