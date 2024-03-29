
import streamlit as st
from analyze import analyze
from about import about
from compare import compare
from API import API
if 'learnMore' not in st.session_state:
	st.session_state.learnMore = True
if 'count2' not in st.session_state:
	st.session_state.count2 = 0
if 'count3' not in st.session_state:
	st.session_state.count3 = 0

st.image("Vito.png")
st.title("Vito")
st.subheader("Detecting Infectious Diseases With Wearables")
st.caption("We at Vito believe you its vital to be able to learn more about your health without invading privacy.  Vito empowers you to explore your health via your vitals and on-device machine learning.")
col1, col2, col3 = st.columns(3)
start = col1.button("Analyze")
if start:
    st.session_state.learnMore = False
# compareBtn = col2.button("Compare")
st.session_state.learnMore = col2.button("About")

if st.session_state.learnMore:
    about()
   
else:
    analyze()


# if compareBtn:
#     st.session_state.count3 += 1

# if  st.session_state.count3 > 0:
#         compare()

