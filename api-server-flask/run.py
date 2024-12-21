from app import create_app
from flask_cors import CORS
# Create the app instance
app = create_app()

# Allow all origins (completely open)
CORS(app)
if __name__ == "__main__":
    app.run(debug=True)
