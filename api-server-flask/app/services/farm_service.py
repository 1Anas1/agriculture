from app.models.farm import Farm
from geopy.distance import geodesic


def get_nearby_farms(farm_id, radius_km):
    # Retrieve the base farm by its ID
    farm = Farm.find_farm_by_id(farm_id)
    if not farm:
        return []  # Return an empty list if the farm doesn't exist

    farm_location = farm['location']['coordinates']

    nearby_farms = []
    for other_farm in Farm.find_all_farms():
        if other_farm['_id'] == farm_id:
            continue  # Skip the base farm itself
        other_location = other_farm['location']['coordinates']
        distance = geodesic(farm_location, other_location).km
        if distance <= radius_km:
            nearby_farms.append(other_farm)

    return nearby_farms
