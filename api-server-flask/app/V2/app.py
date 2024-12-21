import streamlit as st
import json
from groq import Groq
import os
from dotenv import load_dotenv
import base64
from openai import OpenAI
from io import BytesIO
from PIL import Image
import toml
from toolhouse import Toolhouse

# Function to load the recycling data
def load_recycling_data():
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'data.json')

    try:
        with open(file_path, ) as file:

            return json.load(file)
    except FileNotFoundError:
        st.error("Could not find data.json file")
        return None

def init_tool_house():
    api_key = st.secrets['api_keys']['toolhouse']
    return Toolhouse(api_key=api_key,
provider="openai")


# Initialize Groq client
def init_groq():
    api_key = st.secrets['api_keys']['groq']
    if not api_key:
        st.error("Please set your Groq API key")
        return None
    return Groq(api_key=api_key)

def init_openai():
    api_key = st.secrets['api_keys']['openai']
    if not api_key:
        st.error("Please set your OpenAI API key")
        return None
    return OpenAI(api_key=api_key)

def analyze_image(client, image_data, recycling_data):
    if not client:
        return "Error: OpenAI client not initialized"
    
    try:
        # Encode image to base64
        base64_image = base64.b64encode(image_data.getvalue()).decode('utf-8')

        prompt = """Analyze this image and detect visible symptoms of plant disease.
Guidelines for detection:
Identify symptoms using clear, descriptive terms (e.g., "yellowing leaves," "dark spots," "wilting stems")
Specify the affected plant parts (e.g., "leaf edges," "fruit surface")
Focus only on disease-related signs, ignoring healthy areas and unrelated elements
Use a comma-separated format. Example:
"yellowing leaf edges, black spots on fruits, white fungal growth on stems"
Provide your analysis in the specified format.
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a plant disease detection assistant that identifies visible symptoms of plant diseases in images. Provide detailed descriptions of symptoms to help users diagnose potential issues."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def get_groq_response(client, content, prompt, th=None):
    if not client:
        return "Error: Groq client not initialized"
    
    try:
        MODEL = "llama3-groq-70b-8192-tool-use-preview"
        messages = [
            {
                "role": "system",
                "content": content
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        
        if th is None: 

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.0,  # Lower temperature for more consistent responses
                max_tokens=2000,

            )
        
            return response.choices[0].message.content
    
    
    
        # Add tools if th is provided
        messages = [{
            "role": "user",
            "content": "Search on web for recycling facilities near Binario F, Rome, Via Marsala, 29H, 00185 Roma RM and give me the results."
        }]

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            # Passes Code Execution as a tool
            tools=th.get_tools()
        )



        # Runs the Code Execution tool, gets the result, 
        # and appends it to the context
        th_response = th.run_tools(response)
        messages += th_response
       
        messages.append({
            "role": "system", 
            "content": "return the result to the user you must NEVER use thesearch tool again"
        })

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
                

        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"

def get_bin_image(waste_type):
    """Return the image path for a given waste type"""
    bin_images = {
       "battery_symbol": "images/battery_symbol.png",
       "blue": "images/blu.png",
       "brown": "images/brown.png",
       "green": "images/green.png",
       "yellow": "images/yellow.png",
       "grey": "images/grey.png",
       "oil_symbol": "images/oil_symbol.png",
       "red": "images/red.png",
       "famacie": "images/farmacie.jpg",
       "yellow_street": "images/yellow_street.png",

    }
    return bin_images.get(waste_type.lower(), None)

# Streamlit UI
def main():
    st.title("🌍 Plant Disease Detection")    
    # # Load recycling data
    recycling_data = load_recycling_data()

    if not recycling_data:
        st.stop()

    th = init_tool_house()

    groq_client = init_groq()
    openai_client = init_openai()
  

    if not groq_client or not openai_client or not th:
        st.stop()

    st.subheader("Upload images for comparison")
    col1, col2 = st.columns(2)

    with col1:
        img_file1 = st.file_uploader("Image 1 (Current State)", type=["jpg", "jpeg", "png"], key="img1")
    with col2:
        img_file2 = st.file_uploader("Image 2 (After 10 Days)", type=["jpg", "jpeg", "png"], key="img2")

    if img_file1 and img_file2:
        with st.spinner("Analyzing and comparing images..."):
            base64_image1 = base64.b64encode(img_file1.getvalue()).decode('utf-8')
            base64_image2 = base64.b64encode(img_file2.getvalue()).decode('utf-8')

            comparison_prompt = """
            You are a specialized plant health assistant tasked with analyzing two images of a plant to compare their health states. For each detected symptom, provide:
            
            1. Symptom: [Describe the symptom]
            2. Image 1 Observation: [Observation from the first image]
            3. Image 2 Observation: [Observation from the second image]
            4. Evaluation: [Improved/Worsened/Unchanged/New Symptom]
            
            Provide a clear and concise report.
            """

            try:
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a plant health analysis assistant."
                        },
                        {
                            "role": "user",
                            "content": comparison_prompt + \
                                       f"\nImage 1 (Current State): data:image/jpeg;base64,{base64_image1}" + \
                                       f"\nImage 2 (After 10 Days): data:image/jpeg;base64,{base64_image2}"
                        }
                    ],
                    max_tokens=1000
                )

                comparison_results = response.choices[0].message.content

                st.write("Comparison Results:")
                st.write(comparison_results)

                col1, col2 = st.columns(2)
                with col1:
                    st.image(img_file1, caption="Image 1 (Current State)")
                with col2:
                    st.image(img_file2, caption="Image 2 (After 10 Days)")

            except Exception as e:
                st.error(f"Error comparing images: {str(e)}")

if __name__ == "__main__":
    main()
