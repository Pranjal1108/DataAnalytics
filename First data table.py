import pandas as pd
import matplotlib.pyplot as plt


data = {
    'Phase': ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'],
    'Year_Range': ['FY23–FY27', 'FY31–FY32', 'FY36–FY37', 'FY40–FY50'],
    'Estimated_Cost_Cr': [4588, 5983, 8415, 10575],
    'Passenger_Capacity_MPPA': [12, 30, 50, 70],
    'Runways': [1, 1, 0, 0],  # Only Phase 1 and 2 mention runways
    'Terminal_Area_sqm': [90000, 90000, 160000, 160000],
    'Cargo_Area_sqm': [50000, 70000, 100000, 150000],  # cumulative till phase
    'Status': ['~90% complete', 'Planned', 'Planned', 'Planned'],
    'Area_Hectares': [1334, 0, 0, 0]  # Only Phase 1 is given
}

df = pd.DataFrame(data)

# --------- Step 2: Bar Chart – Cost per Phase ---------
plt.figure(figsize=(8, 5))
plt.bar(df['Phase'], df['Estimated_Cost_Cr'], color='steelblue')
plt.title('Estimated Cost per Phase (₹ Crore)')
plt.xlabel('Phase')
plt.ylabel('Cost (₹ Crore)')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# --------- Step 3: Pie Chart – Passenger Capacity Share ---------
plt.figure(figsize=(6, 6))
plt.pie(df['Passenger_Capacity_MPPA'], labels=df['Phase'], autopct='%1.1f%%', startangle=90)
plt.title('Passenger Capacity Distribution (MPPA)')
plt.tight_layout()
plt.show()

# --------- Step 4: Timeline with Capacity Labels ---------
plt.figure(figsize=(10, 5))
bars = plt.bar(df['Phase'], df['Passenger_Capacity_MPPA'], color='orange')
plt.title('Construction Phases Timeline & Capacity')
plt.xlabel('Phase')
plt.ylabel('Passenger Capacity (MPPA)')

for bar, year, stat in zip(bars, df['Year_Range'], df['Status']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 2, f"{year}\n{stat}",
             ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# --------- Step 5: Export DataFrame to CSV ---------
df.to_csv("noida_airport_data.csv", index=False)
print("✅ Data saved as 'noida_airport_data.csv' for Power BI.")
