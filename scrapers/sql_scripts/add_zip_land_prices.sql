create table dddm.land_prices_final as
select b.zip, a.*
from dddm.zip_lookup b
left join dddm.land_prices a
on a.MSA = b.city and a.State = b.state_id;

delete from dddm.land_prices_final
where MSA is null;