# Mapping raw GPU names to standardized names
card_mapping = {
    "Intel Arc Graphics": "Intel Arc Graphics",
    "Intel Arc graphics": "Intel Arc Graphics",
    "Intel Arc Graphics 140V": "Intel Arc A-Series 140V",
    "Intel Arc Graphics 130V": "Intel Arc A-Series 130V",
    "Intel Arc 140V GPU": "Intel Arc A-Series 140V",
    "Intel Arc 130V GPU": "Intel Arc A-Series 130V",
    "Intel Iris X\u1d49 Graphics": "Intel Iris Xe Graphics",
    "Intel Iris Xe Graphics": "Intel Iris Xe Graphics",
    "Intel graphics": "Intel Graphics",
    "Intel Graphics": "Intel Graphics",
    "Intel HD Graphics": "Intel HD Graphics",
    "Intel UHD Graphics": "Intel UHD Graphics",
    "Integrated Intel Graphics": "Intel Graphics",
    "Integrated Intel Iris Xe Graphics Functions as UHD Graphics": "Intel Iris Xe Graphics",
    "AMD Radeon Graphics": "AMD Radeon Graphics",
    "AMD Radeon 890M Graphics": "AMD Radeon 890M Graphics",
    "AMD Radeon 880M Graphics": "AMD Radeon 880M Graphics",
    "AMD Radeon 780M Graphics": "AMD Radeon 780M Graphics",
    "AMD Radeon 760M Graphics": "AMD Radeon 760M Graphics",
    "AMD Radeon 660M Graphics": "AMD Radeon 660M Graphics",
    "AMD Radeon RX 6550M, 4 GB": "AMD Radeon RX 6550M",
    "AMD Radeon RX7600S 8GB GDDR6": "AMD Radeon RX 7600S",
    "AMD Radeon RX7700S 8GB GDDR6": "AMD Radeon RX 7700S",
    "Qualcomm Adreno GPU": "Qualcomm Adreno GPU",
    "Integrated Qualcomm Adreno GPU": "Qualcomm Adreno GPU",
    "NVIDIA GeForce RTX 3050 6GB GDDR6": "NVIDIA GeForce RTX 3050",
    "NVIDIA GeForce RTX 3050 4GB GDDR6": "NVIDIA GeForce RTX 3050",
    "NVIDIA GeForce RTX 3050Ti 4GB GDDR6": "NVIDIA GeForce RTX 3050 Ti",
    "NVIDIA GeForce RTX 2050 4GB GDDR6": "NVIDIA GeForce RTX 2050",
    "NVIDIA GeForce RTX2050 4GB GDDR6": "NVIDIA GeForce RTX 2050",
    "NVIDIA GeForce RTX 4050 6GB GDDR6": "NVIDIA GeForce RTX 4050",
    "NVIDIA GeForce RTX 4060 8GB GDDR6": "NVIDIA GeForce RTX 4060",
    "NVIDIA GeForce RTX 4060 8GB GDDR6 140W TGP": "NVIDIA GeForce RTX 4060",
    "NVIDIA GeForce RTX 4070 8GB GDDR6": "NVIDIA GeForce RTX 4070",
    "NVIDIA GeForce RTX 4070 8GB GDDR6 140W TGP": "NVIDIA GeForce RTX 4070",
    "NVIDIA GeForce RTX 4080 12GB GDDR6": "NVIDIA GeForce RTX 4080",
    "NVIDIA GeForce RTX 4090 16GB GDDR6": "NVIDIA GeForce RTX 4090",
    "NVIDIA RTX 500 Ada Generation 4GB GDDR6": "NVIDIA RTX 500 Ada",
    "NVIDIA RTX A500 4GB GDDR6": "NVIDIA RTX A500",
    "NVIDIA RTX A1000 6GB GDDR6": "NVIDIA RTX A1000",
    "NVIDIA RTX A1000 6GB": "NVIDIA RTX A1000",
    "NVIDIA RTX 2000 Ada 8GB GDDR6": "NVIDIA RTX 2000 Ada",
    "NVIDIA RTX 2000 8GB GDDR6": "NVIDIA RTX 2000",
    "NVIDIA GeForce MX550 2GB GDDR6": "NVIDIA GeForce MX550",
    "NVIDIA GeForce MX570 2GB GDDR6": "NVIDIA GeForce MX570",
    "NVIDIA GeForce MX570A 2GB GDDR6": "NVIDIA GeForce MX570A",
    "NVIDIA Geforce RTX 3050 6GB GDDR6": "NVIDIA GeForce RTX 3050",
    "NVIDIA Geforce MX570A, 2 GB": "NVIDIA GeForce MX570A",
    "Nvidia Geforce RTX 4070 8GB GDDR6": "NVIDIA GeForce RTX 4070",
    "Nvidia Geforce RTX 4080 12GB GDDR6": "NVIDIA GeForce RTX 4080",
    "7 nhân GPU": "Custom GPU - 7 Cores",
    "8 nhân GPU": "Custom GPU - 8 Cores",
    "10 nhân GPU": "Custom GPU - 10 Cores",
    "16 nhân GPU": "Custom GPU - 16 Cores",
    "20 nhân GPU": "Custom GPU - 20 Cores",
    "32 nhân GPU": "Custom GPU - 32 Cores",
}