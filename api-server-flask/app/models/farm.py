from app.utils.db import get_collection

class Farm:
    @staticmethod
    def create_farm(data):
        """Create a new farm entry in the database."""
        farms = get_collection('farms')
        return farms.insert_one(data).inserted_id

    @staticmethod
    def find_farm_by_id(farm_id):
        """Find a farm by its ID."""
        farms = get_collection('farms')
        return farms.find_one({"_id": farm_id})

    @staticmethod
    def find_all_farms():
        """Retrieve all farms."""
        farms = get_collection('farms')
        return list(farms.find({}))

    @staticmethod
    def update_farm(farm_id, update_data):
        """Update a farm's information by its ID."""
        farms = get_collection('farms')
        farms.update_one({"_id": farm_id}, {"$set": update_data})
