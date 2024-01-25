import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import yaml
import sys
import colorcet as cc
from combocmd.version import __version__

# Hardcoded default format
default_format = yaml.safe_load(open("aclustermap/default_format.yaml").read())['format']

def read_yaml_from_stdin():
    return yaml.safe_load(sys.stdin)

def build_dataframe(data):
    captions = set()
    for entry in data:
        captions.update(entry[:2])  # Update with the first two elements (captions)
    captions = sorted(captions)

    df = pd.DataFrame(index=captions, columns=captions)
    for entry in data:
        caption1, caption2, value = entry
        df.at[caption1, caption2] = value
    return df.astype(float)

def create_clustermap(df, format_settings):
    plt.figure(figsize=(format_settings['scaleX'], format_settings['scaleY']))
    sns.set(font_scale=format_settings['fontScale'])

    g = sns.clustermap(df, cmap=cc.cm[format_settings['colormap']], vmin=format_settings['vMin'], vmax=format_settings['vMax'],
                       annot=format_settings['showValues'], fmt=f".{format_settings['decimals']}f",
                       cbar_kws={'shrink': format_settings['rightMargin']}, dendrogram_ratio=format_settings['dendrogramRatio'])

    plt.setp(g.ax_heatmap.get_xticklabels(), rotation=format_settings['xCaptionRotate'], horizontalalignment=format_settings['xCaptionHa'])
    plt.setp(g.ax_heatmap.get_yticklabels(), rotation=format_settings['yCaptionRotate'])

    if not format_settings['showDendrogram']:
        g.ax_row_dendrogram.set_visible(False)
        g.ax_col_dendrogram.set_visible(False)

    if format_settings['showLegend']:
        g.ax_cbar.set_visible(True)
    else:
        g.ax_cbar.set_visible(False)

    plt.savefig(format_settings['outputFilename'])

def main():
    yaml_data = read_yaml_from_stdin()

    # Initialize format with default values
    format_settings = default_format.copy()

    # Update with provided format settings if available
    if 'format' in yaml_data:
        format_settings.update(yaml_data['format'])

    df = build_dataframe(yaml_data['data'])
    create_clustermap(df, format_settings)

if __name__ == "__main__":
    main()
