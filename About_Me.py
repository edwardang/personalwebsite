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

st.header('Welcome, my name is Edward 👋.')
st.write("""
         I'm a business oriented data scientist. I love to write, code, and analyze.

         I have a passion for everything business and technology, and will help your organization meet its goals through advanced analytics.   
         """)


col1, col2 = st.columns((2,2))


with col1:
    st.image(f'{ASSETS_DIR}/headshot.png',caption='Me in Los Angeles, CA')

with col2:
    st.subheader('Highlights of my Writing')
    
    highlights = {
    "Increasing Revenue at Universal Studios Hollywood": 'https://medium.com/@edward.ang14/improving-universal-studios-hollywood-revenue-streams-a023a4a15fa7',
    "Is an Equinox Gym Membership worth the cash? If so, are they leaving money on the table?": 'https://medium.com/@edward.ang14/is-an-equinox-gym-membership-worth-the-cash-if-so-are-they-leaving-money-on-the-table-a8eb7fb09cdc'
}
    for title, link in highlights.items():
        with st.expander(title):
            st.write(link)
            

tab1, tab2, tab3 = st.tabs(['About Me', 'Resume','More Information'])
with tab1:
    st.subheader('2014 - 2018')

    col1, col2 = st.columns((5,2))


    with col1:
        st.write("""
    I did my undergrad at Carnegie Mellon University in Pittsburgh, PA, and graduated with a B.S. in Statistics and Machine Learning and a minor in Business Administration. 

    Although I learned a lot, most of the school work was too theoretical for my liking. I wanted to work on things that were more practical and applicable in the real world. 

    I completed two data science internships while in school. One was at an e-commerce startup and one was at Goodyear Tire and Rubber company. 
                
    I learned the importance of good communication especially when working on an analytics team through those internships. 
                
    Your insights are only valuable if you get key decision makers to buy into your vision. That motivated me to dedicate a significant amount of time towards perfecting my communication and social skills. 
                """)
        
    with col2:
        for i in range(5):
            st.write("")
        st.image(f'{ASSETS_DIR}/CMU_logo.png', width=180)
    
    st.write("")
    st.write("---")

    st.header('2018-2023')

    col1, col2 = st.columns((2,5))
    with col1:
        for i in range(9):
            st.write("")
        st.image(f'{ASSETS_DIR}/ibm_logo.png', width=180)

    with col2:
        st.write("""
    I started my full time career at IBM in their advanced analytics consulting sector. 
                
    I chose consulting because I wanted exposure to a wide variety of projects and teams, to travel around the world, and to sharpen my communication skills. IBM is known for their leadership in technical consulting, which is another reason why I chose to work there. 
                
    As expected, I worked on many different projects at IBM including inventory optimization, energy consumption forecasting, OCR software development, and sentiment analysis just to name a few. 
                 
    I've worn many hats such as being a data scientist, data engineer, MLOps engineer, project manager, solution architect, and account executive - each for months at a time. 
                
    I worked my way from an entry level consultant to a manager.
            """)


    st.write("")
    st.write("---")

    st.subheader('2023-Present')
    st.write("""
    I would like to shift my focus and become more specialized. I'm interested in price optimization and experimental design at any company that does business online. 
             
    Contact me for more information.
        """)

with tab2:
    displayPDF(f'{ASSETS_DIR}/EdwardAng_Resume_2023.pdf')


with tab3:
    st.write('Section in progress 🛠️')

