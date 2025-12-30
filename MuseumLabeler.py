import streamlit as st
import pandas as pd
import numpy as np
import base64
import joblib
from data_preprocessing import data_cleaner_list

RANDOM_SEED=65


    
def set_background(image_file):
    """
    Background image.
    """
    try:
        # backround file
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        
        
        css_string = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64_encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        [data-testid="stSidebar"] {{
            background: rgba(255, 255, 255, 0.7);
        }}
        </style>
        """
        
        
        st.markdown(css_string, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error(f"Error: Image File '{image_file}' not found. Make sure it's in the same dir of the this file.")
    except Exception as e:
        st.error(f"Error during background setting: {e}")

set_background('assets/Museum_bkgnd.png')

st.markdown("""
<style>
/* stRadio */
.stRadio > label {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 10px;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* stSelectbox */
.stSelectbox > label {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 10px;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* stColumns */
.stColumns > label {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 10px;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
div[data-testid="stMetricValue"] {
    font-size: 3rem;
}
div[data-testid="stMetricLabel"] {
    font-size: 1.2rem;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.stApp {
    padding-top: 0px !important;
}

[data-testid="stAppViewContainer"] {
    padding-top: 0rem; 
    margin-top: -100px;
}


h1 {
    margin-top: 2rem;
}

body {
    margin: 0 !important;
    padding: 0 !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<p style='font-size: 18px; color: grey;'>ProfessionAI | MuseumLangID</p>", unsafe_allow_html=True)

st.set_page_config(layout="wide", page_title="Museum Language Recognition", page_icon="🌍")
st.title("Detect the language of the label")

# Text input area
user_input = st.text_area(
    "----------------------",
    height=100,
    placeholder="Type or paste your text here...",
    help="Enter text in Italian, English, or German"
)

model = joblib.load('assets/museum_language_detector_pipeline.pkl')

def LangPred(user_input):
    detected = model.predict(user_input)[0]
    if detected==0:
        lang='it'
    elif detected==1:
        lang='en'
    else:
        lang='de'
    return lang, model.predict_proba(user_input)[0][detected]

# Analyze button
if st.button("Press to see the detected language", type="primary"):
    if user_input.strip():
        try:
            # Get the result
            lang_code, probability = LangPred(user_input)
            
            # Map language codes to country codes for flags
            lang_to_flag = {
                'it': ('IT', 'Italian'),
                'en': ('GB', 'English'),
                'de': ('DE', 'German')
            }
            
            # Display results
            st.markdown("---")
            #st.subheader("Detection Result")
            
            if lang_code in lang_to_flag:
                flag_code, lang_name = lang_to_flag[lang_code]
                
                # Display flag and language
                col1, col2 = st.columns([1, 3])
                with col1:
                    # Unicode flag emoji
                    flag_emoji = chr(127462 + ord(flag_code[0]) - ord('A')) + \
                                chr(127462 + ord(flag_code[1]) - ord('A'))
                    st.markdown(f"<div style='font-size: 80px; text-align: center;'>{flag_emoji}</div>", 
                              unsafe_allow_html=True)
                with col2:
                    st.metric(
                        label="Detected Language",
                        value=lang_name,
                        delta=None
                    )
                    st.metric(
                        label="Confidence",
                        value=f"{probability:.5%}"
                    )
            else:
                st.warning(f"⚠️ Detected language '{lang_code}' is not one of the supported languages (IT, EN, DE)")
                st.info(f"Confidence: {probability:.5%}")
                        
        except Exception as e:
            st.error(f"❌ Error during language detection: {str(e)}")
            st.info("Please make sure you've entered enough text for accurate detection.")
    else:
        st.warning("⚠️ Please enter some text to analyze.")

# Footer
st.markdown("---")