import requests
import re

# 1. The website where the video player is hosted (where you pressed F12)
source_url = "https://the-website-you-visit.com/watch-sky-uk" 

# Pretend to be a normal web browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    # 2. Get the website's code
    response = requests.get(source_url, headers=headers)
    
    # 3. Search the code for the specific link structure
    # This looks for anything starting with your specific live.php link
    link_pattern = re.compile(r'(https://skyuk\.tflixcdn\.site/live\.php\?id=[a-zA-Z0-9]+&token=[a-zA-Z0-9_-]+~&format=\.m3u8)')
    match = link_pattern.search(response.text)

    if match:
        fresh_link = match.group(1)
        print(f"Found new link: {fresh_link}")
        
        # 4. Overwrite your GitHub M3U8 file with the fresh link
        m3u8_content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1000000
{fresh_link}
"""
        with open('stream.m3u8', 'w') as file:
            file.write(m3u8_content)
        print("Successfully updated stream.m3u8")
    else:
        print("Could not find the link in the webpage code.")

except Exception as e:
    print(f"An error occurred: {e}")
