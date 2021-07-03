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
experiment_of_interest = "/experiments/ENCSR767LLP/" # An eCLIP dataset with RBFOX2 as target
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

```
