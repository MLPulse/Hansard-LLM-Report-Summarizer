import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta

# Function to download a Hansard report for a specific date
def download_hansard_report(specific_date):
    date_str = specific_date.strftime('%Y-%m-%d')
    
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
    
    # Find if it's a sitting day
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
                pdf_path = f"data/Hansard_{date_str}.pdf"
                with open(pdf_path, 'wb') as file:
                    file.write(pdf_response.content)
                print(f"Hansard report saved at {pdf_path}.")
                return pdf_path
            else:
                print(f"Failed to download the Hansard report for {date_str}. Status code: {pdf_response.status_code}")
        except Exception as e:
            print(f"An error occurred while downloading the report for {date_str}: {e}")
    else:
        print(f"{date_str} is not a sitting day. No Hansard report available.")
    return None

# Function to download Hansard reports over a date range
def download_hansard_reports(start_date=None, end_date=None):
    if start_date is None:
        # No dates provided, use today
        start_date = datetime.now()
        end_date = start_date
    elif end_date is None:
        # Only one date provided, use it as both the start and end date
        end_date = start_date
    
    current_date = start_date
    while current_date <= end_date:
        download_hansard_report(current_date)
        current_date += timedelta(days=1)
