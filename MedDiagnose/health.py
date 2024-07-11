from dotenv import load_dotenv

load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize our Streamlit app
st.set_page_config(page_title="AI MedDiagnose Doctor")

st.header("MedDiagnose Doctor Bot")

# Initialize session state to store past questions and responses
if 'past_responses' not in st.session_state:
    st.session_state.past_responses = []

input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me About this disease")

input_prompt = """
Please upload a clear image of the affected area or describe the symptoms you are experiencing. 

For accurate diagnosis, make sure to provide the following information:
1. Detailed description of the symptoms (e.g., type of pain, duration, severity).
2. Any visible signs (e.g., redness, swelling, rashes).
3. Relevant medical history (e.g., existing conditions, recent surgeries, allergies).
4. Any recent changes in lifestyle or environment (e.g., diet changes, travel history).

Our AI will analyze the provided information to identify the potential condition, its causes, and suggest possible treatments or specialists to consult.

Note: This chatbot is for informational purposes only and not a substitute for professional medical advice, diagnosis, or treatment.
"""

# If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response)
    
    # Save the input and response to session state
    st.session_state.past_responses.append({"input": input, "response": response})

# Display past questions and responses
if st.session_state.past_responses:
    st.subheader("Past Questions and Responses")
    for past in st.session_state.past_responses:
        st.write(f"**Question:** {past['input']}")
        st.write(f"**Response:** {past['response']}")
        st.write("---")
