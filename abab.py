import streamlit as st
import nltk
import re
import string
import pdfplumber
from nltk.corpus import stopwords
from collections import Counter
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import base64
import io

# Ensure NLTK resources are available
def download_nltk_resources():
    required_resources = ['punkt', 'stopwords', 'averaged_perceptron_tagger', 'wordnet']
    for resource in required_resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
            except Exception as e:
                st.error(f"Failed to download NLTK resource: {resource}, Error: {e}")

# Download resources at the start
download_nltk_resources()

# Preprocessing function to clean and tokenize text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return tokens

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""
    return text if text else "No text extracted. Please upload a readable PDF."

# Function to expand keywords using synonyms
def expand_keywords(keywords):
    expanded_keywords = set(keywords)
    for word in keywords:
        for syn in wn.synsets(word):
            for lemma in syn.lemmas():
                expanded_keywords.add(lemma.name())
    return expanded_keywords

# Function to calculate ATS Score using Keyword Matching and TF-IDF
def calculate_ats_score(resume_text, job_description):
    resume_tokens = preprocess_text(resume_text)
    job_description_tokens = preprocess_text(job_description)

    expanded_resume_keywords = expand_keywords(resume_tokens)
    expanded_job_description_keywords = expand_keywords(job_description_tokens)

    resume_word_counts = Counter(resume_tokens)
    job_description_word_counts = Counter(job_description_tokens)

    common_keywords = expanded_resume_keywords.intersection(expanded_job_description_keywords)
    match_score = sum([resume_word_counts[key] * job_description_word_counts[key] for key in common_keywords])

    total_keywords_in_resume = sum(resume_word_counts.values())
    total_keywords_in_job_description = sum(job_description_word_counts.values())

    if total_keywords_in_resume == 0 or total_keywords_in_job_description == 0:
        return 0.0, [], job_description_tokens

    scaled_match_score = match_score * 2.5

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    weighted_score = (scaled_match_score * 0.6) + (cosine_sim * 100 * 0.4)
    normalized_score = min(100, max(0, weighted_score))

    missing_keywords = list(set(job_description_tokens) - set(resume_tokens))

    return round(normalized_score, 2), missing_keywords, job_description_tokens

# Convert image to base64
def image_to_base64(image: Image):
    img_buffer = io.BytesIO()
    image.save(img_buffer, format="JPEG")
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    return img_str

# Sidebar Styling
st.sidebar.markdown("""
    <style>
    [data-testid=stSidebar] {
        background-color: #000000 !important;
    }

    /* General sidebar text color */
    [data-testid=stSidebar] * {
        color: white !important;
    }

    /* Radio button selected option */
    [data-testid=stRadio] > label > div:has(input:checked) {
        background-color: rgba(0, 150, 200, 0.8) !important;
        font-weight: bold !important;
    }

    /* Hover effects */
    .st-bd:hover, .st-be:hover {
        background-color: rgba(0, 100, 150, 0.7) !important;
        transform: scale(1.05) !important;
    }

    /* Navigation links */
    [data-testid=stSidebarNav] a {
        color: white !important;
    }
    [data-testid=stSidebarNav] a:hover {
        color: #00CED1 !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to:", ["Home", "ATS Score Calculator", "Tips"])

# Background image
image = Image.open("img1.jpg")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{image_to_base64(image)}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
    }}
    </style>
    """, unsafe_allow_html=True)

# Home Page
if selection == "Home":
    st.title("Welcome to the ATS Resume Score Calculator App")
    st.write("Upload your resume and a job description to get a similarity score and feedback.")

# ATS Score Calculator
elif selection == "ATS Score Calculator":
    st.title("ATS Resume Score Calculator")

    st.subheader("Upload your resume (PDF)")
    uploaded_resume = st.file_uploader("Choose a PDF file", type=["pdf"])

    st.subheader("Paste the Job Description")
    job_description = st.text_area("Job Description", height=200)

    if uploaded_resume and job_description:
        with st.spinner("Processing..."):
            resume_text = extract_text_from_pdf(uploaded_resume)
            if resume_text.startswith("No text extracted"):
                st.error(resume_text)
            else:
                score, missing_keywords, job_description_tokens = calculate_ats_score(resume_text, job_description)
                st.markdown(f'<div style="color:white; font-size:24px; font-weight:bold;">ATS Resume Score: {score}%</div>', unsafe_allow_html=True)

                if missing_keywords:
                    st.write("### 🔍 Personalized Feedback:")
                    st.markdown(f'<div style="color:#FFB6C1; font-size:18px;">Your resume is missing the following important keywords from the job description:</div>', unsafe_allow_html=True)
                    st.markdown(", ".join(f"**{word}**" for word in missing_keywords))
                else:
                    st.success("✅ Great! Your resume covers most of the important keywords from the job description.")

                # Bar chart
                matched_keywords_count = len(set(job_description_tokens)) - len(missing_keywords)
                missing_keywords_count = len(missing_keywords)

                st.write("### 📊 Keyword Match Summary")
                st.bar_chart({
                    "Keywords": {
                        "Matched": matched_keywords_count,
                        "Missing": missing_keywords_count
                    }
                })

# Tips Page
elif selection == "Tips":
    st.title("ATS Optimization Tips")
    st.write("- **Use Keywords**: Ensure your resume contains keywords from the job description.")
    st.write("- **Simple Layout**: Keep the layout simple to avoid formatting issues.")
    st.write("- **Use Standard Fonts**: Avoid unusual fonts that may not be recognized.")
    st.write("- **File Format**: Use text-based PDF (not scanned images).")
