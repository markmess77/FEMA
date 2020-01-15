This project utilizes data from FEMA found here: https://www.fema.gov/openfema-dataset-disaster-declarations-summaries-v1

A python script was then written to analyze the data from the csv file that was downloaded. 

Custom ratings were created based on the data. `count` metric was created, which simply measures the amount of times a `disasterNumber` was repeated. The more the `disasterNumber` recurred, the more severe the disaster was. 

`rating` was the second metric created to illustrate the severity of each disaster. This was measured simply by dividing the `count` by the absolute value of the duration (in days) a disaster lasted. Absolute values were necessary as data quality was not always ideal as some disasters had a duration of a negative value.

