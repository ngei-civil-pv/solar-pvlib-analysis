# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:27:36 2026

@author: USER
"""

import pvlib
import matplotlib.pyplot as plt


poa_data, metadata = pvlib.iotools.get_pvgis_hourly(latitude= -1.383038, longitude = 36.767872, start=2023, end=2023, raddatabase="PVGIS-SARAH3", 
                                          components=True, surface_tilt=30, surface_azimuth=180, 
                                          outputformat='json', usehorizon=True, userhorizon=None, 
                                          pvcalculation=False, peakpower=None, pvtechchoice='crystSi',
                                          mountingplace='free', loss=0, trackingtype=0, 
                                          optimal_surface_tilt=False, optimalangles=False, url='https://re.jrc.ec.europa.eu/api/', 
                                          map_variables=True, timeout=30)

poa_data["poa_diffuse"] = poa_data["poa_sky_diffuse"] + poa_data["poa_ground_diffuse"]
poa_data["poa_global"] = poa_data["poa_diffuse"] + poa_data["poa_direct"]

poa_data_io = poa_data[["poa_diffuse", "poa_global", "poa_direct", "temp_air", "wind_speed"]]

poa_data_io.plot()
plt.ylabel('irradiance [W/m$^2$]')
plt.show()

# poa_data_io.to_csv("poa_data_io.csv", index = True) 




