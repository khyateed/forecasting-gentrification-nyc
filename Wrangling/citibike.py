import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import os
import datetime as dt


def preprocess_rides(rides_df):
    # get all the unique coordinates from ride starts and ends
    start_coord_df = rides_df[["start station latitude", "start station longitude"]]
    start_coord_df.columns = ["lat", "lon"]
    end_coord_df = rides_df[["end station latitude", "end station longitude"]]
    end_coord_df.columns = ["lat", "lon"]

    coord_df = pd.concat([start_coord_df, end_coord_df]).drop_duplicates().reset_index(drop=True)

    # Load the census tract shapefile
    tracts = gpd.read_file('Data/Raw/tracts2020_shapefile/nyct2020.shp')
    tracts = tracts.to_crs(epsg=4326)

    coords = [tuple(record) for record in
              coord_df.to_records(index=False)]  # [(40.735324, -73.998004), (40.715595,	-73.987030)]

    # Create a GeoDataFrame from the coordinates
    geometry = [Point(lon, lat) for lat, lon in coords]
    points_df = gpd.GeoDataFrame(geometry=geometry, crs="EPSG:4326")
    points_df["lat"] = coord_df["lat"]
    points_df["lon"] = coord_df["lon"]

    # Perform a spatial join to match points to census tracts
    ct_lookup = gpd.sjoin(points_df, tracts, how='left', predicate="within")[["lat", "lon", "GEOID", 'NTAName']]

    # get start station CT from dictionary lookup
    rides_df_ct = rides_df.merge(ct_lookup, left_on=["start station latitude", "start station longitude"],
                                 right_on=["lat", "lon"])
    rides_df_ct.rename(columns={"GEOID": "start_CT"}, inplace=True)
    rides_df_ct.drop(['lat', 'lon'], axis=1, inplace=True)

    # get end station CT from dictionary lookup
    rides_df_ct = rides_df_ct.merge(ct_lookup, left_on=["end station latitude", "end station longitude"],
                                    right_on=["lat", "lon"])
    rides_df_ct.rename(columns={"GEOID": "end_CT"}, inplace=True)
    rides_df_ct.drop(['lat', 'lon'], axis=1, inplace=True)

    # convert time to year
    rides_df_ct["starttime"] = rides_df_ct["starttime"].dt.year
    rides_df_ct.rename(columns={'starttime': 'Year'}, inplace=True)

    # clean up columns TODO maybe explore some of these other columns for features later
    rides_df_ct = rides_df_ct[['Year','start_CT','end_CT','NTAName_x','NTAName_y']]

    # count each "start" and "end" as one trip in that CT
    temp1 = rides_df_ct[['start_CT', 'NTAName_x']].copy()
    temp1.rename(columns={'start_CT':'Tract','NTAName_x':'Name'}, inplace=True)
    temp2 = rides_df_ct[['end_CT', 'NTAName_y']].copy()
    temp2.rename(columns={'end_CT':'Tract','NTAName_y': 'Name'}, inplace=True)
    df_processed = pd.concat([temp1, temp2]).value_counts().rename(
        'Num_citibike_rides').reset_index()
    df_processed['Year'] = rides_df_ct.iloc[0]['Year']
    df_processed['Year'] = df_processed['Year'].astype(str)
    return df_processed

directory = "Data/Raw/Citibike"
all_years_list = []

for yr_folder in os.listdir(directory)[1:]:  # each year in teh folder
    monthly_rides_list = []
    if yr_folder != '.DS_Store':
        for filename in os.listdir(directory+'/'+yr_folder):  # each month in the year
            if filename.endswith('.csv'):
                print(filename)
                file_path = os.path.join(directory, yr_folder,filename)
                df = pd.read_csv(file_path, low_memory=False)
                df.rename(columns={'started_at':'starttime',
                                    'start_lat':"start station latitude",
                                    'start_lng':"start station longitude",
                                    'end_lat':'end station latitude',
                                    'end_lng':'end station longitude',
                                   'Start Time': 'starttime',
                                   'Start Station Latitude':"start station latitude",
                                   'Start Station Longitude':"start station longitude",
                                   'End Station Latitude':'end station latitude',
                                   'End Station Longitude': 'end station longitude'
                                   }, inplace=True)
                df = df[['starttime',"start station latitude","start station longitude",
                         'end station latitude','end station longitude']]
                df["starttime"] = pd.to_datetime(df["starttime"])  # convert to datetime here bc inconsistent types across years
                monthly_rides_list.append(df)
        year_rides_df = pd.concat(monthly_rides_list)
        print('done reading files')
        year_rides_df = preprocess_rides(year_rides_df)
        print('done processing')
        year_rides_df.to_parquet(f'Data/Cleaned/{filename[:4]}_citibike.parquet')
        print('saved')
#         all_years_list.append(year_rides_df)

# all_years_df = pd.concat(all_years_list).sort_values('Tract')
# all_years_df.to_parquet('Data/Cleaned/citibike.parquet')
