# Environmental Genome

CSC 491/591 project on Environmental Genome for prediction of location of oil and petroleum refineries in United States based on PESTLE (Political, Economic, Social, Technical, Legal and Environmental) framework, using Python to develop the front & back-end of the application, and MySQL as the relational database.

Problem Statement - "Based on external factors such as population density, land conditions and other plant locations, is it favorable to build a chemical plant (oil and petroleum refinery) in a given location in the United States?"

The objective of this project is to learn making data-driven decisions based on quantitative and qualitative nature of the data. The project helps in critically thinking about the given problem statement, the external factors contributing to the decision, deciding upon the right data sources, and building decision rules. The major steps involved were crawling the different web resources to collect the data, processing that data for storing in the relational data format, building decision rules for attributes, training the decision model and making predictions based on the zipcodes of United States.

Data pre-requisites - application/exported_data contains the training and testing data that can be imported into the mysql database using addAllModelData.py. More details for importing data can be found at https://docs.google.com/document/d/1D9NLfbDC19MmgJblQlQS4dHkf-cXh6s61VdUP156Mxg/edit?usp=sharing

The application runs from GUI.py under application folder taking following inputs:
1. Zipcode for which the prediction has to be made for building an oil and petroleum refinery
2. Radius (in miles) to collect attribute data for the given location

The GUI triggers a call to an API(http://www.zipcodeapi.com/) that dynamically fetches the list of zipcodes lying within the given radius (in miles) around the given location. Using this list of zipcodes, we fetch seaport, oil reserves, land prices, population density, elevation (using Google API), railroad, natural disaster, and existing plant data present in the database. This data is standardized to provide corresponding weights to these factors to be fed into the trained model (Random Forest Model) for prediction of 'Yes' or 'No'. If the system approves the decision of constructing an oil refinery in a given zipcode, few more details are given to the user for intelligence augumentation which includes frequency of earthquakes reported in that area in last 10 years, number of water surrounding that aread and the general rules imposed by the government while drilling oil well in the given location.



Department of Computer Science,
North Carolina State University,
Raleigh, NC.




