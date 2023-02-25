import openai
import streamlit as st
import os
import json
from pathlib import Path
from base64 import b64decode
import os
import replicate
import requests
from io import BytesIO



os.environ["REPLICATE_API_TOKEN"] = "72b509c5c8b102615de42e1d3889a68c275d7de4"
model = replicate.models.get("prompthero/openjourney")
version = model.versions.get("9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb")

# Set up Streamlit page layout
st.set_page_config(page_title="NFT Generator", page_icon="logo.png")
st.image("logo.png", width=200)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



def generate_nft(prompt):
    try : 
        inputs = {
            'prompt': prompt,
            'width': 512,
            'height': 512,
            'prompt_strength': 0.8,
            'num_outputs': 1,
            'num_inference_steps': 150,
            'guidance_scale': 7.5,
            'scheduler': "KLMS",
        }
        
        
        output = version.predict(**inputs)
        st.sidebar.header("Generated NFT")
        url = output[0]
        response = requests.get(url)
        
        filename = 'generated-nft.png'
        with open(filename, "wb") as f:
            f.write(response.content)

        st.sidebar.image(filename, width=250)
        
        filename = "generated-nft.png"
        with open(filename, "rb") as f:
            # Add download button to sidebar
            st.sidebar.download_button(
                label='Download Image',
                data=f,
                file_name='generated-nft.png',
                mime='image/png'
            )
            
    except :
        
        # Define the danger message
        error_message = "Ooops, it seems like the application is down. Please consider returning back after a while."
        st.sidebar.header(error_message)   
    
    
# Define Streamlit app
def main():
    # Set up sidebar with prompt and model selection
    st.header("Enter your prompt")
    
    prompt = st.text_input("What NFT are you looking to generate ?", placeholder=" ")
    
    # Generate NFT when the user clicks the "Generate" button
    if st.button("Generate"):
        if prompt.strip() != "":
            generate_nft(prompt)

            
       
# Run Streamlit app
if __name__ == "__main__":
    main()
