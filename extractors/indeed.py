from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_page_count(search_term):
    base_url = "https://kr.indeed.com/jobs"
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(options=options)
    browser.get(f"{base_url}?q={search_term}")
    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("ul", class_="css-1g90gv6 eu4oa1w0")
    pages = pagination.find_all("li", recursive=False)
    if len(pages) == 0:
        return 1
    count = len(pages)
    if count >= 5:
        return 5
    else:
        return count    

def extract_indeed_jobs(search_term):
    pages = get_page_count(search_term)
    print("Found", pages, "pages")
    results = []
    for page in range(pages):
        base_url = "https://kr.indeed.com/jobs"
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        print(f"requesting {base_url}?q={search_term}&start={page}0")
        browser = webdriver.Chrome(options=options)
        browser.get(f"{base_url}?q={search_term}&start={page}0")
        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_ = "css-zu9cdh eu4oa1w0")
        jobs = job_list.find_all("li", recursive=False)

        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", attrs={"data-testid": "company-name"})
                location = job.find("div", attrs={"data-testid": "text-location"})
                job_data = {
                    "position": title,
                    "link": f"https://kr.indeed.com{link}",
                    "company": company.string,
                    "location": location.string,
                }
                results.append(job_data)
    return results