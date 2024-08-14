# core
import json
from dataclasses import asdict

# lib
import requests
from requests.compat import urljoin

# files
from .settings import YALIDINE_URL
from .entity import (
    Parcel,
    ParcelFilter,
    HistoryFilter,
    CenterFilter,
    CommunesFilter,
    WilayasFilter,
    DeliveryFeesFilter,
)


exclude_none_value = lambda x: {k: v for (k, v) in x if v is not None}

asdict_true_value = lambda x: asdict(x, dict_factory=exclude_none_value)

dict_to_query_string = lambda x: "&".join([f"{k}={v}" for k, v in x.items()])


def response_or_exception(fn):
    from functools import wraps

    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        response: requests.Response = fn(self, *args, **kwargs)
        if response.status_code == 422:
            raise requests.exceptions.HTTPError(response, response=response)
        response.raise_for_status()
        self.last_response_headers = response.headers
        return response.json()

    return wrapper


# ===============================
# MARK: YalidineClient
# ===============================
class YalidineClient:
    def __init__(self, api_id, api_token, url=YALIDINE_URL):
        self.url = url
        self.api_id = api_id
        self.api_token = api_token
        self.last_response_headers = None
        self.headers = {
            "X-API-ID": self.api_id,
            "X-API-TOKEN": self.api_token,
            "Content-Type": "application/json",
        }

    # ===============================
    # MARK: Parcels
    # ===============================
    @response_or_exception
    def get_parcel(self, parcel_id):
        response = requests.get(
            urljoin(self.url, f"parcels/{parcel_id}"),
            headers=self.headers,
        )

        return response

    @response_or_exception
    def get_parcels(self, filter: ParcelFilter = None):
        query = ""

        if filter:
            f = asdict_true_value(filter)
            query = dict_to_query_string(f)

        response = requests.get(
            urljoin(self.url, f"parcels/?{query}"),
            headers=self.headers,
        )
        print(response.url)
        return response

    @response_or_exception
    def create_parcel(self, parcel_list: list[Parcel]):
        assert isinstance(parcel_list, list)
        
        body = [asdict(parcel) for parcel in parcel_list]

        response = requests.post(
            urljoin(self.url, "parcels"),
            headers=self.headers,
            json=body,
        )

        return response

    @response_or_exception
    def update_parcel(self, parcel_id: str, data: Parcel):
        response = requests.patch(
            urljoin(self.url, f"parcels/{parcel_id}"),
            headers=self.headers,
            json=asdict_true_value(data),
        )

        return response

    @response_or_exception
    def delete_parcel(self, parcel_id: str):
        response = requests.delete(
            urljoin(self.url, f"parcels/{parcel_id}"),
            headers=self.headers,
        )

        return response

    @response_or_exception
    def delete_parcels(self, parcel_ids: list[str]):
        response = requests.delete(
            urljoin(self.url, f"parcels/?tracking={','.join(parcel_ids)}"),
            headers=self.headers,
        )
        return response

    # ===============================
    # MARK: Histories
    # ===============================

    @response_or_exception
    def get_histories(self, filter: HistoryFilter = None):
        query = ""

        if filter:
            f = asdict_true_value(filter)
            query = dict_to_query_string(f)

        response = requests.get(
            urljoin(self.url, f"histories/?{query}"),
            headers=self.headers,
        )
        print(response.url)

        return response

    @response_or_exception
    def get_parcel_history(self, traking_id: str):
        response = requests.get(
            urljoin(self.url, f"histories/{traking_id}"),
            headers=self.headers,
        )

        return response

    # ===============================
    # MARK: Centers
    # ===============================
    @response_or_exception
    def get_centers(self, filter: CenterFilter = None):
        query = ""

        if filter:
            f = asdict_true_value(filter)
            query = dict_to_query_string(f)

        response = requests.get(
            urljoin(self.url, f"centers/?{query}"),
            headers=self.headers,
        )

        return response

    @response_or_exception
    def get_center(self, center_id: str):
        response = requests.get(
            urljoin(self.url, f"centers/{center_id}"),
            headers=self.headers,
        )

        return response

    # ===============================
    # MARK: Communes
    # ===============================
    @response_or_exception
    def get_communes(self, filter: CommunesFilter = None):
        query = ""

        if filter:
            f = asdict_true_value(filter)
            query = dict_to_query_string(f)

        response = requests.get(
            urljoin(self.url, f"communes/?{query}"),
            headers=self.headers,
        )

        return response

    @response_or_exception
    def get_commune(self, commune_id: str):
        response = requests.get(
            urljoin(self.url, f"communes/{commune_id}"),
            headers=self.headers,
        )

        return response

    # ===============================
    # MARK: Wilayas
    # ===============================
    @response_or_exception
    def get_wilayas(self, filter: WilayasFilter = None):
        query = ""

        if filter:
            f = asdict_true_value(filter)
            query = dict_to_query_string(f)

        response = requests.get(
            urljoin(self.url, f"wilayas/?{query}"),
            headers=self.headers,
        )

        return response

    @response_or_exception
    def get_wilaya(self, wilaya_id: str):
        response = requests.get(
            urljoin(self.url, f"wilayas/{wilaya_id}"),
            headers=self.headers,
        )

        return response

    # ===============================
    # MARK: Delivery Fees
    # ===============================
    @response_or_exception
    def get_delivery_fees(self, filter: DeliveryFeesFilter = None):
        query = ""

        if filter:
            f = asdict_true_value(filter)
            query = dict_to_query_string(f)

        response = requests.get(
            urljoin(self.url, f"deliveryfees/?{query}"),
            headers=self.headers,
        )

        return response

    @response_or_exception
    def get_wilaya_delivery_fee(self, wilaya_id: str):
        response = requests.get(
            urljoin(self.url, f"deliveryfees/{wilaya_id}"),
            headers=self.headers,
        )

        return response
