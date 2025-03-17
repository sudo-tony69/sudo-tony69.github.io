import os
import random
import tweepy

# Load API credentials from environment variables
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Authenticate with the Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def update_banner():
    # Path to the directory containing banners
    banners_dir = "./banners"
    
    # List all banner images
    banners = [f for f in os.listdir(banners_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    if not banners:
        print("No banner images found!")
        return
    
    # Select a random banner
    random_banner = random.choice(banners)
    banner_path = os.path.join(banners_dir, random_banner)
    
    try:
        # Update the profile banner
        api.update_profile_banner(banner_path)
        print(f"Successfully updated banner to: {random_banner}")
    except Exception as e:
        print(f"Error updating banner: {e}")

if __name__ == "__main__":
    update_banner()