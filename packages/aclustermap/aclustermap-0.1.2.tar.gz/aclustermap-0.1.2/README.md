**Install**
```
pip install aclustermap
```

aclustermap converts a piped YAML description of data and (optionally) custom format parameters and outputs a [clustermap](https://seaborn.pydata.org/generated/seaborn.clustermap.html).
This is a clustered heatmap (defaults to displaying with a dendrogram).

It expects data formatted as a YAML list called `data:` of [caption1, caption2, value] sublists each describing a cell in the clustermap. Example:

**Example data YAML**
```
data:
  -  - caption1
     - caption1
     - 1
  -  - caption 1
       caption 2
       2
  -  - caption 2
     - caption 1
     - 3
  -  - caption 2
     - caption 2
     - 4
```

**Example format YAML**
These are the default settings. You can pipe in a `format:` YAML dict with only a subset of these parameters.
Default settings will be applied for any parameters not submitted.
```
format: 
  "outputFilename": "clustermap.png"
  "colormap": "CET_CBL1"
  "scaleX": 1
  "scaleY": 1
  "xCaptionRotate": 45
  "yCaptionRotate": 0
  "xCaptionHa": "right"
  "showValues": True
  "fontScale": 1.0
  "vMin": 0
  "vMax": 1
  "rightMargin": 0.2
  "dendrogramRatio": 0.2
  "showDendrogram": True
  "showLegend": True
  "decimals": 2
```

**Example usage**
The following shows three ways to generate a clustermap of sin(a)sin(b)+cos(a)cos(b).
In the example, a and b correspond to caption values (0 to 720 degrees in steps of 45 degrees).

```
mkdir example
wget https://raw.githubusercontent.com/yardimcilab/aclustermap/main/example/data.yaml -O example/data.yaml
wget https://raw.githubusercontent.com/yardimcilab/aclustermap/main/example/format.yaml -O example/format.yaml
wget https://raw.githubusercontent.com/yardimcilab/aclustermap/main/example/sinsq%2Bcossq.py -O example/sinsq+cossq.py

# Cluster map from file with default format
cat example/data.yaml | aclustermap

# Cluster map from file with custom format
(cat example/data.yaml; cat example/format.yaml) | aclustermap

# Generate YAML data and output to stdout, then produce clustermap with custom format 
(python3 example/sinsq+cossq.py; cat format.yaml) | aclustermap
```

![Example output](example/example.png)
