# Investigating-And-Modeling-the-Factors-that-Effects-the-Performance-of-Genetic-Circuits
This repository contains the data-files and scripts necessary to reproduce the results of the "Investigating And Modeling the Factors that Effects the Performance of Genetic Circuits" journal article.



## experimental_results

Folder containing the fluorescence results on which the parameterization algorithms will draw upon.

- `shai timer_20210811_123450_ON AraC 2 plasmids.xlsx`

  Contains the characterization fluorescence results for the AraC gate when adding inducer.

- `shai timer_20210812_090202 OFF AraC 2 plasmidsd.xlsx`

  Contains the characterization fluorescence results for the AraC gate when removing inducer.

- `Timer (Modified)_20210808_125346 ON LuxR 2 plasmids.xlsx`

  Contains the characterization fluorescence results for the LuxR gate when adding inducer.

- `Timer (Modified)_20210809_090959 OFF LuxR 2 plasmids.xlsx`

  Contains the characterization fluorescence results for the LuxR gate when removing inducer.

- `Timer (Modified)_20210808_125346 ON LuxR 2 plasmids - Cropped.xlsx`

  Contains the characterization fluorescence results for the LuxR gate when adding inducer, but the fluorescence graphs have been moved to origin for each different induction time. 


## Free parameters
Folder containing the scripts to determine the paper's model parameter values, without fixing any parameter values

## Fixed parameters
Folder containing the scripts to determine the paper's model parameter values, fixing all the parameter values except for $/Tau_{ON}^Y$