from scraper import JobinjaScraper

import concurrent.futures
import time
import json    



scraper = JobinjaScraper()
data_file = open("job_data.json", "w", encoding="utf-8")
total_pages = 12

def scrape_page(page_num):
    print("I run On Page", page_num)
    url = scraper._build_url(page=page_num)
    data = scraper.get_job_listings(url)
    return data

start_time = time.time()


with concurrent.futures.ThreadPoolExecutor() as executor:
    future_to_page = {executor.submit(scrape_page, page_num): page_num for page_num in range(1, total_pages+1)}
    jobs_data = []
    for future in concurrent.futures.as_completed(future_to_page):
        page_num = future_to_page[future]
        jobs_data.append(future.result())
    json.dump(jobs_data, data_file, ensure_ascii=False)

end_time = time.time()

print(f"Scraped {total_pages} pages in {end_time - start_time:.2f} seconds")

