import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt

# Load NetCDF file
file_path = "cmems_mod_glo_wav_my_0.2deg_PT3H-i_1740485667545.nc"  # Endre til riktig fil
data = xr.open_dataset(file_path)

# Hent signifikant bølgehøyde og tid
wave_height = data["VHM0"].mean(dim=["latitude", "longitude"])  # Gjennomsnitt over området
time = data["time"]

# ----------------------------------------------------------------------------------------------#

# # Konverter NetCDF til Pandas DataFrame for enklere analyse
# df = wave_height.to_dataframe().reset_index()

# # Lagre til CSV
# df.to_csv("wave_height_data_nordsjø.csv", index=False)
# print("Data lagret som wave_height_data_nordsjø.csv!")

# ----------------------------------------------------------------------------------------------#

# Last inn CSV-filen
df = pd.read_csv("wave_height_data_nordsjø.csv")

# Konverter 'time'-kolonnen til datetime-format
df["time"] = pd.to_datetime(df["time"])

# Beregn gjennomsnittlig bølgehøyde per dag
daily_avg = df.groupby(df["time"].dt.date)["VHM0"].mean().reset_index()

# Gi nytt navn til kolonnene
daily_avg.columns = ["date", "mean_wave_height"]

# Lagre til CSV
daily_avg.to_csv("daily_wave_heights_nordsjø.csv", index=False)

# Filtrer for dager med bølgehøyde < 1.5m
low_wave_days = daily_avg[daily_avg["mean_wave_height"] < 1.5]

# Filtrer for dager med bølgehøyde < 2.5m
mid_wave_days = daily_avg[daily_avg["mean_wave_height"] < 2.5]

# Antall dager der bølgehøyden er lav
num_low_wave_days = len(low_wave_days)
num_mid_wave_days = len(mid_wave_days)
prosent_low = (num_low_wave_days / 365) * 100
prosent_mid = (num_mid_wave_days / 365) * 100

print(f"Antall dager i året med bølgehøyde under 1.5m: {num_low_wave_days}")
print(f"Prosentandel av året med signifikant bølgehøyde under 1.5m: {prosent_low:.2f}%")

print(f"Antall dager i året med bølgehøyde under 2.5m: {num_mid_wave_days}")
print(f"Prosentandel av året med signifikant bølgehøyde under 2.5m: {prosent_mid:.2f}%")

# ----------------------------------------------------------------------------------------------#

# Her plottes signifikant bølgehøyde mot tid

# # Last inn CSV-filen med daglig gjennomsnittlig bølgehøyde
# daily_avg = pd.read_csv("daily_wave_heights_nordsjø.csv")

# # Konverter 'date'-kolonnen til datetime-format
# daily_avg["date"] = pd.to_datetime(daily_avg["date"])

# # Plotte bølgehøyde over tid
# plt.figure(figsize=(12, 6))
# plt.plot(daily_avg["date"], daily_avg["mean_wave_height"], label="Daglig gj.sn. bølgehøyde", color="b")

# # Marker 1.5m-grensen for lav bølgehøyde
# plt.axhline(y=1.5, color="r", linestyle="--", label="1.5m grense")

# # Tilpasse plottet
# plt.xlabel("Tid")
# plt.ylabel("Signifikant bølgehøyde (m)")
# plt.title("Daglig gjennomsnittlig signifikant bølgehøyde over tid")
# plt.legend()
# plt.grid()

# # Vise plottet
# plt.show()
