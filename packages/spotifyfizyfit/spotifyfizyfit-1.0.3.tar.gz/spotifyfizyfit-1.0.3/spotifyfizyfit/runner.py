import json
import time
import argparse
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Style, init

# Initialize colorama
def run():
    init(autoreset=True)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Transfer Spotify playlists to Fizy.')
    parser.add_argument('json_file', type=str, help='Path to the JSON file containing playlist data')
    args = parser.parse_args()

    json_file_path = args.json_file

    if not json_file_path:
        print(Fore.RED + "Error: JSON file path not provided.")
        sys.exit(1)

    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(Fore.RED + f"Error: {e}")
        sys.exit(1)

    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    driver.get('https://account.fizy.com/login')
    user_input = input(Fore.GREEN + "Press Enter to continue after completing the login process..." + Fore.RED + " If you want to exit, type 'esc' and press Enter: ")
    
    if user_input.lower() == 'esc':
        driver.quit()
        return

    driver.get('https://play.fizy.com/explore')
    time.sleep(1)

    isNewPlaylist = True
    for playlist in data['playlists']:
        print(Fore.GREEN + "Creating a new playlist: " + playlist['name'])
        
        isNewPlaylist = True
        for item in playlist['items']:
            track = item['track']
            song_name = f"{track['artistName']} {track['trackName']}"
            
            if isNewPlaylist:
                driver.get('https://play.fizy.com/explore')

                before_new_playlist_ahref = driver.find_element(By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/fizy-nav-search/a')
                before_new_playlist_ahref.click()
                time.sleep(1)
                search_input = driver.find_element(By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/div/form/input')
                search_input.send_keys(song_name)
                new_playlist_before_button = driver.find_element(By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/search-result/section[1]/div[2]/fizy-slider/div/div[2]/div/div/div[1]/div/div/track-list/track-list-item-album[1]/div/div[5]/span[4]')
                new_playlist_before_button.click()
                time.sleep(1)

                new_playlist_button = driver.find_element(By.XPATH, '/html/body/ul/li[1]/ul/li[1]')
                new_playlist_button.click()
                time.sleep(1)

                new_playlist_name_input = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/input')
                new_playlist_name_input.send_keys(song_name)

                new_playlist_create_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/button[2]')
                new_playlist_create_button.click()
                time.sleep(1)
                isNewPlaylist = False

                print(Fore.BLUE + f"Created a new playlist: {song_name}")
            else:
                search_input = driver.find_element(By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/div/form/input')

                search_input.clear()
                search_input.send_keys(song_name)

                time.sleep(2)
                search_button = driver.find_element(By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/div/form/button')
                search_button.click()
                time.sleep(2)

                first_album = driver.find_element(By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/search-result/section[1]/div[2]/fizy-slider/div/div[2]/div/div/div[1]/div/div/track-list/track-list-item-album[1]/div/div[5]/span[4]')
                first_album.click()
                time.sleep(2)

                first_album_list = driver.find_element(By.XPATH, '/html/body/ul/li[1]/ul/li[2]')
                first_album_list.click()
                time.sleep(1)
            print(Fore.YELLOW + f"Added {track['artistName']} - {track['trackName']} to the playlist to {playlist['name']}")      
            time.sleep(2)

    driver.quit()