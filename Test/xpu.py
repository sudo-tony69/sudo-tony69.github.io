import tweepy
import os
import sys
from PIL import Image
import io

def setup_api():
    """Set up and return the Twitter API client with proper authentication."""
    # You'll need to create an app at https://developer.twitter.com/en/portal/dashboard
    # and obtain these credentials
    consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
    consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
    
    # Check if credentials are available
    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("Error: Twitter API credentials not found in environment variables.")
        print("Please set TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, and TWITTER_ACCESS_TOKEN_SECRET")
        sys.exit(1)
    
    # Create API instance
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    api = tweepy.API(auth)
    
    # Verify credentials
    try:
        api.verify_credentials()
        print("Authentication successful!")
        return api
    except Exception as e:
        print(f"Error during authentication: {e}")
        sys.exit(1)

def update_profile(api, name=None, bio=None, profile_image=None, banner_image=None):
    """Update the user's profile with the provided information."""
    try:
        # Update profile info (name and bio)
        if name or bio:
            profile_params = {}
            if name:
                profile_params['name'] = name
            if bio:
                profile_params['description'] = bio
            
            api.update_profile(**profile_params)
            print(f"Successfully updated profile {'name' if name else ''} {'and' if name and bio else ''} {'bio' if bio else ''}")
        
        # Update profile image
        if profile_image:
            # Resize and prepare the image if needed
            img = Image.open(profile_image)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr.seek(0)
            
            # Upload the profile image
            api.update_profile_image(filename=profile_image)
            print("Successfully updated profile image")
        
        # Update banner image
        if banner_image:
            # Resize and prepare the image if needed
            img = Image.open(banner_image)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr.seek(0)
            
            # Upload the banner image
            api.update_profile_banner(filename=banner_image)
            print("Successfully updated profile banner")
            
        return True
    
    except Exception as e:
        print(f"Error updating profile: {e}")
        return False

def main():
    """Main function to run the profile updater."""
    print("X (Twitter) Profile Updater")
    print("==========================")
    
    # Set up the API
    api = setup_api()
    
    # Get user input for profile changes
    print("\nEnter new profile information (leave blank to keep current):")
    name = input("Display Name: ").strip()
    bio = input("Bio: ").strip()
    
    profile_image_path = input("Profile Image Path (leave blank to keep current): ").strip()
    banner_image_path = input("Banner Image Path (leave blank to keep current): ").strip()
    
    # Validate image paths
    if profile_image_path and not os.path.exists(profile_image_path):
        print(f"Error: Profile image file not found at {profile_image_path}")
        profile_image_path = None
    
    if banner_image_path and not os.path.exists(banner_image_path):
        print(f"Error: Banner image file not found at {banner_image_path}")
        banner_image_path = None
    
    # Confirm changes
    print("\nReady to update profile with the following changes:")
    if name:
        print(f"- New display name: {name}")
    if bio:
        print(f"- New bio: {bio}")
    if profile_image_path:
        print(f"- New profile image: {profile_image_path}")
    if banner_image_path:
        print(f"- New banner image: {banner_image_path}")
    
    confirm = input("\nProceed with these changes? (y/n): ").lower()
    
    if confirm == 'y':
        success = update_profile(
            api, 
            name=name if name else None,
            bio=bio if bio else None,
            profile_image=profile_image_path if profile_image_path else None,
            banner_image=banner_image_path if banner_image_path else None
        )
        
        if success:
            print("\nProfile updated successfully!")
        else:
            print("\nFailed to update profile. Please try again.")
    else:
        print("Update cancelled.")

if __name__ == "__main__":
    main()