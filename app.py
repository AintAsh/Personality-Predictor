import numpy as np
import pickle
import tensorflow as tf
from fastapi import FastAPI
from pydantic import BaseModel

# --------------------------------------------------
# Load trained ANN model and preprocessing objects
# --------------------------------------------------

model = tf.keras.models.load_model("personality_ann_model.h5")

with open("scaler_personality.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# --------------------------------------------------
# Initialize FastAPI app
# --------------------------------------------------

app = FastAPI(
    title="Personality Prediction API",
    description="ANN-based Personality Type Prediction",
    version="1.0"
)

# --------------------------------------------------
# Input schema (29 personality features)
# --------------------------------------------------

class PersonalityInput(BaseModel):
    social_energy: float
    alone_time_preference: float
    talkativeness: float
    deep_reflection: float
    group_comfort: float
    party_liking: float
    listening_skill: float
    empathy: float
    creativity: float
    organization: float
    leadership: float
    risk_taking: float
    public_speaking_comfort: float
    curiosity: float
    routine_preference: float
    excitement_seeking: float
    friendliness: float
    emotional_stability: float
    planning: float
    spontaneity: float
    adventurousness: float
    reading_habit: float
    sports_interest: float
    online_social_usage: float
    travel_desire: float
    gadget_usage: float
    work_style_collaborative: float
    decision_speed: float
    stress_handling: float

# --------------------------------------------------
# Health check endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {"message": "Personality Prediction ANN API is running"}

# --------------------------------------------------
# Prediction endpoint
# --------------------------------------------------

@app.post("/predict")
def predict_personality(data: PersonalityInput):

    input_array = np.array([[
        data.social_energy,
        data.alone_time_preference,
        data.talkativeness,
        data.deep_reflection,
        data.group_comfort,
        data.party_liking,
        data.listening_skill,
        data.empathy,
        data.creativity,
        data.organization,
        data.leadership,
        data.risk_taking,
        data.public_speaking_comfort,
        data.curiosity,
        data.routine_preference,
        data.excitement_seeking,
        data.friendliness,
        data.emotional_stability,
        data.planning,
        data.spontaneity,
        data.adventurousness,
        data.reading_habit,
        data.sports_interest,
        data.online_social_usage,
        data.travel_desire,
        data.gadget_usage,
        data.work_style_collaborative,
        data.decision_speed,
        data.stress_handling
    ]])

    # Scale input using saved scaler
    input_scaled = scaler.transform(input_array)

    # Predict probabilities
    prediction = model.predict(input_scaled)

    # Extract class and confidence
    class_index = int(np.argmax(prediction, axis=1)[0])
    confidence = float(np.max(prediction))

    # Decode personality label
    personality = label_encoder.inverse_transform([class_index])[0]

    return {
        "predicted_personality": personality,
        "confidence": round(confidence, 4)
    }
