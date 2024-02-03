from playwright.sync_api import sync_playwright
import os
# this python scripts access https://www.chosic.com/spotify-playlist-analyzer/ and downloads a csv file with
# the information about a playlist
# the csv file is downloaded and saved as default on the /Download folder


def getplaylistlink() -> str:
    playlist_link = input('Please enter your spotify playlist link to be analysed.\n')
    entire = playlist_link
    # https://open.spotify.com/playlist/37i9dQZF1DWWQRwui0ExPn?si=a4509ced02c544b5
    # playlist_link = playlist_link.split('/')
    # for index in range(len(playlist_link[-1])):    # acess the last position of the string and look for the ? character
    #    if playlist_link[-1][index] == '?':
    #        playlist_link = playlist_link[-1][:index]
    #        break
    return entire


def connection(link: str) -> None:
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            print(f'[+] accessing https://www.chosic.com/spotify-playlist-analyzer/ with {browser_type.name}')
            browser = browser_type.launch(headless=False)
            page = browser.new_page()
            page.goto('https://www.chosic.com/spotify-playlist-analyzer/')
            page.get_by_placeholder("Paste a Spotify playlist link").fill(link)
            page.get_by_role("button", name="Analyze").click()
            with page.expect_download(timeout=90000) as download_info:
                # Perform the action that initiates download
                page.get_by_role("button", name="Export to CSV").click(timeout=60000)   # 1 minute of wait
            download = download_info.value
            # page.screenshot(path=f'example-{browser_type.name}.png')  # if you want to take a screenshot of the page
            # Wait for the download process to complete and save the downloaded file
            download.save_as(os.path.expanduser('~') + os.path.join("/Downloads", download.suggested_filename))
            print(f"File downloaded and named as {download.suggested_filename} in {os.path.expanduser('~') + os.path.join('/Downloads', download.suggested_filename)}")
            browser.close()


if __name__ == "__main__":
    pl_link = getplaylistlink()
    connection(pl_link)
