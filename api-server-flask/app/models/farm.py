from app.utils.db import get_collection

class Farm:
    @staticmethod
    def create_farm(data):
        farms = get_collection('farms')
        return farms.insert_one(data).inserted_id

    @staticmethod
    def find_farm_by_id(farm_id):
        farms = get_collection('farms')
        return farms.find_one({"_id": farm_id})

    @staticmethod
    def update_farm(farm_id, update_data):
        farms = get_collection('farms')
        farms.update_one({"_id": farm_id}, {"$set": update_data})
