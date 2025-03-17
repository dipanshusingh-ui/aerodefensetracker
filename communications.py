import streamlit as st
import pandas as pd
from data_generator import generate_comm_logs

def render_communications_page():
    st.title("📡 Satellite Communications")
    
    # Initialize communication logs in session state if not exists
    if 'comm_logs' not in st.session_state:
        st.session_state['comm_logs'] = generate_comm_logs()
    
    # Communication status overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Channels", "4")
    with col2:
        st.metric("Signal Strength", "98%")
    with col3:
        st.metric("Pending Messages", 
                 len(st.session_state['comm_logs'][st.session_state['comm_logs']['status'] == 'Pending']))
    
    # Communication logs
    st.subheader("Communication Logs")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        priority_filter = st.multiselect("Priority", ['High', 'Medium', 'Low'], default=['High', 'Medium', 'Low'])
    with col2:
        status_filter = st.multiselect("Status", ['Received', 'Pending', 'Acknowledged'], 
                                     default=['Received', 'Pending', 'Acknowledged'])
    
    # Filter logs
    filtered_logs = st.session_state['comm_logs'][
        (st.session_state['comm_logs']['priority'].isin(priority_filter)) &
        (st.session_state['comm_logs']['status'].isin(status_filter))
    ]
    
    # Display logs with custom formatting
    for _, log in filtered_logs.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                    **{log['timestamp']}** - {log['message_type']}  
                    {log['message']}
                """)
            with col2:
                priority_color = {
                    'High': 'red',
                    'Medium': 'orange',
                    'Low': 'green'
                }
                st.markdown(f"""
                    Priority: <span style='color: {priority_color[log['priority']]}'>{log['priority']}</span>  
                    Status: {log['status']}
                """, unsafe_allow_html=True)
            st.divider()
