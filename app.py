# app.py
import streamlit as st
from pdf_utils import extract_text_from_pdf_bytes
from ocr_utils import ocr_image_pil
from llm_engine import answer_with_llm

st.set_page_config(page_title="Mini Legal AI Demo", layout="centered")
st.title("Mini Legal AI — Demo (OCR + LLM)")

st.markdown("Upload a PDF/image (contract) → type a question → get an answer based on uploaded text. **Demo only — not legal advice.**")

uploaded_file = st.file_uploader("Upload a PDF or image", type=["pdf", "png", "jpg", "jpeg"])
extracted_text = ""

if uploaded_file:
    file_type = uploaded_file.type
    if file_type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
        st.info("Extracting text from PDF...")
        extracted_text = extract_text_from_pdf_bytes(uploaded_file.read())
    else:
        st.info("Running OCR on image...")
        from PIL import Image
        image = Image.open(uploaded_file)
        extracted_text = ocr_image_pil(image)
#hi how are you

    #name is umer yasin
#hello



    st.subheader("Extracted text")
    st.text_area("Document text", value=extracted_text[:10000], height=250)

user_question = st.text_input("Ask a question about this document:")

if st.button("Get Answer"):
    if not extracted_text.strip() and not user_question.strip():
        st.warning("Upload a document and/or type a question first.")
    else:
        with st.spinner("Contacting LLM..."):
            prompt_context = extracted_text
            answer = answer_with_llm(context=prompt_context, question=user_question)
        st.subheader("Answer")
        st.write(answer)
        st.info("⚠️ Demo only — informational. Verify with a lawyer before taking action.")
