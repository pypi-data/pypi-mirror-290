from src.yalidine.entity import Parcel, ParcelFilter, HistoryFilter, CenterFilter, WilayasFilter, CommunesFilter,DeliveryFeesFilter
from src.yalidine import YalidineClient
from pprint import pprint

api_id = "38365500522746692479"
api_token = "N4hkkIXnFagzRl6T9zMZtDB9UQsP4VJcHPXhSLm52TJIBfY7Esij01RbQ7H0Cewm"

client = YalidineClient(api_id, api_token)
# parcels = client.get_parcels(filters={})
# pprint(parcels)

filter = DeliveryFeesFilter(page=1, page_size=1)
print(client.get_delivery_fees(filter=filter))
print(client.last_response_headers)
