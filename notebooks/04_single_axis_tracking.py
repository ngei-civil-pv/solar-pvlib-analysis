# -*- coding: utf-8 -*-
"""
Created on Mon May  4 10:01:58 2026

@author: USER
"""

import pvlib
import pandas as pd
import matplotlib.pyplot as plt
from pvlib.location import Location
from pvlib.pvsystem import PVSystem, Array, SingleAxisTrackerMount
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

# Single axis tracker system
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


mount_1 = SingleAxisTrackerMount(axis_tilt=30,
                        axis_azimuth=180,
                        max_angle=90,
                        backtrack=False)

mount_2 = SingleAxisTrackerMount(axis_tilt=30,
                        axis_azimuth=0,
                        max_angle=90,
                        backtrack= False)


start = "2023-01-15 00:00"
end = "2023-01-15 23:00"

sol_pos = location.get_solarposition(times= pd.date_range(start= start, end= end,
                                                          freq= "1min"))
orientation_1 = mount_1.get_orientation(solar_zenith = sol_pos["apparent_zenith"],
                                    solar_azimuth = sol_pos["azimuth"])

orientation_1["tracker_theta"].fillna(0).plot(title = "South tracker orientation")
plt.show()

orientation_2 = mount_2.get_orientation(solar_zenith = sol_pos["apparent_zenith"],
                                    solar_azimuth = sol_pos["azimuth"])

orientation_2["tracker_theta"].fillna(0).plot(title = "North tracker orientation")
plt.show()

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

sat_system = PVSystem(arrays=[arr_1, arr_2], inverter_parameters= inverter,
                      name= location.name )

mc = ModelChain(sat_system, location, aoi_model='physical')

data_south = poa_data.copy()
data_north = poa_data.copy()

mc.run_model_from_poa(data= (data_south, data_north))

# AC Output

ac_power = mc.results.ac
ac_power.plot(figsize=(16, 9), title="AC Power Output")
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
daily.plot(figsize=(16,9), title="Daily Energy")
plt.ylabel("kWh/day")
plt.show()

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

fig = plt.figure(figsize=(9,8))
ax = fig.add_subplot(111, aspect='equal')
sc = ax.scatter(x=poa_data['p_mp'],y=poa_data['p_ac'],c=poa_data['cell_temp'])
ax.set_xlabel('Modeled DC Power [KW]')
ax.set_ylabel('Modeled AC Power [KW]')
fig.colorbar(sc, label='Cell Temperature [deg C]')
plt.show()


