# -*- coding: utf-8 -*-
"""
Created on Mon May  4 12:34:57 2026

@author: USER
"""
import math
import pandas as pd
import matplotlib.pyplot as plt

import pvlib
from pvlib.modelchain import ModelChain
from pvlib.pvsystem import PVSystem
from pvlib.location import Location


weather_df = pd.read_csv("df_poa.csv", index_col= 0)
weather_df.index = pd.to_datetime(weather_df.index)
print(weather_df.head())

# retrieve the inverter and panel specifications from the pvlib library

cec_modules = pvlib.pvsystem.retrieve_sam("cecmod")
sapm_inverters = pvlib.pvsystem.retrieve_sam("cecinverter")
module = cec_modules["Znshine_PV_Tech_ZXP6_72_295_P"]
inverter = sapm_inverters["ABB__MICRO_0_3_I_OUTD_US_208__208V_"]
temperature_model_parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS[
    "sapm"
]["open_rack_glass_glass"]

# Create a Location and a PV System
location = Location(
    latitude= -1.383038,
    longitude= 36.767872,
    tz = "Africa/Nairobi",
    name="MMU_pitch",
    altitude=1678.0)

system = PVSystem(
        surface_tilt=35,
        surface_azimuth=180,
        module_parameters=module,
        inverter_parameters=inverter,
        temperature_model_parameters=temperature_model_parameters)

# Create and run PV Model
mc = ModelChain(system, location, aoi_model="physical")
mc.run_model_from_poa(weather_df)
ac_power = mc.results.ac.fillna(0)

# Define panel dimensions and peak power for Znshine_PV_Tech_ZXP6_72_295_P

panel_height = 1.95
panel_width = 0.99
panel_peak_power = 295          # Watts
tilt_angle = 35
roof_area = 400                 # m²

# Calculate the area occupied by the PV panel on a flat roof
panel_area_flat_roof = (
        panel_height
        * panel_width
        * math.cos(tilt_angle * math.pi / 180)
    )

# calculate amount of panels that fit in a certain roof area
roof_area = 400
panel_count = math.floor(roof_area / panel_area_flat_roof)

# calculate the peak capacity of this system in kWp
system_peak_capacity = panel_count * panel_peak_power / 1000

print("\n" + "="*60)
print("ROOF INSTALLATION SUMMARY")
print("="*60)
print(f"Roof Area                  : {roof_area} m²")
print(f"Panels that can fit        : {panel_count} panels")
print(f"System Peak Capacity       : {system_peak_capacity:.2f} kWp")
print("="*60)


# --- Hourly Power Output ---
plt.figure(figsize=(14, 7))
plt.plot(ac_power.index, ac_power, linewidth=1.5)
plt.title("Hourly AC Power Output - Single Module")
plt.ylabel("Power (W)")
plt.xlabel("Time")
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 2: Daily Energy Production
daily_energy = ac_power.resample("D").sum() / 1000   # kWh

plt.figure(figsize=(14, 7))
daily_energy.plot(kind='bar', color='skyblue', width=0.8)
plt.title("Daily Energy Production - Single Module")
plt.ylabel("Energy (kWh)")
plt.xlabel("Date")
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 3: Monthly Energy Production
monthly_energy = ac_power.resample("ME").sum() / 1000

plt.figure(figsize=(10, 6))
monthly_energy.plot(kind='bar', color='darkblue')
plt.title("Monthly Energy Production - Single Module")
plt.ylabel("Energy (kWh)")
plt.xlabel("Month")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Total Summary
total_energy_kwh = ac_power.sum() / 1000
print(f"\nTotal Energy Produced by One Module in the period: {total_energy_kwh:.1f} kWh")






