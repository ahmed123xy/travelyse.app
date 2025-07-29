import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="Travelyse AI Assistant", page_icon="✈️", layout="centered")
st.title("✈️ Travelyse – Your AI Travel Assistant")
st.write("Describe your trip, and let AI plan it for you.")

# Input form
prompt = st.text_area("Tell us about your trip:",
    placeholder="E.g. I want to visit Amsterdam from Sept 20–24, budget 700 EUR, stay near the center, love canals and museums.",
    height=150)

# Set up OpenRouter API
API_KEY = "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"  # Replace with your actual key
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Model selection (optional)
model = "mistralai/mistral-7b-instruct"  # You can try other models too

# When user clicks the button
generate = st.button("🎒 Generate Travel Plan")

if generate:
    if not prompt:
        st.warning("Please enter your trip details above.")
    else:
        with st.spinner("Planning your trip..."):
            formatting_hint = """
Format flight suggestions like this:

🛫 Departure
Date: Sat, Sep 20
Time: 6:45 PM – 10:10 PM
Airline: Lufthansa
Stops: 1 stop via Frankfurt (FRA)
Duration: 3h 25m

🛬 Return
Date: Wed, Sep 24
Time: 3:00 PM – 7:45 PM
Airline: SWISS
Stops: 1 stop via Zurich (ZRH)
Duration: 4h 45m

💰 Price: $282 per person ($564 total)
✔️ Free cancellation within 41 hours
"""

            full_prompt = prompt + "\n\n" + formatting_hint

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful AI travel assistant."},
                    {"role": "user", "content": full_prompt}
                ]
            }

            try:
                headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
                response = requests.post(API_URL, headers=headers, json=payload)
                if response.status_code == 200:
                    output = response.json()["choices"][0]["message"]["content"]
                    st.success("✅ Here's your travel plan:")
                    st.markdown(output)
                else:
                    st.error(f"❌ API Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"⚠️ An error occurred: {str(e)}")
