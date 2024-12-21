import os
import base64
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image
from app.models.plant import Plant
from app.models.disease import Disease
from app.models.notification import Notification
from app.utils.db import get_collection
from app.PlantDiseaseDetection.app import analyze_image  # Import your analysis logic

# Directory to store uploaded images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def detect_disease(user_id, plant_id, disease_name, treatment, image_base64, follow_up_in_days):
    """
    Detect disease, save image, and update plant records for a specific user.
    """
    # Decode the base64 image
    try:
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))

        # Save the image to the server
        image_path = os.path.join(UPLOAD_FOLDER, f"{user_id}_{plant_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
        image.save(image_path)
    except Exception as e:
        raise ValueError(f"Failed to process the image: {str(e)}")

    # Analyze the image to detect symptoms
    symptoms = analyze_image(image_data)
    if not symptoms:
        raise ValueError("Failed to analyze the image")

    # Create a disease record
    disease_data = {
        "user_id": user_id,
        "plant_id": plant_id,
        "disease_name": disease_name,
        "treatment": treatment,
        "date_detected": datetime.now(),
        "follow_up_date": datetime.now() + timedelta(days=follow_up_in_days),
        "condition": "In Progress",
        "image_path": image_path,
        "symptoms": symptoms
    }
    disease_id = Disease.create_disease(disease_data)

    # Update the plant with the disease record
    Plant.update_plant(
        plant_id,
        {"$push": {"disease_records": disease_data}, "current_condition": "Infected"}
    )

    # Create a notification for follow-up
    notification_data = {
        "user_id": user_id,
        "message": f"Follow-up for plant {plant_id} scheduled in {follow_up_in_days} days.",
        "status": "Pending",
        "date_created": datetime.now()
    }
    Notification.create_notification(notification_data)

    return {
        "user_id": user_id,
        "disease_name": disease_name,
        "follow_up_date": disease_data["follow_up_date"],
        "symptoms": symptoms
    }


def get_user_plants(user_id):
    """
    Retrieve all plants associated with a specific user.
    """
    plants_collection = get_collection('plants')
    plants = plants_collection.find({"user_id": user_id})  # Filter by user_id
    # Convert the Cursor object to a list of dictionaries
    return [plant for plant in plants]


def get_plant_treatment_details(plant_id):
    """
    Retrieve all treatment records for a specific plant.
    """
    plant = Plant.find_plant_by_id(plant_id)
    if not plant:
        raise ValueError("Plant not found")
    return plant.get("treatment_records", [])
