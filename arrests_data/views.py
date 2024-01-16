import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from django.http import HttpResponse
import requests
from .models import ArrestRecord
import requests
from bs4 import BeautifulSoup
import datetime

from twocaptcha import TwoCaptcha

from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from datetime import timedelta

from django.utils import timezone

from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from django.db.models import Count

import json
from django.db.models.functions import TruncDay


# graph
def arrest_records_by_date(request):
    current_date = datetime.date.today()
    start_of_month = current_date.replace(day=1)
    end_of_month = datetime.date(current_date.year, current_date.month + 1, 1) if current_date.month < 12 else datetime.date(current_date.year + 1, 1, 1)

    records = ArrestRecord.objects.filter(
        arrest_date__range=(start_of_month, end_of_month)
    ).annotate(
        day=TruncDay('arrest_date')
    ).values('day').annotate(count=Count('id')).order_by('day')

    formatted_records = [{'day': record['day'].strftime("%Y-%m-%d"), 'count': record['count']} for record in records]

    context = {
        'records_json': json.dumps(formatted_records)
    }

    return render(request, 'accounts/stats.html', context)


# dashboard
@login_required
def dashboard(request):
    time_filter = request.GET.get('time_filter', '24 hours')
    now = timezone.now()

    if time_filter == '24 hours':
        start_date = now - timedelta(days=1)
    elif time_filter == '7 days':
        start_date = now - timedelta(days=7)
    elif time_filter == 'Month':
        start_date = now - timedelta(days=30) 
    elif time_filter == 'Year':
        start_date = now - timedelta(days=365)
    else:
        start_date = now - timedelta(days=1)

    records_list = ArrestRecord.objects.filter(arrest_date__gte=start_date).order_by('-arrest_date', 'id')
    total_records = records_list.count()
    paginator = Paginator(records_list, 10)

    page_number = request.GET.get('page')
    records = paginator.get_page(page_number)
    return render(request, 'accounts/dashboard.html', {
        'records': records, 
        'total_records': total_records,
        'time_filter': time_filter
        })


def get_state():
    html=requests.get("https://apps.adacounty.id.gov/sheriff/reports/").text
    soup=BeautifulSoup(html,"html.parser")
    state=soup.find("input",{"id":"__VIEWSTATE"})["value"]
    state_generator=soup.find("input",{"id":"__VIEWSTATEGENERATOR"})["value"]
    event_validation=soup.find("input",{"id":"__EVENTVALIDATION"})["value"]
    
    return state,state_generator,event_validation

def get_report():
    state, state_generator, event_validation = get_state()

    headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Accept-Language': 'en-US,en;q=0.9,ar-TN;q=0.8,ar;q=0.7',
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive',
		'Origin': 'https://apps.adacounty.id.gov',
		'Pragma': 'no-cache',
		'Referer': 'https://apps.adacounty.id.gov/sheriff/reports/',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
		'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
	}
    
    data = {
		'__EVENTTARGET': 'ctl00$ContentPlaceHolder1$btnSearch',
		'__EVENTARGUMENT': '',
		'__LASTFOCUS': '',
		'__VIEWSTATE': state,
		'__VIEWSTATEGENERATOR': state_generator,
		'__EVENTVALIDATION': event_validation,
		'ctl00$ContentPlaceHolder1$ddlViewOption': '120',
		'ctl00$ContentPlaceHolder1$ddlSortOption': '2',
		'ctl00$ContentPlaceHolder1$ddlReverseOption': '0',
		'ctl00$ContentPlaceHolder1$txtFilterText': '',
		'ctl00$ContentPlaceHolder1$txtPersonID': '0',
	}
	
    html = requests.post('https://apps.adacounty.id.gov/sheriff/reports/', headers=headers, data=data).text
    soup=BeautifulSoup(html,"html.parser")

    arrests=soup.find_all("div",{"class":"arrest"})
    message="<head><meta http-equiv='Content-Type' content='text/html; charset=utf-8'><style type='text/css'>table {width: 100%; table-layout: fixed; border-collapse: collapse;border: 1px solid black;}td {border: 1px solid black;}</style></head>"
    message+="<table style='border: black 1px solid;'><tr><td><strong>Name</strong></td><td><strong>Age</strong></td><td><strong>Address</strong></td><td><strong>Date</strong></td><td><strong>Time</strong></td><td><strong>agency</strong></td><td><strong>Severity</strong></td><td><strong>Charge</strong></td><td><strong>Statute</strong></td><td><strong>Type</strong></td></tr>\n"

    arrest_names = []
    for arrest in arrests:
        
        arrest_name=arrest.find("div",{"class":"myNameTitle"}).find("strong").text
        address=arrest.find("div",{"class":"myNameTitle"}).find("small").text
        warnings=arrest.find("table",{"class":"charge table table-condensed table-responsive"}).find_all("tr")
        info=arrest.find("div",{"class":"info"}).text
        try:
            age=info.split("Age:")[1].split("Arrest Date:")[0].strip()
        except:
            age=""
        try:
            date=info.split("Arrest Date:")[1].split("Time")[0].strip()
        except:
            date=""
        try:
            time=info.split("Time:")[1].split("Status")[0].strip()
        except:
            time=""

        try:
            # Split the date string and add the current year
            date_parts = date.split(' ')
            if len(date_parts) > 1:
                date_str = date_parts[1]
            else:
                continue 

            current_year = datetime.datetime.now().year
            date_str = f'{date_str}/{current_year}'
        except ValueError as e:
            print(e)


        for warning in warnings[1:]:
            agency=warning.find_all("td")[0].text
            severity=warning.find_all("td")[1].text
            charge=warning.find_all("td")[2].text
            statute=warning.find_all("td")[3].text
            type=warning.find_all("td")[4].text
            if severity=="M" and "driving under the influence" in charge.lower():
                message+="<tr><td>"+arrest_name+"</td><td>"+age+"</td><td>"+address+"</td><td>"+date+"</td><td>"+time+"</td><td>"+agency+"</td><td>"+severity+"</td><td>"+charge+"</td><td>"+statute+"</td><td>"+type+"</td></tr>\n"
                arrest_details=[arrest_name,address,agency,severity,charge,statute,type,age,date,time]
                arrest_names.append(arrest_name)
                #print(arrest_details)

                record = ArrestRecord(
                name=arrest_name,
                address=address,
                agency=agency,
                severity=severity,
                charge=charge,
                statute=statute,
                arrest_type=type,
                age=age,
                arrest_date = datetime.datetime.strptime(date_str, '%m/%d/%Y').date(),
                arrest_time = datetime.datetime.strptime(time, '%I:%M %p').time()
            )
            try:
                record.save()
            except Exception as e:
                print(f"Error saving record: {e}")


def run_script(request):
    get_report()

    return redirect('dashboard')


from selenium.common.exceptions import TimeoutException
def search_script(request):

    solver = TwoCaptcha('3608f5e5012070ab8e5d1209dca111d6')

    # Use Firefox options and driver instead of Chrome
    firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument("--incognito")
    # Set headless mode
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    for record in ArrestRecord.objects.all():
        print(record.name)
        # Navigate to the website
        driver.get("https://mycourts.idaho.gov/odysseyportal/Home/Dashboard/29")

        # Find the search input field and enter the name
        search_box = driver.find_element(By.XPATH, "//*[@id='caseCriteria_SearchCriteria']")
        search_box.clear()
        search_box.send_keys(record.name)

        time.sleep(10)

        try:
            print("recaptcha find")
            result = solver.recaptcha(
				sitekey='6LfqmHkUAAAAAAKhHRHuxUy6LOMRZSG2LvSwWPO9',
                url='https://mycourts.idaho.gov/odysseyportal/Home/Dashboard/29')
            print("recaptcha find 1")
            driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{result['code']}';")
            print("recaptcha find 2")
        except Exception as e:
            print("recaptcha find not")
            print(e)
            
        submit_button = driver.find_element(By.XPATH, "//*[@id='btnSSSubmit']")
        submit_button.click()
        
        try:
            wait = WebDriverWait(driver, 50)
            results_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "caseLink")))
            
            if "CR01-24-00" in results_element.text:
                results_element.click()

                state_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='divPartyInformation_body']/div[1]/div[2]/div[2]/div[1]/div/div/div")))
                defendant_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='divPartyInformation_body']/div[3]/div[2]/div[2]/div[1]/div/div/div")))

                state_text = state_element.text
                defendant_text = defendant_element.text
                #print("State:", state_text)
                print(f"State for {record.name} is: {state_text}")
                print(f"Defendant for {record.name} is: {defendant_text}")
                record.state_lawyer = state_text
                record.defendant_lawyer = defendant_text

                # Save the updated record to the database
                record.save()

            else:
                print("No Lawyer")
        except TimeoutException:
            print(f"No results found for {record.name}, moving to next record.")
            continue

    driver.quit()
    return redirect('dashboard')

