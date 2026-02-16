"""
Main Entry Point - Streamlit app initialization
This is the MVC restructured version of the trading app
"""
import streamlit as st
from controllers.app_controller import AppController

# Configure Streamlit page
st.set_page_config(
    page_title="Trading App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    h1 {
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize and run the app controller
def main():
    """Main function to run the app"""
    controller = AppController()
    controller.run()

if __name__ == "__main__":
    main()
