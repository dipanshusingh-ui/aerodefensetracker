
import streamlit as st

# Configure Streamlit page before any other imports
st.set_page_config(
    page_title="Aerospace Defense System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Now import all other dependencies
import folium
from streamlit_folium import folium_static
from auth import login, check_authentication
from inventory import render_inventory_page
from communications import render_communications_page
from data_generator import generate_aircraft_data
from styles import apply_custom_styles
from export_utils import render_export_page

def main():
    # Apply custom styles
    apply_custom_styles()

    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state['page'] = 'dashboard'
    if 'sidebar_expanded' not in st.session_state:
        st.session_state['sidebar_expanded'] = False

    # Authentication check
    if not check_authentication():
        login()
    else:
        # Sidebar navigation
        st.sidebar.markdown(f"Welcome, {st.session_state['username']}")
        st.sidebar.title("Menu")

        pages = {
            "Dashboard": "dashboard",
            "Inventory": "inventory",
            "Communications": "communications",
            "Export & Reports": "export"
        }

        for page_name, page_key in pages.items():
            if st.sidebar.button(page_name):
                st.session_state['page'] = page_key

        # Auto-collapse sidebar by reloading the page
        if not st.session_state["sidebar_expanded"]:
            st.markdown("<script>window.location.reload();</script>", unsafe_allow_html=True)
          
        # Logout button
        if st.sidebar.button("Logout"):
            st.session_state['authenticated'] = False
            st.rerun()

        # Page rendering
        if st.session_state['page'] == 'dashboard':
            st.title("Aerospace & Defense Home")

            # Update aircraft data periodically
            if 'aircraft_data' not in st.session_state:
                st.session_state['aircraft_data'] = generate_aircraft_data()

            # Key metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Active Aircraft", len(st.session_state['aircraft_data']))
            with col2:
                st.metric("Average Altitude", f"{st.session_state['aircraft_data']['altitude'].mean():.0f} ft")
            with col3:
                st.metric("Average Speed", f"{st.session_state['aircraft_data']['speed'].mean():.0f} knots")

            # Aircraft map
            st.subheader("Aircraft Positions")
            m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

            for _, aircraft in st.session_state['aircraft_data'].iterrows():
                folium.Marker(
                    [aircraft['latitude'], aircraft['longitude']],
                    popup=f"""
                        Aircraft: {aircraft['aircraft_id']}<br>
                        Type: {aircraft['type']}<br>
                        Altitude: {aircraft['altitude']:.0f} ft<br>
                        Speed: {aircraft['speed']:.0f} knots
                    """,
                    icon=folium.Icon(color='red', icon='plane', prefix='fa')
                ).add_to(m)

            with st.container():
              folium_static(m, width=800)
              st.markdown('</div>', unsafe_allow_html=True)

            # Aircraft list
            st.subheader("Active Aircraft")
            st.dataframe(st.session_state['aircraft_data'], use_container_width=True)

        elif st.session_state['page'] == 'inventory':
            render_inventory_page()
        elif st.session_state['page'] == 'communications':
            render_communications_page()
        elif st.session_state['page'] == 'export':
            render_export_page()

        # Data source note
        st.markdown("Data is collected from various sources, including real-time aircraft tracking systems, operational databases, and simulations. This data is dynamically updated and visualized on the dashboard.")

if __name__ == "__main__":
    main()
