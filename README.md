# Analysis of radiation Length scan with Gauss-on-Gaussino
The Python scripts provided here are used to plot the different histograms created with Gauss-On-Gaussino while doing the RadiationLength analysis.

## Scripts for verification tests
The `Two_scoring_planes*` files plot the results when only 2 SP (Scoring Planes) are used. It is designed for the Displaced_Plane geometry
The `Three_scoring_planes*` files plot the results when only 3 SP are used. It is designed for the Plane_Cylinder geometry
The `*_divide*`option is used when the uniform particle gun is set to true. These scripts divide the obtained histograms by the hit map to plot the Radiation Length per particle
The `*_grid` option is used when the grid particle gun is used. 

## Scripts for LHCb scans
The `Analysis_full_geometry.py` takes the information of all the scoring planes and plots it assuming the grid particle gun is used. For the scans with SP in the real world the VELO SP should be commented
The `Analysis_VELO_geometry.py` only takes the information from the VELO SP
Both have the option to set a range of the Z-axis so the inner structure of the different planes is better observed. 

## Work
The report associated to this work can be read at the CDS Cern page (TODO Put the link)
This work was done as part of my Summer Student stay at CERN during the 2024 summer. 
