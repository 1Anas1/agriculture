from datetime import datetime, timedelta
from app.models.plant import Plant
from app.models.disease import Disease
from app.models.notification import Notification

def detect_disease(plant_id, disease_name, treatment, image_url, follow_up_in_days):
    # Create a disease record
    disease_data = {
        "plant_id": plant_id,
        "disease_name": disease_name,
        "treatment": treatment,
        "date_detected": datetime.now(),
        "follow_up_date": datetime.now() + timedelta(days=follow_up_in_days),
        "condition": "In Progress",
        "image_url": image_url
    }
    disease_id = Disease.create_disease(disease_data)

    # Update the plant with the disease record
    Plant.update_plant(
        plant_id,
        {"$push": {"disease_records": disease_id}, "current_condition": "Infected"}
    )

    # Create a notification for follow-up
    notification_data = {
        "user_id": "test_user",  # Replace with actual logic to retrieve user
        "message": f"Follow-up for plant {plant_id} scheduled in {follow_up_in_days} days.",
        "status": "Pending",
        "date_created": datetime.now()
    }
    Notification.create_notification(notification_data)

    return {
        "disease_name": disease_name,
        "follow_up_date": disease_data["follow_up_date"]
    }
