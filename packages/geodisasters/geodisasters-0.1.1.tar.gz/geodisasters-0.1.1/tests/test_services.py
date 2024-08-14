# author: Jan Tschada
# SPDX-License-Identifer: Apache-2.0

from datetime import date
from geodisasters.services import query, hotspots, aggregate
from georapid.factory import EnvironmentClientFactory
from unittest import TestCase



class TestServices(TestCase):

    def setUp(self) -> None:
        self._client = EnvironmentClientFactory.create_client_with_host('geodisasters.p.rapidapi.com')
    
    def test_query(self):
        geojson_result = query(self._client, date(2023, 5, 24), date(2023, 5, 24))
        self.assertIsNotNone(geojson_result, "Result must not be None!")
        self.assertTrue('features' in geojson_result, "GeoJSON response must have features!")
        features = geojson_result['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")

    def test_hotspots(self):
        geojson_result = hotspots(self._client, date(2023, 5, 24))
        self.assertIsNotNone(geojson_result, "Result must not be None!")
        self.assertTrue('features' in geojson_result, "GeoJSON response must have features!")
        features = geojson_result['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")

    def test_aggregate(self):
        geojson_result = aggregate(self._client, date(2023, 5, 24))
        self.assertIsNotNone(geojson_result, "Result must not be None!")
        self.assertTrue('features' in geojson_result, "GeoJSON response must have features!")
        features = geojson_result['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")