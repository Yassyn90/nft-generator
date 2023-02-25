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



os.environ["REPLICATE_API_TOKEN"] = "106aef97974cb28c4ae1fb605ccac9183d53fbcb"
model = replicate.models.get("prompthero/openjourney")
version = model.versions.get("9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb")
openai.api_key = "OPENAI_API_KEY"

# Set up Streamlit page layout
st.set_page_config(page_title="NFT Generator")

def generate_nft(prompt):

    inputs = {
        'prompt': "Generate a {}  NFT token with a unique design and high value. The NFT should be one-of-a-kind and highly desirable to collectors.".format(prompt),
        
        'width': 512,
        'height': 512,
        'prompt_strength': 0.8,
        'num_outputs': 1,
        'num_inference_steps': 150,
        'guidance_scale': 7.5,
        'scheduler': "KLMS",
    }

    output = version.predict(**inputs)
    url = output[0]
    response = requests.get(url)

    filename = 'generated-nft.png'
    with open(filename, "wb") as f:
        f.write(response.content)
        
    st.image(filename, width=400, caption="{} NFT".format(prompt))
    
 
    
# Define Streamlit app
def main():
    # Set up sidebar with prompt and model selection
    st.sidebar.header("Enter your prompt")
    prompt = st.sidebar.text_input("What NFT are you looking to generate ?")
    temp = ""
    
    # Check if prompt is provided and generate NFT if it is
    if prompt != temp and prompt != "":
        temp = prompt
        st.header("Generated NFT")
        generate_nft(prompt)
            
        filename = "generated-nft.png"
        with open(filename, "rb") as f:
            # Add download button to sidebar
            st.sidebar.download_button(
                label='Download Image',
                data=f,
                file_name='generated-nft.png',
                mime='image/png'
            )

# Run Streamlit app
if __name__ == "__main__":
    main()