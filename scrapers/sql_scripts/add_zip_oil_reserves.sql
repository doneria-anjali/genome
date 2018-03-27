create table oil_reserve_final as
select *
from dddm.oil_reserve a
	inner join dddm.us_cities b
		on a.state = b.State Name;