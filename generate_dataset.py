import numpy as np
import pandas as pd
import os

# Set random seed for reproducibility
np.random.seed(42)

# Locations and their base price per sqft (in INR)
locations = {
    'MVP Colony': 7200,
    'Seethammadhara': 6800,
    'Siripuram': 8500,
    'Rushikonda': 6200,
    'Madhurawada': 4500,
    'Yendada': 5500,
    'Gajuwaka': 4200,
    'Muralinagar': 4800,
    'Sujathanagar': 4000,
    'Pendurthi': 3500
}

num_samples = 1500

loc_choices = np.random.choice(list(locations.keys()), size=num_samples, p=[0.12, 0.10, 0.08, 0.10, 0.18, 0.12, 0.10, 0.08, 0.06, 0.06])

areas = []
bedrooms_list = []
bathrooms_list = []
parking_list = []
property_age_list = []
floors_list = []
prices = []

for loc in loc_choices:
    # Bedrooms: 1 to 5
    bhk = np.random.choice([1, 2, 3, 4, 5], p=[0.08, 0.40, 0.38, 0.11, 0.03])
    
    # Area roughly scaled with BHK
    if bhk == 1:
        area = np.random.randint(500, 750)
        baths = 1
        park = np.random.choice([0, 1], p=[0.6, 0.4])
    elif bhk == 2:
        area = np.random.randint(850, 1300)
        baths = np.random.choice([1, 2], p=[0.25, 0.75])
        park = np.random.choice([0, 1, 2], p=[0.2, 0.7, 0.1])
    elif bhk == 3:
        area = np.random.randint(1300, 2100)
        baths = np.random.choice([2, 3], p=[0.3, 0.7])
        park = np.random.choice([1, 2], p=[0.65, 0.35])
    elif bhk == 4:
        area = np.random.randint(2000, 3200)
        baths = np.random.choice([3, 4], p=[0.4, 0.6])
        park = np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])
    else: # 5 BHK Luxury / Villa
        area = np.random.randint(3000, 4800)
        baths = np.random.choice([4, 5], p=[0.5, 0.5])
        park = np.random.choice([2, 3], p=[0.6, 0.4])
        
    age = np.random.randint(0, 25)
    floors = np.random.choice([1, 2, 3, 4], p=[0.35, 0.40, 0.18, 0.07])
    
    # Pricing formula with realistic economics
    base_rate = locations[loc]
    base_cost = area * base_rate
    
    # Amenities & structural premiums
    bath_premium = (baths - 1) * 120000
    parking_premium = park * 250000
    floor_premium = (floors - 1) * 180000
    
    # Age depreciation (approx 0.9% per year up to 25 years)
    depreciation_factor = max(0.75, 1.0 - (age * 0.009))
    
    # Market noise (+/- 4% Gaussian noise)
    noise = np.random.normal(1.0, 0.04)
    
    final_price = (base_cost + bath_premium + parking_premium + floor_premium) * depreciation_factor * noise
    
    # Round to nearest thousand
    final_price = round(final_price / 1000) * 1000
    
    areas.append(area)
    bedrooms_list.append(bhk)
    bathrooms_list.append(baths)
    parking_list.append(park)
    property_age_list.append(age)
    floors_list.append(floors)
    prices.append(final_price)

df = pd.DataFrame({
    'location': loc_choices,
    'area': areas,
    'bedrooms': bedrooms_list,
    'bathrooms': bathrooms_list,
    'parking': parking_list,
    'property_age': property_age_list,
    'floors': floors_list,
    'price': prices
})

os.makedirs('dataset', exist_ok=True)
df.to_csv('dataset/house_data.csv', index=False)
print(f"Dataset generated successfully with {len(df)} records.")
