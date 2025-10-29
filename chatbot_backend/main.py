from fastapi import FastAPI
import pickle
import pandas as pd
import random



from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Load model and vectorizer
with open("chatbot_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
    # 📂 Load your dataset that has 'intent' and 'reply' columns
df = pd.read_excel("CustomerSupportDataSet.xlsx")

# 💬 Function to get random reply for a given intent
def get_reply(intent):
    replies = df[df['intent'] == intent]['reply'].tolist()
    return random.choice(replies) if replies else "I'm not sure how to respond to that."

@app.get("/")
def home():
    return {"message": "Chatbot API is running"}

@app.post("/predict")
def predict(user_input: str):
    X = vectorizer.transform([user_input])
    intent = model.predict(X)[0]
    return {"intent": intent}

# 📨 Route for predicting intent + returning reply
@app.post("/chat")
def chat(user_input: str):
    X = vectorizer.transform([user_input])
    intent = model.predict(X)[0]
    reply = get_reply(intent)
    return {"intent": intent, "reply": reply} 