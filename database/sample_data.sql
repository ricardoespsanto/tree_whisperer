-- Sample data for Tree Whisperer database
USE tree_whisperer;

-- Insert tree species
INSERT INTO tree_species (scientific_name, common_name, family, genus, species, native_region, max_height_meters, max_diameter_cm, lifespan_years, growth_rate, wood_density) VALUES
('Quercus alba', 'White Oak', 'Fagaceae', 'Quercus', 'alba', 'Eastern North America', 45.0, 150.0, 300, 'slow', 0.75),
('Pinus strobus', 'Eastern White Pine', 'Pinaceae', 'Pinus', 'strobus', 'Eastern North America', 50.0, 120.0, 200, 'fast', 0.35),
('Sequoia sempervirens', 'Coast Redwood', 'Cupressaceae', 'Sequoia', 'sempervirens', 'California Coast', 115.0, 300.0, 2000, 'moderate', 0.40),
('Pinus ponderosa', 'Ponderosa Pine', 'Pinaceae', 'Pinus', 'ponderosa', 'Western North America', 60.0, 100.0, 300, 'moderate', 0.45),
('Acer saccharum', 'Sugar Maple', 'Sapindaceae', 'Acer', 'saccharum', 'Eastern North America', 35.0, 100.0, 300, 'slow', 0.63),
('Pseudotsuga menziesii', 'Douglas Fir', 'Pinaceae', 'Pseudotsuga', 'menziesii', 'Pacific Northwest', 70.0, 200.0, 500, 'fast', 0.50),
('Fagus grandifolia', 'American Beech', 'Fagaceae', 'Fagus', 'grandifolia', 'Eastern North America', 30.0, 80.0, 300, 'slow', 0.65),
('Tsuga canadensis', 'Eastern Hemlock', 'Pinaceae', 'Tsuga', 'canadensis', 'Eastern North America', 30.0, 100.0, 800, 'slow', 0.42);

-- Insert forest regions
INSERT INTO forest_regions (region_name, country, state_province, latitude, longitude, area_hectares, forest_type, climate_zone, elevation_meters) VALUES
('Maine North Woods', 'USA', 'Maine', 46.5, -69.0, 12000000, 'Boreal', 'Continental', 300),
('Pacific Northwest Forest', 'USA', 'Washington', 47.5, -121.5, 8000000, 'Temperate Rainforest', 'Marine West Coast', 500),
('California Redwood Forest', 'USA', 'California', 40.0, -124.0, 2000000, 'Temperate Rainforest', 'Mediterranean', 200),
('Appalachian Forest', 'USA', 'Pennsylvania', 40.5, -77.5, 5000000, 'Temperate Deciduous', 'Humid Continental', 400),
('Rocky Mountain Forest', 'USA', 'Colorado', 39.0, -105.5, 3000000, 'Montane', 'Continental', 2000),
('Great Lakes Forest', 'USA', 'Michigan', 46.0, -84.0, 4000000, 'Boreal', 'Continental', 200);

-- Insert forest inventory data
INSERT INTO forest_inventory (forest_region_id, tree_species_id, year_recorded, tree_count, average_height_meters, average_diameter_cm, total_biomass_kg, carbon_storage_kg, health_status) VALUES
-- Maine North Woods 2020
(1, 1, 2020, 1500000, 25.0, 45.0, 45000000, 22500000, 'healthy'),
(1, 2, 2020, 2000000, 30.0, 35.0, 60000000, 30000000, 'healthy'),
(1, 7, 2020, 800000, 20.0, 30.0, 16000000, 8000000, 'healthy'),
(1, 8, 2020, 1200000, 22.0, 25.0, 24000000, 12000000, 'healthy'),

-- Pacific Northwest Forest 2020
(2, 3, 2020, 500000, 80.0, 200.0, 200000000, 100000000, 'healthy'),
(2, 6, 2020, 3000000, 45.0, 60.0, 135000000, 67500000, 'healthy'),
(2, 4, 2020, 1000000, 35.0, 40.0, 35000000, 17500000, 'healthy'),

-- California Redwood Forest 2020
(3, 3, 2020, 200000, 90.0, 250.0, 180000000, 90000000, 'healthy'),
(3, 6, 2020, 800000, 50.0, 70.0, 40000000, 20000000, 'healthy'),

-- Appalachian Forest 2020
(4, 1, 2020, 800000, 28.0, 50.0, 22400000, 11200000, 'healthy'),
(4, 5, 2020, 600000, 22.0, 35.0, 13200000, 6600000, 'healthy'),
(4, 7, 2020, 400000, 18.0, 25.0, 7200000, 3600000, 'healthy'),

-- 2021 data
(1, 1, 2021, 1520000, 26.0, 46.0, 45600000, 22800000, 'healthy'),
(1, 2, 2021, 2050000, 31.0, 36.0, 61500000, 30750000, 'healthy'),
(2, 3, 2021, 510000, 82.0, 205.0, 209100000, 104550000, 'healthy'),
(2, 6, 2021, 3100000, 46.0, 61.0, 142600000, 71300000, 'healthy'),

-- 2022 data
(1, 1, 2022, 1540000, 27.0, 47.0, 46200000, 23100000, 'healthy'),
(1, 2, 2022, 2100000, 32.0, 37.0, 63000000, 31500000, 'healthy'),
(2, 3, 2022, 520000, 84.0, 210.0, 218400000, 109200000, 'healthy'),
(2, 6, 2022, 3200000, 47.0, 62.0, 150400000, 75200000, 'healthy');

-- Insert logging records
INSERT INTO logging_records (forest_region_id, tree_species_id, year_logged, trees_logged, volume_cubic_meters, value_usd, logging_type, sustainability_certification) VALUES
-- Maine logging 2020-2022
(1, 1, 2020, 15000, 4500, 225000, 'selective', 'FSC'),
(1, 2, 2020, 25000, 7500, 300000, 'selective', 'FSC'),
(1, 1, 2021, 12000, 3600, 180000, 'selective', 'FSC'),
(1, 2, 2021, 20000, 6000, 240000, 'selective', 'FSC'),
(1, 1, 2022, 18000, 5400, 270000, 'selective', 'FSC'),
(1, 2, 2022, 22000, 6600, 264000, 'selective', 'FSC'),

-- Pacific Northwest logging
(2, 6, 2020, 5000, 1500, 75000, 'selective', 'FSC'),
(2, 6, 2021, 4000, 1200, 60000, 'selective', 'FSC'),
(2, 6, 2022, 6000, 1800, 90000, 'selective', 'FSC'),

-- Appalachian logging
(4, 1, 2020, 8000, 2400, 120000, 'selective', 'FSC'),
(4, 5, 2020, 3000, 900, 45000, 'selective', 'FSC'),
(4, 1, 2021, 6000, 1800, 90000, 'selective', 'FSC'),
(4, 5, 2021, 2500, 750, 37500, 'selective', 'FSC');

-- Insert forest growth data
INSERT INTO forest_growth (forest_region_id, year_measured, total_area_hectares, forest_cover_percentage, net_growth_hectares, deforestation_hectares, reforestation_hectares, carbon_sequestration_tonnes, biodiversity_index) VALUES
-- Maine North Woods
(1, 2020, 12000000, 85.5, 5000, 2000, 7000, 150000, 8.2),
(1, 2021, 12020000, 85.7, 3000, 1500, 4500, 155000, 8.3),
(1, 2022, 12035000, 85.9, 2500, 1000, 3500, 160000, 8.4),

-- Pacific Northwest Forest
(2, 2020, 8000000, 92.0, 8000, 1000, 9000, 200000, 9.1),
(2, 2021, 8008000, 92.1, 6000, 800, 6800, 205000, 9.2),
(2, 2022, 8014000, 92.2, 5000, 600, 5600, 210000, 9.3),

-- California Redwood Forest
(3, 2020, 2000000, 95.0, 2000, 100, 2100, 180000, 9.5),
(3, 2021, 2002000, 95.1, 1500, 80, 1580, 185000, 9.6),
(3, 2022, 2003500, 95.2, 1200, 60, 1260, 190000, 9.7),

-- Appalachian Forest
(4, 2020, 5000000, 78.0, 3000, 2000, 5000, 120000, 7.8),
(4, 2021, 5003000, 78.2, 2500, 1500, 4000, 125000, 7.9),
(4, 2022, 5005500, 78.4, 2000, 1000, 3000, 130000, 8.0);
