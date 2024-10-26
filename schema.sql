-- Table to store basic information about victims and their resource needs
CREATE TABLE victims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,       -- Email contact information
    phone TEXT,                -- Phone contact information
    country TEXT NOT NULL,
    region TEXT,               -- County/State
    completed BOOLEAN DEFAULT 0  -- 0 for False, 1 for True (indicating if all needs have been fulfilled)
);

-- Table to store the types of resources requested by victims, with specific details if needed
CREATE TABLE resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    victim_id INTEGER NOT NULL,
    resource_type TEXT CHECK(resource_type IN ('Food', 'Medicine', 'Shelter', 'Clothes', 'Money', 'Transport', 'Other')) NOT NULL,
    description TEXT,  -- Optional field for specific needs (e.g., specific type of medicine)
    completed BOOLEAN DEFAULT 0,  -- 0 for False, 1 for True (indicating if the specific resource has been fulfilled)
    FOREIGN KEY (victim_id) REFERENCES victims (id) ON DELETE CASCADE
);

-- Table to store available resources from donors
CREATE TABLE donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,  -- Email contact information
    phone TEXT,           -- Phone contact information
    country TEXT NOT NULL,
    region TEXT,          -- County/State
    completed BOOLEAN DEFAULT 0  -- 0 for False, 1 for True (indicating if all resources from this donor have been matched)
);

-- Table to link donor offers with specific resources they can provide
CREATE TABLE donor_resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_id INTEGER NOT NULL,
    resource_type TEXT CHECK(resource_type IN ('Food', 'Medicine', 'Shelter', 'Clothes', 'Money', 'Transport', 'Other')) NOT NULL,
    description TEXT,  -- Optional field for specificity (e.g., specific type of food or medicine)
    completed BOOLEAN DEFAULT 0,  -- 0 for False, 1 for True (indicating if the specific resource has been matched)
    FOREIGN KEY (donor_id) REFERENCES donors (id) ON DELETE CASCADE
);

-- Table to manage matches between requested resources and available resources from donors
CREATE TABLE matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id INTEGER NOT NULL,   -- Refers to a specific entry in the resources table
    donor_resource_id INTEGER NOT NULL,  -- Refers to a specific entry in the donor_resources table
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resource_id) REFERENCES resources (id) ON DELETE CASCADE,
    FOREIGN KEY (donor_resource_id) REFERENCES donor_resources (id) ON DELETE CASCADE
);
