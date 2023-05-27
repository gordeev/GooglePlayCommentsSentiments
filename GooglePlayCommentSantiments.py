import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# URL of the app
app_url = "GOOGLE_PLAY_STORE_URL"

# Initialize Selenium driver
driver = webdriver.Chrome(executable_path='./chromedriver')

driver.get(app_url)

# Click the "See all reviews" button
see_all_reviews_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "See all reviews")]')))
see_all_reviews_button.click()

# Collect reviews
reviews = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="h3YV2d"]')))

review_texts = []
for i, review in enumerate(reviews):
    if i == 100:  # Stop collecting after 100 reviews
        break
    review_texts.append(review.text)

driver.quit()

# Truncate the review text to 3800 characters
review_text = " ".join(review_texts)
if len(review_text) > 3800:
    review_text = review_text[:3800]

# Create the API prompt
prompt = f"Here are 100 reviews of the game at {app_url}: {review_text}.\n\nPlease provide a summary of the game's strong points and weak points based on these reviews in JSON format like this: {{'strong_points': ['point1', 'point2', 'point3'], 'weak_points': ['point1', 'point2', 'point3']}}. Please provide the response strictly in JSON format."

openai.api_key = "your-api-key"

# Loop until we get a valid JSON response
while True:
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=300
    )

    # Parse the model's response into JSON
    try:
        report = json.loads(response.choices[0].text.strip())
        break
    except json.JSONDecodeError:
        print("Failed to parse the model's response as JSON. Retrying...")
        continue

# Write the result to a file
package_name = app_url.split("=")[1].split("&")[0]
with open(f"{package_name}.json", 'w') as f:
    json.dump(report, f, indent=4)
