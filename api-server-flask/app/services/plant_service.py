from app.models.plant import Plant
from app.models.disease import Disease
from app.models.notification import Notification
from datetime import datetime, timedelta

def detect_disease(plant_id, disease_name, treatment, image_url, follow_up_in_days):
    # Create disease record
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

    # Update plant with disease reference
    Plant.update_plant(plant_id, {"$push": {"disease_records": disease_id}, "current_condition": "Infected"})

    # Schedule notification for follow-up
    notification_data = {
        "user_id": "...",  # Retrieve based on plant-farm relationship
        "message": f"Follow-up for plant {plant_id} scheduled in {follow_up_in_days} days.",
        "status": "Pending",
        "date_created": datetime.now()
    }
    Notification.create_notification(notification_data)
