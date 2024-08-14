from dataclasses import dataclass, field
from typing import Optional, List




# ===============================
# MARK: Parcel
# ===============================
@dataclass
class Parcel:
    """
	Parcel object

	...

	Attributes
	----------
		order_id : str
		A string representing the order id of the parcel
		from_wilaya_name : str
			A string representing the sender's wilaya name.
		firstname : str
			The receiver's first name.
		familyname : str
			The receiver's family name.
		contact_phone : str
			The receiver's phone numbers (can be separated by commas if many)
		address : str
			The receiver's address
		to_commune_name : str
			A string representing the receiver's commune name.
		to_wilaya_name : str
			A string representing the receiver's wilaya name.
		product_list : str
			The description of the shipment's content.
		price : int
			An integer amount representing the price you want to recover from the receiver. (equal or between 0 and 150000).
		do_insurance : bool
			Whether or not you opt for an insurance. if `True`, 0% fee of `declared_value` is applicable, the refund is 100%.
		declared_value : int
			Represents the financial estimation of the items within the parcel. (must be between 0 and 150000).
		length : int
			An integer amount representing the length of the parcel's content. (greater than or equal to 0).
		width : int
			An integer amount representing the width of the parcel's content. (greater than or equal to 0).
		height : int
			An integer amount representing the height of the parcel's content. (greater than or equal to 0).
		weight : int
			An integer amount representing the weight of the parcel's content. (greater than or equal to 0).
		freeshipping : bool
			A Boolean representing whether the delivery fee is free (paid by the sender) or not.
				- `True = paid by the sender`.
				- `False = paid by the receiver`.
		is_stopdesk : bool
			Whether the delivery will be done in a stop-desk or home delivery.
				- `True = delivery` in stop desk, you must include the param `stopdesk_id`.
				- `False = home delivery`.
		stopdesk_id : str
			This parameter is required if `is_stopdesk` is true, optional if not.
		has_exchange : bool
			A Boolean representing Whether or not you want to make an exchange request for this parcel.
		product_to_collect: str
			This parameter is required if `has_exchange` is true, optional if not.

    """

    order_id: Optional[str] = None
    from_wilaya_name: Optional[str] = None
    firstname: Optional[str] = None
    familyname: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    to_commune_name: Optional[str] = None
    to_wilaya_name: Optional[str] = None
    product_list: Optional[str] = None
    price: Optional[int] = None
    do_insurance: Optional[bool] = None
    declared_value: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    freeshipping: Optional[bool] = None
    is_stopdesk: Optional[bool] = None
    stopdesk_id: Optional[str] = None
    has_exchange: Optional[bool] = None
    product_to_collect: Optional[str] = None


# ===============================
# MARK: ParcelFilter
# ===============================
@dataclass
class ParcelFilter:
	"""
	ParcelFilter object

	...

	Attributes
	----------
		tracking : str
			The unique identifier for the parcel.
				- eg: one item \"yal-123456\"
				- eg: list of items \"yal-123456,yal-789123,yal-456789\"
		order_id: str
			The receiver’s order id
		import_id: int
			The id of the operation of bulk-creation of the parcel (through importation or API creation)
		to_wilaya_id: int
			The id of the receiver’s wilaya
		to_commune_name: str
			The receiver’s commune name.
		is_stopdesk: bool
			Whether the delivery is done in a stop-desk or home delivery.
				- `True` means delivery in stop desk
				- `False` means home delivery
		is_exchange: bool
			Whether or not the package is the annexed parcel for an exchange request.
		has_exchange: bool
			Whether or not you want to make an exchange request for this parcel.
		freeshipping: bool
			Whether the delivery fee is free (paid by the sender).
		date_creation: str
			The parcel’s date of creation in the format **YYYY-MM-DD**
				- Only one date: `date_creation=2021-01-01`
				- Between two dates: `date_creation=2021-01-01,2021-01-31`
        date_last_status: str
			The parcel’s date of the last status in the format **YYYY-MM-DD**
				- Only one date: `date_last_status=2021-01-01`
				- Between two dates: `date_last_status=2021-01-01,2021-01-31`
		payment_status: str
			The current payment status of the parcel.
				- not-ready
				- ready
				- receivable
				- payed
        last_status: str
			The current status of the parcel's delivery.
				- Pas encore expédié
				- A vérifier
				- En préparation
				- Pas encore ramassé
				- Prêt à expédier
				- Ramassé
				- Bloqué
				- Débloqué
				- Transfert
				- Expédié
				- Centre
				- En localisation
				- Vers Wilaya
				- Reçu à Wilaya
				- En attente du client
				- Sorti en livraison
				- En attente
				- En alerte
				- Tentative échouée
				- Livré
				- Echèc livraison
				- Retour vers centre
				- Retourné au centre
				- Retour transfert
				- Retour groupé
				- Retour à retirer
				- Retour vers vendeur
				- Retourné au vendeur
				- Echange échoué
        fields: str
			You can specify which fields you want returned by using the field parameter and listing each field separated by a comma.
        
		page : int
			The number of the page you would request
		page_size : int
			A limit on the number of objects to be returned, between 1 and 1000
               
        order_by: str
				- date_creation
				- date_last_status 
				- tracking 
				- order_id 
				- import_id 
				- to_wilaya_id 
				- to_commune_id 
				- last_status
                    
        desc: bool
			Order the result descening
        asc: bool
			Order the result ascending
	"""
		
	tracking: Optional[str] = None
	order_id: Optional[str] = None
	import_id: Optional[int] = None
	to_wilaya_id: Optional[int] = None
	to_commune_id: Optional[int] = None
	is_stopdesk: Optional[bool] = None
	is_exchange: Optional[bool] = None
	has_exchange: Optional[bool] = None
	freeshipping: Optional[bool] = None
	date_creation: Optional[str] = None
	date_last_status: Optional[str] = None
	payment_status: Optional[str] = None
	last_status: Optional[str] = None
	fields: Optional[str] = None
	page: Optional[int] = None
	page_size: Optional[int] = None
	order_by: Optional[str] = None
	desc: Optional[bool] = None
	asc: Optional[bool] = None


#===============================
# MARK:  HistoryFilter
#===============================


@dataclass
class HistoryFilter:
    """
	HistoryFilter object

	...

	Attributes
	----------
		tracking : str
			The identifier of the parcels.
		status: str
			The status of the parcel
				- Pas encore expédié
				- A vérifier
				- En préparation
				- Pas encore ramassé
				- Prêt à expédier
				- Ramassé
				- Bloqué
				- Débloqué
				- Transfert
				- Expédié
				- Centre
				- En localisation
				- Vers Wilaya
				- Reçu à Wilaya
				- En attente du client
				- Sorti en livraison
				- En attente
				- En alerte
				- Alerte résolue
				- Tentative échouée
				- Livré
				- Echèc livraison
				- Retour vers centre
				- Retourné au centre
				- Retour transfert
				- Retour groupé
				- Retour à retirer
				- Retour vers vendeur
				- Retourné au vendeur
				- Echange échoué
        date_status: str
			The status’s date of creation in the format YYYY-MM-DD.
				- Only one date: `date_status=2021-01-01`
				- Between two dates: `date_status=2021-01-01,2021-01-31`
        reason: str
			The reason of a failed delivery attempt or a parcel hold
		fields: str
			You can specify which fields you want returned by using the field parameter and listing each field separated by a comma.	
		page : int
			the number of the page you would request
		page_size : int
			the number of result in the same page
		order_by: str
			By default, the results in the histories response are ordered by the date_status in a descending way.
		desc: bool
			Order the result descening
        asc: bool
			Order the result ascending

	"""
    tracking: Optional[str] = None
    status: Optional[str] = None
    date_status: Optional[str] = None
    reason: Optional[str] = None
    fields: Optional[str] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    order_by: Optional[str] = None
    desc: Optional[bool] = None
    asc: Optional[bool] = None
    

#===============================
# MARK:  CenterFilter
#===============================

@dataclass
class CenterFilter:
	"""
	CenterFilter object

	...

	Attributes
	----------
		center_id: str
            The identifier of the center
		commune_id: str
            The identifier of the center's commune
		commune_name: str
            The commune’s name of the center.
		wilaya_id: str
            The identifier of the center's wilaya
		wilaya_name: str
            The wilaya’s name of the center.
		fields: str
            You can specify which fields you want returned by using the field parameter and listing each field separated by a comma.
        page : int
			the number of the page you would request
		page_size : int
			the number of result in the same page
		order_by: str
			By default, the result in the centers results is ordered by center_id in an ascending way
        desc: bool
			Order the result descening
        asc: bool
			Order the result ascending
	"""
	center_id: Optional[str] = None
	commune_id: Optional[str] = None
	commune_name: Optional[str] = None
	wilaya_id: Optional[str] = None
	wilaya_name: Optional[str] = None
	fields: Optional[str] = None
	page: Optional[int] = None
	page_size: Optional[int] = None
	order_by: Optional[str] = None
	desc: Optional[bool] = None
	asc: Optional[bool] = None
      
#===============================
# MARK: CommunesFilter
#===============================

@dataclass
class CommunesFilter:
	"""
	CommunesFilter object

	...

	Attributes
	----------
		id: str
			The identifier of the commune
		wilaya_id: str
			The commune’s wilaya id
		has_stop_desk: bool
			Whether or not the commune has a stop desk
		is_deliverable: bool
			Whether or not the commune is deliverable
		fields: str
			You can specify which fields you want returned by using the field parameter and listing each field separated by a comma.
		page : int
			the number of the page you would request
		page_size : int
			the number of result in the same page
		order_by: str
			By default, the result in the communes results is ordered by id in an ascending way
		desc: bool
			Order the result descening
		asc: bool
			Order the result ascending
	"""
	id: Optional[str] = None
	wilaya_id: Optional[str] = None
	has_stop_desk: Optional[bool] = None
	is_deliverable: Optional[bool] = None
	fields: Optional[str] = None
	page: Optional[int] = None
	page_size: Optional[int] = None
	order_by: Optional[str] = None
	desc: Optional[bool] = None
	asce: Optional[bool] = None

#===============================
# MARK: WilayasFilter
#===============================

@dataclass
class WilayasFilter:
	"""
	WilayasFilter object

	...

	Attributes
		id: str
			The identifier of the wilaya
		name: str
			The wilaya’s name
		fields: str
			You can specify which fields you want returned by using the field parameter and listing each field separated by a comma.
		page : int
			the number of the page you would request
		page_size : int
			the number of result in the same page
		order_by: str
			By default, the result in the wilayas results is ordered by id in an ascending way
		desc: bool
			Order the result descening
		asc: bool
			Order the result ascending
	"""
	id: Optional[str] = None
	name: Optional[str] = None
	fields: Optional[str] = None
	page: Optional[int] = None
	page_size: Optional[int] = None
	order_by: Optional[str] = None
	desc: Optional[bool] = None
	asc: Optional[bool] = None

#===============================
# MARK: DeliveryFeesFilter
#===============================

@dataclass
class DeliveryFeesFilter:
	"""
	DeliveryFeesFilter object

	...

	Attributes
		wilaya_id: str
			The wilaya’s id
		fields: str
			You can specify which fields you want returned by using the field parameter and listing each field separated by a comma.
		page : int
			the number of the page you would request
		page_size : int
			the number of result in the same page
		order_by: str
			By default, the result in the delivery fees results is ordered by wilaya_id in an ascending way
		desc: bool
			Order the result descening
		asc: bool
			Order the result ascending
	"""
	wilaya_id: Optional[str] = None
	fields: Optional[str] = None
	page: Optional[int] = None
	page_size: Optional[int] = None
	order_by: Optional[str] = None
	desc: Optional[bool] = None
	asc: Optional[bool] = None