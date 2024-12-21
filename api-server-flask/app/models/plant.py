from app.utils.db import get_collection

class Plant:
    @staticmethod
    def create_plant(data):
        plants = get_collection('plants')
        return plants.insert_one(data).inserted_id

    @staticmethod
    def find_plant_by_id(plant_id):
        plants = get_collection('plants')
        return plants.find_one({"_id": plant_id})

    @staticmethod
    def update_plant(plant_id, update_data):
        plants = get_collection('plants')
        plants.update_one({"_id": plant_id}, {"$set": update_data})
