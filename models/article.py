import dataclasses

@dataclasses.dataclass
class Article(object):
    description: str # Leche entera Carrefour brik 1l.
    name: str # Name
    price: float # € 
    offer_price: float # € 
    meassure: str # L
    pum: float # price per meassure 0,56€/L
    size: float # ie. 1L
    brand: str # Carrefour
    meassure_description:str # brick 1L
    market: str # Carrefour/mercadona
    timestamp: float # Unix timestamp
    identifier: str
