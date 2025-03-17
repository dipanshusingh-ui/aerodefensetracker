import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from database import Database

def export_to_excel(df, filename):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output

def export_to_csv(df, filename):
    return df.to_csv(index=False).encode('utf-8')

def get_exportable_data(data_type, filters=None):
    db = Database()
    try:
        if data_type == "inventory":
            data = db.get_all_inventory()
        elif data_type == "aircraft":
            data = db.get_all_aircraft()
        elif data_type == "communications":
            data = db.get_communications(limit=None)
        
        if filters:
            for column, value in filters.items():
                if value:
                    if isinstance(value, list):
                        data = data[data[column].isin(value)]
                    else:
                        data = data[data[column].str.contains(value, case=False, na=False)]
        
        return data
    finally:
        db.close()

def render_export_page():
    st.title("📊 Data Export and Reports")
    
    # Data type selection
    data_type = st.selectbox(
        "Select Data Type",
        ["inventory", "aircraft", "communications"],
        format_func=lambda x: x.title()
    )
    
    # Filter options
    with st.expander("🔍 Filter Options"):
        filters = {}
        if data_type == "inventory":
            status_filter = st.multiselect(
                "Status",
                ["Available", "In Use", "Maintenance"]
            )
            if status_filter:
                filters['status'] = status_filter
                
            search_term = st.text_input("Search by Item Name")
            if search_term:
                filters['item_name'] = search_term
                
        elif data_type == "aircraft":
            aircraft_type = st.multiselect(
                "Aircraft Type",
                ["F-22", "F-35", "F-16", "C-130", "KC-135"]
            )
            if aircraft_type:
                filters['type'] = aircraft_type
                
        elif data_type == "communications":
            priority_filter = st.multiselect(
                "Priority",
                ["High", "Medium", "Low"]
            )
            if priority_filter:
                filters['priority'] = priority_filter
    
    # Preview data
    data = get_exportable_data(data_type, filters)
    st.subheader("📋 Data Preview")
    st.dataframe(data.head(10), use_container_width=True)
    st.info(f"Total records: {len(data)}")
    
    # Export options
    col1, col2 = st.columns(2)
    with col1:
        export_format = st.selectbox(
            "Export Format",
            ["Excel (.xlsx)", "CSV (.csv)"]
        )
    
    with col2:
        filename = st.text_input(
            "Filename",
            value=f"{data_type}_export_{datetime.now().strftime('%Y%m%d')}"
        )
    
    if st.button("📥 Export Data"):
        try:
            if export_format == "Excel (.xlsx)":
                output = export_to_excel(data, filename)
                file_ext = "xlsx"
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            else:
                output = export_to_csv(data, filename)
                file_ext = "csv"
                mime = "text/csv"
            
            st.download_button(
                label="⬇️ Download Export",
                data=output,
                file_name=f"{filename}.{file_ext}",
                mime=mime
            )
            st.success("Export prepared successfully!")
            
        except Exception as e:
            st.error(f"Error preparing export: {str(e)}")
