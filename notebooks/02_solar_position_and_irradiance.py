# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 16:48:44 2026

@author: USER
"""

# 02 - Solar Position and POA Irradiance Calculation

## Objective
# Calculate solar position and transpose irradiance to Plane-of-Array for different system configurations.


import pvlib
from pvlib.location import Location
import pandas as pd
import matplotlib.pyplot as plt
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS


print("pvlib version :", pvlib.__version__)

df_tmy, metadata = pvlib.iotools.get_pvgis_tmy(latitude= -1.383038, longitude = 36.767872, outputformat='json', 
                                           usehorizon=True, userhorizon=None, 
                                           startyear=2010, endyear=2023, map_variables=True, 
                                           url='https://re.jrc.ec.europa.eu/api/', timeout=30, 
                                           roll_utc_offset=None, coerce_year=None)

df= df_tmy[['ghi', 'dni', 'dhi', 'temp_air', 'wind_speed']]
first_week = df.head(24*7)


Irradiance = first_week[["ghi", "dni", "dhi"]]
Irradiance.plot()
plt.ylabel('Irradiance [W/m$^2$]')
plt.show()


first_week[["temp_air"]].plot()
plt.ylabel("Ambient Temperature [°C]")
plt.show()


first_week[["wind_speed"]].plot()
plt.ylabel("Wind Speed [m/s]")
plt.show()

# monthly_ghi = df["ghi"].resample("ME").mean()
# monthly_ghi = monthly_ghi.tz_localize(None)   # remove tz for clean plotting
# monthly_ghi.plot.bar()
# plt.ylabel('Monthly Global Horizontal Irradiance\n[W h/m²]')
# plt.title('Monthly average GHI')
# plt.show()



lat = -1.383038
lon = 36.767872
tz = "Africa/Nairobi"

location = pvlib.location.Location(latitude= lat, longitude= lon, tz = tz)
sol_pos = location.get_solarposition(times= df.index)
df_poa = pvlib.irradiance.get_total_irradiance(surface_tilt = 30, surface_azimuth= 180,
                                                 solar_zenith = sol_pos["apparent_zenith"],
                                                 solar_azimuth= sol_pos["azimuth"], 
                                                 dni= df["dni"], 
                                                 ghi = df["ghi"],
                                                 dhi = df["dhi"])
print("POA columns:", df_poa.columns.tolist())
print(df_poa.head())

# df_full = pd.concat([df, df_poa], axis=1)

irradiance_poa = df_poa[["poa_global"]]
irradiance_poa.plot()
plt.ylabel("irradiance_poa [W/m$^2$]")
plt.show()

temp_params = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']
df_poa['cell_temp'] = pvlib.temperature.sapm_cell(
    poa_global=df_poa['poa_global'],
    temp_air=df['temp_air'],
    wind_speed=df['wind_speed'],
    **temp_params
)

df_poa.to_csv("df_poa.csv", index= True)







