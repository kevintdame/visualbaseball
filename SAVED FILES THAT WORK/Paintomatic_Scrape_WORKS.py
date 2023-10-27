from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
options.page_load_strategy = 'eager'

# Set up the Selenium web driver with Chrome
browser = webdriver.Chrome(options=options)
browser.set_window_size(2880, 1620)
browser.maximize_window()
browser.get('https://www.fangraphs.com/leaders/major-league?pos=all&stats=pit&type=8')

pitch_types = ["FA%", "FT%", "FC%", "FS%", "FO%", "SI%", "SL%", "CU%", "KC%", "EP%", "CH%", "SC%", "KN%"]
h_movement_types = ["FA-X", "FT-X", "FC-X", "FS-X", "FO-X", "SI-X", "SL-X", "CU-X", "KC-X", "EP-X", "CH-X", "SC-X", "KN-X"]
v_movement_types = ["FA-Z", "FT-Z", "FC-Z", "FS-Z", "FO-Z", "SI-Z", "SL-Z", "CU-Z", "KC-Z", "EP-Z", "CH-Z", "SC-Z", "KN-Z"]
velocity_types = ["vFA", "vFT", "vFC", "vFS", "vFO", "vSI", "vSL", "vCU", "vKC", "vEP", "vCH", "vSC", "vKN"]
pitch_type_value_types = ["wFA", "wFT", "wFC", "wFS", "wFO", "wSI", "wSL", "wCU", "wKC", "wEP", "wCH", "wSC", "wKN"]

sleep_duration = 1

columns = ['Name', 'Team'] + pitch_types + h_movement_types + v_movement_types + velocity_types + pitch_type_value_types


def check_and_close_popup(xpath_to_close_button, short_wait_duration=3):
    """
    Check for the popup and close it if present.
    """
    try:
        # Wait for short duration for the close button of the popup to appear
        wait = WebDriverWait(browser, short_wait_duration)
        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_to_close_button)))
        close_button.click()
        print("closed pop up")
        time.sleep(1)
    except Exception as e:
        # If the close button doesn't appear within the short wait duration, simply pass
        #print("no pop up found")
        pass

       

    

try:
    # Navigate to the URL
    browser.get('https://www.fangraphs.com/leaders/major-league?pos=all&stats=pit&type=8')
    wait = WebDriverWait(browser, 3)
    browser.maximize_window()
    time.sleep(sleep_duration)

    # Attempt to close any popups
    check_and_close_popup('//*[@id=":r0:"]/button')

    element = browser.find_element(By.XPATH, '//*[@id="content"]/div[7]/div[2]')
    browser.execute_script("arguments[0].scrollIntoView(true); window.scrollBy(0, -150);", element)  # Adjusts the scroll position by -150 pixels

    # Locate the dropdown
    dropdown = browser.find_element(By.XPATH, '//*[@id="content"]/div[16]/div[2]/div[3]/div[1]/select')   

    # Convert the dropdown WebElement to a Select object
    select = Select(dropdown)

    # Select by visible text (change 'All' to the desired option if different)
    select.select_by_visible_text('Infinity')

    # Wait for the page to refresh and the new set of data to load
    time.sleep(sleep_duration)

    # Initialize an empty DataFrame to store all players' data
    all_players_data = pd.DataFrame()

# Loop through each player
    for i in range(1, 101):  # Adjust this number based on the number of players
        try:
            player_data_dict = {}  # Initialize the dictionary for each player here
            rows = []  # Initialize the 'rows' list here

            # Extract player name and team (adjust the XPath according to the actual table structure)
            name_xpath = f'//table/tbody/tr[{i}]/td[1]'  # Assuming the name is in the first column
            team_xpath = f'//table/tbody/tr[{i}]/td[2]'  # Assuming the team is in the second column

            name = browser.find_element(By.XPATH, name_xpath).text
            team = browser.find_element(By.XPATH, team_xpath).text

            player_data_dict[name] = {
                'Name': name,
                'Team': team
            }


            time.sleep(sleep_duration)


            # Click the "Pitch-Level Data" button
            pitch_level_data_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[7]/div[2]')))
            pitch_level_data_button.click()
            #print("pitch level data button clicked")

            time.sleep(sleep_duration)


            # PITCH TYPE SCRAPING

            #print("TIME TO CHECK PITCH TYPE")

            # Attempt to close any popups
            check_and_close_popup('//*[@id=":r0:"]/button')

            # Click the "Pitch Type" button
            pitch_type_button = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[12]/div[4]/a[1]')))
            pitch_type_button.click()
            #print("pitch type button clicked")

            time.sleep(sleep_duration)

            # Attempt to close any popups
            check_and_close_popup('//*[@id=":r0:"]/button')

            IP_column_header = wait.until(EC.element_to_be_clickable((By.XPATH, '//th[@data-stat="IP"]')))
            IP_column_header.click()
            #print("IP button clicked")
            time.sleep(sleep_duration)


            # Parse the page content with BeautifulSoup
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            player_rows = soup.select('div.table-scroll > table > tbody > tr')
            if len(player_rows) >= i:
                current_player_row = player_rows[i - 1]
            else:
                break  # Exit the loop if there are no more rows

            # Extract Basic Player Info and Pitch Type Data
            name_element = current_player_row.select_one('td.align-left.fixed > a')
            name = name_element.text.strip()
            team = current_player_row.select_one('td:nth-child(3)').text.strip()

            player_data_pitch = [current_player_row.select_one(f'td[data-stat="{pitch}"]').text.strip() for pitch in pitch_types]

            # Store the extracted data in the DataFrame
            player_data_dict[name] = {
                'Name': name,
                'Team': team
            }


            for pitch, value in zip(pitch_types, player_data_pitch):
                player_data_dict[name][pitch] = value


            # H-MOVEMENT SCRAPING

            #print("TIME TO CHECK H-MOVEMENT")


            # Attempt to close any popups
            check_and_close_popup('//*[@id=":r0:"]/button')

            # Click the H-Movement button
            h_movement_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[12]/div[4]/a[3]')))
            h_movement_button.click()
            #print("H movement button clicked")

            time.sleep(sleep_duration)


            # Attempt to close any popups
            check_and_close_popup('//*[@id=":r0:"]/button')

            IP_column_header = wait.until(EC.element_to_be_clickable((By.XPATH, '//th[@data-stat="IP"]')))
            IP_column_header.click()
            #print("IP button clicked")
            time.sleep(sleep_duration)

            # Parse the page content again
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            player_rows = soup.select('div.table-scroll > table > tbody > tr')
            if len(player_rows) >= i:
                current_player_row = player_rows[i - 1]
            else:
                continue  # Skip to the next iteration of the loop if there are no more rows

            # Extract H-Movement data
            h_movement_data = [
                current_player_row.select_one(f'td[data-stat="{pitch_type}"]').text.strip() 
                if current_player_row.select_one(f'td[data-stat="{pitch_type}"]') else None 
                for pitch_type in h_movement_types
            ]

            # Store the H-Movement data in the player_data_dict using the href as the key
            for h_movement, value in zip(h_movement_types, h_movement_data):
                player_data_dict[name][h_movement] = value


            # V-MOVEMENT SCRAPING ---------

            # Attempt to close any popups
            check_and_close_popup('//*[@id=":r0:"]/button')

            # Click the V-Movement button
            v_movement_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[12]/div[4]/a[4]')))
            v_movement_button.click()
            time.sleep(sleep_duration)


            # Attempt to close any popups
            check_and_close_popup('//*[@id=":r0:"]/button')

            IP_column_header = wait.until(EC.element_to_be_clickable((By.XPATH, '//th[@data-stat="IP"]')))
            IP_column_header.click()
            time.sleep(sleep_duration)

            # Parse the page content again
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            player_rows = soup.select('div.table-scroll > table > tbody > tr')
            if len(player_rows) >= i:
                current_player_row = player_rows[i - 1]
            else:
                continue  # Skip to the next iteration of the loop if there are no more rows

            # Extract V-Movement data
            v_movement_data = [
                current_player_row.select_one(f'td[data-stat="{pitch_type}"]').text.strip() 
                if current_player_row.select_one(f'td[data-stat="{pitch_type}"]') else None 
                for pitch_type in v_movement_types
            ]

            # Store the V-Movement data in the player_data_dict using the href as the key
            for v_movement, value in zip(v_movement_types, v_movement_data):
                player_data_dict[name][v_movement] = value


            # VELOCITY SCRAPING

            # Attempt to close any popups
            check_and_close_popup('//*[@id=":r0:"]/button')

            # Click the Velocity button
            velocity_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[12]/div[4]/a[2]')))
            velocity_button.click()
            time.sleep(sleep_duration)

            # Attempt to close any popups
            check_and_close_popup('//*[@id=":r0:"]/button')

            IP_column_header = wait.until(EC.element_to_be_clickable((By.XPATH, '//th[@data-stat="IP"]')))
            IP_column_header.click()
            time.sleep(sleep_duration)

            # Parse the page content again
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            player_rows = soup.select('div.table-scroll > table > tbody > tr')
            if len(player_rows) >= i:
                current_player_row = player_rows[i - 1]
            else:
                continue  # Skip to the next iteration of the loop if there are no more rows

            # Extract Velocity data
            velocity_data = [
                current_player_row.select_one(f'td[data-stat="{pitch_type}"]').text.strip() 
                if current_player_row.select_one(f'td[data-stat="{pitch_type}"]') else None 
                for pitch_type in velocity_types
            ]

            # Store the Velocity data in the player_data_dict using the href as the key
            for velocity, value in zip(velocity_types, velocity_data):
                player_data_dict[name][velocity] = value


            # VALUE SCRAPING

            # Attempt to close any popups
            check_and_close_popup('//*[@id=":r0:"]/button')

            # Click the Pitch Value button
            pitch_type_value_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[12]/div[4]/a[5]')))
            pitch_type_value_button.click()
            time.sleep(sleep_duration)

            # Attempt to close any popups
            check_and_close_popup('//*[@id=":r0:"]/button')

            IP_column_header = wait.until(EC.element_to_be_clickable((By.XPATH, '//th[@data-stat="IP"]')))
            IP_column_header.click()
            time.sleep(sleep_duration)

            # Parse the page content again
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            player_rows = soup.select('div.table-scroll > table > tbody > tr')
            if len(player_rows) >= i:
                current_player_row = player_rows[i - 1]
            else:
                continue  # Skip to the next iteration of the loop if there are no more rows

            # Extract Pitch Value data
            pitch_type_value_data = [
                current_player_row.select_one(f'td[data-stat="{pitch_type}"]').text.strip() 
                if  current_player_row.select_one(f'td[data-stat="{pitch_type}"]') else None 
                for pitch_type in pitch_type_value_types
            ]

            # Store the Pitch Value data in the player_data_dict using the href as the key
            for pitch_type_value, value in zip(pitch_type_value_types, pitch_type_value_data):
                player_data_dict[name][pitch_type_value] = value

            # Print the dictionary to check the extracted data
            #print(player_data_dict)

            # Create an empty list to store the transformed data
            transformed_data = []

            # Define the pitch abbreviations for better readability
            pitch_abbreviations = {
                "FA%": "FA", "FT%": "FT", "FC%": "FC", "FS%": "FS", "FO%": "FO", 
                "SI%": "SI", "SL%": "SL", "CU%": "CU", "KC%": "KC", "EP%": "EP", 
                "CH%": "CH", "SC%": "SC", "KN%": "KN", "UN%": "UN"
            }

            # Transform the data
            for pitch, abbreviation in pitch_abbreviations.items():
                entry = {
                    'Pitch': abbreviation,
                    'Usage': player_data_dict[name].get(pitch, ''),
                    'X Axis': player_data_dict[name].get(f"{abbreviation}-X", ''),
                    'Y Axis': player_data_dict[name].get(f"{abbreviation}-Z", ''),
                    'Velocity': player_data_dict[name].get(f"v{abbreviation}", ''),
                    'Value': player_data_dict[name].get(f"w{abbreviation}", '')
                }
                transformed_data.append(entry)

            # Convert the list of dictionaries to a DataFrame
            df_transformed = pd.DataFrame(transformed_data)

            # Save the DataFrame to a CSV file
            filename_transformed = f"{name.replace(' ', '-')}-Paintomatic.csv"
            df_transformed.to_csv(filename_transformed, index=False)
            print(f"Transformed data saved to {filename_transformed}")




            # Loop through each pitch type and format the data as desired
            for pitch_type in pitch_types:
            # Extract the pitch type abbreviation (e.g., "FA%")
                pitch_abbr = pitch_type.split('%')[0]

            # Create a new row for each pitch type
                row = {
                    'Pitch': pitch_abbr,
                    'Usage': player_data_dict[name].get(pitch_type, ''),
                    'X Axis': player_data_dict[name].get(f"{pitch_abbr}-X", ''),
                    'Y Axis': player_data_dict[name].get(f"{pitch_abbr}-Z", ''),
                    'Velocity': player_data_dict[name].get(f"v{pitch_abbr}", ''),
                    'Value': player_data_dict[name].get(f"w{pitch_abbr}", '')
            }

            # Print the row to verify
            #print(row)

            # Append the row to the list
            rows.append(row)

        except Exception as e_inner:
                print(f"Error processing player at row {i}: {e_inner}")
                # Optionally continue to the next player or handle the error as needed

except Exception as e:
    print(f"Error encountered: {e}")

finally:
    browser.quit()
