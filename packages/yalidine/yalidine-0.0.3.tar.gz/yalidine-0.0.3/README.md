# Yalidine
[Yalidine](https://github.com/tarek-berkane/yalidine) a Python library that implement [Yalidine](https://yalidine.com/) `REST` API.

![alt text](images/yalidine-logo.png)

## Instaltion
```bash
pip install yalidine
```

## Usage
### Initialize client
```py
from yalidine import YalidineClient

app_id = "APP-ID"
app_token = "APP-TOKEN"

client = YalidineClient(app_id, app_token)

print(client.get_parcels())
```
### Check api limit
```python

response = client.get_parcels()
limit = client.last_response_headers
# last_response_headers include api limit status from last request
print(limit)
```


### Parcel
```py
parcel = Parcel(
    order_id="test_parcel",
    firstname="firstname",
    ... # Fill Fields
)

# create parcel
response = client.create_parcel([parcel])

# update parcel
response = client.update_parcel(parcel_id=parcel_id, data=parcel)

# delete parcel
response = client.delete_parcel(parcel_id="parcel_id")

# Get parcel 
response = client.get_parcel(parcel_id="parcel_id")

# Get parcel list
response = client.get_parcels()

# Get parcel list using filter
from yalidine.entity import ParcelFilter
response = client.get_parcels(filter=ParcelFilter(page=1))

```

### History
```python
from yalidine.entity import HistoryFilter

responce = client.get_histories(filter=HistoryFilter(page_size=2))

```

### Centers
```python
from yalidine.entity import CenterFilter

responce = client.get_centers(filter=CenterFilter(page_size=2))

```

### Wilayas
```python
from yalidine.entity import WilayasFilter

responce = client.get_wilayas(filter=WilayasFilter(page_size=2))
```

### Communes
```python
from yalidine.entity import CommunesFilter

responce = client.get_communes(filter=CommunesFilter(page_size=2))
```

#### Delivery Fees
```python
from yalidine.entity import DeliveryFeesFilter

responce = client.get_delivery_fees(filter=DeliveryFeesFilter(page_size=2))
```