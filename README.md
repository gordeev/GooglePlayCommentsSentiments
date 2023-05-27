# Mobile Game Review Analysis Using OpenAI and Selenium
This project uses Selenium to scrape reviews from Google Play Store and then OpenAI's GPT-3 model to analyze and summarize the reviews.

# What It Does
The script fetches the first 100 reviews of a specified mobile game from the Google Play Store. It then sends these reviews to OpenAI's GPT-3 model and asks the model to summarize the strong and weak points of the game based on these reviews. The result is saved in a JSON file.

# Setup
Clone the repository or download the game_review_analysis.py file.
Download the ChromeDriver and place it in the same directory as the script. Please download the version that matches with your installed Chrome version.
You need to have Python 3 installed, and the Python packages openai, selenium.
Set the app_url variable in the script to the URL of the game on the Google Play Store that you wish to analyze.
Set the openai.api_key to your OpenAI API key.
Run the script with python game_review_analysis.py.
Warnings
This script continues to send requests to the OpenAI API until it receives a response in a format that can be parsed as JSON. This is because the script requires the output in a structured format. However, this might cause the script to enter a loop if the model consistently returns responses that cannot be parsed as JSON, which might result in a higher than expected API usage and costs.

# You should be aware of this possibility and consider implementing appropriate error handling and rate limiting measures. The provided code is a simple demonstration and might not be suitable for production use without further refinement.

# License
This project is available under the MIT license.

# Contribution
Feel free to fork the project and make contributions.
