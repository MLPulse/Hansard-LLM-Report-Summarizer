import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def download_hansard_report(specific_date):
    # Convert the specific date to the format used by the website
    date_str = specific_date.strftime('%Y-%m-%d')
    
    # Check if the specific date is a sitting day
    calendar_url = 'https://www.ourcommons.ca/en/sitting-calendar/2024'
    
    try:
        response = requests.get(calendar_url)
        if response.status_code != 200:
            print(f"Failed to fetch the parliamentary calendar for {date_str}.")
            return
    except Exception as e:
        print(f"An error occurred while fetching the calendar for {date_str}: {e}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find if the specific date is a sitting day
    sitting_days = soup.find_all('td', class_=lambda x: x and date_str in x and 'chamber-meeting' in x)

    if sitting_days:
        print(f"{date_str} is a sitting day. Proceeding to fetch the Hansard report.")
        
        # Construct the URL for the Hansard PDF
        session_number = '441'  # Example session number; update as needed
        sitting_number = '328'  # Example sitting number; automate based on real data

        hansard_filename = f'HAN{sitting_number}-E.PDF'
        hansard_url = f'https://www.ourcommons.ca/Content/House/{session_number}/Debates/{sitting_number}/{hansard_filename}'
        
        try:
            pdf_response = requests.get(hansard_url)
            if pdf_response.status_code == 200:
                with open(f'Hansard_{date_str}.pdf', 'wb') as file:
                    file.write(pdf_response.content)
                print(f"Hansard report for {date_str} downloaded successfully.")
            else:
                print(f"Failed to download the Hansard report for {date_str}. Status code: {pdf_response.status_code}")
        except Exception as e:
            print(f"An error occurred while downloading the Hansard PDF for {date_str}: {e}")
    else:
        print(f"No sitting day on {date_str}. Cannot proceed with Hansard report download.")

def download_hansard_reports(start_date=None, end_date=None):
    if start_date is None:
        # No dates provided, use today's date
        start_date = datetime.now()
        end_date = start_date
    elif end_date is None:
        # Only one date provided, use it as both the start and end date
        end_date = start_date
    
    current_date = start_date
    while current_date <= end_date:
        download_hansard_report(current_date)
        current_date += timedelta(days=1)

if __name__ == "__main__":
    # Example usage
    download_hansard_reports(datetime(2024, 6, 17), datetime(2024, 6, 19))
