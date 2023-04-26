import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from src.co2_calculator.structures.wall_MIP_EPD import MIPWall_EPD
from matplotlib import cm
import numpy as np

def create_tCO2eq_piechart(structure):
    """ Creates tCO2eq pie chart for a structure
    """
    data = pd.DataFrame({
                        'Category': ['Material production', 'Material transport', 'Disposal transport', 'Equipment', 'Energy/ electricity/ hour', 'Mobilization/ demobilization', 'Persons transport'],
                        'tCO2_eq': [structure.out_material_production, structure.out_material_transport, structure.out_disposal_transport, structure.out_equipment, structure.out_energy_electricity_hour, structure.out_mob_demob, structure.out_persons_transport]
                        })
    base = alt.Chart(data).configure_legend(
        #titleFontSize=18,
        labelFontSize=16
        ).encode(
        theta=alt.Theta(field='tCO2_eq', type='quantitative'),
        color=alt.Color(field='Category', type='nominal'),
    )
    pie = base.mark_arc(radius=140, stroke='#fff')
    return pie

    #base = alt.Chart(data).encode(
    #    theta=alt.Theta('tCO2_eq:Q', stack=True),
    #    radius=alt.Radius('tCO2_eq', scale=alt.Scale(type='sqrt', zero=True, rangeMin=20.)),
    #    #radius=alt.Radius('tCO2_eq'),
    #    color=alt.Color('Category:N'),
    #)

    #pie = base.mark_arc(stroke='#fff')
    #text = base.mark_text(radiusOffset=20, size=16).encode(text='tCO2_eq:Q')
    ##text = base.mark_text(radius=180, size=16).encode(text='tCO2_eq:Q')
    ##text = base.mark_text(radius=180, size=16).encode(text='Category:N')
    #return (pie+text).configure_legend(
    #    #titleFontSize=18,
    #    labelFontSize=16)


def create_tCO2eq_piechart_matplotlib(structure):
    """ Creates tCO2eq pie chart for a structure with matplotlib
    """
    df = pd.DataFrame({
                        'Category': ['Material production', 'Material transport', 'Disposal transport', 'Equipment', 'Energy/ electricity/ hour', 'Mobilization/ demobilization', 'Persons transport'],
                        'tCO2_eq': [structure.out_material_production, structure.out_material_transport, structure.out_disposal_transport, structure.out_equipment, structure.out_energy_electricity_hour, structure.out_mob_demob, structure.out_persons_transport]
                        },
                        index = ['Material production', 'Material transport', 'Disposal transport', 'Equipment', 'Energy/ electricity/ hour', 'Mobilization/ demobilization', 'Persons transport'])

    fig, ax = plt.subplots()
    #df.plot.pie(y='tCO2_eq', stacked=False, colormap='cool', ax=ax, legend=False, autopct="%.1f%%")
    wedges, _ = ax.pie(list(df['tCO2_eq']))
    categories = list(df['Category'])
    categories_with_percentage = [item + ': {:.1f}%'.format(100*tCO2eq/df['tCO2_eq'].sum()) for item, tCO2eq in zip(categories, list(df['tCO2_eq']))]
    ax.legend(wedges, categories_with_percentage,
          title="Category",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

    return ax


def create_tCO2eq_barchart_all_projects_categories(projects):
    """ Create tCO2eq bar chart for all projects
    This is to compare total tCO2eq for each of the categories
    """
    #categrogy = ['Material production', 'Material transport', 'Disposal transport', 'Equipment', 'Energy/ electricity/ hour', 'Mobilization/ demobilization', 'Persons transport']
    categrogy = ['MP', 'MT', 'DT', 'EQ', 'EE', 'MD', 'PT', 'Total']

    df = pd.DataFrame({
                        'Category': categrogy,
                        })
    for project in projects:
        total_material_production =         sum([structure.out_material_production for structure in project.structures])
        total_material_transport =          sum([structure.out_material_transport for structure in project.structures])
        total_disposal_transport =          sum([structure.out_disposal_transport for structure in project.structures])
        total_equipment =                   sum([structure.out_equipment for structure in project.structures])
        total_energy_electricity_hour =     sum([structure.out_energy_electricity_hour for structure in project.structures])
        total_mob_demob =                   sum([structure.out_mob_demob for structure in project.structures])
        total_persons_transport =           sum([structure.out_persons_transport for structure in project.structures])

        sum_total = sum([total_material_production, total_material_transport, total_disposal_transport, total_equipment,
                        total_energy_electricity_hour, total_mob_demob, total_persons_transport])

        data_project = [total_material_production, total_material_transport, total_disposal_transport, total_equipment,
                        total_energy_electricity_hour, total_mob_demob, total_persons_transport, sum_total]

        df[project.project_variant] = data_project
    
    project_names = [project.project_variant for project in projects]

    c = alt.Chart(df).mark_bar().configure_legend(
        #titleFontSize=18,
        labelFontSize=16
        ).configure_axis(
        titleFontSize=18,
        labelFontSize=16,
        ).encode(
            x = 'tCO2_eq:Q',
            #y = 'Projects:N',
            y = alt.X('Projects:N', axis=alt.Axis(labelAngle=-45), title=None),
            color = 'Projects:N',
            row=alt.Row('Category')
            ).transform_fold(
                            as_=['Projects', 'tCO2_eq'],
                            fold=project_names
                            )
    
    #text = alt.Chart(df).mark_text(
    #    align='left',
    #    baseline='middle',
    #    dx=3
    #).encode(
    #    x = 'tCO2_eq:Q',
    #    #y = 'Projects:N',
    #    text='tCO2:eq:Q',
    #    row=alt.Row('Category')
    #    )#.transform_fold(
    #     #                   as_=['Projects', 'tCO2_eq'],
    #     #                   fold=project_names
    #     #                   )
    
    #chart_with_text = alt.layer(c, text)
    
    return c.properties(height=60, width=1200)


# faceted chart
def create_tCO2eq_barchart_all_projects_categories_2(projects):
    """ Create tCO2eq bar chart for all projects
    This is to compare total tCO2eq for each of the categories
    """
    #categrogy = ['Material production', 'Material transport', 'Disposal transport', 'Equipment', 'Energy/ electricity/ hour', 'Mobilization/ demobilization', 'Persons transport']

    df = pd.DataFrame({
                        #'Category': categrogy,
                        })

    for project in projects:
        if project.structures:
            total_material_production =         sum([structure.out_material_production for structure in project.structures])
            total_material_transport =          sum([structure.out_material_transport for structure in project.structures])
            total_disposal_transport =          sum([structure.out_disposal_transport for structure in project.structures])
            total_equipment =                   sum([structure.out_equipment for structure in project.structures])
            total_energy_electricity_hour =     sum([structure.out_energy_electricity_hour for structure in project.structures])
            total_mob_demob =                   sum([structure.out_mob_demob for structure in project.structures])
            total_persons_transport =           sum([structure.out_persons_transport for structure in project.structures])

            sum_total = sum([total_material_production, total_material_transport, total_disposal_transport, total_equipment,
                            total_energy_electricity_hour, total_mob_demob, total_persons_transport])

            data_project = {'MP': total_material_production, 'MT': total_material_transport, 'DT': total_disposal_transport, 'EQ': total_equipment,
                            'EE': total_energy_electricity_hour, 'MD': total_mob_demob, 'PT': total_persons_transport, 'Total': sum_total, 'Project': project.project_variant}

            df = df.append(data_project, ignore_index=True)

    base = alt.Chart(df).mark_bar().encode(
        x = 'Project:N',
        #y = 'MP:Q',
        #y = alt.Y('MP:Q', axis=alt.Axis(labelAngle=-45), title=None),
        color = 'Project:N',
    )

    base_text = base.mark_text(
        align='center',
        baseline='top',
        dy=-12
    )

    categrogy = ['MP', 'MT', 'DT', 'EQ', 'EE', 'MD', 'PT', 'Total']
    chart = alt.vconcat(data=df)
    for item in categrogy:
        y_encode = item+':Q'
        c = base.encode(y=y_encode)
        c_text = base_text.encode(text=y_encode).encode(y=alt.Y(y_encode))
        chart |= (c + c_text)
    
    chart.configure_legend(
        #titleFontSize=18,
        labelFontSize=16
        ).configure_axis(
        titleFontSize=18,
        labelFontSize=16
        )

    return chart.resolve_scale(y='shared')


def create_tCO2eq_barchart_all_projects_matplotlib(projects):
    """ Create tCO2eq bar chart for all projects with matplotlib
    This is to compare total tCO2eq for each of the categories
    """

    df = pd.DataFrame({
                        })

    for project in projects:
        if project.structures:
            total_material_production =         sum([structure.out_material_production for structure in project.structures])
            total_material_transport =          sum([structure.out_material_transport for structure in project.structures])
            total_disposal_transport =          sum([structure.out_disposal_transport for structure in project.structures])
            total_equipment =                   sum([structure.out_equipment for structure in project.structures])
            total_energy_electricity_hour =     sum([structure.out_energy_electricity_hour for structure in project.structures])
            total_mob_demob =                   sum([structure.out_mob_demob for structure in project.structures])
            total_persons_transport =           sum([structure.out_persons_transport for structure in project.structures])

            sum_total = sum([total_material_production, total_material_transport, total_disposal_transport, total_equipment,
                            total_energy_electricity_hour, total_mob_demob, total_persons_transport])

            data_project = {'MP': total_material_production, 'MT': total_material_transport, 'DT': total_disposal_transport, 'EQ': total_equipment,
                            'EE': total_energy_electricity_hour, 'MD': total_mob_demob, 'PT': total_persons_transport, 'Total': sum_total, 'Project': project.project_variant}

            df = df.append(data_project, ignore_index=True)

    fig, ax = plt.subplots()
    # settings for color: green (lowest total tCO2_eq) to orange (highest total tCO2_eq)
    colors = cm.summer(df['Total'] / float(max(df['Total'])))
    #ax = df.plot.barh(x='Category', stacked=False, colormap='summer')
    #ax = df.plot.barh(x='Project', stacked=False, colormap='cool')
    df.plot.barh(x='Project', stacked=False, colormap='cool', ax=ax)
    ax.set_xlabel('tCO2_eq')
    return fig, ax, df


def create_tCO2eq_barchart_all_categories_matplotlib(projects):
    """ Create tCO2eq bar chart for all projects with matplotlib
    This is to compare total tCO2eq for each of the categories
    """
    categrogy = ['Total', 'MP', 'MT', 'DT', 'EQ', 'EE', 'MD', 'PT']

    df = pd.DataFrame({
                        'Category': categrogy,
                        })
    for project in projects:
        total_material_production =         sum([structure.out_material_production for structure in project.structures])
        total_material_transport =          sum([structure.out_material_transport for structure in project.structures])
        total_disposal_transport =          sum([structure.out_disposal_transport for structure in project.structures])
        total_equipment =                   sum([structure.out_equipment for structure in project.structures])
        total_energy_electricity_hour =     sum([structure.out_energy_electricity_hour for structure in project.structures])
        total_mob_demob =                   sum([structure.out_mob_demob for structure in project.structures])
        total_persons_transport =           sum([structure.out_persons_transport for structure in project.structures])

        sum_total = sum([total_material_production, total_material_transport, total_disposal_transport, total_equipment,
                        total_energy_electricity_hour, total_mob_demob, total_persons_transport])

        data_project = [sum_total, total_material_production, total_material_transport, total_disposal_transport, total_equipment,
                        total_energy_electricity_hour, total_mob_demob, total_persons_transport]

        df[project.project_variant] = data_project

    fig, ax = plt.subplots()
    # settings for color: green (lowest total tCO2_eq) to orange (highest total tCO2_eq)
    #colors = cm.summer(df['Total'] / float(max(df['Total'])))
    #ax = df.plot.barh(x='Category', stacked=False, colormap='summer')
    #df.plot.barh(x='Category', stacked=False, colormap='summer', ax=ax)
    #ax.set_xlabel('tCO2_eq')

    # colors
    colors_scale = np.linspace(0.4, 0.8, len(projects)) # higher number is darker
    variants_tCO2eq_sum_total = [df[proj.project_variant][0] for proj in projects]
    variants_tCO2eq_sum_total_index = sorted(range(len(variants_tCO2eq_sum_total)), key=lambda k:variants_tCO2eq_sum_total[k])
    #colors_scale_sorted # a variant with bigger tCO2_eq is darker
    colors_scale_sorted = [0]*len(projects)
    for i, index in enumerate(variants_tCO2eq_sum_total_index):
        colors_scale_sorted[index] = colors_scale[i]
    colors = plt.cm.GnBu(colors_scale_sorted)

    # some divisions for good spacing
    width = 7
    x = np.linspace(0, width, len(categrogy))
    group_width = 0.6
    bar_width = group_width/len(projects)
    x = x - group_width/2 - bar_width/2
    for i, proj in enumerate(projects):
        ax.bar(x, df[proj.project_variant], width=bar_width, color=colors[i], label=proj.project_variant)
        x = x + bar_width + bar_width/5

    ax.set_xticks(x - group_width/2 - bar_width/2)
    ax.set_xticklabels(categrogy)
    ax.legend(fontsize=8)
    ax.set_ylabel('tCO2_eq')

    # For each bar in the chart, add a text label.
    for bar in ax.patches:
      # The text annotation for each bar should be its height.
      bar_value = bar.get_height()
      # Format the text with commas to separate thousands. You can do
      # any type of formatting here though.
      #text = f'{bar_value:,}'
      text = '{:.0f}'.format(bar_value)
      # This will give the middle of each bar on the x-axis.
      text_x = bar.get_x() + bar.get_width() / 2
      # get_y() is where the bar starts so we add the height to it.
      text_y = bar.get_y() + bar_value
      # If we want the text to be the same color as the bar, we can
      # get the color like so:
      bar_color = bar.get_facecolor()
      # If you want a consistent color, you can just set it as a constant, e.g. #222222
      ax.text(text_x, text_y, text, ha='center', va='bottom', color='black',
              size=7)

    return fig, ax, df


def create_tCO2eq_barchart_epd_matplotlib(projects):
    """ Create tCO2eq bar chart for all projects with matplotlib
    No splitting of tCO2eq following categrogies, only total tC02eq calculated according to EPD is plotted
    """
    categrogy = ['Total']

    df = pd.DataFrame({
                        'Category': categrogy,
                        })
    for project in projects:
        sum_project = 0.0
        for structure in project.structures:
            sum_structure = structure.calc_co2eq()
            sum_project += sum_structure

        data_project = [sum_project]  # only total CO2 for each of the projects is stored for plotting

        df[project.project_variant] = data_project

    fig, ax = plt.subplots()
    # settings for color: green (lowest total tCO2_eq) to orange (highest total tCO2_eq)
    #colors = cm.summer(df['Total'] / float(max(df['Total'])))
    #ax = df.plot.barh(x='Category', stacked=False, colormap='summer')
    #df.plot.barh(x='Category', stacked=False, colormap='summer', ax=ax)
    #ax.set_xlabel('tCO2_eq')

    # colors
    colors_scale = np.linspace(0.4, 0.8, len(projects)) # higher number is darker
    variants_tCO2eq_sum_total = [df[proj.project_variant][0] for proj in projects]
    variants_tCO2eq_sum_total_index = sorted(range(len(variants_tCO2eq_sum_total)), key=lambda k:variants_tCO2eq_sum_total[k])
    #colors_scale_sorted # a variant with bigger tCO2_eq is darker
    colors_scale_sorted = [0]*len(projects)
    for i, index in enumerate(variants_tCO2eq_sum_total_index):
        colors_scale_sorted[index] = colors_scale[i]
    colors = plt.cm.GnBu(colors_scale_sorted)

    # some divisions for good spacing
    width = 1
    x = np.linspace(0, width, len(categrogy))
    group_width = 0.1
    bar_width = group_width/len(projects)
    x = x - group_width/2 - bar_width/2
    for i, proj in enumerate(projects):
        ax.bar(x, df[proj.project_variant], width=bar_width, color=colors[i], label=proj.project_variant)
        x = x + bar_width + bar_width*3

    ax.set_xticks(x - group_width/2 - bar_width/2)
    ax.set_xticklabels(categrogy)
    ax.legend(fontsize=8)
    ax.set_ylabel('tCO2_eq')

    # For each bar in the chart, add a text label.
    for bar in ax.patches:
      # The text annotation for each bar should be its height.
      bar_value = bar.get_height()
      # Format the text with commas to separate thousands. You can do
      # any type of formatting here though.
      #text = f'{bar_value:,}'
      text = '{:.0f}'.format(bar_value)
      # This will give the middle of each bar on the x-axis.
      text_x = bar.get_x() + bar.get_width() / 2
      # get_y() is where the bar starts so we add the height to it.
      text_y = bar.get_y() + bar_value
      # If we want the text to be the same color as the bar, we can
      # get the color like so:
      bar_color = bar.get_facecolor()
      # If you want a consistent color, you can just set it as a constant, e.g. #222222
      ax.text(text_x, text_y, text, ha='center', va='bottom', color='black',
              size=7)

    return fig, ax, df

def create_tCO2eq_barchart_all_projects(projects):
    """ Create tCO2eq bar chart for all projects
    This is to compare total tCO2eq
    """

    df = pd.DataFrame({
                        })
    for project in projects:
        total_material_production =         sum([structure.out_material_production for structure in project.structures])
        total_material_transport =          sum([structure.out_material_transport for structure in project.structures])
        total_disposal_transport =          sum([structure.out_disposal_transport for structure in project.structures])
        total_equipment =                   sum([structure.out_equipment for structure in project.structures])
        total_energy_electricity_hour =     sum([structure.out_energy_electricity_hour for structure in project.structures])
        total_mob_demob =                   sum([structure.out_mob_demob for structure in project.structures])
        total_persons_transport =           sum([structure.out_persons_transport for structure in project.structures])

        data_project = [total_material_production, total_material_transport, total_disposal_transport, total_equipment,
                        total_energy_electricity_hour, total_mob_demob, total_persons_transport]

        df[project.project_variant] = data_project
        df['tCO2_eq_total'] = sum([total_material_production, total_disposal_transport, total_disposal_transport, total_equipment,
                                total_energy_electricity_hour, total_mob_demob, total_persons_transport])
    
    project_names = [project.project_variant for project in projects]

    c = alt.Chart(df).mark_bar().properties(
        width = 800,
        height = 120,
        ).configure_legend(
        #titleFontSize=18,
        labelFontSize=16
        ).configure_axis(
        titleFontSize=18,
        labelFontSize=16,
        ).encode(
            x = 'tCO2_eq_total:Q',
            y = alt.X('Projects:N', axis=alt.Axis(labelAngle=-45)),
            color = 'Projects:N',
            #row=alt.Row('Category')
            ).transform_fold(
                            as_=['Projects', 'tCO2_eq_total'],
                            fold=project_names
                            )
    return c