import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from database import Database

def create_aircraft_scatter():
    db = Database()
    try:
        aircraft_data = db.get_all_aircraft()
        fig = px.scatter_mapbox(
            aircraft_data,
            lat='latitude',
            lon='longitude',
            hover_name='aircraft_id',
            hover_data=['type', 'altitude', 'speed'],
            color='type',
            size_max=15,
            zoom=3,
            title='Aircraft Positions'
        )
        fig.update_layout(
            mapbox_style="carto-darkmatter",
            margin={"r":0,"t":30,"l":0,"b":0},
            height=400
        )
        return fig
    finally:
        db.close()

def create_inventory_treemap():
    db = Database()
    try:
        inventory_data = db.get_all_inventory()
        fig = px.treemap(
            inventory_data,
            path=['status', 'item_name'],
            values='quantity',
            title='Inventory Distribution'
        )
        fig.update_layout(
            margin={"r":0,"t":30,"l":0,"b":0},
            height=400
        )
        return fig
    finally:
        db.close()

def create_communications_timeline():
    db = Database()
    try:
        comm_data = db.get_communications(limit=100)
        fig = px.timeline(
            comm_data,
            x_start='timestamp',
            y='priority',
            color='message_type',
            title='Communications Timeline'
        )
        fig.update_layout(
            xaxis_showgrid=True,
            height=300
        )
        return fig
    finally:
        db.close()

def render_dashboard():
    st.title("Interactive Dashboard")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        time_range = st.selectbox(
            "Time Range",
            ["Last 24 Hours", "Last Week", "Last Month"],
            index=0
        )
    with col2:
        data_type = st.multiselect(
            "Data Types",
            ["Aircraft", "Inventory", "Communications"],
            default=["Aircraft", "Inventory", "Communications"]
        )
    
    # Aircraft tracking
    if "Aircraft" in data_type:
        st.subheader("Aircraft Tracking")
        aircraft_map = create_aircraft_scatter()
        st.plotly_chart(aircraft_map, use_container_width=True)
    
    # Inventory analysis
    if "Inventory" in data_type:
        st.subheader("Inventory Analysis")
        col1, col2 = st.columns(2)
        with col1:
            inventory_tree = create_inventory_treemap()
            st.plotly_chart(inventory_tree, use_container_width=True)
        
        with col2:
            # Add inventory status distribution
            db = Database()
            try:
                inventory_data = db.get_all_inventory()
                status_counts = inventory_data['status'].value_counts()
                fig = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title='Inventory Status Distribution'
                )
                st.plotly_chart(fig, use_container_width=True)
            finally:
                db.close()
    
    # Communications analysis
    if "Communications" in data_type:
        st.subheader("Communications Analysis")
        comm_timeline = create_communications_timeline()
        st.plotly_chart(comm_timeline, use_container_width=True)
        
        # Add communication priority distribution
        db = Database()
        try:
            comm_data = db.get_communications(limit=100)
            priority_counts = comm_data['priority'].value_counts()
            fig = px.bar(
                x=priority_counts.index,
                y=priority_counts.values,
                title='Communication Priority Distribution',
                labels={'x': 'Priority', 'y': 'Count'}
            )
            st.plotly_chart(fig, use_container_width=True)
        finally:
            db.close()
