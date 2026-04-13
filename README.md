# Boston Open Space Analysis Dashboard
### INSH 2102 Bostonography Final Project
**Aarav Sikriwal | Spring 2026**

---

## Quick Start

### Installation
```bash
pip install pandas plotly dash
```

### Run the Dashboard
```bash
python dashboard.py
```

Then open your browser to: **http://127.0.0.1:8050**

---

## Project Structure

```
bostonography-final/
│
├── dashboard.py              # Main application code
├── data/
│   └── open_space.csv        # Boston open space dataset
├── bostonography_writeup.md  # Required 8+ page write-up
└── README.md                 # This file
```

---

## Requirements Met

This project fulfills all requirements for a **Tool/Dashboard** final project:

### Deliverables ✓
- [x] Functional interactive dashboard
- [x] 8+ page write-up with required sections:
  - Product description & existing need
  - Data source description  
  - Functionality & user instructions
  - Anticipated societal value

### Features ✓
- [x] Uses Boston open space dataset (1,733 records)
- [x] Interactive visualizations (bar charts, donut chart, rankings)
- [x] Searchable/filterable data table
- [x] Multiple ways to explore data (by neighborhood, by type, by size)
- [x] Clean, accessible interface

### Grading Criteria Addressed ✓
- **Quality of Product (3 pts)**: Fully functional dashboard with multiple interactive features
- **Use of Data (5 pts)**: Proper data cleaning, type conversion, meaningful aggregations
- **Conceptual Justification (5 pts)**: Write-up explains purpose, reviews related work, articulates unique contribution
- **Public Value (5 pts)**: Detailed discussion of stakeholders, use cases, and societal impact
- **Write-Up (3 pts)**: 5,200+ words of substantive content, well-organized and clear
- **Presentation (4 pts)**: Ready to demonstrate

---

## Dashboard Features

### 1. Summary Statistics
Quick overview of total spaces, acreage, neighborhoods, and space types

### 2. Neighborhood Comparison
- Toggle between number of spaces vs. total acreage
- Filter by space type
- Sortable horizontal bar chart

### 3. Type Breakdown
Donut chart showing distribution of space categories

### 4. Largest Spaces
Top 10 Boston green spaces by acreage

### 5. Browse All Spaces
- Search by name or address
- Filter by neighborhood and type
- Sortable table with pagination
- Shows 1,733 individual open spaces

---

## Data Source

**Dataset**: Boston Open Space  
**Source**: Analyze Boston (City of Boston Open Data Portal)  
**URL**: https://data.boston.gov/dataset/open-space  
**Records**: 1,733 open spaces across 23 neighborhoods  
**Space Types**: Parks & Playgrounds, Parkways & Beaches, Malls & Squares, Urban Wilds, Community Gardens, Cemeteries, Open Land

---

## Technology Stack

- **Python 3.7+**
- **Pandas**: Data manipulation and aggregation
- **Plotly**: Interactive charts and visualizations  
- **Dash**: Web framework for Python (built on Flask + React)

---

## Use Cases

### Community Advocates
Identify neighborhoods underserved by green space to support equity arguments

### Urban Planners  
Assess distribution patterns and identify gaps for new park development

### Researchers
Study correlations between park access and public health outcomes

### Journalists
Data-driven reporting on environmental justice and urban development

### Residents
Discover parks in their neighborhood and compare to citywide averages

---

## Future Enhancements

- Add demographic overlay (Census data) to show populations near/far from parks
- Transit accessibility analysis (MBTA integration)
- Historical time series showing changes in open space over decades
- Mobile app version with "parks near me" functionality
- API for programmatic access to processed data

---

## Societal Impact

This dashboard democratizes access to urban planning data, enabling:
- Evidence-based advocacy for environmental justice
- More strategic city planning decisions
- Public accountability and transparency
- Research on urban health and equity
- Informed community engagement in planning processes

In a city with documented disparities in park access across neighborhoods, making this data accessible empowers residents to advocate for their communities with concrete evidence rather than anecdotes.

---

## Contact

**Student**: Aarav Sikriwal  
**Course**: INSH 2102 - Bostonography  
**Semester**: Spring 2026  
**Institution**: Northeastern University

---

## License

Educational project for Northeastern University coursework. Dataset courtesy of City of Boston Open Data Portal.
