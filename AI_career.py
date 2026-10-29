import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from groq import Groq

load_dotenv(find_dotenv())

st.set_page_config(page_title="AI Career Blueprint Generator", page_icon="🎯", layout="wide")

st.title("🎯 AI Career Blueprint Generator")
st.write("Plan your goals and discover the steps to achieve them.")
st.markdown("---")

st.sidebar.title("About This App")
st.sidebar.write(
    "This app uses AI to help you explore career options, "
    "develop skills and create a practical action plan."
)

st.subheader("📋 Tell Us About Yourself")

with st.form("career_form"):
    age = st.number_input("Age", min_value=10, max_value=100, value=18)
    goal = st.text_area("🎯 Main Goal / Dream", placeholder="What do you want to achieve?")
    interests = st.text_area("💡 Interests & Passions", placeholder="What do you enjoy?")
    situation = st.text_area("📍 Current Situation", placeholder="What are you doing currently?")
    challenge = st.text_area("🧩 Biggest Challenge", placeholder="What is stopping you?")

    submitted = st.form_submit_button("✨ Generate My Blueprint", use_container_width=True)

if submitted:
    if not all(x.strip() for x in [goal, interests, situation, challenge]):
        st.warning("Please fill in all the fields.")
    elif not os.getenv("GROQ_API_KEY"):
        st.error("API key not found. Please check your .env file.")
    else:
        prompt = f"""
Create a personalized career and goal blueprint.

Age: {age}
Main Goal: {goal}
Interests: {interests}
Current Situation: {situation}
Biggest Challenge: {challenge}

Include these sections:
1. Goal Analysis
2. Three Possible Paths
3. Required Skills and Resources
4. Six-Month Action Plan
5. Challenges and Solutions
6. Long-Term Strategy
7. Three Actions to Start This Week

Use simple language, clear headings and practical advice.
Consider all fields, including business, sports, YouTube, arts and technology.
Personalize the plan using the user's information.
"""

        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))

            with st.spinner("Creating your blueprint..."):
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a helpful career and goal-planning advisor."},
                        {"role": "user", "content": prompt}
                    ],
                    model="openai/gpt-oss-120b",
                    temperature=0.4
                )

            report = response.choices[0].message.content

            if report:
                st.success("Your blueprint is ready!")
                st.markdown("---")
                st.subheader("📊 Your Personal Blueprint")
                st.markdown(report)

                st.download_button(
                    "📥 Download Blueprint",
                    report,
                    file_name="career_blueprint.md",
                    mime="text/markdown"
                )

        except Exception as e:
            st.error("Unable to generate the blueprint. Check your API key, internet or model access.")
            st.caption(str(e))

st.markdown("---")
st.caption("Built with Python, Streamlit and Groq AI ❤️")