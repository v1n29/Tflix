from playwright.sync_api import sync_playwright
import time

source_url = "https://tflix.life/watch/sky-sports-cricket"
found_link = None

# This function acts like your F12 Network tab. 
# It checks every single network request the webpage makes.
def handle_request(request):
    global found_link
    # If the URL contains our target keywords, we catch it!
    if "live.php" in request.url and "token=" in request.url and ".m3u8" in request.url:
        found_link = request.url

def main():
    print("Starting Playwright Headless Browser...")
    with sync_playwright() as p:
        # Launch an invisible Chromium browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Tell the browser to send every network request to our interceptor function
        page.on("request", handle_request)
        
        print(f"Visiting {source_url}...")
        try:
            # Go to the webpage and wait until the network is mostly quiet
            page.goto(source_url, wait_until="networkidle", timeout=30000)
            
            # Wait an extra 10 seconds just to give the video player time to load the m3u8
            print("Waiting 10 seconds for the video player to generate the token...")
            page.wait_for_timeout(10000) 
        except Exception as e:
            print(f"Page loaded with a note/warning: {e}")
        
        browser.close()

    # After closing the browser, check if we caught the link
    if found_link:
        print(f"\nSUCCESS! Caught hidden link: {found_link}")
        
        m3u8_content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1000000
{found_link}
"""
        with open('stream.m3u8', 'w') as file:
            file.write(m3u8_content)
        print("Successfully updated stream.m3u8")
    else:
        print("\nFAILED: Could not intercept the link.")
        print("Cloudflare might have blocked the invisible browser, or the site is down.")

if __name__ == "__main__":
    main()
    
