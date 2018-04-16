create table dddm.land_prices_final as
select b.zip, a.*
from dddm.zip_lookup b
left join dddm.land_prices a
on a.MSA = b.city and a.State = b.state_id;

#open Edit->Preferences, under SQL Editor, disable safe-updates and 
#run following query
delete from dddm.land_prices_final where MSA is null;