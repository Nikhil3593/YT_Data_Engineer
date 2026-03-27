import requests

API_KEY="AIzaSyCwrfliF_ELfKxD6bRTN4dRjU1LBKHikz0"
CHANNEL_HANDLE="MrBeast"

url=f"https://youtube.googleapis.com/youtube/v3/channels?part=contentdetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"