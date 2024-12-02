import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')


# App Layout
st.set_page_config(page_title="Artistica Vision", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .analysis-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 4px;
        border-left: 4px solid #495057;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .header-container {
        background: linear-gradient(to right, #2c3e50, #3498db);
        color: white;
        padding: 2.5rem;
        border-radius: 4px;
        margin-bottom: 2rem;
    }
    .header-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    .subheader {
        color: #495057;
        font-weight: 400;
        letter-spacing: 0.3px;
        border-bottom: 2px solid #dee2e6;
        padding-bottom: 0.5rem;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .archive-entry {
        background-color: #fff;
        padding: 1.5rem;
        border-radius: 4px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    .art-type-selector {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .medium-tag {
        display: inline-block;
        background-color: #e9ecef;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    .details-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 4px;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if 'archive' not in st.session_state:
    st.session_state.archive = []

# Analysis frameworks dictionary
analysis_frameworks = {
    "Contemporary Critical Analysis": {
        "general": "Conduct a comprehensive critical analysis examining the work's formal elements, conceptual depth, and contemporary relevance.",
        "sculpture": "Analyze the sculpture's form, spatial relationships, materiality, and its interaction with the surrounding space.",
        "painting": "Examine the painting's composition, color theory, brushwork, and pictorial elements.",
        "installation": "Evaluate the installation's spatial dynamics, viewer interaction, and environmental impact.",
    },
    "Technical Composition Study": {
        "general": "Perform an in-depth technical analysis of compositional elements, medium utilization, and artistic techniques.",
        "sculpture": "Examine the sculptural techniques, material properties, structural elements, and three-dimensional composition.",
        "painting": "Analyze the painting techniques, layering, medium manipulation, and surface treatment.",
        "installation": "Study the technical aspects of installation components, assembly methods, and spatial arrangement.",
    },
    "Historical-Cultural Context": {
        "general": "Examine the artwork through its historical-cultural lens, analyzing influences, period context, and artistic movements.",
        "sculpture": "Place the sculpture within its historical tradition, considering influential sculptural movements and cultural significance.",
        "painting": "Connect the painting to its art historical context, artistic movements, and cultural implications.",
        "installation": "Contextualize the installation within contemporary art practices and cultural discourse.",
    },
    "Aesthetic Philosophy": {
        "general": "Explore the philosophical and aesthetic principles embodied in the work, considering its contribution to artistic discourse.",
        "sculpture": "Examine the sculptural work's relationship to space, form, and materiality from a philosophical perspective.",
        "painting": "Analyze the painting's aesthetic principles and philosophical underpinnings.",
        "installation": "Investigate the installation's conceptual framework and philosophical implications.",
    }
}

def get_gemini_response(input, image, prompt):
    try:
        response = model.generate_content([input, image[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"Analysis Generation Error: {str(e)}")
        return None

def input_image_setup(uploaded_file):
    try:
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
            return image_parts
        else:
            raise FileNotFoundError("No artwork submitted")
    except Exception as e:
        st.error(f"Image Processing Error: {str(e)}")
        return None

def save_analysis(image_name, artwork_type, prompt, analysis, additional_details=None):
    """Save analysis to session archive with artwork type and details"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": timestamp,
        "artwork_title": image_name,
        "artwork_type": artwork_type, 
        "framework": prompt,
        "analysis": analysis,
        "additional_details": additional_details or {}
    }
    st.session_state.archive.append(entry)


# Main Header
st.markdown('<div class="header-container">', unsafe_allow_html=True)
st.markdown('<h1 class="header-title">ARTISTICA VISION</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1.1rem; opacity: 0.9;">Advanced Art Analysis & Interpretation Platform</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### Analysis Parameters")
    
    artwork_type = st.selectbox(
        "Artwork Medium",
        ["Painting", "Sculpture", "Installation Art", "Mixed Media", "Digital Art", "Photography", "Other"]
    )
    
    analysis_mode = st.selectbox(
        "Analysis Framework",
        ["Contemporary Critical Analysis",
         "Technical Composition Study",
         "Historical-Cultural Context",
         "Aesthetic Philosophy",
         "Custom Framework"]
    )
    
    if analysis_mode == "Custom Framework":
        custom_framework = st.text_input("Define Custom Framework")
    
    # Medium-specific parameters
    if artwork_type == "Sculpture":
        st.markdown("### Sculpture-Specific Parameters")
        material_analysis = st.checkbox("Material Analysis")
        spatial_analysis = st.checkbox("Spatial Relationship Analysis")
        structural_analysis = st.checkbox("Structural Integrity Analysis")
    
    view_archive = st.checkbox("View Analysis Archive")
    
    st.markdown("---")
    st.markdown("### About Artistica Vision")
    st.markdown("""
        A sophisticated platform for analyzing diverse artistic mediums 
        including paintings, sculptures, installations, and more, using 
        advanced AI-driven analytical frameworks.
    """)

# Main Content Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<h3 class="subheader">Artwork Submission</h3>', unsafe_allow_html=True)
    st.markdown(f'<div class="medium-tag">Selected Medium: {artwork_type}</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(f"Submit {artwork_type.lower()} images for analysis", type=["jpg", "jpeg", "png", "jfif"])
    
    if uploaded_file:
        st.markdown('<div class="success-message">Artwork successfully submitted for analysis</div>', unsafe_allow_html=True)
        
        # Additional inputs based on artwork type
        additional_details = {}
        if artwork_type == "Sculpture":
            st.markdown('<div class="details-card">', unsafe_allow_html=True)
            st.markdown("### Sculpture Details")
            additional_details['materials'] = st.text_input("Primary Materials Used")
            additional_details['dimensions'] = st.text_input("Dimensions (H x W x D)")
            additional_details['viewing_angles'] = st.multiselect(
                "Important Viewing Angles",
                ["Front", "Back", "Left", "Right", "Top", "Bottom", "Three-Quarter"]
            )
            st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<h3 class="subheader">Visual Preview</h3>', unsafe_allow_html=True)
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Submitted {artwork_type}", use_container_width=True)

# Analysis Configuration
if uploaded_file:
    st.markdown("---")
    st.markdown('<h3 class="subheader">Analysis Configuration</h3>', unsafe_allow_html=True)
    
    # Get the appropriate template based on artwork type
    artwork_category = artwork_type.lower() if artwork_type.lower() in ["sculpture", "painting", "installation"] else "general"
    selected_framework = analysis_frameworks[analysis_mode][artwork_category] if analysis_mode in analysis_frameworks else ""
    
    # Add medium-specific analysis points
    if artwork_type == "Sculpture":
        if material_analysis:
            selected_framework += "\n\n- Analyze material properties, texture, and surface treatment."
        if spatial_analysis:
            selected_framework += "\n\n- Evaluate spatial relationships and viewer interaction."
        if structural_analysis:
            selected_framework += "\n\n- Assess structural composition and balance."
    
    framework_col1, framework_col2 = st.columns([2, 1])
    
    with framework_col1:
        analysis_prompt = st.text_area(
            "Refine Analysis Framework:",
            value=selected_framework,
            height=100
        )
    
    with framework_col2:
        st.markdown("### Analysis Depth")
        comprehensive_analysis = st.checkbox("Comprehensive Technical Analysis")
        contextual_comparison = st.checkbox("Contextual Artist Comparisons")
        
        if comprehensive_analysis:
            analysis_prompt += "\n\nProvide exhaustive technical analysis of methodologies employed."
        if contextual_comparison:
            analysis_prompt += "\n\nPosition this work within its broader artistic context through comparative analysis."

# Generate Analysis
if uploaded_file and analysis_prompt:
    st.markdown("---")
    if st.button("Generate Analysis", type="primary"):
        with st.spinner('Conducting artwork analysis...'):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            image_data = input_image_setup(uploaded_file)
            if image_data:
                response = get_gemini_response(analysis_prompt, image_data, analysis_prompt)
                if response:
                    st.markdown('<h3 class="subheader">Generated Analysis</h3>', unsafe_allow_html=True)
                    st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
                    st.markdown(response)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Save to archive with additional details
                    additional_details = locals().get('additional_details', {})
                    save_analysis(uploaded_file.name, artwork_type, analysis_prompt, response, additional_details)
                    
                    # Download options
                    st.download_button(
                        label="Download Analysis",
                        data=response,
                        file_name=f"artistica_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )

# Display Archive
if view_archive and st.session_state.archive:
    st.markdown("---")
    st.markdown('<h3 class="subheader">Analysis Archive</h3>', unsafe_allow_html=True)
    for i, entry in enumerate(reversed(st.session_state.archive)):
        with st.expander(f"Analysis {i+1}: {entry['artwork_title']} - {entry['artwork_type']} - {entry['timestamp']}"):
            if entry.get('additional_details'):
                st.markdown("**Artwork Details:**")
                for key, value in entry['additional_details'].items():
                    st.markdown(f"- {key.title()}: {value}")
            st.markdown("**Analysis Framework:**")
            st.markdown(entry.get('framework', 'No framework provided'))
            st.markdown("**Detailed Analysis:**")
            st.markdown(entry.get('analysis', 'No analysis generated'))