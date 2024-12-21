def init_db(mongo):
    # Set up indexes, validation, or initialization logic here
    db = mongo.db
    db.farms.create_index([("location", "2dsphere")])  # For geospatial queries

def get_collection(collection_name):
    from app import mongo
    return mongo.db[collection_name]
