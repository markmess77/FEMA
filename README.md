This project utilizes data from FEMA found here: https://www.fema.gov/openfema-dataset-disaster-declarations-summaries-v1

Columns from the csv utilizes were:
`disasterNumber` `state` `fyDeclared` `incidentType` `title` `incidentBeginDate` `incidentEndDate`

A python script was then written to analyze the data from the csv file that was downloaded. 

Custom ratings were created based on the data. `count` metric was created, which simply measures the amount of times a `disasterNumber` was repeated. The more the `disasterNumber` recurred, the more severe the disaster was. 

`rating` was the second metric created to illustrate the severity of each disaster. This was measured simply by dividing the `count` by the absolute value of the duration (in days) a disaster lasted. Absolute values were necessary as data quality was not always ideal as some disasters had a duration of a negative value.

A new dataframe excluding outliers was created in order to better display the box plot. `count` and `rating` metrics were both heavily skewed toward lower intensity. The outliers were removed in order to obtain a better scope of the whole as well as remove some data points with questionable data quality.

Another new dataframe was created to only include disasters after 1980 due to poor data quality. This dataframe is intended to be used for the line graph, illustrating change in `count` or `rating` over time.
