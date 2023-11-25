from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jops(keyword):
  base_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="
  # search_term = input("Enter a search term: ")
  search_term = keyword
  url = base_url + search_term

  response = get(f"{url}")

  if response.status_code != 200:
    print("Error: ", response.status_code)
  else:
    results = []
    soup = BeautifulSoup(response.text, "html.parser")
    jobss = soup.find_all('section', class_="jobs")

    for job_section in jobss:
      job_posts = job_section.find_all('li')
      job_posts.pop(-1)
      for post in job_posts:
        anchors = post.find_all('a')
        anchor = anchors[1]
        link = anchor['href']
        company, kind, region = anchor.find_all('span', class_="company")
        title = anchor.find('span', class_="title")
        job_data = {
            'link': f"https://weworkremotely.com{link}",
            # 'link': link,
            'company': company.string,
            'region': region.string,
            'position': title.string,
            'jobType': kind.string,
        }
        results.append(job_data)
    return results
