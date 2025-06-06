import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


plt.style.use('dark_background')

data = {
    'Phase': ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'],
    'Year_Range': ['FY23–FY27', 'FY31–FY32', 'FY36–FY37', 'FY40–FY50'],
    'Estimated_Cost_Cr': [4588, 5983, 8415, 10575],
    'Passenger_Capacity_MPPA': [12, 30, 50, 70],
    'Runways': [1, 1, 2, 3],
    'Terminal_Area_sqm': [90000, 90000, 160000, 220000],
    'Cargo_Area_sqm': [50000, 70000, 100000, 150000],
    'Area_Hectares': [1334, 1800, 2200, 3000],
    'Gates': [12, 24, 36, 50],
    'Parking_Slots': [20, 35, 50, 70],
    'Metro_Connectivity': ['Yes', 'Planned', 'Planned', 'Planned'],
    'Solar_Power_Capacity_MW': [10, 25, 40, 60],
    'Green_Building_Rating': ['Platinum', 'Platinum', 'Platinum', 'Platinum'],
    'Status': ['~90% complete', 'Planned', 'Planned', 'Planned'],
    'Facilities': [
        ['ATC Tower', 'Fire Station', 'Hotels', 'Metro Link'],
        ['Additional Taxiways', 'Extended Terminal', 'Cargo Expansion'],
        ['2nd Runway', 'MRO Facility', 'Airport City Development'],
        ['3rd Runway', 'Intermodal Hub', 'Aerotropolis Expansion']
    ]
}

df = pd.DataFrame(data)


plt.figure(figsize=(8, 5))
plt.bar(df['Phase'], df['Estimated_Cost_Cr'], color='#00ffff')  
plt.title('Estimated Cost per Phase (₹ Crore)', color='white')
plt.xlabel('Phase', color='white')
plt.ylabel('Cost (₹ Crore)', color='white')
plt.grid(axis='y', color='gray', alpha=0.3)
plt.tight_layout()
plt.show()

plt.figure(figsize=(6, 6))
plt.pie(df['Passenger_Capacity_MPPA'], labels=df['Phase'], autopct='%1.1f%%', startangle=90,
        colors=['#00ffff', '#008080', '#00ced1', '#20b2aa'], textprops={'color':'white'})
plt.title('Passenger Capacity Distribution (MPPA)', color='white')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
bars = plt.bar(df['Phase'], df['Passenger_Capacity_MPPA'], color='#00ffff')
plt.title('Construction Phases Timeline & Capacity', color='white')
plt.xlabel('Phase', color='white')
plt.ylabel('Passenger Capacity (MPPA)', color='white')
plt.grid(axis='y', color='gray', alpha=0.3)
for bar, year, stat in zip(bars, df['Year_Range'], df['Status']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 2, f"{year}\n{stat}",
             ha='center', va='bottom', fontsize=8, color='white')
plt.tight_layout()
plt.show()

df.to_csv("noida_airport_data.csv", index=False)
print("✅ Data saved as 'noida_airport_data.csv' for Power BI.")

facility_icons = {
    "ATC Tower": "C:/Users/pranj/OneDrive/Documents/codes/Python Codes/DA project/atc.png",
    "Fire Station": "C:/Users/pranj/OneDrive/Documents/codes/Python Codes/DA project/fire.png",
    "Hotels": "C:/Users/pranj/OneDrive/Documents/codes/Python Codes/DA project/hotel.png",
    "Metro Link": "C:/Users/pranj/OneDrive/Documents/codes/Python Codes/DA project/metro.png",
    "Additional Taxiways": "C:/Users/pranj/OneDrive/Documents/codes/Python Codes/DA project/taxiway.png",
    "Extended Terminal": "C:/Users/pranj/OneDrive/Documents/codes/Python Codes/DA project/terminal.png",
    "Cargo Expansion": "C:/Users/pranj/OneDrive/Documents/codes/Python Codes/DA project/cargo.png",
    "2nd Runway": "C:/Users/pranj/OneDrive/Documents/codes/Python Codes/DA project/runway2.png",
    "MRO Facility": "C:/Users/pranj/OneDrive/Documents/codes/Python Codes/DA project/mro.png",
    "Airport City Development": "C:/Users/pranj/OneDrive/Documents/codes/Python Codes/DA project/city.png",
    "3rd Runway": "C:/Users/pranj/OneDrive/Documents/codes/Python Codes/DA project/runway3.png",
    "Intermodal Hub": "C:/Users/pranj/OneDrive/Documents/codes/Python Codes/DA project/transport.png",
    "Aerotropolis Expansion": "C:/Users/pranj/OneDrive/Documents/codes/Python Codes/DA project/city2.png"
}

root = tk.Tk()
root.title("Noida Airport Facilities by Phase")
root.geometry("950x600")


bg_color = "#121212"  
fg_color = "#00ffff"  
frame_bg = "#1e1e1e"  
accent_color = "#00bcd4"  
scrollbar_bg = "#333333"
scrollbar_trough = "#222222"

root.configure(bg=bg_color)

canvas = tk.Canvas(root, bg=bg_color, highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview,
                        bg=scrollbar_bg, troughcolor=scrollbar_trough, activebackground=accent_color)

scrollable_frame = ttk.Frame(canvas)

style = ttk.Style()
style.theme_use('clam')  
style.configure('TFrame', background=frame_bg)
style.configure('TLabel', background=frame_bg, foreground=fg_color)
style.configure('TLabelframe', background=frame_bg, foreground=fg_color)
style.configure('TLabelframe.Label', background=frame_bg, foreground=fg_color, font=('Helvetica', 14, 'bold'))
style.configure('TScrollbar', background=scrollbar_bg, troughcolor=scrollbar_trough)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

header = tk.Label(scrollable_frame, text="Noida Airport Facilities by Construction Phase",
                  font=("Helvetica", 20, "bold"), bg=bg_color, fg=fg_color)
header.pack(pady=20)

image_refs = {}

for i in range(len(df)):
    phase = df.loc[i, 'Phase']
    facilities = df.loc[i, 'Facilities']
    frame = ttk.LabelFrame(scrollable_frame, text=phase, padding=15)
    frame.pack(padx=30, pady=15, fill="x")
    icons_frame = ttk.Frame(frame)
    icons_frame.pack()

    for facility in facilities:
        icon_path = facility_icons.get(facility)
        try:
            img = Image.open(icon_path)
            img = img.resize((96, 96), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            image_refs[facility] = photo

            icon_bg = "#0a525f"
            icon_frame = tk.Frame(icons_frame, bg=icon_bg, padx=5, pady=5)
            icon_frame.pack(side="left", padx=10, pady=10)

            label = ttk.Label(icon_frame, image=photo, text=facility, compound="top",
                            background=icon_bg, foreground=fg_color)
            label.pack()
        except FileNotFoundError:
            fallback = ttk.Label(icons_frame, text=f"Image not found for {facility}", padding=10)
            fallback.pack(side="left", padx=10)
        except Exception as e:
            fallback = ttk.Label(icons_frame, text=f"Error loading {facility}: {str(e)}", padding=10)
            fallback.pack(side="left", padx=10)


canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()


# Note: All the GUI won't open simultaneously, you need to close the previous one to open the next one.
# This code creates a GUI to display the Noida Airport facilities by construction phase.
# It uses Tkinter for the GUI, Pandas for data handling, and PIL for image processing.
# The images are loaded from specified paths, change them according to your directory structure. 
# All the images are copyrighted, please use them for educational purposes only. I don't own any of the images.
# All the data used is taken from the official Noida Airport website and other reliable sources.