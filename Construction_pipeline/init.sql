-- Create all tables automatically

CREATE TABLE IF NOT EXISTS site_data (
    site_name VARCHAR(100),
    location_address TEXT
);

CREATE TABLE IF NOT EXISTS machines_data (
    machine_id VARCHAR(50),
    date DATE,
    machine_name VARCHAR(100),
    machine_status VARCHAR(50),
    working_time FLOAT,
    idle_time FLOAT,
    fuel_used FLOAT,
    fuel_cost FLOAT,
    working_site VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS labours_data (
    id SERIAL,
    date DATE,
    labour_id VARCHAR(50),
    labour_name VARCHAR(100),
    labour_number VARCHAR(20),
    labour_rating INT,
    labour_cost FLOAT,
    working_days INT,
    total_cost FLOAT,
    working_site VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS machines_maintenance (
    maintenance_id SERIAL,
    machine_id VARCHAR(50),
    date DATE,
    machine_fault TEXT,
    repair_cost NUMERIC(12,2) DEFAULT 0,
    maintenance_cost NUMERIC(12,2) DEFAULT 0,
    total_cost NUMERIC(12,2)
    GENERATED ALWAYS AS (repair_cost + maintenance_cost) STORED
);

CREATE TABLE IF NOT EXISTS material_data (
    material_id SERIAL,
    date DATE,
    material VARCHAR(100),
    tons FLOAT,
    cost_material NUMERIC(12,2),
    transporter VARCHAR(100),
    vehicle_number VARCHAR(50),
    trips INT,
    phone_number VARCHAR(20),
    trip_cost NUMERIC(12,2),
    total_cost NUMERIC(12,2),
    working_site VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS progress_data (
    progress_id SERIAL,
    date DATE,
    working_site VARCHAR(100),
    image_path TEXT,
    progress_percentage INT
);