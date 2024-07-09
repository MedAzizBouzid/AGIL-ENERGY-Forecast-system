import pandas as pd



def compare_city_names(name1, name2):
  """
  Compares two place names to check if they likely belong to the same city.

  Args:
    name1: The first place name.
    name2: The second place name.

  Returns:
    True if the names suggest the same city, False otherwise.
  """

  # Remove "kiosk" and extract city names
  city1 = name1.lower().replace("kiosk", "").strip()
  city2 = name2.lower().replace("kiosk", "").strip()

  # Check for exact match or partial match with common words
  return city1 == city2 or any(word in city1 for word in city2.split())


kiosks = pd.read_csv("featured_reviews_task_1.csv")

# Identify kiosks
kiosks_with_kiosk_name = kiosks[kiosks["place_name"].str.contains("kiosk", case=False)]

# Function to identify kiosks in the same city
def identify_kiosks_in_same_city(kiosks):
  """
  Identifies kiosks located in the same city based on place names.

  Args:
    kiosks: A list of dictionaries containing kiosk information.

  Returns:
    A list of tuples, where each tuple contains the names of two kiosks located in the same city.
  """

  kiosks_in_same_city = []

  # Iterate over each kiosk
  for i in range(len(kiosks)):
    kiosk_i = kiosks[i]

    # Check if it's a kiosk
    if "kiosk" in kiosk_i["place_name"].lower():
      # Compare with remaining kiosks
      for j in range(i + 1, len(kiosks)):
        kiosk_j = kiosks[j]

        # Check if both are kiosks and names suggest same city
        if "kiosk" in kiosk_j["place_name"].lower() and compare_city_names(kiosk_i["place_name"], kiosk_j["place_name"]):
          kiosks_in_same_city.append((kiosk_i["place_name"], kiosk_j["place_name"]))

  return kiosks_in_same_city

# Identify kiosks in the same city
kiosks_in_same_city = identify_kiosks_in_same_city(kiosks_with_kiosk_name)

# Print the results
print("Kiosks located in the same city:")
for kiosk_pair in kiosks_in_same_city:
    print(f"\t- {kiosk_pair[0]} and {kiosk_pair[1]}")