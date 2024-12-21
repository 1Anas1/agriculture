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


    img_file = st.file_uploader("Upload a picture of the item", type=["jpg", "jpeg", "png"])
    if img_file is not None:
        with st.spinner("Analyzing image..."):
            identified_items = analyze_image(openai_client, img_file, recycling_data)
            
            if not isinstance(identified_items, str) or identified_items.startswith("Error"):
                st.error(identified_items)
            else:
                st.write("Detected Items:", identified_items)

                items = identified_items
                context = json.dumps(recycling_data)
                GROQ_CONTENT = """You are a specialized plant disease detection assistant with deep knowledge of plant pathology and symptom analysis.Your goal is to provide accurate, practical advice that helps users identify visible symptoms of plant diseases and suggests possible next steps for diagnosis or treatment."""
                GROQ_PROMPT = f"""You are a plant disease detection expert assistant. Using the provided plant care and disease guidelines, analyze these symptoms: {items}  
Context (plant care and disease guidelines):  
{context}  

For each symptom, provide a structured analysis:  
1. Symptom Description:  
- Affected Plant Part: [Specify the part of the plant showing symptoms]  
- Possible Disease: [List likely diseases causing the symptoms]  
- Reason: [Explain why this disease is suspected]  
- Recommended Action: [Suggest diagnosis or treatment steps]  

Guidelines for your response:  
- Separate each symptom with a blank line  
- Be specific about plant parts and possible diseases  
- If a symptom is not in the guidelines, suggest further diagnostic steps  
- Mention any preventive or corrective measures  
- Include any relevant notes about environmental factors or plant care practices  
- If symptoms involve multiple parts, explain how they are connected  

Please format your response clearly and concisely for each symptom."""

                
if __name__ == "__main__":
    main()