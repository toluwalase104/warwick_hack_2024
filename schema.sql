-- Table to store basic information about victims and their resource needs
CREATE TABLE victims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,       -- Email contact information
    phone TEXT UNIQUE,                -- Phone contact information
    address TEXT NOT NULL,
    postcode TEXT,                    -- County/State
    completed BOOLEAN DEFAULT 0,      -- 0 for False, 1 for True (indicating if all needs have been fulfilled)
    description TEXT DEFAULT ""       -- Optional field for specific needs (e.g., specific type of medicine)
);

-- Table to store the types of resources requested by victims, with specific details if needed
CREATE TABLE requested_resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    victim_id INTEGER NOT NULL,
    resource_type TEXT CHECK(resource_type IN ('Food', 'First Aid', 'Shelter', 'Clothes', 'Money', 'Transport', 'Other')) NOT NULL,
    completed BOOLEAN DEFAULT 0,     -- 0 for False, 1 for True (indicating if the specific resource has been fulfilled)
    FOREIGN KEY (victim_id) REFERENCES victims (id) ON DELETE CASCADE,
    UNIQUE (victim_id, resource_type) -- Prevent duplicate entries of the same resource type for a victim
);

-- Table to store available resources from donors
CREATE TABLE donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,       -- Email contact information
    phone TEXT UNIQUE,                -- Phone contact information
    country TEXT NOT NULL,
    region TEXT,                      -- County/State
    completed BOOLEAN DEFAULT 0,      -- 0 for False, 1 for True (indicating if all resources from this donor have been matched)
    description TEXT DEFAULT ""       -- Optional field for specific details
);

-- Table to link donor offers with specific resources they can provide
CREATE TABLE donor_resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_id INTEGER NOT NULL,
    resource_type TEXT CHECK(resource_type IN ('Food', 'Medicine', 'Shelter', 'Clothes', 'Money', 'Transport', 'Other')) NOT NULL,
    completed BOOLEAN DEFAULT 0,      -- 0 for False, 1 for True (indicating if the specific resource has been matched)
    FOREIGN KEY (donor_id) REFERENCES donors (id) ON DELETE CASCADE,
    UNIQUE (donor_id, resource_type)  -- Prevent duplicate entries of the same resource type for a donor
);

-- Table to manage matches between requested resources and available resources from donors
CREATE TABLE matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id INTEGER NOT NULL,     -- Refers to a specific entry in the requested_resources table
    donor_resource_id INTEGER NOT NULL, -- Refers to a specific entry in the donor_resources table
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resource_id) REFERENCES requested_resources (id) ON DELETE CASCADE,
    FOREIGN KEY (donor_resource_id) REFERENCES donor_resources (id) ON DELETE CASCADE
);