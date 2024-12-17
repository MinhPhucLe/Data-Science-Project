ram_brand_mapping = {
    "DDR5": "DDR5",
    "DDR4": "DDR4",
    "LPDDR5": "LPDDR5",
    "LPDDR5X": "LPDDR5X",
    "LPDDR5x": "LPDDR5X",  # Normalize case
    "LPDDR4X": "LPDDR4X",
    "LPDDR3": "LPDDR3",
    "LPDDR4": "LPDDR4",
    "LPDDR4x": "LPDDR4X",  # Normalize case
    "DDR5 4800MHz": "DDR5",  # Remove speed
    "DDR5-4800": "DDR5",  # Remove speed
    "DDR5 4800": "DDR5",  # Remove speed
    "DDR5-5600": "DDR5",  # Remove speed
    "DDR4-3200": "DDR4",  # Remove speed
    "LPDDR5x-7467": "LPDDR5X",  # Normalize case and remove speed
    "LPDDR5-6400": "LPDDR5",  # Remove speed
    "LPDDR5-5200": "LPDDR5",  # Remove speed
    "3200": None,  # Invalid (speed, not a brand)
    "5600": None,  # Invalid (speed, not a brand)
    "4800": None,  # Invalid (speed, not a brand)
    "5200": None,  # Invalid (speed, not a brand)
    "7467": None,  # Invalid (speed, not a brand)
    "6400": None,  # Invalid (speed, not a brand)
    "7500": None,  # Invalid (speed, not a brand)
    "1TB": None,  # Invalid (storage, not RAM)
    "Soldered": None,  # Invalid (not a RAM brand)
    "LPDDDR5": "LPDDR5",  # Correct typo
    "": None  # Empty value
}