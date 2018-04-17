#indices on final tables
create index `orf_zip` on dddm.oil_reserve_final(zip(50));
create index `lpf_zip` on dddm.land_prices_final(zip(50));
create index `spf_zip` on dddm.seaports_final(Zipcode(50));
create index `ddf_zip` on dddm.disaster_data_final(zip(50));
create index `ddf_zip` on dddm.disaster_data_final(zip(50));
create index `pl_zip` on dddm.plant_locations(zip_code(50));
create index `pdf_zip` on dddm.population_density_final(zip(50));
create index `rdf_zip` on dddm.railroad_data_final(zip(50));
create index `zfp_zip` on dddm.zips_for_project(zip(50));
