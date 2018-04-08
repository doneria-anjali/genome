create table dddm.railroad_data_final as
select b.zip, a.*
from dddm.zip_lookup b
inner join dddm.railroad_data a
on a.StateCode = b.state_id;