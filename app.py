import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Page setup
st.set_page_config(page_title="Document Detective", page_icon="🕵️‍♂️")
# --- Custom Font Injection ---
st.markdown(
    """
   <style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
</style>
    """,
    unsafe_allow_html=True
)
# -----------------------------

st.title("🕵️‍♂️ The Document Detective")
st.write("Upload a PDF, and I will answer questions based **only** on its contents.")

# Setup Sidebar
st.sidebar.header("Setup")
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

# File Uploader and Question Input
uploaded_file = st.file_uploader("Upload your PDF here", type=["pdf"])
user_question = st.text_input("What would you like to know about this document?")

# The "Ask" Button
if st.button("Ask the Detective"):
    if not api_key:
        st.warning("Please enter your Gemini API Key in the sidebar.")
    elif not uploaded_file:
        st.warning("Please upload a PDF document.")
    elif not user_question:
        st.warning("Please ask a question.")
    else:
        try:
            # 1. Read the PDF and extract text
            with st.spinner("Reading the document..."):
                pdf_reader = PdfReader(uploaded_file)
                document_text = ""
                for page in pdf_reader.pages:
                    # Extract text from each page and add it to our master string
                    extracted = page.extract_text()
                    if extracted:
                        document_text += extracted + "\n"
            
            # 2. Connect to Gemini (Using the lite model to avoid rate limits!)
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash-lite')
            
            # 3. Create the Contextual Prompt
            prompt = f"""
            You are a helpful Document Detective. 
            Read the following document text and answer the user's question based ONLY on this text.
            If the answer is not in the document, say "I cannot find the answer in the provided document."
            
            DOCUMENT TEXT:
            {document_text}
            
            USER QUESTION:
            {user_question}
            """
            
            # 4. Get the Answer
            with st.spinner("Investigating the text..."):
                response = model.generate_content(prompt)
                
            # 5. Display the result
            st.success("Case Closed!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Oops! Something went wrong: {e}")
