from app.utils.db import get_collection

class Disease:
    @staticmethod
    def create_disease(data):
        diseases = get_collection('diseases')
        return diseases.insert_one(data).inserted_id

    @staticmethod
    def find_diseases_by_plant(plant_id):
        diseases = get_collection('diseases')
        return list(diseases.find({"plant_id": plant_id}))

    @staticmethod
    def update_disease(disease_id, update_data):
        diseases = get_collection('diseases')
        diseases.update_one({"_id": disease_id}, {"$set": update_data})
