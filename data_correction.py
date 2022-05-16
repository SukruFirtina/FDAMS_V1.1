import math

import numpy as np
import pandas as pd
import enchant
from itertools import chain
import environment as env
from scipy.signal import savgol_filter
import geopy.distance


def fix_strings(row):
    my_dict = enchant.PyPWL("res/words.txt")
    row = row.values.tolist()
    print("before strings\n", row)
    length_of_arr = len(row)

    # **************************************************************
    #   Yanlış değer gelme ihtimalinden dolayı düzenleme yapılacak
    # **************************************************************
    for i in range(length_of_arr):
        word_exists = my_dict.check(row[i])
        if not word_exists:
            if i != 0 and i != length_of_arr - 1:
                if row[i + 1] == row[i - 1]:
                    row[i] = row[i + 1]
                else:
                    row[i] = row[i - 1]

            elif i == 0:
                row[i] = row[i + 1]

            else:
                row[i] = row[i - 1]

        else:
            row[i] = my_dict.suggest(row[i])[0]
    print("after strings\n", row)
    return row


def fix_day(row):
    my_dict = enchant.PyPWL("res/check_is_day.txt")
    row = row.values.tolist()
    print("before strings\n", row)
    length_of_arr = len(row)

    for i in range(length_of_arr):
        word_exists = my_dict.check(row[i])
        if i < 3 and i != length_of_arr - 1:
            if row[i - 1] == row[i - 2]:
                row[i] = row[i - 1]
            else:
                row[i] = row[i - 1]

        elif i != 0 and i != length_of_arr - 1:
            if row[i + 1] == row[i - 1]:
                row[i] = row[i + 1]
            else:
                row[i] = row[i - 1]


        elif word_exists:
            row[i] = my_dict.suggest(row[i])[0]

    print("after strings\n", row)
    return row


def fix_lon_degree(row):
    my_dict = enchant.PyPWL("res/check_is_lon_degree.txt")
    row = row.values.tolist()
    print("before strings\n", row)
    length_of_arr = len(row)

    for i in range(length_of_arr):

        if i != 0 and i != length_of_arr - 1:
            if row[i + 1] == row[i - 1]:
                row[i] = row[i + 1]
            else:
                row[i] = my_dict.suggest(str(row[i]))[0]

        if i > 1 and i < length_of_arr - 2:
            if row[i + 2] == row[i - 2]:
                row[i] = row[i + 2]
            else:
                row[i] = my_dict.suggest(str(row[i]))[0]

        if i > 2 and i + 3 < length_of_arr:
            if row[i + 3] == row[i - 3]:
                row[i] = row[i + 3]
            else:
                row[i] = my_dict.suggest(str(row[i]))[0]

    print("after strings\n", row)
    return row


def fix_lat_degree(row):
    my_dict = enchant.PyPWL("res/check_is_lat_degree.txt")
    row = row.values.tolist()
    print("before strings\n", row)
    length_of_arr = len(row)

    for i in range(length_of_arr):

        # **************************************************************
        #   Burası ifler yerine while ile yazılacak
        # **************************************************************

        if i != 0 and i != length_of_arr - 1:
            if row[i + 1] == row[i - 1]:
                row[i] = row[i + 1]
            else:
                row[i] = my_dict.suggest(str(row[i]))[0]

        if i > 1 and i < length_of_arr - 2:
            if row[i + 2] == row[i - 2]:
                row[i] = row[i + 2]
            else:
                row[i] = my_dict.suggest(str(row[i]))[0]

        if i > 2 and i + 3 < length_of_arr:
            if row[i + 3] == row[i - 3]:
                row[i] = row[i + 3]
            else:
                row[i] = my_dict.suggest(str(row[i]))[0]

    print("after strings\n", row)
    return row


def fix_min_sec(row):
    my_dict = enchant.PyPWL("res/is_min_sec.txt")
    row = row.values.tolist()
    print("before strings\n", row)
    length_of_arr = len(row)

    for i in range(length_of_arr):

        # **************************************************************
        #   Burası ifler yerine while ile yazılacak
        # **************************************************************

        if i > 0 and i != length_of_arr - 1:
            if row[i + 1] == row[i - 1]:
                row[i] = row[i + 1]
            else:
                row[i] = my_dict.suggest(str(row[i]))[0]

        if i > 1 and i < length_of_arr - 2:
            if row[i + 2] == row[i - 2]:
                row[i] = row[i + 2]
            else:
                row[i] = my_dict.suggest(str(row[i]))[0]

        if i > 2 and i < length_of_arr - 3:
            if row[i + 3] == row[i - 3]:
                row[i] = row[i + 3]
            else:
                row[i] = my_dict.suggest(str(row[i]))[0]

    print("after strings\n", row)
    return row


def fix_int(row):
    my_dict = enchant.PyPWL("res/min.txt")
    row = row.values.tolist()
    length_of_arr = len(row)

    for i in range(length_of_arr):
        word_exists = my_dict.check(row[i])
        if not word_exists:
            if i != 0 and i != length_of_arr - 1:
                if row[i + 1] == row[i - 1]:
                    row[i] = row[i + 1]
                elif i >= 2 and row[i - 1] == row[i - 2]:
                    row[i] = row[i - 1]
                else:
                    row[i] = my_dict.suggest(row[i])[0]

            elif i == 0:
                row[i] = my_dict.suggest(row[i])[0]

            elif i == length_of_arr - 1:
                row[i] = my_dict.suggest(row[i])[0]

    return row


# def fix_anomalies(row, change_sensitivity):
#    arr = pd.to_numeric(row.array, errors='coerce')
#    print(arr)
#
#    length_of_arr = len(arr)
#
#    elements = np.array(arr)
#    mean = np.nanmean(elements, axis=0)
#    sd = np.nanstd(elements, axis=0)
#    print(mean, sd)
#    print(mean - change_sensitivity * sd)
#    print(mean + change_sensitivity * sd)
#    arr[np.isnan(arr)] = 50
#
#    for i in range(length_of_arr):
#
#        if not (mean + change_sensitivity * sd) >= arr[i] >= (mean - change_sensitivity * sd):
#
#            if i != 0 and i != length_of_arr - 1:
#                if not (mean + change_sensitivity * sd) >= arr[i + 1] >= (mean - change_sensitivity * sd):
#                    arr[i + 1] = mean
#
#                if arr[i + 1] == arr[i - 1]:
#                    arr[i] = arr[i + 1]
#
#                elif i >= 2 > abs(arr[i - 1] - arr[i - 2]):
#                    arr[i] = (arr[i - 1] + arr[i - 2]) / 2
#                else:
#                    arr[i] = (arr[i + 1] + arr[i - 1]) / 2
#
#            elif i == 0:
#                if not i+1 == length_of_arr:
#                    if not (mean + change_sensitivity * sd) >= arr[i + 1] >= (mean - change_sensitivity * sd):
#                        arr[i + 1] = mean
#                        arr[i] = arr[i + 1]
#                else:
#                    arr[i] = mean
#            elif i == length_of_arr - 1:
#                arr[i] = arr[i - 1]
#
#    arr[np.isnan(arr)] = 50
#    arr = arr.astype(pd.Float64Dtype)
#    # arr = arr.astype(int)
#
#    print(arr)
#    return arr

# def fix_anomalies(row, change_sensitivity):
#    arr = pd.to_numeric(row.array, errors='coerce')
#    print(arr)
#
#    length_of_arr = len(arr)
#
#    elements = np.array(arr)
#    mean = np.nanmean(elements, axis=0)
#    sd = np.nanstd(elements, axis=0)
#    print(mean, sd)
#    print(mean - change_sensitivity * sd)
#    print(mean + change_sensitivity * sd)
#    arr[np.isnan(arr)] = -99999
#
#    for i in range(length_of_arr):
#
#        if not (mean + change_sensitivity * sd) >= arr[i] >= (mean - change_sensitivity * sd):
#
#            if i != 0 and i != length_of_arr - 1:
#                if (mean + change_sensitivity * sd) >= arr[i + 1] >= (mean - change_sensitivity * sd):
#                    if arr[i + 1] == arr[i - 1]:
#                        arr[i] = arr[i + 1]
#                    else:
#                        arr[i] = mean
#                elif not (mean + change_sensitivity * sd) >= arr[i + 1] >= (mean - change_sensitivity * sd):
#                    arr[i] = mean
#                    arr[i + 1] = mean
#
#
#                elif i >= 2 > abs(arr[i - 1] - arr[i - 2]):
#                    arr[i] = (arr[i - 1] + arr[i - 2]) / 2
#                else:
#                    arr[i] = (arr[i + 1] + arr[i - 1]) / 2
#
#            elif i == 0:
#                if not i + 1 == length_of_arr:
#                    if not (mean + change_sensitivity * sd) >= arr[i + 1] >= (mean - change_sensitivity * sd):
#                        arr[i + 1] = mean
#                    arr[i] = arr[i + 1]
#            elif i == length_of_arr - 1:
#                arr[i] = arr[i - 1]
#
#    arr[np.isnan(arr)] = 50  ################################ Düzeltilecek!!!!!!!!!
#    arr = arr.astype(pd.Float64Dtype)
#    # arr = arr.astype(int)
#
#    print(arr)
#    return arr

def fix_anomalies(row, change_sensitivity):
    # **************************************************************
    #   Test edilip düzeltilecek !!!!!
    # **************************************************************
    arr = pd.to_numeric(row.array, errors='coerce')
    print(arr)

    length_of_arr = len(arr)

    elements = np.array(arr)
    mean = np.nanmean(elements, axis=0)
    sd = np.nanstd(elements, axis=0)
    print(mean, sd)
    print(mean - change_sensitivity * sd)
    print(mean + change_sensitivity * sd)
    arr[np.isnan(arr)] = 99999

    for i in range(length_of_arr):


        if not (mean + change_sensitivity * sd) >= arr[i] >= (mean - change_sensitivity * sd):

            if i != 0 and i != length_of_arr - 1:
                if not (mean + change_sensitivity * sd) >= arr[i + 1] >= (mean - change_sensitivity * sd):
                    arr[i + 1] = mean

                if arr[i + 1] == arr[i - 1]:
                    arr[i] = arr[i + 1]
                elif i >= 2 > abs(arr[i - 1] - arr[i - 2]):
                    arr[i] = (arr[i - 1] + arr[i - 2]) / 2
                else:
                    arr[i] = (arr[i + 1] + arr[i - 1]) / 2

            elif i == 0 and i != length_of_arr - 1:
                if not (mean + change_sensitivity * sd) >= arr[i + 1] >= (mean - change_sensitivity * sd):
                    arr[i + 1] = mean
                arr[i] = arr[i + 1]
            elif i == length_of_arr - 1:
                arr[i] = arr[i - 1]
    arr[np.isnan(arr)] = 50  ################################ Düzeltilecek!!!!!!!!!
    arr = arr.astype(pd.Float64Dtype)
    # arr = arr.astype(int)

    print(arr)
    return arr


def sender_fix_anomalies(data_list, num_by_num, sensitivity):
    final_list = []
    print("ilk", data_list.tolist(), type(data_list.tolist()))
    for i in range(0, len(data_list), num_by_num):
        group_list = (map(str, data_list[i:i + num_by_num]))
        send = pd.Series(group_list)
        result = fix_anomalies(send, sensitivity)
        final_list.append(result)

    final_list = list(chain.from_iterable(final_list))
    final_list = pd.to_numeric(final_list, errors='coerce')
    print("son", final_list, type(final_list))
    return final_list


def fix_time_digit(i):
    list = []
    for i_ in i:
        if i_ < 10:
            list.append('0' + str(i_))
        else:
            list.append(str(i_))

    return list


def monthToNum(monthlist):
    for i in range(len(monthlist)):
        monthlist[i] = {
            'JAN': 1,
            'FEB': 2,
            'MAR': 3,
            'APR': 4,
            'MAY': 5,
            'JUN': 6,
            'JUL': 7,
            'AUG': 8,
            'SEP': 9,
            'OCT': 10,
            'NOV': 11,
            'DEC': 12
        }[monthlist[i]]
    return monthlist


def fix_time(hour, minute, second):
    hour = pd.to_numeric(hour.array, errors='coerce').astype(float)
    minute = pd.to_numeric(minute.array, errors='coerce').astype(float)
    second = pd.to_numeric(second.array, errors='coerce').astype(float)
    print("Time GIRENLER", hour, minute, second)
    second_difference = 1 / env.fps_variable.get()
    time = 3600 * hour + 60 * minute + second
    print("TOPLAM Time GIRENLER", time)

    # **************************************************************
    #   ilk değerin yanlış olma ihtimaline karşı, düzeltme yapılacak
    # **************************************************************

    for i in range(len(time) - 1):
        if abs(time[i + 1] - time[i]) > 1:
            time[i + 1] = time[i] + second_difference
        hour[i + 1] = time[i + 1] / 3600
        minute[i + 1] = (time[i + 1] % 3600) / 60
        second[i + 1] = (time[i + 1] % 3600) % 60

    print("Time CIKANLAR", hour, minute, second)
    return hour, minute, second


#def distances(lon, lat):
#    distances = []
#    for i in range(len(lon) - 1):
#        distances[i] = geopy.distance.geodesic((lat[i], lon[i]), (lat[i + 1], lon[i + 1])).km
#
#    return distances


def fix_by_distances(lon, lat):

    for i in range(0, len(lon)-1):
        if geopy.distance.geodesic((lat[i], lon[i]), (lat[i + 1], lon[i + 1])).km > 1/env.fps_variable.get():
            lon[i+1] = lon[i]
            lat[i+1] = lat[i]

    return lon, lat




def check_arms(lon, lat, num_by_num, tolerance):
    distances = []

    for i in range(len(lon) - 1):
        distances.append(geopy.distance.geodesic((lat[i], lon[i]), (lat[i + 1], lon[i + 1])).km)
    print("DISTANCES.", distances)

    group_list = distances

    print("group list.", group_list)
    group_list = group_list * 1000
    mean = np.nanmean(list(group_list), axis=0)
    sd = np.nanstd(list(group_list), axis=0)
    lon_mean = np.nanmean(lon, axis=0)
    lat_mean = np.nanmean(lat, axis=0)
    print(mean, sd)
    print(mean - tolerance * sd)
    print(mean + tolerance * sd)

    for i in range(0, len(group_list)):
        print("asdfghjkl iiii", i)
        if group_list[i + 1] - group_list[i + 1] > 20:
            k = 1
            # if not i == len(group_list)-1:
            #    if not (mean + tolerance * sd) >= group_list[i + 1] >= (mean - tolerance * sd):
            #        while not (i+k) >= len(group_list):
            #            if k == 10:
            #                lon[i] = lon_mean
            #                lat[i] = lat_mean
            #                break
            #            k += 1
            # else:
            now = i + 1
            print("SDIUGHSDFIUHGIUFDHGIUSDH", lon, "\n", lon[now])
            lon[now] = (lon[now + 1] + lon[now - 1]) / 2
            print("SONRA", lon, "\n", lon[now])
            lat[now] = (lat[now + 1] + lat[now - 1]) / 2
            print("SONRA LAT", lon, "\n", lat[now])

    # for i in range(len(lon) - 1):
    #    distances.append(round(geopy.distance.geodesic((lat[i], lon[i]), (lat[i + 1], lon[i + 1])).km, 6))

    return lon, lat, distances


# def fix_locations(locations_df):
#    locations = pd.to_numeric(locations_df.array, errors='coerce')
#
#    print("LOCATIONS GIRENLER", locations )
#
#
#    for i in range(len(time) - 1):
#        if abs(time[i + 1] - time[i]) > 2*second_difference :
#            time[i + 1] = time[i] + second_difference
#        hour[i + 1] = time[i + 1] / 3600
#        minute[i + 1] = (time[i + 1] % 3600) / 60
#        second[i + 1] = (time[i + 1] % 3600) % 60
#
#    print("Time CIKANLAR", hour, minute, second)
#    return hour, minute, second

def between(min, max, list):
    list = pd.to_numeric(list, errors='coerce')
    list.tolist()
    # list = np.array(list, dtype=np.int)
    # list = pd.Series(list)

    print(list)
    fixed = False
    for i in range(len(list)):
        l = 1
        r = 1
        if not min <= list[i] <= max:
            # statistics.mode([list[i],list[i],list[i],list[i],list[i],list[i],list[i],list[i]])
            for j in range(7):
                print("1")
                if i - l == -1:
                    l += 6
                if i + r == len(list):
                    r -= 6
                if list[i - l] == list[i + r]:
                    list[i] = list[i + r]
                    break

        r = 1
        if not (i + 1) == len(list):
            if abs(list[i] - list[i + 1]) > 1:
                for j in range(7):
                    print("2")
                    if i - l == -1:
                        l += 6
                    if i + r == len(list):
                        r -= 6
                    if list[i - l] == list[i + r]:
                        list[i] = list[i + r]
                        fixed = True
                        break
                    if not fixed:
                        list[i] = 50
                        # for j in range (7):
                #    print("3")
                #    if i-l == -1:
                #        l+=6
                #    if i+r == len(list):
                #        r-=6
                #    if list[i-l]==list[i+r]:
                #        list[i]=list[i+r]
                #        break

    return list


# def fix_df(df):
#    # df['minute_lat'] = fix_int(df['minute_lat'])
#    # df['second_lat'] = fix_int(df['second_lat'])
#    # df['minute_lon'] = fix_int(df['minute_lon'])
#    # df['second_lon'] = fix_int(df['second_lon'])
#
#    df['month'] = monthToNum(fix_strings(df['month']))
#
#    df['direction_lat'] = fix_strings(df['direction_lat'])
#    df['direction_lon'] = fix_strings(df['direction_lon'])
#    df['target_direction_lat'] = fix_strings(df['target_direction_lat'])
#    df['target_direction_lon'] = fix_strings(df['target_direction_lon'])
#    df['year'] = fix_strings(df['year'])
#    df['day'] = fix_day(df['day'])
#
#    df['day'] = np.array((sender_fix_anomalies(df['day'], 10, 0.5)), dtype=np.int)
#    df['hour'] = np.array((sender_fix_anomalies(df['hour'], 10, 1)), dtype=np.int)
#    df['min'] = sender_fix_anomalies(df['min'], 10, 3)
#    df['sec'] = sender_fix_anomalies(df['sec'], 10, 3)
#    df['hour'], df['min'], df['sec'] = fix_time(df['hour'], df['min'], df['sec'])
#    df['hour'] = np.array(df['hour'], dtype=np.int)
#    df['min'] = np.array(df['min'], dtype=np.int)
#    df['sec'] = np.array(df['sec'], dtype=np.int)
#
#    # df['degree_lat'] = between(0, 90, df['degree_lat'])
#    df['degree_lat'] = np.array((sender_fix_anomalies(df['degree_lat'], 10, 1.2)), dtype=np.int)
#    df['degree_lat'] = np.array((sender_fix_anomalies(df['degree_lat'], 20, 1)), dtype=np.int)
#    df = df[df['degree_lat'] < 91]
#
#    df['minute_lat'] = np.array((sender_fix_anomalies(df['minute_lat'], 10, 2.1)), dtype=np.int)
#    df['second_lat'] = np.array((sender_fix_anomalies(df['second_lat'], 10, 3)), dtype=np.int)
#    df['degree_lon'] = np.array((sender_fix_anomalies(df['degree_lon'], 10, 1.2)), dtype=np.int)
#    df['degree_lon'] = np.array((sender_fix_anomalies(df['degree_lon'], 10, 1)), dtype=np.int)
#    df = df[df['degree_lon'] < 181]
#    df['minute_lon'] = np.array((sender_fix_anomalies(df['minute_lon'], 10, 2.1)), dtype=np.int)
#    df['second_lon'] = np.array((sender_fix_anomalies(df['second_lon'], 10, 3)), dtype=np.int)
#
#    # df['target_degree_lat'] = between(0, 90, df['target_degree_lat'])
#    df['target_degree_lat'] = np.array((sender_fix_anomalies(df['target_degree_lat'], 10, 1)), dtype=np.int)
#    df['target_degree_lat'] = np.array((sender_fix_anomalies(df['target_degree_lat'], 20, 1)), dtype=np.int)
#    df = df[df['target_degree_lat'] < 91]
#
#    df['target_minute_lat'] = np.array((sender_fix_anomalies(df['target_minute_lat'], 10, 2)), dtype=np.int)
#    df['target_second_lat'] = np.array((sender_fix_anomalies(df['target_second_lat'], 10, 3)), dtype=np.int)
#
#    df['target_degree_lon'] = np.array((sender_fix_anomalies(df['target_degree_lon'], 10, 1)), dtype=np.int)
#    df = df[df['target_degree_lon'] < 181]
#
#    df['target_minute_lon'] = np.array((sender_fix_anomalies(df['target_minute_lon'], 10, 2.1)), dtype=np.int)
#    df['target_second_lon'] = np.array((sender_fix_anomalies(df['target_second_lon'], 10, 3)), dtype=np.int)
#
#    # **************************************************************
#    #   Daha fazla data için denenmedi. Konum verileri için farklı bir algoritma geliştirilse daha iyi olur.
#    # **************************************************************
#    df['target_degree_lon'] = np.array(np.ceil(savgol_filter(df['target_degree_lon'], 5, 1)), dtype=np.int)
#    df['target_degree_lat'] = np.array(np.ceil(savgol_filter(df['target_degree_lat'], 5, 1)), dtype=np.int)
#    df['degree_lon'] = np.array(np.ceil(savgol_filter(df['target_degree_lon'], 5, 1)), dtype=np.int)
#    df['degree_lat'] = np.array(np.ceil(savgol_filter(df['target_degree_lat'], 5, 1)), dtype=np.int)
#
#    df['target_degree_lon'] = np.array(np.ceil(savgol_filter(df['target_degree_lon'], 5, 1)), dtype=np.int)
#    df['target_degree_lat'] = np.array(np.ceil(savgol_filter(df['target_degree_lat'], 5, 1)), dtype=np.int)
#    df['degree_lon'] = np.array(np.ceil(savgol_filter(df['target_degree_lon'], 5, 1)), dtype=np.int)
#    df['degree_lat'] = np.array(np.ceil(savgol_filter(df['target_degree_lat'], 5, 1)), dtype=np.int)
#
#    df['heading_angle'] = np.array((sender_fix_anomalies(df['heading_angle'], 5, 2)), dtype=np.int)
#
#    return df

def fix_df(df):
    # df['minute_lat'] = fix_int(df['minute_lat'])
    # df['second_lat'] = fix_int(df['second_lat'])
    # df['minute_lon'] = fix_int(df['minute_lon'])
    # df['second_lon'] = fix_int(df['second_lon'])

    df['month'] = monthToNum(fix_strings(df['month']))

    df['direction_lat'] = fix_strings(df['direction_lat'])
    df['direction_lon'] = fix_strings(df['direction_lon'])
    df['target_direction_lat'] = fix_strings(df['target_direction_lat'])
    df['target_direction_lon'] = fix_strings(df['target_direction_lon'])
    df['year'] = fix_strings(df['year'])
    df['day'] = fix_day(df['day'])
    df['degree_lon'] = fix_lon_degree(df['degree_lon'])
    df['degree_lat'] = fix_lat_degree(df['degree_lat'])
    df['target_degree_lon'] = fix_lon_degree(df['target_degree_lon'])
    df['target_degree_lat'] = fix_lat_degree(df['target_degree_lat'])
    df['minute_lat'] = fix_min_sec(df['minute_lat'])
    df['second_lat'] = fix_min_sec(df['second_lat'])
    df['minute_lon'] = fix_min_sec(df['minute_lon'])
    df['second_lon'] = fix_min_sec(df['second_lon'])
    df['target_minute_lat'] = fix_min_sec(df['target_minute_lat'])
    df['target_second_lat'] = fix_min_sec(df['target_second_lat'])
    df['target_minute_lon'] = fix_min_sec(df['target_minute_lon'])
    df['target_second_lon'] = fix_min_sec(df['target_second_lon'])

    df['day'] = np.array((sender_fix_anomalies(df['day'], 10, 0.5)), dtype=np.int)
    df['hour'] = np.array((sender_fix_anomalies(df['hour'], 10, 1)), dtype=np.int)
    df['min'] = sender_fix_anomalies(df['min'], 10, 3)
    df['sec'] = sender_fix_anomalies(df['sec'], 10, 3)
    df['hour'], df['min'], df['sec'] = fix_time(df['hour'], df['min'], df['sec'])
    df['hour'] = np.array(df['hour'], dtype=np.int)
    df['min'] = np.array(df['min'], dtype=np.int)
    df['sec'] = np.array(df['sec'], dtype=np.int)

    # df['degree_lat'] = between(0, 90, df['degree_lat'])
    df['degree_lat'] = np.array((sender_fix_anomalies(df['degree_lat'], 10, 1.2)), dtype=np.int)
    df = df[df['degree_lat'] < 91]

    df['minute_lat'] = np.array((sender_fix_anomalies(df['minute_lat'], 10, 2.1)), dtype=np.int)
    df['second_lat'] = np.array((sender_fix_anomalies(df['second_lat'], 10, 3)), dtype=np.int)
    df['degree_lon'] = np.array((sender_fix_anomalies(df['degree_lon'], 10, 1.2)), dtype=np.int)
    df['minute_lon'] = np.array((sender_fix_anomalies(df['minute_lon'], 10, 2.1)), dtype=np.int)
    df['second_lon'] = np.array((sender_fix_anomalies(df['second_lon'], 10, 3)), dtype=np.int)

    # df['target_degree_lat'] = between(0, 90, df['target_degree_lat'])
    df['target_degree_lat'] = np.array((sender_fix_anomalies(df['target_degree_lat'], 10, 1)), dtype=np.int)

    df['target_minute_lat'] = np.array((sender_fix_anomalies(df['target_minute_lat'], 10, 2)), dtype=np.int)
    df['target_second_lat'] = np.array((sender_fix_anomalies(df['target_second_lat'], 10, 3)), dtype=np.int)
    df['target_degree_lon'] = np.array((sender_fix_anomalies(df['target_degree_lon'], 10, 1)), dtype=np.int)

    df['target_minute_lon'] = np.array((sender_fix_anomalies(df['target_minute_lon'], 10, 2.1)), dtype=np.int)
    df['target_second_lon'] = np.array((sender_fix_anomalies(df['target_second_lon'], 10, 3)), dtype=np.int)

    # **************************************************************
    #   Daha fazla data için denenmedi. Konum verileri için farklı bir algoritma geliştirilse daha iyi olur.
    # **************************************************************
    df['target_degree_lon'] = np.array(np.ceil(savgol_filter(df['target_degree_lon'], 33, 1)), dtype=np.int)
    df['target_degree_lat'] = np.array(np.ceil(savgol_filter(df['target_degree_lat'], 33, 1)), dtype=np.int)

    df['heading_angle'] = np.array((sender_fix_anomalies(df['heading_angle'], 5, 2)), dtype=np.int)

    return df
