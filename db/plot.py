import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.offline as plt
from .models import *

def tax_bar_plot(taxonomy_pk, countmatrix_pk, samples=None, level=6, relative=True):
    linnean_levels = {y: x for x,y in enumerate(["kingdom", "phylum", "class", "order", "family", "genus", "species"])}
    if level in linnean_levels:
        level = linnean_levels[level]
    elif type(level) == str:
        level = int(level)
    tax_result = Result.objects.get(pk=taxonomy_pk)
    count_matrix_result = Result.objects.get(pk=countmatrix_pk)
    matrix = count_matrix_result.values.instance_of(Matrix).first().data.get().get_value()
    if relative:
        matrix = matrix/matrix.sum(axis=0)
    else:
        matrix = matrix.todense()
    sample_pks = count_matrix_result.samples.order_by("pk")
    sample_names = count_matrix_result.samples.order_by("pk")
    if samples:
        sample_pks = sample_pks.filter(pk__in=samples)
        sample_names = sample_names.filter(pk__in=samples)
    sample_pks = list(sample_pks.values_list("pk",flat=True))
    sample_names = list(sample_names.values_list("name",flat=True))
    tax_df = tax_result.dataframe(value_names=["taxonomic_classification"], 
                                  additional_fields=["features__pk"])
    tax_df["value_data"] = tax_df["value_data"].str.split(";").apply(lambda x: x[-1] if len(x) <= level else x[level])
    tax_merge = tax_df.groupby("value_data").apply(lambda x: x['features__pk'].unique())
    data = []
    for tax, merge in tax_merge.items():
        data.append(go.Bar(name=tax, 
                           x=sample_names, 
                           y=matrix[merge][:,sample_pks].sum(axis=0).tolist()[0]))
    fig = go.Figure(data=data)
    # Change the bar mode
    fig.update_layout(barmode='stack',
                     legend_orientation='h',
                     legend=dict(x=0,y=-0.45),
                     height=750)

    return plt.plot(fig, output_type='div')