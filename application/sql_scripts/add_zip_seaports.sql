create table seaports_final as
SELECT distinct CITY_OR_TO, STATE_POST, ZIPCODE, PORT_NAME 
FROM dddm.seaports;