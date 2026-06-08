import streamlit as st
import requests

st.set_page_config(page_title="AI Travel Planner", layout="wide")

backend_url = st.secrets["backend_url"]

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.4);
    z-index: 0;
}

.main {
    position: relative;
    z-index: 1;
}

.centered-title {
    text-align: center;
    color: white;
    font-size: 3rem;
    font-weight: bold;
    margin-bottom: 2rem;
}

.plan-card {
    background-color: rgba(255, 255, 255, 0.95);
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    color: #111111;
    margin-top: 1.5rem;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)
st.markdown('<h1 class="centered-title">✈️ AI Travel Planner</h1>', unsafe_allow_html=True)

st.sidebar.header("Plan Your Trip")

From_city = st.sidebar.text_input("Start Destination", value="Delhi")
To_city = st.sidebar.text_input("End Destination", value="Mumbai")

days = st.sidebar.slider("Days", 1, 15, 5)
budget = st.sidebar.number_input("Budget(₹)", min_value=0, value=10000)

trip_type = st.sidebar.selectbox("Trip Type", ["Solo", "Couple", "Family", "Friends"])
Travel = st.sidebar.selectbox("Travel By", ["Flight", "Train", "Bus"])

intrest = st.sidebar.multiselect(
    "Interests",
    ["Temples", "Beaches", "Mountains", "Boating", "Adventure", "Culture", "Shopping"],
    default=["Adventure"]
)

generate = st.sidebar.button("🚀 Generate Plan")

if generate:
    with st.spinner("AI Agent is collecting live transport, weather, and building your itinerary..."):
        payload = {
            "From": From_city,
            "To": To_city,
            "days": days,
            "budget": budget,
            "trip_type": trip_type,
            "Travel": Travel,
            "intrest": intrest
        }

        try:
            res = requests.post(f"{backend_url}/plan", json=payload, timeout=120)
            
            if res.status_code == 200:
                data = res.json()
                
                # Check both common backend dictionary keys safely
                itinerary = data.get("response") or data.get("agent_response")
                
                st.markdown('<div class="plan-card">', unsafe_allow_html=True)
                st.header("📌 Final Travel Plan")
                
                if itinerary:
                    st.markdown(itinerary)
                else:
                    st.warning("⚠️ Received an empty layout from the AI Agent. Check backend terminal logs.")
                    st.write("Raw data payload response structure received:", data)

                images = data.get("images", {})
                if images:
                    st.write("---")
                    st.subheader("📸 Explore Your Destination")
                    for interest, img_list in images.items():
                        if img_list:
                            cols = st.columns(len(img_list))
                            for i, img in enumerate(img_list):
                                with cols[i]:
                                    st.image(img, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error(f"Backend Server Error (Status Code: {res.status_code}). Detail: {res.text}")

        except Exception as e:
            st.error(f"Failed to communicate with deployed backend: {e}")