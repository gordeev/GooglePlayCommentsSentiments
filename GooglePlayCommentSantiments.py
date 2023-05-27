import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# URL of the app
app_url = "GOOGLE_PLAY_GAME_URL"

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

openai.api_key = "OPENAI_API_KEY"

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful mobile game producer assistant."},
        {"role": "user", "content": review_text},
        {"role": "user", "content": "Summarize the comments of the game and identify 5 strengths and 5 weaknesses of the video based on the comments."}
    ]
)

print(response['choices'][0]['message']['content'])
report = response['choices'][0]['message']['content']

# Write the result to a file
package_name = app_url.split("=")[1].split("&")[0]
with open(f"{package_name}.txt", 'w') as f:
    json.dump(report, f, indent=4)

