-- Tree Whisperer Database Schema
-- This database contains information about trees, forests, and ecosystems

CREATE DATABASE IF NOT EXISTS tree_whisperer;
USE tree_whisperer;

-- Tree species table
CREATE TABLE tree_species (
    id INT PRIMARY KEY AUTO_INCREMENT,
    scientific_name VARCHAR(255) NOT NULL UNIQUE,
    common_name VARCHAR(255) NOT NULL,
    family VARCHAR(100),
    genus VARCHAR(100),
    species VARCHAR(100),
    native_region VARCHAR(255),
    max_height_meters DECIMAL(8,2),
    max_diameter_cm DECIMAL(8,2),
    lifespan_years INT,
    growth_rate VARCHAR(50),
    wood_density DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Forest regions table
CREATE TABLE forest_regions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    region_name VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL,
    state_province VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    area_hectares DECIMAL(15, 2),
    forest_type VARCHAR(100),
    climate_zone VARCHAR(50),
    elevation_meters INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Forest inventory table (tracks trees in specific forests)
CREATE TABLE forest_inventory (
    id INT PRIMARY KEY AUTO_INCREMENT,
    forest_region_id INT NOT NULL,
    tree_species_id INT NOT NULL,
    year_recorded YEAR NOT NULL,
    tree_count INT NOT NULL,
    average_height_meters DECIMAL(8,2),
    average_diameter_cm DECIMAL(8,2),
    total_biomass_kg DECIMAL(12,2),
    carbon_storage_kg DECIMAL(12,2),
    health_status VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (forest_region_id) REFERENCES forest_regions(id),
    FOREIGN KEY (tree_species_id) REFERENCES tree_species(id),
    UNIQUE KEY unique_forest_species_year (forest_region_id, tree_species_id, year_recorded)
);

-- Logging/harvesting records
CREATE TABLE logging_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    forest_region_id INT NOT NULL,
    tree_species_id INT NOT NULL,
    year_logged YEAR NOT NULL,
    trees_logged INT NOT NULL,
    volume_cubic_meters DECIMAL(12,2),
    value_usd DECIMAL(12,2),
    logging_type VARCHAR(50),
    sustainability_certification VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (forest_region_id) REFERENCES forest_regions(id),
    FOREIGN KEY (tree_species_id) REFERENCES tree_species(id)
);

-- Forest growth/change tracking
CREATE TABLE forest_growth (
    id INT PRIMARY KEY AUTO_INCREMENT,
    forest_region_id INT NOT NULL,
    year_measured YEAR NOT NULL,
    total_area_hectares DECIMAL(15, 2),
    forest_cover_percentage DECIMAL(5,2),
    net_growth_hectares DECIMAL(15, 2),
    deforestation_hectares DECIMAL(15, 2),
    reforestation_hectares DECIMAL(15, 2),
    carbon_sequestration_tonnes DECIMAL(12,2),
    biodiversity_index DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (forest_region_id) REFERENCES forest_regions(id),
    UNIQUE KEY unique_forest_year (forest_region_id, year_measured)
);

-- Create read-only user for the application
CREATE USER IF NOT EXISTS 'tree_user'@'%' IDENTIFIED BY 'secure_password_change_me';
GRANT SELECT ON tree_whisperer.* TO 'tree_user'@'%';
FLUSH PRIVILEGES;
