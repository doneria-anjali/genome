create table dddm.disaster_data_final as
select b.zip, a.*
from dddm.zip_lookup b
inner join dddm.disaster_data a
on a.StateCode = b.state_id;