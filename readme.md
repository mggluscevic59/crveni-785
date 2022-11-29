# Crystapp software for continous crystalization

## How to use this software
* Start Julabo MS device (make sure it is started, on device monitor, before proceeding to starting server)
* Start OPC UA server (local version 0.2.6 - methods with bool input)
* Connect Raman USB & power cabel
* Client PC:
    - Double click `edit` script to input parameters:
        - Integration time (miliseconds)
        - Acquisition interpolation (number of measurement to interpolate)
        - Count (number of measurement)
        - Delay time (miliseconds)
    - Double click `start` script to run measurement.
    - Double click link to data. Folder should contain CSV file(s) with current date & measurement number (per day)
## How to manipulate CSV data in Microsoft Office
* Open document in Excel
* Select All (`ctr+A`)
* `Data > Text to data` opens a wizard
* Choose: tabulated format, click `NEXT`
* Select [ `tab,comma` ] values & press `ADVANCED`
* Choose: delimiter: `dot (.)` => `comma (,)`
    - explanation: Comma separated value file helds comma (,) simbol for delimiter of data. Croatian input (differenciating from American) uses the same comma for output of number. Ergo, finall output must have comma separated numbers (i.e. 3,14 kunas) in order to be able to shown data in graph.
* Click `FINISH`
