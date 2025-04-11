ATS Resume Score Calculator 🧠📄
This is a Streamlit-based web application that analyzes a user's resume and compares it with a job description to generate an ATS (Applicant Tracking System) Score. It highlights missing keywords, provides similarity metrics, and offers tips for improving the resume to make it more job-relevant.

📌 Project Overview
In today's hiring processes, many resumes are first screened by automated systems (ATS) that look for keyword relevance. This project helps users:

Upload a resume in PDF format

Paste a job description

Analyze the keyword overlap and semantic similarity

Get a score representing how well the resume aligns with the job description

Receive feedback on missing keywords and optimization tips

⚙️ How to Run the Project
Clone the repository and navigate to the project folder

(Optional) Create and activate a virtual environment

Install the required dependencies listed in the requirements.txt file

Download NLTK resources if not already downloaded:

punkt

stopwords

averaged_perceptron_tagger

wordnet

Run the Streamlit app using the streamlit run app.py command

🧰 Tools & Dependencies Used
Streamlit – Web UI framework for creating the app

NLTK – Text processing, tokenization, synonym expansion

pdfplumber – Extracts text from PDF resumes

scikit-learn – TF-IDF vectorization and cosine similarity

Pillow (PIL) – Image handling for UI styling

base64, io, re, collections – Supporting libraries for image encoding and text processing

🖼️ UI Highlights
Clean and styled sidebar navigation

Background image for aesthetic appeal

ATS score display with custom feedback

Bar chart visualization of keyword match

Tips section to help improve resume quality

📄 Folder Structure
app.py – Main Streamlit app file

img1.jpg – Background image used in UI

requirements.txt – Python dependencies

README.md – Project documentation

💡 Future Improvements
Add support for .docx resume uploads

Improve NLP with named entity recognition and lemmatization

Add keyword weighting customization

Generate resume improvement suggestions using LLMs (e.g., GPT)

📃 License
This project is open-source and licensed under the MIT License.

🤝 Contributions
Feel free to fork this repository, raise issues, and submit pull requests to enhance the project.