# PVLib Solar System Modeling

**Comprehensive photovoltaic performance modeling using PVLib Python** for fixed-tilt, single-axis tracking, and rooftop systems.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![PVLib](https://img.shields.io/badge/PVLib-0.10+-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Project Overview

This repository contains all the work done for the **solar project** using the `pvlib` library. It demonstrates end-to-end photovoltaic system modeling, from raw weather data processing to performance simulation of different mounting configurations.

### Key Features

- **Data Preparation**: Using `pvlib.iotools` to load and process weather station data
- **Solar Position & Irradiance**: Calculation of solar zenith/azimuth and transposition to Plane-of-Array (POA) irradiance
- **System Modeling**:
  - Fixed-tilt ground-mounted system
  - Single-axis tracking system
  - Rooftop system (with custom tilt & azimuth)
- **Performance Analysis**: Energy yield, performance ratio, temperature effects, etc.
- **Visualization**: Professional plots for irradiance, power output, and system comparison

## 📁 Repository Structure

pvlib-solar-modeling/
├── README.md                  
├── LICENSE                    
├── requirements.txt           
├── environment.yml            
├── .gitignore
│
├── data/                      # Raw and processed data
│   ├── raw/
│   │   ├── Dc 2016 data.csv
│   └── processed/             # Cleaned/POA data
│       ├── df_poa.csv
        ├── poa_data_io.csv
├── notebooks/                 
│   ├── 01_data_preparation.ipynb
│   ├── 02_solar_position_and_irradiance.ipynb
│   ├── 03_fixed_tilt_system.ipynb
│   ├── 04_single_axis_tracking.ipynb
│   ├── 05_rooftop_system_modeling.ipynb
│   └── 06_results_analysis.ipynb
├── plots/                     # All generated figures (high quality)
│   ├── fixed_tilt/
│   ├── single_axis/
│   ├── solar irradiance plots/

## 🚀 Key Analyses

### 1. Data Preparation & POA Transposition
- Loading weather data using `pvlib.iotools`
- Solar position calculation (`pvlib.solarposition`)
- Irradiance transposition to POA using `get_total_irradiance()`

### 2. Fixed-Tilt System
- Optimal tilt angle modeling
- Temperature-corrected performance
- DC and AC power output

### 3. Single-Axis Tracking
- Backtracking configuration
- Tracker rotation angle calculation
- Comparison with fixed-tilt (expected gain)

### 4. Rooftop System
- Real-world rooftop constraints (available tilt/azimuth)
- Shading considerations (basic)
- Urban environment modeling

## 📊 Results Highlights
- Single-axis tracking showed **25%** more annual energy yield compared to fixed-tilt
- Rooftop system achieved performance ratio of **%**
- Best performing configuration: Single-axis tracking though requires more capital as compared to fixed system.

Plots Included
All major plots are available in the /plots folder:Irradiance time series
Solar path diagrams
Daily/annual energy yield
System comparison charts
Temperature vs efficiency plots

Data
-Raw weather data (TMY or measured) located in data/raw/
-Processed POA datasets in data/processed/

Technologies Used 
-pvlib – Core modeling library
-pandas / numpy – Data handling
-matplotlib / seaborn – Visualization
-Jupyter – Interactive analysis

Future Improvements
-Add bifacial modeling
-Integrate machine learning for soiling/ degradation
-Full economic analysis (LCOE)
-PVSyst validation

About This Project
This work is part of my larger Solar Project portfolio. It showcases my ability to:
-Work with real weather/irradiance data
-Apply industry-standard PV modeling practices
-Compare different mounting technologies
-Produce clean, reproducible, and well-documented analysis

Feel free to explore the notebooks!

## 🛠️ How to Run

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/pvlib-solar-modeling.git
cd pvlib-solar-modeling

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run notebooks in order (recommended)
jupyter lab
