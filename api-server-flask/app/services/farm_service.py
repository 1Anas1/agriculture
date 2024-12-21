from app.models.farm import Farm
from app.models.plant import Plant
from geopy.distance import geodesic

def get_nearby_farms(farm_id, radius_km):
    farm = Farm.find_farm_by_id(farm_id)
    farm_location = farm['location']['coordinates']

    nearby_farms = []
    for other_farm in Farm.find_all_farms():
        other_location = other_farm['location']['coordinates']
        distance = geodesic(farm_location, other_location).km
        if distance <= radius_km:
            nearby_farms.append(other_farm)

    return nearby_farms
