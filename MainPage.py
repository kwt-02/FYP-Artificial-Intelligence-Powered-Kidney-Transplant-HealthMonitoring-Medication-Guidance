import streamlit as st
from streamlit_option_menu import option_menu
from Kidney import monitor_kidney_page
from Chatbot import chatbot_page

def home_page():
    st.title('Health Monitoring System 🧑‍⚕️')
    st.write("Welcome to our Health Monitoring System 👋. This system is designed to assist you with kidney health analysis and to provide reliable information on anti-immunosuppressant medications.")
    
    st.header('Start Guide ✅')
    st.markdown("**Kidney Health Monitoring:**\n- Get predictions on kidney health.\n- View personalized advice based on results.\n\n**Chatbot for Medication Queries:**\n- Ask questions and get expert-backed responses regarding medications.")

    st.subheader('Try a Quick Health Check 🔎')
    age = st.slider("Select Your Age", 18, 100, 50)
    if st.button('Analyze'):
        st.markdown("Based on your age, regular kidney health monitoring is recommended.")
    
        
def main():
    # Initialize the session state for current page if not already set
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Main Page'
    
    # Sidebar for navigation
    with st.sidebar:
        page = option_menu(
            menu_title="Main Menu",  # Title of the menu
            options=["Main Page", "Monitor Kidney", "Chatbot"],  # List of page options
            icons=["house", "clipboard-data", "chat"],  # List of icons for each option
        )
    
    # Update the current page based on sidebar selection
    st.session_state.current_page = page

    # Display the selected page based on the session state
    if st.session_state.current_page == 'Main Page' :
        home_page()
    elif st.session_state.current_page == 'Monitor Kidney':
        monitor_kidney_page()
    elif st.session_state.current_page == 'Chatbot':
        chatbot_page()
              
if __name__ == '__main__':
    main()