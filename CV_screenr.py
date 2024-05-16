import PyPDF2
import openai
import streamlit as st

# Set your OpenAI API key in a secure way instead of hardcoding it into the script.
openai.api_key = 'sk-proj-ZmJN9dnPUewdYYU6suOxT3BlbkFJUYj8e5q0YUeBXO8qgWCA'


def pdf_to_text(uploaded_file):
    # Read the PDF file from the UploadedFile object
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    # Iterate over each page in the PDF
    for page in range(len(pdf_reader.pages)):
        # Extract text from each page and concatenate it to the text variable
        text += pdf_reader.pages[page].extract_text()
    return text


def analyze_cv(cv_text, job_profile):
    # Construct a prompt for the OpenAI model to follow for analysis
    prompt = f"""
### Job Profile
{job_profile}

### CV
{cv_text}

### Contextually aware & Industry-specific skills Analysis
Analyze the CV and job description in the context of the [industry/sector]. Identify the key industry-specific 
skills required for the job and evaluate the candidate’s proficiency in these skills based on their CV. 
Provide a rating from 1 to 10 and justify your assessment with specific examples.

### Relevant experience Analysis
Considering the responsibilities outlined in the job description for the role of [specific job title], 
assess the candidate’s relevant experience as detailed in their CV. Highlight specific past roles or projects 
that demonstrate their suitability for this position. 
Provide a suitability score from 1 to 10 with detailed explanations.

### Soft skills Analysis
Examine the candidate’s soft skills and personal attributes as described in the CV. How do these align with the soft skills 
and cultural attributes emphasized in the job description? 
Provide a rating from 1 to 10 and explain your reasoning with specific examples.

#### Strong Points
- Identify the areas where the candidate's CV aligns well with the job profile requirements.

#### Weak Points & Recommendations for Improvement
- List the areas where the candidate's CV does not meet the job profile requirements, and suggest how the candidate might improve these aspects.

#### Conclusion
- Summarize the overall fit of the candidate for the position based on the CV and job profile.

#### Final CV Score
- Evaluate the final CV score based on Industry-specific skills Analysis, Relevant experience Analysis, 
Soft skills Analysis & Weak points.

### Table of Results
- Provide a table summarizing the strong points, weak points, recommendations for improvement, conclusion, and final CV score.
"""

    # Call the OpenAI API using the created prompt for text analysis
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=3500
    )

    # Extract the content from the response received from the API
    analysis = response.choices[0].message.content.strip()
    return analysis


st.title("CV Analyzer")

st.write("Enter Job Profile:")
job_profile = st.text_area("Job Profile", height=200)

uploaded_file = st.file_uploader("Upload CV PDF", type=["pdf"])

if uploaded_file is not None:
    # Convert the uploaded PDF file to text
    cv_text = pdf_to_text(uploaded_file)
    st.write("CV Uploaded Successfully")

    if st.button("Submit Analysis"):
        if job_profile.strip() == "":
            st.error("Please enter a job profile before submitting.")
        else:
            # Analyze the CV using the extracted text and job profile
            analysis = analyze_cv(cv_text, job_profile)
            # Display the analysis result
            st.subheader("Analysis Result")
            st.text_area("Result", analysis, height=400)
