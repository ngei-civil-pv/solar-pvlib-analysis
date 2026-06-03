# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:42:47 2026

@author: USER
"""

# 03 - Fixed-Tilt PV System Modeling with PVLib

# **Author:** Denis Ngei  
# **Date:** 01/05/2026
# **Project:** Solar PV Performance Modeling

# ---

# ## 🎯 Objective

# Model the performance of a **fixed-tilt ground-mounted photovoltaic system** using real weather data and the `pvlib` library. This notebook covers system definition, Plane-of-Array (POA) irradiance calculation, DC/AC power modeling, and performance analysis.

# ## 📋 Table of Contents
# 1. [Imports & Setup](#imports)  
# 2. [Data Loading & Preparation](#data)  
# 3. [Location & System Definition](#system)  
# 4. [Solar Position & POA Irradiance](#poa)  
# 5. [PV System Modeling](#modeling)  
# 6. [Results & Visualization](#results)  
# 7. [Performance Metrics](#metrics)  
# 8. [Conclusions & Next Steps](#conclusion)



import pvlib
import pandas as pd
import matplotlib.pyplot as plt
from pvlib.location import Location
from pvlib.pvsystem import PVSystem, Array, FixedMount
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
from pvlib.modelchain import ModelChain



lat = -1.383038
lon = 36.767872
tz = "Africa/Nairobi"

alt = pvlib.location.lookup_altitude(latitude= lat, longitude= lon)
print("Altitude:", alt,"m")

location = pvlib.location.Location(latitude= lat, longitude= lon, tz = tz, 
                                   altitude= alt, name= "mmu_pitch")
poa_data = pd.read_csv("poa_data_io.csv", index_col= 0)
poa_data.index = pd.date_range(start= "2023-01-01 00:00",
                               periods= len(poa_data.index),
                               freq ="h")
print(poa_data)
poa_data.plot(subplots=True)
plt.show()

# Fixed Tilt System
cec_modules = pvlib.pvsystem.retrieve_sam(name="CECMod")
module = cec_modules['Yingli_Energy__China__YL300P_35b']
cec_inverters=pvlib.pvsystem.retrieve_sam(name='CECInverter')
inverter=cec_inverters['Satcon_Technology__PVS_50_S_MT__480V_']

temp_params = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']
poa_data['cell_temp'] = pvlib.temperature.sapm_cell(
    poa_global= poa_data['poa_global'],
    temp_air=poa_data['temp_air'],
    wind_speed=poa_data['wind_speed'],
    **temp_params
)

mount_1 = pvlib.pvsystem.FixedMount(surface_tilt=30, surface_azimuth=180)
mount_2 = pvlib.pvsystem.FixedMount(surface_tilt=30, surface_azimuth=0)

arr_1 = pvlib.pvsystem.Array(mount = mount_1, 
                             module_parameters=module, module = module,
                             albedo= .2,
                             temperature_model_parameters=temp_params,
                             modules_per_string=10,
                             strings=2, name = "Array_South")
arr_2 = pvlib.pvsystem.Array(mount = mount_2, 
                             module_parameters=module, albedo= .2,
                             module = module,
                             temperature_model_parameters=temp_params,
                             modules_per_string=10,
                             strings=2, name = "Array_North")

system = PVSystem(arrays= [arr_1, arr_2], inverter_parameters= inverter,
                  name= location.name)
print(f"Number of arrays: {system.num_arrays}")

# print(system)
# print('module specs')
# print(module)
# print('inverter specs')
# print(inverter)

mc = pvlib.modelchain.ModelChain(system,location,
                               aoi_model='physical',
                               transposition_model='perez',
                               spectral_model='no_loss',
                               losses_model='pvwatts',
                               name=location.name)
print(mc)
data_south = poa_data.copy()
data_north = poa_data.copy()

mc.run_model_from_poa(data=(data_south, data_north))

# AC Power (main output)
ac_power = mc.results.ac
ac_power.plot(figsize=(14, 6), title="AC Power Output")
plt.ylabel("Power (W)")
plt.ylabel("Power (W)")
plt.show()

# Monthly
monthly = mc.results.ac.resample("ME").sum() / 1000   # kWh
monthly.plot(kind= "bar", figsize=(12,6), title="Monthly Energy Production")
plt.ylabel("Energy (kWh)")
plt.show()

# Daily energy yield
daily = mc.results.ac.resample("D").sum() / 1000
daily.plot(figsize=(14,6), title="Daily Energy")
plt.ylabel("kWh/day")
plt.show()

# Cell Temperature
# cell_temperature= mc.results.cell_temperature
# cell_temperature.plot(figsize=(12,5), title="Cell Temperature")
# plt.ylabel("°C")
# plt.show()

dc_south = mc.results.dc[0]
dc_north = mc.results.dc[1]
print("South annual:", dc_south.sum()/1000, "kWh")
print("North annual:", dc_north.sum()/1000, "kWh")

poa_data["p_mp"]   = dc_south['p_mp'] + dc_north['p_mp']
poa_data['p_ac']= mc.results.ac
poa_data["p_loss"] = poa_data["p_mp"] - poa_data["p_ac"]


poa_data.loc['2023-01-15',['poa_direct','poa_diffuse','poa_global']].plot()
plt.show()

poa_data.loc['2023-01-15', ['poa_global','p_mp', 'p_ac', 'p_loss']].plot(subplots=True)
plt.show()

poa_data.loc['2023-07-15',['poa_direct','poa_diffuse','poa_global']].plot()
plt.show()

poa_data.loc['2023-07-15', ['poa_global','p_mp', 'p_ac', 'p_loss']].plot(subplots=True)
plt.show()

fig = plt.figure(figsize=(16,9))
ax = fig.add_subplot(111)
sc = ax.scatter(x=poa_data['poa_global'],y=poa_data['p_mp'],c=poa_data['cell_temp'])
ax.set_xlabel('POA Global')
ax.set_ylabel('Modeled DC Power [KW]')
fig.colorbar(sc, label='Cell Temperature [deg C]')
plt.show()

fig = plt.figure(figsize=(16,9))
ax = fig.add_subplot(111, aspect='equal')
sc = ax.scatter(x=poa_data['p_mp'],y=poa_data['p_ac'],c=poa_data['cell_temp'])
ax.set_xlabel('Modeled DC Power [KW]')
ax.set_ylabel('Modeled AC Power [KW]')
fig.colorbar(sc, label='Cell Temperature [deg C]')
plt.show()

# poa_data['month']=poa_data.index.month
# monthly_fixed=poa_data[['month','poa_global','p_mp','p_ac', 'p_loss']].groupby('month').sum()*.001
# monthly_fixed['total_losses']=1-monthly_fixed.p_ac/monthly_fixed.p_mp
# round(monthly_fixed,3)

# round(monthly_fixed.agg(['sum','mean']),3)
# monthly_fixed.plot(subplots=True)
# plt.show()

# # print(dir(mc.results))
# print(mc.results)















