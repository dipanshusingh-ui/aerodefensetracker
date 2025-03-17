import streamlit as st
import pandas as pd
from database import Database
from styles import apply_custom_styles


def render_inventory_page():
  apply_custom_styles()
  st.title("Inventory Management")

  db = Database()

  # Add new item form with improved styling
  with st.expander("Add New Item", expanded=False):
    st.markdown('<div class="inventory-form">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
      new_item_name = st.text_input("Item Name")
      new_quantity = st.number_input("Quantity", min_value=0)
    with col2:
      new_status = st.selectbox("Status",
                                ["Available", "In Use", "Maintenance"],
                                index=0)
      categories = [
          "Engine Parts", "Avionics", "Landing Gear", "Fuel Systems",
          "Electronics", "Other"
      ]
      st.selectbox("Category", categories)

    notes = st.text_area(
        "Notes", placeholder="Enter any additional notes about the item")

    if st.button("Add Item", key="add_item"):
      if not new_item_name:
        st.error("Item name is required")
      else:
        new_id = f"INV{pd.Timestamp.now().strftime('%H%M%S')}"
        item_data = {
            'item_id': new_id,
            'item_name': new_item_name,
            'quantity': new_quantity,
            'status': new_status
        }
        db.insert_inventory_item(item_data)
        st.success(f"Added item {new_item_name} to inventory")
    st.markdown('</div>', unsafe_allow_html=True)

  # Inventory filters
  st.subheader("Inventory Search")
  col1, col2 = st.columns(2)
  with col1:
    status_filter = st.multiselect(
        "Filter by Status", ["Available", "In Use", "Maintenance"],
        default=["Available", "In Use", "Maintenance"])
  with col2:
    search_term = st.text_input("Search Items",
                                placeholder="Enter item name or ID")

  # Display inventory with filters
  inventory_data = db.get_all_inventory()
  if status_filter:
    inventory_data = inventory_data[inventory_data['status'].isin(
        status_filter)]
  if search_term:
    mask = (inventory_data['item_name'].str.contains(
        search_term, case=False, na=False)
            | inventory_data['item_id'].str.contains(
                search_term, case=False, na=False))
    inventory_data = inventory_data[mask]

  # Display inventory statistics
  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric("Total Items", len(inventory_data))
  with col2:
    available_items = len(
        inventory_data[inventory_data['status'] == 'Available'])
    st.metric("Available Items", available_items)
  with col3:
    maintenance_items = len(
        inventory_data[inventory_data['status'] == 'Maintenance'])
    st.metric("Items in Maintenance", maintenance_items)

  # Display inventory table with improved styling
  st.subheader("Current Inventory")
  st.dataframe(inventory_data,
               use_container_width=True,
               hide_index=True,
               column_config={
                   "item_id": "ID",
                   "item_name": "Item Name",
                   "quantity": "Quantity",
                   "status": "Status",
                   "last_updated": "Last Updated"
               })

  db.close()
