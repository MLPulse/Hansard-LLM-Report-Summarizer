import requests
from bs4 import BeautifulSoup
import os

def download_hansard_report(specific_date):
    date_str = specific_date  # assuming date is already in YYYY-MM-DD format

    # Create 'data/' directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    # Check if the specific date is a sitting day
    calendar_url = 'https://www.ourcommons.ca/en/sitting-calendar/2024'
    
    try:
        response = requests.get(calendar_url)
        if response.status_code != 200:
            print(f"Failed to fetch the parliamentary calendar for {date_str}.")
            return None
    except Exception as e:
        print(f"An error occurred while fetching the calendar for {date_str}: {e}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check if it's a sitting day
    sitting_days = soup.find_all('td', class_=lambda x: x and date_str in x and 'chamber-meeting' in x)

    if sitting_days:
        print(f"{date_str} is a sitting day. Proceeding to fetch the Hansard report.")
        
        session_number = '441'  # Example session number
        sitting_number = '328'  # Example sitting number (can automate retrieval)
        hansard_filename = f'HAN{sitting_number}-E.PDF'
        hansard_url = f'https://www.ourcommons.ca/Content/House/{session_number}/Debates/{sitting_number}/{hansard_filename}'
        
        try:
            pdf_response = requests.get(hansard_url)
            if pdf_response.status_code == 200:
                pdf_path = f"data/{hansard_filename}"
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_response.content)
                print(f"Hansard report saved at {pdf_path}.")
                return pdf_path
            else:
                print(f"Failed to download Hansard report for {date_str}.")
        except Exception as e:
            print(f"An error occurred while downloading the report: {e}")
    else:
        print(f"{date_str} is not a sitting day.")
    return None
