import os
import unittest

from dotenv import load_dotenv
import requests

from src.yalidine.api import YalidineClient
from src.yalidine.entity import (
    Parcel,
    ParcelFilter,
    HistoryFilter,
    CenterFilter,
    WilayasFilter,
    CommunesFilter,
    DeliveryFeesFilter,
)


class TestYalidineAPI(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        self.api_id = os.getenv("API_ID")
        self.api_token = os.getenv("API_TOKEN")
        self.client = YalidineClient(self.api_id, self.api_token)

    #===============================
    # MARK: Test Limits status
    #===============================
    def test_get_limits(self):
        response = self.client.get_parcels()
        limit = self.client.last_response_headers
        print(limit)
        self.assertIsInstance(limit, dict)

    # ===============================
    # MARK: Parcels
    # ===============================

    def test_get_parcels(self):
        response = self.client.get_parcels()
        self.assertIsInstance(response, dict)

    def test_crud_parcel(self):
        parcel = Parcel(
            order_id="test_parcel",
            firstname="firstname",
            familyname="familyname",
            contact_phone="0555885588",
            address="Bouira",
            from_wilaya_name="Bouira",
            to_commune_name="Aïn Bessem",
            to_wilaya_name="Bouira",
            product_list="Press a cafe",
            price=3000,
            do_insurance=False,
            declared_value=3500,
            height=10,
            width=10,
            length=30,
            weight=10,
            freeshipping=False,
            is_stopdesk=False,
            has_exchange=0,
            product_to_collect="Test",
        )

        response = self.client.create_parcel([parcel])
        self.assertIsNotNone(response["test_parcel"])

        parcel_id = response["test_parcel"]["tracking"]

        parcel.familyname = "familyname_2"
        response = self.client.update_parcel(parcel_id=parcel_id, data=parcel)

        self.assertIsInstance(response, dict)
        self.assertEqual(response['familyname'],'familyname_2')

        response = self.client.get_parcel(parcel_id=parcel_id)
        self.assertIsInstance(response, dict)
        self.assertIsInstance(response['data'],list)
        self.assertEqual(response['data'][0]['familyname'],'familyname_2')

        response = self.client.delete_parcel(parcel_id=parcel_id)
        self.assertTrue(response[0]["deleted"])

    # ===============================
    # MARK: History
    # ===============================
    def test_get_histories(self):
        response = self.client.get_histories(filter=HistoryFilter(page_size=2))
        print(response)
        self.assertIsInstance(response, dict)

    #===============================
    # MARK: Centers
    #===============================
    def test_get_centers(self):
        response = self.client.get_centers(filter=CenterFilter(page_size=2))
        print(response)
        self.assertIsInstance(response, dict)

    # ===============================
    # MARK: Wilayas
    # ===============================
    def test_get_wilayas(self):
        response = self.client.get_wilayas(filter=WilayasFilter(page_size=2))
        print(response)
        self.assertIsInstance(response, dict)

    # ===============================
    # MARK: Communes
    # ===============================

    def test_get_communes(self):
        response = self.client.get_communes(filter=CommunesFilter(wilaya_id="10",page_size=2))
        print(response)
        self.assertIsInstance(response, dict)

    # ===============================
    # MARK: Delivery Fees
    # ===============================
    def test_get_delivery_fees(self):
        response = self.client.get_delivery_fees(
            filter=DeliveryFeesFilter(wilaya_id="10")
        )
        print(response)
        self.assertIsInstance(response, dict)
