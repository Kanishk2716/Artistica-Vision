# Artistica Vision 🎨  
Advanced Art Analysis & Interpretation Platform  

**Artistica Vision** is an AI-driven platform designed to provide in-depth analysis and interpretation of artworks across various mediums, including paintings, sculptures, installations, and more. Leveraging the power of Generative AI, it offers insights into the technical, historical, cultural, and aesthetic aspects of submitted artworks.  

---

## Features 🚀  

### 🖼️ Artwork Submission  
- Upload images of artworks in formats like `JPG`, `JPEG`, `PNG`, or `JFIF`.  
- Visual preview of uploaded artwork within the app.  

### 🧠 Advanced Analysis Frameworks  
Choose from pre-defined analysis frameworks:  
1. **Contemporary Critical Analysis**  
2. **Technical Composition Study**  
3. **Historical-Cultural Context**  
4. **Aesthetic Philosophy**  
5. **Custom Frameworks** (Define your own analysis approach).  

### 🏺 Medium-Specific Parameters  
Tailored analysis options based on artwork medium:  
- **Sculpture**: Material analysis, spatial relationship, and structural integrity.  
- **Painting**: Composition, color theory, and brushwork.  
- **Installation Art**: Spatial dynamics and viewer interaction.  

### 📝 Analysis Archive  
- Save generated analyses with metadata, such as title, medium, framework, and additional details.  
- View past analyses through an archive feature.  

### 📥 Download Options  
- Export generated analyses as text files.  

---

## Tech Stack 💻  

- **Frontend:** [Streamlit](https://streamlit.io/) for interactive UI.  
- **Backend:**  
  - `Pillow` for image handling.  
  - `google.generativeai` for artwork analysis (powered by the Gemini Model).  
  - `dotenv` for managing environment variables.  
- **Deployment:** Python-based with lightweight requirements.  

---

## Installation 🔧  

1. Clone the repository:  
   
    - git clone https://github.com/your-username/artistica-vision.git
    - cd artistica-vision
   
3. Install dependencies:

    - pip install -r requirements.txt
   
3. Set up environment variables:

    - Create a .env file in the root directory.
    - Add your Google Generative AI API key:
    - GOOGLE_API_KEY=your_api_key_here
4. Run the app:

    - streamlit run app.py
      
# Usage Guide 📖

Upload an Artwork: Choose the medium and upload an image.
Select Analysis Framework: Choose from pre-defined or custom frameworks.
Generate Analysis: Click "Generate Analysis" to receive insights.
View Archive: Access past analyses from the sidebar.

# Project Structure 📂

artistica-vision/
├── app.py                # Main application code
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variable file
├── README.md             # Project documentation
└── archive/              # Optional folder for storing saved analyses

# Fork the repository.

 - Create your feature branch: git checkout -b feature-name.
 - Commit your changes: git commit -m 'Add feature'.
 - Push to the branch: git push origin feature-name.
 - Open a Pull Request.

# License 📜

This project is licensed under the MIT License.

# Acknowledgments 🙌

Google Generative AI: For powering advanced art analysis.
Streamlit: For providing an intuitive framework for building interactive web apps.
