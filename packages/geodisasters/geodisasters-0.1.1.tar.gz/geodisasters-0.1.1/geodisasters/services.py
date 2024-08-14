# author: Jan Tschada
# SPDX-License-Identifer: Apache-2.0

from datetime import date, datetime, timedelta, timezone
from georapid.client import GeoRapidClient
from georapid.formats import OutFormat
import requests



def query(client: GeoRapidClient, from_date: date, to_date: date, format: OutFormat = OutFormat.GEOJSON):
    """
    Returns the most common locations related to natural disasters using a specific date range.
    The maximum date range is between 2023-05-24 and yesterday.

    :param client: The client instance to use for this query.
    :param from_date: The start value for the date range. Must not smaller than 2023-05-24
    :param to_date: The end value for the date range. Must not be greater than yesterday.
    :param format: Defines the output format.

    :return: The most common locations as geospatial point features using the specified output format.
    """

    if None is from_date:
        raise ValueError(f'You must specify the from_date!')

    if from_date < date(2023, 5, 24):
        raise ValueError(f'Invalid from_date! {from_date} is smaller than 2023-05-24.')
    
    if None is to_date:
        raise ValueError(f'You must specify the to_date!')

    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)
    if yesterday < to_date:
        raise ValueError(f'Invalid to_date! {to_date} is larger than yesterday.')

    endpoint = '{0}/query'.format(client.url)
    params = {
        'from': from_date.isoformat(),
        'to': to_date.isoformat(),
        'format': str(format)
    }
    response = requests.request('GET', endpoint, headers=client.auth_headers, params=params)
    response.raise_for_status()

    return response.json()

def hotspots(client: GeoRapidClient, seen_date: date = None, format: OutFormat = OutFormat.GEOJSON):
    """
    Returns the hotspot locations related to natural disasters.

    The date is optional. When not specified, we return the features from yesterday.
    The underlying knowledge graph collects locations since 2023-05-24 and yesterday should be the latest available date.
    The format can be geojson or esri.

    :param client: The client instance to use for this query.
    :param seen_date: The value for the date of interest. Must be in the range of [2023-05-24, yesterday].
    :param format: Defines the output format.

    :return: The hotspot locations as geospatial point features using the specified output format.
    """

    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)

    if None is seen_date:
        seen_date = yesterday

    if seen_date < date(2023, 5, 24):
        raise ValueError(f'Invalid seen_date! {seen_date} is smaller than 2023-05-24.')

    if yesterday < seen_date:
        raise ValueError(f'Invalid seen_date! {seen_date} is larger than yesterday.')
    
    endpoint = '{0}/hotspots'.format(client.url)
    params = {
        'date': seen_date.isoformat(),
        'format': str(format)
    }
    response = requests.request('GET', endpoint, headers=client.auth_headers, params=params)
    response.raise_for_status()

    return response.json()

def aggregate(client: GeoRapidClient, seen_date: date = None, format: OutFormat = OutFormat.GEOJSON):
    """
    Aggregates the broadcasted news related to natural disasters using a spatial grid and returns the features as hexagonal bins.

    The date is optional. When not specified, we return the features from yesterday.
    The underlying knowledge graph contains locations since 2023-05-24 and yesterday should be the latest available date.
    The format can be geojson or esri.

    :param client: The client instance to use for this query.
    :param seen_date: The value for the date of interest. Must be in the range of [2023-05-24, yesterday].
    :param format: Defines the output format.

    :return: The aggregated geospatial hexagonal bins using the specified output format.
    """

    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)

    if None is seen_date:
        seen_date = yesterday

    if seen_date < date(2023, 5, 24):
        raise ValueError(f'Invalid seen_date! {seen_date} is smaller than 2023-05-24.')

    if yesterday < seen_date:
        raise ValueError(f'Invalid seen_date! {seen_date} is larger than yesterday.')
    
    endpoint = '{0}/aggregate'.format(client.url)
    params = {
        'date': seen_date.isoformat(),
        'format': str(format)
    }
    response = requests.request('GET', endpoint, headers=client.auth_headers, params=params)
    response.raise_for_status()

    return response.json()