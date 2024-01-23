import os
import json
import requests
from typing import List

import numpy as np
import pandas as pd

import psycopg
from sqlalchemy import create_engine

from munpy import config


def readBinary(filename: str, N_streets: int, dtype=np.float32, mode='array'):
    """
    Los outputs/inputs del modelo tienen la distribución (Nt, N_st)
    es decir pasos temporales X número de calles. Los binarios se cargan
    en un array de numpy justo con este formato. Si se desea se devuelven
    como dataframe.

    :param filename: archivo binario para decodificar.
    :param N_streets: número de calles de la simulación.
    :param dtype: tipo de dato guardado.
    :param mode: devolver como np.ndarray o como pd.DataFrame.
    :return: numpy.ndarray | pd.DataFrame
    """
    byte_size = np.dtype(dtype).itemsize
    Nt = int(
        os.stat(filename)[6] / byte_size / N_streets
    )
    length = Nt * N_streets
    data = np.fromfile(filename, dtype, length)
    data.shape = (Nt, N_streets)

    if mode == 'df':
        data = pd.DataFrame(data)

    return data


def dumpBinary(array: np.ndarray, filename: str):
    array.tofile(filename)


def dat_to_db(streets: pd.DataFrame, intersections: pd.DataFrame):
    """
    Converts the content of streets to format of crate database.

    :param streets: DataFrame loaded from 'street.dat'
    :param intersections: DataFrame lodaded from the raw intersections
    file, that only contains an intersectoin id and its coordinates.

    :return: DataFrame with street_id and a LineString of its coordinates.
    """

    ids, coordinates = [], []
    for _, street in streets.iterrows():
        ids.append(int(street['street_id']))
        first_inter = int(street['begin_inter'])
        second_inter = int(street['end_inter'])

        coords_ini = intersections.loc[
            intersections['node_id'] == first_inter, ['lon', 'lat']
        ].to_numpy()[0]

        coords_fin = intersections.loc[
            intersections['node_id'] == second_inter, ['lon', 'lat']
        ].to_numpy()[0]

        coordinates.append([list(coords_ini), list(coords_fin)])

    return pd.DataFrame({'street_id': ids, 'coordinates': coordinates})


def dat_to_street_center(streets: pd.DataFrame, intersections: pd.DataFrame):
    """
    Genera e archivo all_streets.csv, que contiene street_id y centro de las coordenadas
    :param streets: load(street.dat)
    :param intersections: load(raw_intersection.dat))
    :return:
    """

    street_dataframe = dat_to_db(streets, intersections)
    center_lat = [
        np.mean(coords, axis=0)[0]
        for coords in street_dataframe['coordinates']
    ]
    center_lon = [
        np.mean(coords, axis=0)[1]
        for coords in street_dataframe['coordinates']
    ]

    street_dataframe['lat'] = center_lat
    street_dataframe['lon'] = center_lon

    return street_dataframe


def db_to_street_center(streets: pd.DataFrame):
    """
    Añade una columna con el centro de la calle al csv de calles. Exactamente igual que
    dat_to_street_center pero empezando desde el formato database.
    :param streets:
    :return:
    """

    center_lat = [
        np.mean(json.loads(coords), axis=0)[1]
        for coords in streets['coordinates']
    ]
    center_lon = [
        np.mean(json.loads(coords), axis=0)[0]
        for coords in streets['coordinates']
    ]

    streets['center_lat'] = center_lat
    streets['center_lon'] = center_lon

    return streets


def dat_to_geojson(streets: pd.DataFrame, intersections: pd.DataFrame, color=None):
    """
    Genera un geojson de calles a partir del dataframe.
    :param streets:
    :param intersections:
    :param color: color con el que pintar las calles, ej: #ff0000 rojo puro
    :return:
    """

    streets = dat_to_db(streets, intersections)

    features = []
    for _, street in streets.iterrows():
        # GeoJSON lee por defecto las coordenadas en [longitud, latitud]
        coords = street['coordinates']

        feature = {
            "type": "Feature",
            "properties": {
                "id": str(street['street_id'])
            },
            "geometry": {
                "coordinates": coords,
                "type": "LineString"
            }
        }

        if color:
            feature['properties']["stroke"] = color

        features.append(feature)

    geojs = {"type": "FeatureCollection", "features": features}

    return geojs


def get_district_traffic(city, district=None):
    """
        A partir de un Dataframe que contenga identificadores y posición de puntos de medida de tráfico,
        como por ejemplo el que se puede descargar para la ciudad de Madrid en
        'https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=ee941ce6ba6d3410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD'
        Los campos deben llamarse igual que en dicho CSV: id, longitud, latitud.
        :param city: Ciudad con datos de tráfico para procesar.
        :param district: En caso de que exista este campo en el DataFrame, si se especifica el distrito, solo
        se guardarán los puntos de medida correspondientes a ese distrito.
        :return: geoJSON con un punto por cada punto de medición.
        """

    city_dir = os.path.join(config.LEZ_DIR, city)
    traffic_dir = os.path.join(city_dir, 'traffic')
    measure_points = pd.read_csv(
        os.path.join(traffic_dir, 'pmed_ubicacion_09-2023.csv'),
        sep=';', usecols=['id', 'latitud', 'longitud', 'distrito']
    )

    features = []

    if district is not None:
        traffic_points = measure_points.loc[measure_points['distrito'].isin(district)]

    for _, pt in traffic_points.iterrows():
        # GeoJSON lee por defecto las coordenadas en [longitud, latitud]
        latitud, longitud = pt['latitud'], pt['longitud']

        feature = {
            "type": "Feature",
            "properties": {
                "id": str(pt['id'])
            },
            "geometry": {
                "coordinates": [longitud, latitud],
                "type": "Point"
            }
        }

        features.append(feature)

    geojs = {"type": "FeatureCollection", "features": features}

    filename = os.path.join(traffic_dir, f'points_dist_{"_".join([str(d) for d in district])}.geojson')
    with open(filename, 'w') as gj:
        json.dump(geojs, gj, indent=4)

    return geojs


def is_in_list(pair: List, existing_pairs: List) -> bool:
    """ Comprueba si ya existe determinada calle

    Args:
        pair (List): nueva calle
        existing_pairs (List): calles añadidas anteriormente

    Returns:
        bool: True/False si la calle está o no está en la lista.
    """

    pair_rev = pair.copy()
    pair_rev.reverse()

    return (pair in existing_pairs) or (pair_rev in existing_pairs)


def findStreets(intersection_id: int, streets: pd.DataFrame) -> List:
    """ Encuentra qué calles forman la intersección con id "intersection_id".

    Args:
        intersection_id (int): intersección de interés
        streets (pd.DataFrame): dataframe generado con el script "streets.py"

    Returns:
        List: lista con los ids de las calles que forman la intersección.
    """

    streets_as_array = streets[["begin_inter", "end_inter"]].to_numpy()

    # Encontrar todas las calles en las que aparece "intersection_id"
    positions = np.where(np.any(intersection_id == streets_as_array, axis=1))[0]
    streets_with_intersection = streets.loc[positions]
    street_ids = streets_with_intersection["street_id"].to_numpy().ravel()
    return list(street_ids)


def haversine_distance(coords_1, coords_2, r=6371.0, mode='grad'):
    """
    Calcula la distancia entre 2 puntos con coordenadas (lat_i, lon_i) expresada
    en grados.

    :param coords_1:
    :param coords_2:
    :param r:
    :param mode: 'grad' --> las coordenadas están expresadas en grados.
    'rad' --> las coordenadas están expresadas en radianes
    :return: distancia en metros
    """

    """
    coords_shape = coords_1.shape
    if len(coords_shape) == 2:
        lat1, lon1 = coords_1[:, 0], coords_1[:, 1]
        lat2, lon2 = coords_2[:, 0], coords_2[:, 1]
    else:
        lat1, lon1 = coords_1
        lat2, lon2 = coords_2
    """

    lat1, lon1 = coords_1
    lat2, lon2 = coords_2

    # Convert latitudes and longitudes to radians
    if mode == 'grad':
        lat1 = lat1 * np.pi/180
        lon1 = lon1 * np.pi/180
        lat2 = lat2 * np.pi/180
        lon2 = lon2 * np.pi/180

    # Calculate differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Apply haversine formula
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    # Calculate distance
    distance = r * c
    return distance * 1000


def generalized_normal(x, mu=0, sigma=1, beta=2):
    """
    Generalized normal distribution. With the default parameters, it is exactly equal
    to a normal distribution. Vary parameter 'beta' to obtain different shapes. For
    example:
        - beta = 1 --> Laplace distribution
        - beta = infinity --> uniform distribution

    :param x: number or array. The interval where the distribution is defined.
    :param mu: center of the distribution
    :param sigma: spreadness of the distribution
    :param beta: defines the shape of the distribution
    :return: number or array like.
    """

    # normalizer = beta / ( 2 * sigma * gamma(1 / beta))
    return np.exp(- (np.abs(x - mu) / sigma) ** beta)  # * normalizer


def get_nc_index(lez_latitude, lez_longitude, ncdataset, mode='chimere'):
    """
    Obtiene el índice de interés del Dataset NETCDF a partir de una latitud
    y una longitud.

    :param lez_latitude:
    :param lez_longitude:
    :param ncdataset:
    :param mode: ['chimere', 'copernicus']. Si se usa en modo 'chimere', los nombres
    de latitud y longitud son 'XLAT', 'XLONG'. No obstante, en modo 'copernicus', los
    nombres son 'latitude' y 'longitude'.
    :return:
    """

    if mode == 'wrf':
        lat_name, lon_name = config.LATITUDE, config.LONGITUDE
        nc_latitude, nc_longitude = (ncdataset.variables[lat_name][0, :, :],
                                     ncdataset.variables[lon_name][0, :, :])

        N_lats, N_lons = nc_latitude.shape[-2:]
        i_min_distance = j_min_distance = 0
        min_distance = haversine_distance(
            [lez_latitude, lez_longitude],
            [nc_latitude[0, 0], nc_longitude[0, 0]]
        )

        for i in range(N_lats):
            for j in range(N_lons):
                dist = haversine_distance(
                    [lez_latitude, lez_longitude],
                    [nc_latitude[i, j], nc_longitude[i, j]]
                )

                if dist < min_distance:
                    min_distance = dist
                    i_min_distance = i
                    j_min_distance = j

    elif mode == 'chimere':
        lat_name, lon_name = 'lat', 'lon'
        nc_latitude, nc_longitude = (ncdataset.variables[lat_name][:, :],
                                     ncdataset.variables[lon_name][:, :])

        N_lats, N_lons = nc_latitude.shape[-2:]
        i_min_distance = j_min_distance = 0
        min_distance = haversine_distance(
            [lez_latitude, lez_longitude],
            [nc_latitude[0, 0], nc_longitude[0, 0]]
        )

        for i in range(N_lats):
            for j in range(N_lons):
                dist = haversine_distance(
                    [lez_latitude, lez_longitude],
                    [nc_latitude[i, j], nc_longitude[i, j]]
                )

                if dist < min_distance:
                    min_distance = dist
                    i_min_distance = i
                    j_min_distance = j

    else:
        lat_name, lon_name = 'latitude', 'longitude'
        nc_latitude, nc_longitude = (ncdataset.variables[lat_name][:],
                                     ncdataset.variables[lon_name][:])

        N_lats, N_lons = len(nc_latitude), len(nc_longitude)
        i_min_distance = j_min_distance = 0
        min_distance = haversine_distance(
            [lez_latitude, lez_longitude],
            [nc_latitude[0], nc_longitude[0]]
        )

        for i in range(N_lats):
            for j in range(N_lons):
                dist = haversine_distance(
                    [lez_latitude, lez_longitude],
                    [nc_latitude[i], nc_longitude[i]]
                )

                if dist < min_distance:
                    min_distance = dist
                    i_min_distance = i
                    j_min_distance = j

    # WARNINGS
    if not np.min(nc_latitude) < lez_latitude < np.max(nc_latitude):
        print(f'WARGING: LEZ latitude out of WRF simulation domain:')
        print(f'{np.min(nc_latitude)} ?< {lez_latitude} ?< {np.max(nc_latitude)}')

    if not np.min(nc_longitude) < lez_longitude < np.max(nc_longitude):
        print(f'WARGING: LEZ longitude out of WRF simulation domain:')
        print(f'{np.min(nc_longitude)} ?< {lez_longitude} ?< {np.max(nc_longitude)}')

    if min_distance >= 2e4:
        print(f'WARNING: Retrieving meteorological data from too far ({min_distance / 1000} km)')

    return i_min_distance, j_min_distance, min_distance


def reshape(parameter: np.ndarray, N_times=None, N_streets=None, mode='street'):
    """
    Reformatea una variable a la forma requerida por
    Munich. N_streets --> número de calles / intersecciones (en caso correspondiente).

    :param parameter: array con los valores conocidos
    :param N_times: Si mode='street' se extrae de parameter.shape, si mode='time', debe
    darse como parámetro de la función.
    :param N_streets: Si mode='street' debe darse como parámetro de la función si mode='time',
    se extrae de parameter.shape.
    :param mode: 'street' o 'time'. Si es 'street': Se rellenan las columnas de forma que
    los valores cambian en cada timestep, pero todas las columnas se mantienen iguales. Si
    es 'time', se rellenan las filas haciendo que sean las calles las que varían, y todos los
    timesteps tienen el mismo valor.
    :return:
    """

    if mode == 'street':
        N_times = parameter.shape[0]
        reshaped_par = np.zeros((N_times, N_streets))
        for time_step in range(N_times):
            reshaped_par[time_step, :] = parameter[time_step]

    elif mode == 'time':
        N_streets = parameter.shape[0]
        reshaped_par = np.zeros((N_times, N_streets))
        for time_step in range(N_times):
            reshaped_par[time_step, :] = parameter

    return reshaped_par.astype(np.float32)


def sql_connection(host, database, user, password, port):
    """

    :param host:
    :param database:
    :param user:
    :param password:
    :param port:
    :return:
    """

    db_url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(db_url)
    return engine


def connect(url, db, user, password, port):
    params_dic = {
        "host": url,
        "dbname": db,
        "user": user,
        "password": password,
        "port": port,
    }

    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg.connect(**params_dic)
    except (Exception, psycopg.DatabaseError) as error:
        print(error)
        exit(1)
    return conn


def dataframe_to_postgresql(conn, insert_query):
    cursor = conn.cursor()
    try:
        cursor.execute(insert_query)
        conn.commit()
    except (Exception, psycopg.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    cursor.close()


def postgresql_to_dataframe(conn, select_query):
    """
    Function to download a dataframe from a query

    :param conn: the connection object (connect method)
    :param select_query: the query
    :type select_query: str
    :return: DataFrame obtained from the query
    :rtype: pandas.DataFrame
    """

    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return None

    # Naturally we get a list of tuples
    tuples = cursor.fetchall()

    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tuples, columns=[e.name for e in cursor.description])
    cursor.close()

    return df


def descargar_eea(dir, stations, gases, contaminant_codes, year, time_coverage='Last7days'):
    """
    Función para descargarte los datos de la EEA para un año en concreto a partir de los códigos de las estaciones,
    los contaminantes y el código de los contaminantes. Las descargas se colocarán dentro del directorio especificado.

    :param dir: nombre del directorio donde se guardarán las descargas
    :type dir: str
    :param stations: lista con los códigos de las estaciones de las que se quiere descargar los datos
    :type stations: list
    :param gases: lista con los nombres de los contaminantes que se quieren descargar
    :type gases: list
    :param contaminant_codes: lista con los códigos de los contaminantes, en el mismo orden
    :type contaminant_codes: list
    :param year: año para el que se quieren descargar los datos
    :param time_coverage: descargar un año entero: 'Year'. Descargar últimos 7 días: 'Last7days'.
    :type time_coverage: string
    :type year: int
    """

    # Vamos estación por estación
    for s in stations:
        station_dir = os.path.join(dir, s)
        # Creamos dentro del directorio de las descargas un subdirectorio para cada una de las estaciones
        if not os.path.exists(station_dir):
            os.makedirs(station_dir)

        # Ahora vamos contaminante por contaminante
        for gas, code in zip(gases, contaminant_codes):
            # El nombre del fichero descargado será {estacion}_{contaminante}.csv
            fileName = os.path.join(station_dir, gas+'.csv')

            # Ahora formamos la URL y descargamos
            url_request = (f"https://fme.discomap.eea.europa.eu/fmedatastreaming/AirQualityDownload/AQData_Extract.fmw"
                           f"?CountryCode=&CityName=&Pollutant={code}&Year_from={year}&Year_to={year}"
                           f"&Station=&Samplingpoint=&Source=All&Output=HTML&UpdateDate=&TimeCoverage="
                           f"{time_coverage}&EoICode={s}")
            print(f"Downloading historical data: {url_request}")
            uri = requests.get(url_request).content

            if len(uri) > 0:
                file = requests.get(
                    f"https://{str(uri).split('https://')[1].split('.csv')[0]}.csv"
                ).content

                with open(fileName, 'wb') as f:
                    f.write(file)

                print("Saved as: %s " % fileName)
                print("-----")

    print("Download finished")


def bulk_load_streets(
    street_coordinates: pd.DataFrame, city, db_url,
    db_name, db_user, db_password, db_port
):
    """

    :param street_coordinates:
    :param city:
    :param db_url:
    :param db_name:
    :param db_port:
    :param db_user:
    :param db_password:
    :return:
    """

    engine = sql_connection(db_url, db_name, db_user, db_password, port=db_port)
    name = config.STREET_COORDINATES_TABLE
    street_coordinates.to_sql(name, engine, schema=city, if_exists='replace', index=False)


if __name__ == '__main__':
    valencia = 'valencia'
    city_dir = os.path.join(config.LEZ_DIR, valencia)
    domain_dir = os.path.join(city_dir, 'domain')
    results_dir = os.path.join(city_dir, 'results/2024-01-10')

    # Get N_streets
    street_df = pd.read_csv(os.path.join(domain_dir, 'street.csv'))
    N_streets = len(street_df)

    # Load result
    no2_file = os.path.join(results_dir, 'NO2.bin')
    no2 = readBinary(no2_file, N_streets=N_streets)
    print(no2.shape)
