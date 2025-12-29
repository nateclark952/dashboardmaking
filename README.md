# Asset Management Dashboard

A comprehensive Streamlit dashboard for visualizing and analyzing asset management data.

## Features

- 📊 **Interactive Visualizations**: Charts and graphs powered by Plotly
- 🔍 **Advanced Filtering**: Filter by Company, Building, Room, Status, and Active status
- 📈 **Multiple Analysis Views**:
  - Overview: Asset distribution and statistics
  - Location Analysis: Building and room breakdowns
  - Timeline Analysis: Asset additions and updates over time
  - Financial Analysis: Cost, depreciation, and financial metrics
  - Data Table: Searchable, filterable data table with export functionality
- 💾 **Data Export**: Download filtered data as CSV
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run dashboard.py
```

2. Upload your CSV file using the file uploader
3. Use the sidebar filters to narrow down your data
4. Explore different tabs for various analyses

## File Structure

```
.
├── dashboard.py          # Main Streamlit application
├── requirements.txt      # Python dependencies
└── README.md           # This file
```

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- NumPy

## Notes

- The dashboard automatically handles date parsing for date columns
- All visualizations are interactive and can be zoomed/panned
- Data is cached for better performance
- The dashboard supports large datasets efficiently

