from pathlib import Path

import streamlit as st  # pip install streamlit
from PIL import Image  # pip install pillow

import base64

import streamlit.components.v1 as components

# --- PATH SETTINGS ---
THIS_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
ASSETS_DIR = THIS_DIR / "assets"
STYLES_DIR = THIS_DIR / "styles"
CSS_FILE = STYLES_DIR / "main.css"

def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

st.set_page_config(
    page_title="Edward Ang",
    page_icon=f"{ASSETS_DIR}/logo.png",
)
load_css_file(CSS_FILE)

############ SIDEBAR ##################

st.sidebar.success("Select a case study above.")
with st.sidebar:
    # --- CONTACT FORM ---
    # video tutorial: https://youtu.be/FOULV9Xij_8
    st.subheader("Let's get in contact")
    contact_form = f"""
    <form action="https://formsubmit.co/edward.ang14@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit" class="button">Send ✉</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)

    # st.write("")
    st.write("---")

    linkedin, medium, github = st.columns(3)

    linkedin.markdown("""
                        <a href='https://www.linkedin.com/in/edward-ang-a9a0a6aa/'>
                        <img src='https://img.icons8.com/?size=48&id=13930&format=png'></a>
                        """, unsafe_allow_html=True)

    medium.markdown("""
                        <a href='https://medium.com/@edward.ang14'>
                        <img src='https://img.icons8.com/?size=50&id=XVNvUWCvvlD9&format=png'></a>
                        """, unsafe_allow_html=True)

    github.markdown("""
                        <a href='https://github.com/edwardang'>
                        <img src='https://img.icons8.com/material-outlined/48/000000/github.png'></a>
                        """, unsafe_allow_html=True)
    
############# PAGE START ##################

st.header('Welcome 👋')
st.write("""
         My name is Edward and I'm a business oriented data scientist. I love to write, code, and think.

         I have a passion for business and will help your business make more money. 
         """)


col1, col2 = st.columns((2,2))


with col1:
    st.image(f'{ASSETS_DIR}/headshot.png',caption='Me in Los Angeles, CA')

with col2:
    st.write('Highlights')
    
    faq = {
    "Question 1": 'asdf',
    "Question 2": 'asdf',
    "Question 3": 'asdfasdf'
}
    for question, Answer in faq.items():
        with st.expander(question):
            st.write(Answer)
            







tab1, tab2, tab3 = st.tabs(['About Me', 'Resume','More Information'])
with tab1:
    st.write("""
Hello, my name is Edward. Thanks for visiting my website. 
        
I am a business oriented data scientist that specializes in optimizing business operations through insights derived from advanced analytics. 
        
I did my undergrad at Carnegie Mellon Universtiy and graduated with a B.S. in Statistics and Machine Learning in 2018.
        
I have 5 years of experience working in the technical consulting industry at IBM.
        
I am passionate about people as well. What good are insights if you aren't able to communicate the value to the people whom it will benefit. 
        
Eclectic interests. Tennis, nutrition, Poker, game theory, social psychology, sociology, etc. I'm a great conversationalist and love to connect with people. I write on Medium and Quora to convey my ideas and let the world know what I'm up to. 
        
I've done music production. Affiliate marketing. 
        
I love to read. My favorite books are the Power of Now by Eckhart Tolle. Also business books. Pricing. Lean Startup. 

I do sales and marketing too.
        
I want to be part of a fast growing startup. Scrappy and no rules. Wear many hats. Want to be part of something where my unique opinions and contributions matter, and can actually see the results. 

""")

with tab2:
    displayPDF(f'{ASSETS_DIR}/EdwardAng_Resume_2023.pdf')


with tab3:
    st.write('tab3')

