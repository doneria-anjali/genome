create table dddm.weather_final as
select b.zip, a.*
from dddm.zip_lookup b
left join dddm.weather_observations a
on a.City = b.city and a.State = b.state_id;

#delete from dddm.land_prices_final where MSA is null;