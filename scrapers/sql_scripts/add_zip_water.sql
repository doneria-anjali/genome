drop table dddm.temp;

create table dddm.temp as
select distinct a.MonitoringLocationTypeName, 
	ROUND(a.LatitudeMeasure, 2) as Lat, ROUND(a.LongitudeMeasure, 2) as Lon
from dddm.water_locations a;

create table dddm.water_final as
select b.zip, a.*
from dddm.temp a
	inner join dddm.zip_lookup b
		on (b.lat between a.Lat and (a.Lat + .01))
			and (b.lng between a.Lon and (a.Lon + .01));