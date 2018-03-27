create table land_prices_final as
select a.*, b.lat, b.lng
from dddm.land_prices a
left join dddm.zip_lookup b
on a.MSA = b.city and a.State = b.state_id;