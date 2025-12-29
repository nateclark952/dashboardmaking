import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Asset Management Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data(file_path):
    """Load and preprocess the CSV data"""
    try:
        df = pd.read_csv(file_path)
        # Convert date columns if they exist
        date_columns = ['Date Added', 'Last Updated', 'Acquisition Date', 
                       'Warranty Start Date', 'Warranty End Date', 
                       'Lease Start Date', 'Lease End Date', 'Check Out Date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def main():
    st.markdown('<h1 class="main-header">📊 Asset Management Dashboard</h1>', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload your asset CSV file",
        type=['csv'],
        help="Upload the AllAssets CSV file"
    )
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is not None and not df.empty:
            # Sidebar filters
            st.sidebar.header("🔍 Filters")
            
            # Company filter
            if 'Company' in df.columns:
                companies = ['All'] + sorted(df['Company'].dropna().unique().tolist())
                selected_company = st.sidebar.selectbox("Company", companies)
                if selected_company != 'All':
                    df = df[df['Company'] == selected_company]
            
            # Building filter
            if 'Building' in df.columns:
                buildings = ['All'] + sorted(df['Building'].dropna().unique().tolist())
                selected_building = st.sidebar.selectbox("Building", buildings)
                if selected_building != 'All':
                    df = df[df['Building'] == selected_building]
            
            # Room filter
            if 'Room Name' in df.columns:
                rooms = ['All'] + sorted(df['Room Name'].dropna().unique().tolist())
                selected_room = st.sidebar.selectbox("Room", rooms)
                if selected_room != 'All':
                    df = df[df['Room Name'] == selected_room]
            
            # Status filter
            if 'Status' in df.columns:
                statuses = ['All'] + sorted(df['Status'].dropna().unique().tolist())
                selected_status = st.sidebar.selectbox("Status", statuses)
                if selected_status != 'All':
                    df = df[df['Status'] == selected_status]
            
            # Active filter
            if 'Active' in df.columns:
                active_filter = st.sidebar.selectbox("Active Status", ['All', 'Yes', 'No'])
                if active_filter != 'All':
                    df = df[df['Active'] == active_filter]
            
            # Main dashboard
            st.markdown("---")
            
            # Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_assets = len(df)
                st.metric("Total Assets", f"{total_assets:,}")
            
            with col2:
                if 'Building' in df.columns:
                    unique_buildings = df['Building'].nunique()
                    st.metric("Buildings", unique_buildings)
                else:
                    st.metric("Buildings", "N/A")
            
            with col3:
                if 'Room Name' in df.columns:
                    unique_rooms = df['Room Name'].nunique()
                    st.metric("Rooms", unique_rooms)
                else:
                    st.metric("Rooms", "N/A")
            
            with col4:
                if 'Active' in df.columns:
                    active_count = len(df[df['Active'] == 'Yes'])
                    st.metric("Active Assets", f"{active_count:,}")
                else:
                    st.metric("Active Assets", "N/A")
            
            st.markdown("---")
            
            # Tabs for different views
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📈 Overview", 
                "🏢 By Location", 
                "📅 Timeline Analysis", 
                "💰 Financial", 
                "📋 Data Table"
            ])
            
            with tab1:
                st.header("Asset Overview")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Assets by Building
                    if 'Building' in df.columns:
                        building_counts = df['Building'].value_counts().head(10)
                        fig_building = px.bar(
                            x=building_counts.index,
                            y=building_counts.values,
                            title="Assets by Building (Top 10)",
                            labels={'x': 'Building', 'y': 'Number of Assets'},
                            color=building_counts.values,
                            color_continuous_scale='Blues'
                        )
                        fig_building.update_layout(showlegend=False)
                        st.plotly_chart(fig_building, use_container_width=True)
                
                with col2:
                    # Assets by Room
                    if 'Room Name' in df.columns:
                        room_counts = df['Room Name'].value_counts().head(10)
                        fig_room = px.pie(
                            values=room_counts.values,
                            names=room_counts.index,
                            title="Assets by Room (Top 10)"
                        )
                        st.plotly_chart(fig_room, use_container_width=True)
                
                # Active vs Inactive
                if 'Active' in df.columns:
                    active_counts = df['Active'].value_counts()
                    fig_active = px.bar(
                        x=active_counts.index,
                        y=active_counts.values,
                        title="Active vs Inactive Assets",
                        labels={'x': 'Status', 'y': 'Count'},
                        color=active_counts.index,
                        color_discrete_map={'Yes': '#2ecc71', 'No': '#e74c3c'}
                    )
                    fig_active.update_layout(showlegend=False)
                    st.plotly_chart(fig_active, use_container_width=True)
            
            with tab2:
                st.header("Location Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Building distribution
                    if 'Building' in df.columns:
                        building_df = df.groupby('Building').size().reset_index(name='Count')
                        building_df = building_df.sort_values('Count', ascending=False)
                        
                        fig = px.treemap(
                            building_df,
                            path=['Building'],
                            values='Count',
                            title="Asset Distribution by Building"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Room distribution
                    if 'Room Name' in df.columns and 'Building' in df.columns:
                        room_building = df.groupby(['Building', 'Room Name']).size().reset_index(name='Count')
                        room_building = room_building.sort_values('Count', ascending=False).head(20)
                        
                        fig = px.sunburst(
                            room_building,
                            path=['Building', 'Room Name'],
                            values='Count',
                            title="Asset Distribution: Building → Room"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                # Interactive map-like view
                if 'Building' in df.columns and 'Room Name' in df.columns:
                    location_summary = df.groupby(['Building', 'Room Name']).size().reset_index(name='Asset Count')
                    location_summary = location_summary.sort_values('Asset Count', ascending=False)
                    
                    st.subheader("Location Summary Table")
                    st.dataframe(
                        location_summary,
                        use_container_width=True,
                        hide_index=True
                    )
            
            with tab3:
                st.header("Timeline Analysis")
                
                # Date Added analysis
                if 'Date Added' in df.columns:
                    df['Date Added'] = pd.to_datetime(df['Date Added'], errors='coerce')
                    df_with_date = df.dropna(subset=['Date Added'])
                    
                    if not df_with_date.empty:
                        df_with_date['Date'] = df_with_date['Date Added'].dt.date
                        daily_additions = df_with_date.groupby('Date').size().reset_index(name='Assets Added')
                        daily_additions = daily_additions.sort_values('Date')
                        
                        fig = px.line(
                            daily_additions,
                            x='Date',
                            y='Assets Added',
                            title="Assets Added Over Time",
                            markers=True
                        )
                        fig.update_traces(line_color='#1f77b4', line_width=2)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Monthly aggregation
                        df_with_date['Year-Month'] = df_with_date['Date Added'].dt.to_period('M').astype(str)
                        monthly_additions = df_with_date.groupby('Year-Month').size().reset_index(name='Assets Added')
                        
                        fig_monthly = px.bar(
                            monthly_additions,
                            x='Year-Month',
                            y='Assets Added',
                            title="Assets Added by Month",
                            color='Assets Added',
                            color_continuous_scale='Blues'
                        )
                        st.plotly_chart(fig_monthly, use_container_width=True)
                
                # Last Updated analysis
                if 'Last Updated' in df.columns:
                    df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')
                    df_updated = df.dropna(subset=['Last Updated'])
                    
                    if not df_updated.empty:
                        df_updated['Update Date'] = df_updated['Last Updated'].dt.date
                        daily_updates = df_updated.groupby('Update Date').size().reset_index(name='Assets Updated')
                        daily_updates = daily_updates.sort_values('Update Date')
                        
                        fig = px.area(
                            daily_updates,
                            x='Update Date',
                            y='Assets Updated',
                            title="Assets Updated Over Time",
                            color_discrete_sequence=['#2ecc71']
                        )
                        st.plotly_chart(fig, use_container_width=True)
            
            with tab4:
                st.header("Financial Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Cost analysis
                    if 'Cost' in df.columns:
                        df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
                        cost_data = df.dropna(subset=['Cost'])
                        
                        if not cost_data.empty:
                            total_cost = cost_data['Cost'].sum()
                            avg_cost = cost_data['Cost'].mean()
                            median_cost = cost_data['Cost'].median()
                            
                            st.metric("Total Asset Value", f"${total_cost:,.2f}")
                            st.metric("Average Asset Cost", f"${avg_cost:,.2f}")
                            st.metric("Median Asset Cost", f"${median_cost:,.2f}")
                            
                            # Cost distribution
                            fig = px.histogram(
                                cost_data,
                                x='Cost',
                                nbins=50,
                                title="Asset Cost Distribution",
                                labels={'Cost': 'Cost ($)', 'count': 'Number of Assets'}
                            )
                            st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Depreciation analysis
                    if 'Depreciated Value' in df.columns:
                        df['Depreciated Value'] = pd.to_numeric(df['Depreciated Value'], errors='coerce')
                        dep_data = df.dropna(subset=['Depreciated Value'])
                        
                        if not dep_data.empty:
                            total_dep = dep_data['Depreciated Value'].sum()
                            st.metric("Total Depreciated Value", f"${total_dep:,.2f}")
                            
                            if 'Amount Depreciated' in df.columns:
                                df['Amount Depreciated'] = pd.to_numeric(df['Amount Depreciated'], errors='coerce')
                                amount_dep = df['Amount Depreciated'].sum()
                                st.metric("Total Amount Depreciated", f"${amount_dep:,.2f}")
                
                # Financial summary table
                financial_cols = ['Cost', 'Depreciated Value', 'Amount Depreciated', 'Scrap Value']
                available_financial = [col for col in financial_cols if col in df.columns]
                
                if available_financial:
                    st.subheader("Financial Summary by Building")
                    if 'Building' in df.columns:
                        financial_summary = df.groupby('Building')[available_financial].sum()
                        for col in available_financial:
                            financial_summary[col] = pd.to_numeric(financial_summary[col], errors='coerce')
                        financial_summary = financial_summary.fillna(0)
                        st.dataframe(financial_summary, use_container_width=True)
            
            with tab5:
                st.header("Data Table")
                
                # Search functionality
                search_term = st.text_input("🔍 Search assets", placeholder="Search by Asset ID, Description, Serial #, etc.")
                
                if search_term:
                    mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
                    display_df = df[mask]
                else:
                    display_df = df
                
                # Column selector
                st.subheader("Select Columns to Display")
                all_columns = df.columns.tolist()
                default_columns = ['Asset ID', 'Company', 'Building', 'Room Name', 'Status', 'Active', 'Date Added', 'Last Updated']
                available_defaults = [col for col in default_columns if col in all_columns]
                selected_columns = st.multiselect(
                    "Choose columns",
                    all_columns,
                    default=available_defaults
                )
                
                if selected_columns:
                    display_df = display_df[selected_columns]
                
                # Display data
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    height=600
                )
                
                # Download button
                csv = display_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download filtered data as CSV",
                    data=csv,
                    file_name=f"filtered_assets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            # Footer
            st.markdown("---")
            st.markdown(
                f"<div style='text-align: center; color: #666; padding: 1rem;'>"
                f"Total records displayed: {len(df):,} | "
                f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                f"</div>",
                unsafe_allow_html=True
            )
        else:
            st.error("The uploaded file is empty or could not be loaded.")
    else:
        st.info("👆 Please upload a CSV file to get started.")
        st.markdown("""
        ### Instructions:
        1. Click on "Browse files" or drag and drop your CSV file
        2. The dashboard will automatically load and display your asset data
        3. Use the sidebar filters to narrow down your view
        4. Explore different tabs for various analyses
        """)

if __name__ == "__main__":
    main()

