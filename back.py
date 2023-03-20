import csv
from datetime import datetime
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
import io
from PIL import Image




def creatMap():
    location_data = {
        1: [39.98966406, 116.403458],
        2: [40.22994018, 116.2330318],
        3: [40.30023118, 116.2324668],
        4: [39.93865024, 116.4350122],
        5: [39.93736379, 116.3693659],
        6: [39.91345006, 116.1956398],
        7: [40.30842471, 116.6469836],
        8: [39.94700908, 116.470307],
        9: [40.17700804, 116.664263],
        10: [39.88797708, 116.417313],
        11: [39.9727465, 116.3056615],
        12: [39.88565298, 116.3747278]
    }
    df = pd.read_csv('concatenated_data.csv')

    location_df = pd.DataFrame.from_dict(location_data, orient='index', columns=['Latitude', 'Longitude'])
    df_merged = df.merge(location_df, left_on='station', right_index=True)
    last_rows = df_merged.groupby('station').tail(1)

    map_center = [39.995, 116.40]
    map_zoom = 9

    map_beijing = folium.Map(location=map_center, zoom_start=map_zoom)

    # Filter the DataFrame for rows, then columns, then remove NaNs
    heat_df = last_rows[['Latitude', 'Longitude', 'PM2.5']]
    heat_df = heat_df.dropna(axis=0, subset=['Latitude', 'Longitude', 'PM2.5'])

    # List comprehension to make our list of lists
    heat_data = [[row['Latitude'], row['Longitude'], row['PM2.5']] for index, row in heat_df.iterrows()]

    # Plot the heatmap with the custom gradient
    HeatMap(heat_data, radius=30).add_to(map_beijing)

    # Plot it on the map
    for point in heat_data:
        lat, lon, value = point
        folium.Marker(
            location=[lat, lon],
            icon=None,
            popup=f"Value: {value}").add_to(map_beijing)

    '''
    # Add the color scale legend to the map
    color_scale.caption = 'PM2.5'
    map_beijing.add_child(color_scale)
    '''

    map_beijing.save('map.html')
    img_data = map_beijing._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img.save('map.png')


def getCluster(attr, attr2, loc='1', sDate="Fri Mar 1 2013", eDate="Tue Feb 28 2017", num_clusters=4):
    csvfile = open('concatenated_data.csv')
    reader = csv.DictReader(csvfile)
    sDate = formateDate(sDate)
    eDate = formateDate(eDate)
    selected_data = []
    selected_date = []
    cluster_data = []
    count = 0
    for row in reader:
        if row['station'] == loc:
            date_str = row['year']
            if int(row["month"]) < 10:
                date_str += '0'
            date_str += row['month']

            if int(row["day"]) < 10:
                date_str += '0'
            date_str += row['day']

            timestamp = int(date_str)

            if sDate <= timestamp <= eDate:
                cluster_data.append([float(row[attr]), float(row[attr2])])
                selected_data.append(float(row[attr]))
                selected_date.append(row["month"] + '-' + row["day"] + '-' + row['year'])
    n = int(len(selected_date) / 7)
    result = [selected_date[0]]
    for i in range(len(selected_date)):
        if i % n == 0:
            result.append(selected_date[i])
    result.append(selected_date[-1])
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(cluster_data)
    return selected_data, result, list(kmeans.labels_)


def update_heatmap(attr, station):
    df = pd.read_csv('concatenated_data.csv')
    specific_station = station
    df_filtered = df[df['station'] == specific_station]

    pivot_data = df_filtered.groupby(['year', 'month'])[attr].mean().unstack()
    normalized_data_df = pd.DataFrame(pivot_data)
    normalized_data_df = (normalized_data_df - normalized_data_df.min().min()) / (
            normalized_data_df.max().max() - normalized_data_df.min().min())
    n_years = len(pivot_data)
    n_months = len(pivot_data.columns)

    theta = np.linspace(0, 2 * np.pi, n_months + 1)
    radii = np.linspace(0.1, 1, n_years + 1)

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(3, 3))
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    # Create grid
    for month in range(n_months):
        ax.plot([theta[month], theta[month]], [0.1, 1], 'k', lw=0.5, alpha=0.5)
    for year in range(n_years):
        ax.plot(theta, np.full_like(theta, radii[year]), 'k', lw=0.5, alpha=0.5)

    # Create heatmap
    for year in range(n_years):
        for month in range(n_months):
            value = normalized_data_df.iloc[year, month]
            color = plt.cm.get_cmap('coolwarm')(value)
            ax.fill_between([theta[month], theta[month + 1]], radii[year], radii[year + 1], color=color)

    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax.set_xticks(theta[:-1])
    ax.set_xticklabels(month_names)
    ax.set_yticks(radii[:-1])
    ax.set_yticklabels(pivot_data.index)
    ax.yaxis.set_tick_params(pad=10)

    cbar = fig.colorbar(plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=pivot_data.min().min(),
                                                                                  vmax=pivot_data.max().max())),
                        ax=ax, pad=0.1, shrink=0.7, aspect=30)
    cbar.ax.set_ylabel('{} ({:.2f} - {:.2f})'.format(attr, pivot_data.min().min(), pivot_data.max().max()),
                       rotation=270, labelpad=15)

    plt.savefig('polar.png')


def formateDate(date):
    date_obj = datetime.strptime(date, '%a %b %d %Y')
    return int(date_obj.strftime('%Y%m%d'))


def getData(attr, loc='1', sDate="Fri Mar 1 2013", eDate="Tue Feb 28 2017"):
    csvfile = open('concatenated_data.csv')
    reader = csv.DictReader(csvfile)
    sDate = formateDate(sDate)
    eDate = formateDate(eDate)
    selected_data = []
    selected_date = []
    for row in reader:
        if row['station'] == loc:
            date_str = row['year']
            if int(row["month"]) < 10:
                date_str += '0'
            date_str += row['month']

            if int(row["day"]) < 10:
                date_str += '0'
            date_str += row['day']

            timestamp = int(date_str)

            if sDate <= timestamp <= eDate:
                selected_data.append(float(row[attr]))
                selected_date.append(row["month"] + '-' + row["day"] + '-' + row['year'])
    n = int(len(selected_date) / 7)
    result = [selected_date[0]]
    for i in range(len(selected_date)):
        if i % n == 0:
            result.append(selected_date[i])
    result.append(selected_date[-1])
    return selected_data, result


# print(getCluster("PM2.5", "10"))
# creatMap()
