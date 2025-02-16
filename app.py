# app.py

import streamlit as st
from home import show_dashboard
from user_agent import UserConversationAgent
from api_calling_agent import APICallingAgent
from summarizer_agent import SummarizerAgent
from best_crop_agent import BestCropRecommendationAgent
from planning_agent import PlanningAgent
from doctor_agent import DoctorAgent

# Custom CSS for styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
    html, body { font-family: 'Poppins', sans-serif; }
    .nav-title { font-size: 24px; font-weight: 600; margin-bottom: 15px; }
    .header { margin-bottom: 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize agents
user_agent = UserConversationAgent()
api_agent = APICallingAgent()
summary_agent = SummarizerAgent()
crop_agent = BestCropRecommendationAgent()
planning_agent_obj = PlanningAgent()
doctor_agent_obj = DoctorAgent()

# Initialize session state variables
if "summarized_data" not in st.session_state:
    st.session_state["summarized_data"] = {}
if "selected_crop" not in st.session_state:
    st.session_state["selected_crop"] = None

# Sidebar Navigation
st.sidebar.markdown('<div class="nav-title">Navigation</div>', unsafe_allow_html=True)
pages = ["🏠 Home", "🌾 Best Crop Recommendation", "📅 Planning", "🩺 Plant Health Diagnosis"]
page = st.sidebar.radio("Go to", pages)

if page == "🏠 Home":
    show_dashboard()

elif page == "🌾 Best Crop Recommendation":
    st.title("Best Crop Recommendation")
    st.subheader("Step 1: Provide Your Farm Details")
    with st.form(key="user_input_form"):
        budget = st.text_input("Budget", placeholder="Enter your budget")
        resources = st.text_input("Resources", placeholder="Enter available resources")
        location = st.text_input("Location", placeholder="Enter your farm location")
        soil_type = st.text_input("Soil Type", placeholder="Enter your soil type")
        water_availability = st.text_input("Water Availability", placeholder="Enter water availability")
        equipment = st.text_input("Equipment", placeholder="Enter available equipment")
        submit_user_data = st.form_submit_button(label="Submit")
    
    if submit_user_data:
        form_data = {
            "budget": budget,
            "resources": resources,
            "location": location,
            "soil_type": soil_type,
            "water_availability": water_availability,
            "equipment": equipment
        }
        user_data = user_agent.collect_user_input(form_data)
        api_data = api_agent.get_all_api_data(location)
        summarized_data = summary_agent.aggregate_data(user_data, api_data)
        st.session_state["summarized_data"] = summarized_data
        st.success("✅ Data collected and summarized successfully!")
    
    if st.session_state["summarized_data"]:
        st.subheader("Step 2: Choose Your Preferred Crop")
        recommended_crops = crop_agent.recommend_crops(st.session_state["summarized_data"]())
        selected_crop = st.radio("Select a Crop", recommended_crops)
        if st.button("Confirm Crop Selection"):
            st.session_state["selected_crop"] = selected_crop
            st.success(f"✅ You have selected: {selected_crop}. Proceed to the Planning page.")

elif page == "📅 Planning":
    st.title("Planning")
    selected_crop = st.session_state.get("selected_crop", None)
    if not selected_crop:
        st.warning("⚠️ Please complete the Best Crop Recommendation page and select a crop first.")
    else:
        st.subheader(f"Planning for: {selected_crop}")
        additional_input = st.text_area("Additional Details (if any)", placeholder="Provide extra information...")
        if st.button("Generate Growing Plan"):
            summarized_data = st.session_state.get("summarized_data", {})
            plan = planning_agent_obj.provide_plan(summarized_data, selected_crop, additional_input)
            st.subheader("Sustainable Growing Plan")
            st.text(plan)

elif page == "🩺 Plant Health Diagnosis":
    st.title("Plant Health Diagnosis")
    uploaded_file = st.file_uploader("Upload a plant image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        if st.button("Diagnose Plant Health"):
            summarized_data = st.session_state.get("summarized_data", {})
            diagnosis = doctor_agent_obj.diagnose_plant(uploaded_file, summarized_data)
            st.subheader("Diagnosis Result")
            st.write(diagnosis)
        query = st.text_input("Ask a follow-up question:")
        if st.button("Get Chat Response"):
            chat_response = doctor_agent_obj.chat_assistant(uploaded_file, query, st.session_state.get("summarized_data", {}))
            st.subheader("Chat Assistant Response")
            st.write(chat_response)
