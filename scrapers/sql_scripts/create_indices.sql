create index `lp_msa` on dddm.land_prices(MSA(50));
create index `lp_state` on dddm.land_prices(State(50));

create index `zlp_city` on dddm.zip_lookup(city(50));
create index `zlp_state` on dddm.zip_lookup(state_id(50));

create index `or_state` on dddm.oil_reserve(state(50));



#indices on final tables
create index `orf_zip` on dddm.oil_reserve_final(zip(50));
create index `lpf_zip` on dddm.land_prices_final(zip(50));
