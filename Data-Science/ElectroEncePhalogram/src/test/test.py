import requests
import numpy as np

# Define API endpoint
url_single = "http://127.0.0.1:8000/predict"

# Given observations
observations = [
    {
        "features": [4285.64, 4004.62, 4264.1,  4115.38, 4320., 4615.9, 4071.79, 4608.72, 4201.03,
                     4224.62, 4162.56, 4271.79, 4584.1,  4352.31],
        "expected": "open"  # Expected output
    },
    {
        "features": [4292.82, 3990.26, 4253.85, 4106.67, 4329.23, 4621.03, 4088.72, 4614.87, 4207.69,
                     4233.33, 4194.87, 4275.9,  4587.69, 4347.69],
        "expected": "closed"  # Expected output
    }
]

# Send requests and compare results
for obs in observations:
    response = requests.post(url_single, json={"features": obs["features"]})
    predicted = response.json()["prediction"]

    print("\n🔹 Testing Observation:")
    print("Input Features:", obs["features"])
    print("🔹 Model Prediction:", predicted)
    print("✅ Expected Output:", obs["expected"])

    # Compare
    if predicted == obs["expected"]:
        print("✅ MATCH ✅")
    else:
        print("❌ MISMATCH ❌")

# Generate Random Simulated Observations
num_simulations = 5  # Change as needed
feature_length = len(observations[0]["features"])  # Ensure correct feature size

print("\n🔹 Running Simulated Observations 🔹")

for i in range(num_simulations):
    random_features = [round(x, 2) for x in np.random.uniform(3900, 4700, feature_length).tolist()]  # Generate values & round
    response = requests.post(url_single, json={"features": random_features})
    predicted = response.json()["prediction"]

    print(f"\n🔹 Simulation {i+1}:")
    print("Random Features:", random_features)
    print("🔹 Model Prediction:", predicted)
