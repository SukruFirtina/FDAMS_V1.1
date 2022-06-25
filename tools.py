import json
import os
import pathlib
import threading
from tkinter import mainloop, DoubleVar

import numpy
from branca.element import IFrame
from requests import Request, Session

import cv2
import pandas as pd
#import serializers as serializers
from folium import plugins
import folium
import sys
#from PyQt5.QtCore import *
#from PyQt5.QtWebEngineWidgets import *
#from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import simplekml
import environment as env
import pathlib
import sys
#from gui_tools import restart_program
from data_correction import fix_time_digit, sender_fix_anomalies, fix_by_distances
import webview
from tkinter import *
from folium.plugins import *
import base64
import json
#from django.forms.models import model_to_dict
#from statsmodels.nonparametric.kernel_regression import KernelReg
from scipy.signal import savgol_filter
import numpy as np
#from folium_jsbutton import JsButton
from tkinter import *
from itertools import islice
from itertools import chain

import json
import string
import enchant


from PIL import Image

def files(image_frames):
    try:
        os.remove(image_frames)
    except OSError as s:
        # print(s)
        pass

    if not os.path.exists(image_frames):
        os.makedirs(image_frames)

    src_vid = cv2.VideoCapture("video.mp4")
    return src_vid


def open_file():
    from os import startfile
    file = pathlib.Path("files/output.txt")
    if file.exists():
        print("File exist")
        startfile("files/output.txt")
    else:
        print("File not exist")
        env.label_information.configure(text="File not exist !!! ")


def fix_image(image):
    start_point = (0, 150)
    end_point = (1920, 920)
    color = (0, 0, 0)
    thickness = -1

    image = cv2.rectangle(image, start_point, end_point, color, thickness)
    image = cv2.medianBlur(image, 3)
    image = cv2.bitwise_not(image)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)[1]
    image = cv2.medianBlur(image, 3)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    image = cv2.dilate(image, kernel)

    return image



def create_kml():


    frames = []
    for i in os.listdir("image_frames"):
        frames.append(str(i))

    df = pd.read_csv("files/fixed_output.csv")
    df = df.dropna()

    kml = simplekml.Kml()

    year = df['year']
    month = df['month']
    day = df['day']
    hour = df['hour']
    minute = df['min']
    second = df['sec']

    year = fix_time_digit(year)
    month = fix_time_digit(month)
    day = fix_time_digit(day)
    hour = fix_time_digit(hour)
    minute = fix_time_digit(minute)
    second = fix_time_digit(second)

    lines = []
    target_lines = []
    between_lines = []
    points = []
    target_points = []
    camera_areas = []

    lon, lat = calculate_location(df['degree_lat'], df['minute_lat'], df['second_lat'], df['direction_lat'],
                                  df['degree_lon'], df['minute_lon'], df['second_lon'], df['direction_lon'])

    target_lon, target_lat = calculate_location(df['target_degree_lat'], df['target_minute_lat'],
                                                df['target_second_lat'], df['target_direction_lat'],
                                                df['target_degree_lon'], df['target_minute_lon'],
                                                df['target_second_lon'], df['target_direction_lon'])







    lon = sender_fix_anomalies(pd.Series(lon), 10, 1)
    lat = sender_fix_anomalies(pd.Series(lat), 10, 1)
    lon = sender_fix_anomalies(pd.Series(lon), 7, 1)
    lat = sender_fix_anomalies(pd.Series(lat), 7, 1)
    target_lon = sender_fix_anomalies(pd.Series(target_lon), 10, 1.5)
    target_lat = sender_fix_anomalies(pd.Series(target_lat), 10, 1.5)
    target_lon = sender_fix_anomalies(pd.Series(target_lon), 6, 1.5)
    target_lat = sender_fix_anomalies(pd.Series(target_lat), 6, 1.5)

    lon, lat = fix_by_distances(lon, lat)
    target_lon, target_lat = fix_by_distances(target_lon, target_lat)

    # **************************************************************
    # SEVGOL uygulanıp uygulanmayacağını kullanıcının seçmesi daha uygun olur.
    # SEVGOL parametreleri seçilen fps değerine göre değişmeli
    # **************************************************************
    lon = savgol_filter(lon, 53, 2)
    lat = savgol_filter(lat, 53, 2)
    target_lon = savgol_filter(target_lon, 53, 2)
    target_lat = savgol_filter(target_lat, 53, 2)

    f = open('flight.kml', 'w')

    # Writing the kml file.
    f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.write("<kml xmlns='http://earth.google.com/kml/2.2'>\n")
    f.write("<Document>\n")
    f.write("   <name>flight</name>\n")
    for i in range(1, len(lon)):
        f.write("<Placemark>\n")
        f.write("        <TimeSpan>\n          <begin>" + '2015-12-02T%02i:%02i:%02iZ' % (
        df['hour'][i], df['min'][i], df['sec'][i]) + "</begin>\n        </TimeSpan>\n")
        f.write("   <LineString>\n")
        f.write("       <extrude>1</extrude>\n")
        f.write("       <altitudeMode>absolute</altitudeMode>\n")
        f.write("        <coordinates>" + str(lon[i - 1]) + "," + str(lat[i - 1]) + "," + str(
            df['altitude'][i-1]*0.3048) + " " + str(lon[i]) + "," + str(lat[i]) + "," + str(
            df['altitude'][i]*0.3048) + "</coordinates>\n")
        f.write("   </LineString>\n")
        f.write("</Placemark>\n")

    f.write("</Document>")
    f.write("</kml>\n")
    f.close()



    for i in range(1, len(lon)):
        longitude = lon[i]
        latitude = lat[i]
        target_longitude = target_lon[i]
        target_latitude = target_lat[i]
        kml.newpoint(coords=[(longitude, latitude)])
        kml.newpoint(coords=[(target_longitude, target_latitude)])

        if i != 1:
            prev_loc = location
            target_prev_loc = target_location

        else:
            map_ = folium.Map(location=(float(latitude), float(longitude)), zoom_start=15)

        location = float(latitude), float(longitude)
        target_location = float(target_latitude), float(target_longitude)

        # folium.Marker(location=location, popup=str(i), draggable=True).add_to(map_)
        # if i != 1:
        #     folium.PolyLine((prev_loc, location)).add_to(map_)

        if i != 1:
            lines.append(
                {"coordinates": [
                    [prev_loc[1], prev_loc[0]],
                    [location[1], location[0]],
                ],
                    "dates": [
                        year[i - 2] + "-" + month[i - 2] + "-" + day[i - 2] + "T" + hour[i - 2] + ":" + minute[
                            i - 2] + ":" +
                        second[i - 2],
                        year[i - 1] + "-" + month[i - 1] + "-" + day[i - 1] + "T" + hour[i - 1] + ":" + minute[
                            i - 1] + ":" +
                        second[i - 1]],
                    "color": "blue",
                    "weight": 9,
                    #"opacity": 0.50
                })
        if i != 1:
            target_lines.append(
                {"coordinates": [
                    [target_prev_loc[1], target_prev_loc[0]],
                    [target_location[1], target_location[0]],
                ],
                    "dates": [
                        year[i - 2] + "-" + month[i - 2] + "-" + day[i - 2] + "T" + hour[i - 2] + ":" + minute[
                            i - 2] + ":" +
                        second[i - 2],
                        year[i - 1] + "-" + month[i - 1] + "-" + day[i - 1] + "T" + hour[i - 1] + ":" + minute[
                            i - 1] + ":" +
                        second[i - 1]],
                    "color": "red",
                    "weight": 9})
        if i != 1:
            between_lines.append(
                {"coordinates": [
                    [location[1], location[0]],
                    [target_location[1], target_location[0]],
                ],
                    "dates": [

                        year[i - 1] + "-" + month[i - 1] + "-" + day[i - 1] + "T" + hour[i - 1] + ":" + minute[
                            i - 1] + ":" +
                        second[i - 1],
                        year[i - 1] + "-" + month[i - 1] + "-" + day[i - 1] + "T" + hour[i - 1] + ":" + minute[
                            i - 1] + ":" +
                        second[i - 1]
                    ],
                    "color": "#40E0D0",
                    "weight": 7,
                    "dash_array" : '10',
                    "offset" : 100
            }
            )

        if i != 1:
            between_lines.append(
                {"coordinates": [
                    [location[1], location[0]],
                    [target_location[1], target_location[0]],
                ],
                    "dates": [

                        year[i - 1] + "-" + month[i - 1] + "-" + day[i - 1] + "T" + hour[i - 1] + ":" + minute[
                            i - 1] + ":" +
                        second[i - 1],
                        year[i - 1] + "-" + month[i - 1] + "-" + day[i - 1] + "T" + hour[i - 1] + ":" + minute[
                            i - 1] + ":" +
                        second[i - 1]
                    ],
                    "color": "black",
                    "weight": 2,
                    "dash_array" : '10',
                    "offset" : 100
            }
            )


        if i != 1:
            points.append(
                {"coordinates": [
                    location[1], location[0]
                ],
                    "dates": [
                        year[i - 1] + "-" + month[i - 1] + "-" + day[i - 1] + "T" + hour[i - 1] + ":" + minute[
                            i - 1] + ":" +
                        second[i - 1],
                    #year[i - 1] + "-" + month[i - 1] + "-" + day[i - 1] + "T" + hour[i - 1] + ":" + minute[
                    #        i - 1] + ":" +
                    #    second[i - 1]
                    ],


                    "color": "blue",
                    "weight": 50,
                    #"opacity": 0.50
                })

        if i != 1:
            target_points.append(
                {"coordinates": [
                    target_location[1], target_location[0]
                ],
                    "dates": [
                        year[i - 1] + "-" + month[i - 1] + "-" + day[i - 1] + "T" + hour[i - 1] + ":" + minute[
                            i - 1] + ":" +
                        second[i - 1]],
                    "color": "blue",
                    "weight": 10,
                    # "opacity": 0.50
                })

        if i != 1:
            camera_areas.append(
                {"coordinates": [((
                    (prev_loc[1], prev_loc[0]),
                    (location[1], location[0]),
                    (target_location[1], target_location[0]),
                    (target_prev_loc[1], target_prev_loc[0]),

                ),)],
                    "dates": [
                        year[i - 1] + "-" + month[i - 1] + "-" + day[i - 1] + "T" + hour[i - 1] + ":" + minute[
                            i - 1] + ":" +
                        second[i - 1]],
                    "color": "blue",
                    "weight": 2,
                    "fillColor": "#458B00",
                    "opacity": 1,
                    "fillOpacity":1,
                    #"opacity": 0.50
                })

        if i != 1:
            camera_areas.append(
                {"coordinates": [((
                                      (location[1], location[0]),
                                      (target_prev_loc[1], target_prev_loc[0]),
                                      (target_location[1], target_location[0]),
                                      (prev_loc[1], prev_loc[0]),
                                      (location[1], location[0]),
                                      (target_location[1], target_location[0]),

                                  ),)],
                    "dates": [
                        year[i - 1] + "-" + month[i - 1] + "-" + day[i - 1] + "T" + hour[i - 1] + ":" + minute[
                            i - 1] + ":" +
                        second[i - 1]],
                    "color": "#00EE00",
                    "weight": 2,
                    "fillColor": "#DC143C",
                    "opacity": 1,
                    "fillOpacity": 1,
                    # "opacity": 0.50
                })
        i += 1
    # **************************************************************
    # Auto zoom
    # **************************************************************
    df_for_auto_zoom = pd.DataFrame({'Lat': lat, 'Long': lon})
    sw = df_for_auto_zoom[['Lat', 'Long']].min().values.tolist()
    ne = df_for_auto_zoom[['Lat', 'Long']].max().values.tolist()
    map_.fit_bounds([sw, ne])
    # **************************************************************


    kml.save('files/coordinates.kml')
    # map_.save('map.html')

    i = 0
    features = []
    features2 = []
    features3 = []
    features4 = []
    features5 = []
    features6 = []
    features7 = []

    marker = []
    #for i in range(len(df)):
    #    img = Image.open(r"image_frames/"+df["frame"][i])
    #    img = img.resize((560,315))
    #    #img = img.rotate(360-df['heading_angle'][i])
    #    img.save("frames_for_map/frame"+str(i)+".png")

    #icon_path = r"plane_marker.png"
    #icon = folium.features.CustomIcon(icon_image=icon_path, icon_size=(50,50))
    #oi = img.objects.get(token=100)
    #oi_dict = model_to_dict(img)
    #img = json.dumps(img)

    for i in range(len(df)):
        img = Image.open(r"res/plane_marker7.png")
        #img = img.resize((60,60))
        img = img.rotate(360-df['heading_angle'][i])
        img.save("markers/marker_"+str(i)+".png")



    coords = [line["coordinates"] for line in lines]
    coords = list(chain.from_iterable(coords))


    i=0


    for line in lines:
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": [list(coords[0:2*i])]


                },
                "properties": {
                    "icon": "marker",
                   #"iconstyle": {
                   #    'iconSize': [15, 15],
                   #    'iconUrl': str(pathlib.Path().resolve().as_uri()) + '/markers/marker_'+ str(i) +'.png'},

                    "popup":
                        '<img src= "' + str(pathlib.Path().resolve().as_uri()) + '/image_frames/' + str(df['frame'][i]) + '"'
                                                                                                                'width="640"'
                                                                                                                'height="360"/>',

                    "times": line["dates"],
                    "style": {
                        "color": line["color"],
                        "weight": line["weight"] if "weight" in line else 2,

                    },

                },
            }
        )

        i += 1

    target_coords = [line["coordinates"] for line in target_lines]
    target_coords = list(chain.from_iterable(target_coords))

    i = 0
    for line in target_lines:
        features2.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": [list(target_coords[0:2*i])],
                },
                "properties": {
                    "icon": 'marker',
                   #"iconstyle": {
                   #    'iconSize': [35, 35],
                   #    'iconUrl': str(pathlib.Path().resolve().as_uri()) + '/res/target_marker.png'},


                    "times": line["dates"],
                    "style": {
                        "color": line["color"],
                        "weight": line["weight"] if "weight" in line else 2,

                    },

                },
            }
        )
        i += 1

    i = 0
    for line in lines:
        features3.append(
            {
                "type": "Feature",
                'geometry': {'type': 'Point', 'coordinates': [sw[1], ne[0]]},

                "properties": {
                    "icon": 'marker',
                    "iconstyle": {
                        'iconSize': [560, 315],
                     #   'iconUrl': str(pathlib.Path().resolve().as_uri()) + '/frames_for_map/frame'+str(i)+'.png'},
                        'iconUrl': str(pathlib.Path().resolve().as_uri()) + '/image_frames/' + frames[i]},


                    "times": line["dates"],

                },
            }
        )
        i += 1


    i = 0
    before_time = []
    for point in points:
#        if before_time == point["dates"][0]:
#            point['coordinates'] = before_coord
        if before_time == point["dates"]:
           point['coordinates'] = before_coord
        features4.append(
            {
                "type": "Feature",
                'geometry': {'type': 'Point', 'coordinates': point['coordinates']},

                "properties": {
                    "icon": 'marker',
                    "iconstyle": {
                        'iconSize': [60, 60],
                        'iconUrl': str(pathlib.Path().resolve().as_uri()) + '/markers/marker_' + str(i) + '.png'},
                    "popup":
                        '<img src= "' + str(pathlib.Path().resolve().as_uri()) + '/image_frames/' + df['frame'][i] + '"'
                                                                                            'width="640"'
                                                                                            'height="360"/>',
                    "times": point["dates"],

                },
            }
        )

#        before_time = point["dates"][0]
#        before_coord =  point['coordinates']
        before_time = point["dates"]
        before_coord =  point['coordinates']
        i += 1

    i = 0
    before_time = []
    for between_line in between_lines:
        if before_time == between_line["dates"]:
            between_line['coordinates'] = before_coord
        features5.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": between_line["coordinates"]},

                "properties": {
                    "icon": 'marker',
                    #"iconstyle": {
                    #    'iconSize': [60, 60],
                    #    'iconUrl': str(pathlib.Path().resolve().as_uri()) + '/markers/marker_' + str(i) + '.png'},
                    #"popup":
                    #    '<img src= "' + str(pathlib.Path().resolve().as_uri()) + '/image_frames/' + df['frame'][i] + '"'
                    #                                                                                                 'width="640"'
                    #                                                                                                 'height="360"/>',
                    "times": between_line["dates"],
                    "style": {
                        "color": between_line["color"],
                        "dash_array": between_line["dash_array"],
                        "offset": between_line["offset"],
                        "weight": between_line["weight"] if "weight" in line else 2,}

                },
            }
        )
        before_time = between_line["dates"]
        before_coord = between_line['coordinates']
        i += 1

    i = 0
    before_time = []
    for target_point in target_points:
        if before_time == target_point["dates"]:
            target_point['coordinates'] = before_coord

        features6.append(
            {
                "type": "Feature",
                'geometry': {'type': 'Point', 'coordinates': target_point["coordinates"]},

                "properties": {
                    "icon": 'marker',
                    "iconstyle": {
                        'iconSize': [50, 50],
                        'iconUrl': str(pathlib.Path().resolve().as_uri()) + '/res/target_marker.png'},


                    "times": target_point["dates"],

                },
            }
        )
        before_time = target_point["dates"]
        before_coord = target_point['coordinates']
        i += 1

    i = 0
    before_time = []
    for camera_area in camera_areas:
        if before_time == camera_area["dates"]:
            camera_area['coordinates'] = before_coord

        features7.append(
            {
                "type": "Feature",
                'geometry': {'type': 'MultiPolygon', 'coordinates': camera_area['coordinates']},

                "properties": {
                    "icon": 'marker',
                    "iconstyle": {
                        'iconSize': [50, 50],
                        'iconUrl': str(pathlib.Path().resolve().as_uri()) + '/res/target_marker.png'},

                    "times": camera_area["dates"],

                    "style": {
                        "color": camera_area["color"],
                        "fillColor": camera_area["fillColor"],
                        "opacity":camera_area["opacity"],
                        "fillOpacity": camera_area["fillOpacity"],
                        "weight": camera_area["weight"] if "weight" in camera_area else 2, }

                },
            }
        )
        before_time = target_point["dates"]
        before_coord = target_point['coordinates']
        i += 1


    i = 0
    popups = folium.FeatureGroup(name='Points and FramePopups', overlay=False).add_to(map_)
    for point in points:
        icon_url = str(pathlib.Path().resolve().as_uri()) + '/markers/marker_' + str(i) + '.png'
        icon = folium.features.CustomIcon(icon_url,
                                          icon_size=(25, 25))
        tooltip = str(df['frame'][i])
        marker = folium.Marker(
            [point['coordinates'][1],point['coordinates'][0]],
            icon=icon,
            popup='<img src= "' + str(pathlib.Path().resolve().as_uri()) + '/image_frames/' + df['frame'][i] + '"'
                                                                                                                         'width="640"'
                                                                                                                         'height="360"/>',
            tooltip=tooltip
        )
        marker.add_to(popups)
        i+=1


    plugins.TimestampedGeoJson(
        {
            "type": "FeatureCollection",
            "features":
                features+features2+features3+features6+features4+features5

            ,
        },
        period="PT1S",
        duration='PT0S',
        add_last_point=False, #False kalacak !
        time_slider_drag_update=False,
        transition_time=400,
        min_speed=1,
        max_speed=4,
        auto_play=False,
        #loop_button=False,
    ).add_to(map_)


    map_.add_child(MeasureControl())
    MousePosition().add_to(map_)

    minimap = MiniMap()
    map_.add_child(minimap)

    folium.TileLayer(
        tiles="http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="google",
        name="google satellite(nameless)",
        max_zoom=20,
        subdomains=["mt0", "mt1", "mt2", "mt3"],
        overlay=False,
        control=True,
    ).add_to(map_)

    folium.TileLayer(
        tiles="http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        attr="google",
        name="google street view",
        max_zoom=20,
        subdomains=["mt0", "mt1", "mt2", "mt3"],
        overlay=False,
        control=True,
    ).add_to(map_)

    folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        attr="google",
        name="google satellite",
        max_zoom=20,
        subdomains=["mt0", "mt1", "mt2", "mt3"],
        overlay=True,
        control=True,
    ).add_to(map_)

    folium.TileLayer(
        tiles="http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
        attr="googleTerrain ",
        name="googleTerrain ",
        max_zoom=20,
        subdomains=["mt0", "mt1", "mt2", "mt3"],
        overlay=False,
        control=True,
    ).add_to(map_)

    folium.raster_layers.WmsTileLayer(
        url="http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi",
        name="weather_demo",
        fmt="image/png",
        layers="nexrad-n0r-900913",
        attr=u"Weather data © 2012 IEM Nexrad",
        transparent=True,
        overlay=False,
        control=True,

    ).add_to(map_)

    folium.raster_layers.WmsTileLayer(
        url="https://cdn-webgl.eegeo.com/eegeojs/api/v0.1.780/eegeo.js",
        name="kılhıluholıj",
        fmt="image/png",
        layers="nexrad-n0r-900913",
        attr=u"Weather data © 2012 IEM Nexrad",
        transparent=True,
        overlay=False,
        control=True,

    ).add_to(map_)


    file_path = "res/check_is_day.txt"

    # instantiating the enchant dictionary
    # with request_pwl_dict()
    pwl = enchant.request_pwl_dict(file_path)
    print("enchant", pwl, type(pwl))
    ALLOWED_LIST = string.ascii_uppercase + string.digits
    print("list_ne", ALLOWED_LIST[5],type(ALLOWED_LIST))

    folium.LayerControl().add_to(map_)

    draw = Draw()

    draw.add_to(map_)



    map_.save('map.html')
    #web.load(QUrl(str(pathlib.Path().resolve().as_uri()) + '/map.html'))
    #web.show()
    env.map_ready=True

    env.label_information.configure(text="KML file is created")

    print(threading.active_count())



def calculate_location(degree_lat, minute_lat, second_lat, direction_lat,
                       degree_lon, minute_lon, second_lon, direction_lon):
    lon = []
    lat = []
    for degree_lat, minute_lat, second_lat, direction_lat, degree_lon, minute_lon, second_lon, direction_lon in zip(
            degree_lat, minute_lat, second_lat, direction_lat,
            degree_lon, minute_lon, second_lon, direction_lon):
        latitude = str(degree_lat) + "-" + str(minute_lat) + "-" + str(second_lat) + direction_lat
        N = 'N' in latitude
        d, m, s = map(float, latitude[:-1].split('-'))
        latitude = (d + m / 60. + s / 3600.) * (1 if N else -1)
        longitude = str(degree_lon) + "-" + str(minute_lon) + "-" + str(second_lon) + direction_lon
        W = 'W' in longitude
        d, m, s = map(float, longitude[:-1].split('-'))
        longitude = (d + m / 60. + s / 3600.) * (-1 if W else 1)
        lon.append(longitude)
        lat.append(latitude)
    return lon, lat

def style_function(feature):
    return {
        'fillColor': '#ffaf00',
        'color': 'grey',
        'weight': 1.5,
        'dashArray': '5, 5'
    }
def highlight_function(feature):
    return {
        'fillColor': '#ffaf00',
        'color': 'black',
        'weight': 3,
        'dashArray': '5, 5'
    }