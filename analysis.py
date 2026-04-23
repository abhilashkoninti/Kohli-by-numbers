import pandas as pd

# Load data
odi = pd.read_csv("Data/virat_kohli_odi_innings_data.csv")
t20 = pd.read_csv("Data/virat_kohli_t20i_innings_data.csv")
test = pd.read_csv("Data/virat_kohli_test_innings_data.csv")

# Clean Runs column - remove * and TDNB/DNB
def clean_runs(df):
    df = df.copy()
    df['Runs'] = df['Runs'].astype(str)
    df = df[~df['Runs'].isin(['TDNB', 'DNB', '-'])]
    df['Runs'] = df['Runs'].str.replace('*', '', regex=False)
    df['Runs'] = pd.to_numeric(df['Runs'], errors='coerce')
    df = df.dropna(subset=['Runs'])
    return df

odi = clean_runs(odi)
t20 = clean_runs(t20)
test = clean_runs(test)

print("ODI innings after cleaning:", len(odi))
print("T20 innings after cleaning:", len(t20))
print("Test innings after cleaning:", len(test))
# Average runs per format
print("\n--- KOHLI CAREER AVERAGES ---")
print("ODI Average:", round(odi['Runs'].mean(), 2))
print("T20 Average:", round(t20['Runs'].mean(), 2))
print("Test Average:", round(test['Runs'].mean(), 2))
# Year wise ODI runs
odi['Year'] = pd.to_datetime(odi['Start Date']).dt.year
year_runs = odi.groupby('Year')['Runs'].mean().round(2)
print("\n--- ODI AVERAGE BY YEAR ---")
print(year_runs)
# Performance vs each opponent
opponent_avg = odi.groupby('Opposition')['Runs'].mean().round(2).sort_values(ascending=False)
print("\n--- ODI AVERAGE VS EACH OPPONENT ---")
print(opponent_avg)
# Centuries and fifties in ODI
centuries = len(odi[odi['Runs'] >= 100])
fifties = len(odi[(odi['Runs'] >= 50) & (odi['Runs'] < 100)])
zeros = len(odi[odi['Runs'] == 0])

print("\n--- ODI MILESTONES ---")
print("Centuries (100+):", centuries)
print("Fifties (50-99):", fifties)
print("Ducks (0):", zeros)
# Save clean files for Power BI
odi['Format'] = 'ODI'
t20['Format'] = 'T20'
test['Format'] = 'Test'

combined = pd.concat([odi, t20, test], ignore_index=True)
combined.to_csv("Data/kohli_clean.csv", index=False)
print("\n✅ Clean data saved to Data/kohli_clean.csv")
# T20 Milestones
t20_centuries = len(t20[t20['Runs'] >= 100])
t20_fifties = len(t20[(t20['Runs'] >= 50) & (t20['Runs'] < 100)])

# Test Milestones  
test_centuries = len(test[test['Runs'] >= 100])
test_fifties = len(test[(test['Runs'] >= 50) & (test['Runs'] < 100)])

print("\n--- T20 MILESTONES ---")
print("Centuries:", t20_centuries)
print("Fifties:", t20_fifties)

print("\n--- TEST MILESTONES ---")
print("Centuries:", test_centuries)
print("Fifties:", test_fifties)

# Year wise for all formats
t20['Year'] = pd.to_datetime(t20['Start Date'], dayfirst=True).dt.year
test['Year'] = pd.to_datetime(test['Start Date'], dayfirst=True).dt.year

print("\n--- TEST AVERAGE BY YEAR ---")
print(test.groupby('Year')['Runs'].mean().round(2))
# Resave with Year column included
combined = pd.concat([odi, t20, test], ignore_index=True)
combined.to_csv("Data/kohli_clean.csv", index=False)
print("\n✅ Final clean data saved with all 3 formats!")