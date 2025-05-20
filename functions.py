import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd
from sklearn.preprocessing import StandardScaler


def rescale_keep_zero(series):
    max_pos = series[series > 0].max()
    min_neg = series[series < 0].min()

    def scale_value(x):
        if x > 0:
            return x / max_pos if max_pos != 0 else 0
        elif x < 0:
            return x / abs(min_neg) if min_neg != 0 else 0
        else:
            return 0
    return series.apply(scale_value)


def choropleth(df, feature, years, cmap, title=None, draw_borders=False, save_img=False, rescale=False):
    ''' Parameters
        ----------
        df : Pandas dataframe
        feature : str
            feature to be plotted
        year : list
            list of years (str) to be used for mapping
        cmap : str
            color map palette - look at seaborn documentation for options
        title : str, optional
            title for chart
        
        Yields
        -------
        matplotlib object
            Choropleth map(s) for specified feature and year(s)'''

    # outside loop so that scale of all years is same
    vmin = df[feature].min()
    vmax = df[feature].max()

    for year in years:
        # Create df specific to year parameter
        map_df = df[df.year == year]
        # rescale data
        if rescale:
            map_df[feature] = rescale_keep_zero(map_df[feature])
            vmin=-1
            vmax=1

        # Read shapefile using Geopandas
        shape_df= gpd.read_file('Data/Raw/tracts2020_shapefile/nyct2020.shp')
        geo_df = shape_df.merge(map_df, on='GEOID')
        fig, ax = plt.subplots(figsize = (40,40), dpi=200)
        ax.patch.set_alpha(0.0)
        # Plot the geodataframe
        geo_df.plot(ax=ax, column =feature, cmap=cmap, legend=False, antialiased=False)

        if draw_borders:  #  draw borders around class
	        for gent_class, data in geo_df.groupby('label'):
	        	if gent_class == 2: #  gentrified tracts
	        		data.boundary.plot(ax=ax, linewidth=1, edgecolor='black')
        # Set tile based on parameter, otherwise use feature name
        if title:
            ax.set_title(title+", "+year, fontdict={'fontsize': 60}, loc='center')
        else:
            ax.set_title(feature+", "+year, fontdict={'fontsize': 60}, loc='center')
        # ax.set(xlim=(-126, -66), ylim=(24, 50));
        # plt.xticks([], [])
        # plt.yticks([], [])
        cax = fig.add_axes([.95, 0.28, 0.02, 0.5])
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
        sm._A = []
        cbr = fig.colorbar(sm, cax=cax)
        cbr.set_label(feature, size=45)
        cbr.ax.tick_params(labelsize=35) 
        ax.set_axis_off()
        # ax.annotate("__Optional Annotation__", xy=(0.25, .1), size=20, xycoords='figure fraction')
        if save_img:
            if title:
                plt.savefig(f'Images/{year}_{title}.png',format = 'png',bbox_inches='tight', transparent=True)
            else:
                plt.savefig(f'Images/{year}_{feature}.png',format = 'png',bbox_inches='tight', transparent=True)


def lineplot(df, features, title=None):
    ''' Parameters
        ----------
        df : Pandas dataframe
        features: list
            one or more features to be plotted
        title: str, optional
            title for chart
        
        Yields
        -------
        matplotlib object
            One or more overlayed lineplots'''
    
    
    plt.figure(figsize=(20, 8));
    for feat in features:
        # x = df.groupby("year")[feat].mean().reset_index().dropna()
        # y = (x[feat] - min(x[feat])) / (max(x[feat]) - min(x[feat]))
        y = df[feat]
        ax= sns.lineplot(x=df['year'].astype(int), y= y, label=feat, linewidth = 4)
    ax.set_title(title, fontsize=24);
    ax.set_ylabel(feat, fontsize=20);
    ax.set_xlabel('Year', fontsize=20);
    ax.legend(prop=dict(size=18));
    plt.xticks(fontsize=16);
    plt.yticks(fontsize=16);
#     plt.savefig('../images/line_'+title+'.png',format = 'png',bbox_inches='tight', transparent=True)



def barchart(df, features, title=None):
    ''' Parameters
        ----------
        df : Pandas dataframe
        features: list
            one or more features to be plotted
        title: str, optional
            title for chart
        
        Yields
        -------
        matplotlib object
            One or more side-by-side barcharts'''
    
    # Create df for year
    plot_df = df.groupby("Year")[features].mean().fillna(0)
    # Plot each feature specified in parameters
    for feat in features:
        plot_df[feat] =(plot_df[feat] - min(plot_df[feat])) / (max(plot_df[feat]) - min(plot_df[feat]))
    plot_df.plot(by='Year',kind='bar',fontsize=16,rot='horizontal',figsize=(25,10));
    plt.xlabel('Year', fontdict={'fontsize':24});
    plt.ylabel('Scaled Count', fontdict={'fontsize':24});
    plt.xticks(fontsize=22);
    plt.yticks(fontsize=22);
    plt.legend(prop=dict(size=22));
    plt.title(title, fontdict={'fontsize':30});
#     plt.savefig('../images/bar_'+title+'.png',format = 'png',bbox_inches='tight', transparent=True)