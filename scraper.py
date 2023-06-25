from requests import post, get
from bs4 import BeautifulSoup
import urllib
import time


class JobinjaScraper:
    base_url = 'https://jobinja.ir'

    def __init__(self):
        self.cookies = {
            'remember_82e5d2c56bdd0811318f0cf078b78bfc': 'eyJpdiI6IlRRbFR6QmVhTFdpMTR3MzNPc2lqT1E9PSIsInZhbHVlIjoiTWFFRVFpY2NueGd3MlpGTzN0SlwvR2dcL2NFaEZPOEk4OXV6YzNYaXVKQWEyTTd4ZkZNS3ArellpaDZIbWxCSk9vS1FBcFRXZCtVTlwvY1RqZ0dzeEs4OHZ3ZW1RWmp4VTJ3K2hzVXhpVndaRjA9IiwibWFjIjoiNjlhYjNhMjkxM2E3NzMxMTQyYjhkOWViZDM2MzM5M2RiZGFjMWMyYmNkY2FhYzEzYzcwYmIwOTc0ZmQyYzU4YiJ9',
            'user_mode': 'eyJpdiI6InMybGRIVUFPbGU5TXdVampvUXJBdHc9PSIsInZhbHVlIjoiS3hSZGlKOWV2Q1dQOW84SFRBa3l6dz09IiwibWFjIjoiYTQyYzU4MjVjYzdiMzYzZGFkZjI0MWZmOTlhNTZjMjcwYTAzMWVjYjYzYjNkYzQ4YTUzNzliM2NkYWZkNmE3ZCJ9',
            'device_id': 'eyJpdiI6IjJhN0V5eng5YkVnTUlVS2d1VFdTMXc9PSIsInZhbHVlIjoib0ZJUlJhRzczbWZ6dUhPeFZ6ZFVFZz09IiwibWFjIjoiYzk3ODM0YTYwNGE2ZjRjNGZkYTgzMzYwYWJlMzcwMDhiY2VhOTkxM2I4MWUzMjVhMDhlMjFlNmQwZTM5OWExYSJ9',
            'XSRF-TOKEN': 'eyJpdiI6IkROejV0TTA5WU1ZWUVKQjNhOEFhNWc9PSIsInZhbHVlIjoienJKSFQra3VSbVNQcVJSbFJvTTRaY25DRGk3WkEyWENlOHVpQnFoa3YrSVV0VXllUjExZ2tGclIxZG12bmgwbmpIbEpUd3JtWTBoYkdjZTA0K3Qxb2c9PSIsIm1hYyI6IjNiMzVkZjA1ZWMyZjY1NmZkODg4ZDVlN2QxZjUzZDlkOTBlYzU5YjNiZDE1OWI1MDkyYmY3NzkyZGVjZDdlYWIifQ^%^3D^%^3D',
            'JSESSID': 'eyJpdiI6Ik1HMVZLNWxiVHQralwvQTNqRW43WGpRPT0iLCJ2YWx1ZSI6IlZtekxwVlRaTlg4NGtWbXdadHUzTHF6c3ZJRXo5OUxpYTFiZWZIdEYzeGRURzlEdjVHaGswRTFoUEJtcnpZTldMM3BlazRVa1UzR2NMeHU0Z08rRVd3PT0iLCJtYWMiOiIyYjIxY2RlMmJmOWJjNzQ5OGQxZDM0M2UxNTE1ZTcxZDY2YWVmMDFjMGI0OTMyZmI3ODE2YzEzMThkZTYxZmQ0In0^%^3D',
            'logglytrackingsession': '3bb8749b-6684-42e0-9b3d-30befa9bd697',
        }

    def _add_filters_to_query_params(self, filters, filter_type, query_params):
        if filters:
            filters = {f'filters[{filter_type}][{str(i)}]': f for i, f in enumerate(filters)}
            query_params.update(filters)

    def _build_url(self, locations=None, keywords=None, categories=None, min_salary=None, max_salary=None, page=1):
        query_params = {
            'page': page,
            'filters[sal_min][4]': f"{min_salary}:" if min_salary else '',
            'filters[sal_max][4]': f":{max_salary}" if max_salary else '',
            'preferred_before': int(time.time())
        }
        self._add_filters_to_query_params(keywords, 'keywords', query_params)
        self._add_filters_to_query_params(locations, 'locations', query_params)
        self._add_filters_to_query_params(categories, 'job_categories', query_params)

        url_parts = list(urllib.parse.urlparse(self.base_url))
        url_parts[2] = '/jobs'
        url_parts[4] = urllib.parse.urlencode(query_params)

        return urllib.parse.urlunparse(url_parts)

    def get_job_listings(self, url):
        response = get(url, cookies=self.cookies)
        soup = BeautifulSoup(response.text, 'html.parser')
        job_list = soup.find_all('div', class_='c-jobListView__itemWrap')
        jobs_data = []
        for job in job_list:
            job_data = self.extract_job_info(job)
            jobs_data.append(job_data)
        return jobs_data

    def extract_job_info(self, job: BeautifulSoup):
        job_title = job.find('a', class_='c-jobListView__titleLink').text.strip().replace("\u200c", " ")
        meta_item = job.find('ul', class_='o-listView__itemComplementInfo').find_all("li")
        job_location = meta_item[1].text.strip()
        job_salary = meta_item[2].text.strip().replace("\n            ", "").replace("\n    ", " ")
        company_img = job.find("img")["src"].split("format(jpeg)/")[-1]
        company_name = job.find('i', class_='c-icon--construction').parent.text.strip()
        detail_url = "/".join(job.find("a")["href"].split("/")[:-1])
        return {
            'job_title': job_title,
            'company_name': company_name,
            'company_img': company_img,
            'job_location': job_location,
            'job_salary': job_salary,
            'detail_url': detail_url,
        }

    def scrape_job_detail(self, job_id):
        pass

    def scrape_jobs(self, location='', keywords=[], categories=[], min_salary=None, max_salary=None, page=1):
        pass

