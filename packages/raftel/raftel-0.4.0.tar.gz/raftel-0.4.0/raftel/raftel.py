# package raftel contains the function to plot list of s2id easily

import math

import s2sphere
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from monochromap import MonochroMap, Polygon, Point

palettes = ['Reds', 'Greens', 'Blues', 'Oranges', 'Purples']


def _rad_to_degree(x):
    """
    Convert radian to degree (duh)
    """
    return x * 180 / math.pi


def get_s2id(lat, lon, level):
    """
    Given coordinates and the level, return the s2id at that particular level that contains the coordinate

    :param lat: the latitude part of the coordinates, from -180 to +180
    :param lon: the longitude part of the coordinates, from -180 to +180
    :param level: the level of s2id, int from 0 to 31
    :returns integer 64 bit with the value of the s2id
    """

    pos = s2sphere.LatLng.from_degrees(lat, lon)
    s2cell = s2sphere.CellId.from_lat_lng(pos).parent(level)

    return s2cell.id()


def get_region(lat, lon, radius, level):
    """
    Get a list of s2ids within the radius from specific lat and long at specified level
    Thanks to Gaurav's answer posted here: https://stackoverflow.com/questions/44649831/using-python-s2-s2sphere-library-find-all-s2-cells-of-a-particular-level-with
    
    :param lat: the latitude part of the coordinates, from -180 to +180
    :param lon: the longitude part of the coordinates, from -180 to +180
    :param radius: the maximum distance from the coordinates that still contains the s2id, in meter
    :param level: the level of s2id, int from 0 to 31
    :returns integer 64 bit with the value of the s2id
    
    """

    earthCircumferenceMeters = 1000 * 40075.017
    radius_radians = (2 * math.pi) * (float(radius) / earthCircumferenceMeters)
    
    latlng = s2sphere.LatLng.from_degrees(float(lat), float(lon)).normalized().to_point()

    region = s2sphere.Cap.from_axis_height(latlng, (radius_radians*radius_radians)/2)
    coverer = s2sphere.RegionCoverer()
    coverer.min_level = int(level)
    coverer.max_level = int(level)
    coverer.max_cells = 2**30
    covering = coverer.get_covering(region)
 
    s2ids = [cell.id() for cell in covering]

    return s2ids


def plot_s2id(s2ids, color='#00ff00', alpha=0.5, auto_render=True, m=None, api_key=''):
    """
    Given list of s2id, plot the area in the map.

    :param s2ids: iterable that contains either int or string of s2id to be plot
    :param color: the color of s2id block in the map
    :param auto_render: option to either return a staticmap object with false, or the image object
    :param m: a staticmap object if you want to add more plot to previously object
    :param alpha: set the transparency of the color

    :returns: either image or staticmap object
    """
    if m is None:
        m = MonochroMap(api_key=api_key)

    if (type(color) is not str):
        if (len(color) != len(s2ids)):
            raise Exception('Please use string or list of string with the same length as the s2id in hexadecimal format')

    for i, s2 in enumerate(s2ids):

        s2cell = s2sphere.CellId(int(s2))
        s = s2sphere.Cell(s2cell)

        lon0, lat0 = _rad_to_degree(s.get_latitude(0, 0)), _rad_to_degree(s.get_longitude(0, 0))
        lon1, lat1 = _rad_to_degree(s.get_latitude(1, 1)), _rad_to_degree(s.get_longitude(1, 1))
        points = [[lat0, lon0], [lat0, lon1], [lat1, lon1], [lat1, lon0]]

        if type(color) is str:
            full_color = f'{color}{math.ceil(alpha*255):02x}'
        else:
            full_color = f'{color[i]}{math.ceil(alpha*255):02x}'

        region = Polygon(points, full_color, 'black', 20)
        m.add_feature(region)

    if auto_render:
        return m.render()
    return m


def plot_point(lats, lons, color='#5cac2d', m=None, auto_render=True, api_key=''):
    """
    Plot set of points indicated by their coordinates into the map
    """
    if m is None:
        m = MonochroMap(api_key=api_key)

    for lat, lon in zip(lats, lons):
        point = Point((lon, lat), color, 5)
        m.add_feature(point)

    if auto_render:
        return m.render()
    return m
    

def area_plot(data=None, s2id_col='s2id', hue='', color='', alpha=1, col='', api_key=''):
    """
    Plot s2id inside a dataframe with seaborn like interface
    """

    if col != '':

        cols = data[col].unique()
        fig, axes = plt.subplots(1, len(cols), figsize=(12*len(cols), 12))
        
        for c, ax in zip(cols, axes.reshape(-1)):

            print('plot ', c)
            img = area_plot(data[data[col] == c], s2id_col, hue, color, alpha, col='', api_key=api_key)
            ax.imshow(img)
        
        return fig

    if hue == '':
        if color == '':
            return plot_s2id(data[s2id_col], alpha=alpha, api_key=api_key)
        
        else:
            colors = _create_color_scheme(data[color], palettes[0])
            m = plot_s2id(data[s2id_col], alpha=alpha, color=colors, api_key=api_key)

            return m

    m = None
    cats = data[hue].unique()
    for i, cat in enumerate(cats):
        
        temp = data[data[hue] == cat]

        if color == '':
            r, g, b = (np.array(sns.color_palette(palettes[i])[-1])*255).astype(int)
            c = f'#{r:02x}{g:02x}{b:02x}'
            m = plot_s2id(temp[s2id_col], color=c, m=m, auto_render=False, alpha=alpha, api_key=api_key)
        
        else:
            colors = _create_color_scheme(temp[color], palettes[i])            
            m = plot_s2id(temp[s2id_col], color=colors, m=m, auto_render=False, alpha=alpha, api_key=api_key)

    return m.render()


def _create_color_scheme(vals, palette):

    min_val = min(vals)
    max_val = max(vals)

    n_unique = (len(vals.unique())-1)
    idx = ((np.array(vals) - min_val) / (max_val - min_val) * n_unique).astype(int)
    colors = [f'#{x[0]:02x}{x[1]:02x}{x[2]:02x}' for x in 
        [(np.array(sns.color_palette(palette, n_unique+1)[j])*255).astype(int) for j in idx]
    ]

    return colors
