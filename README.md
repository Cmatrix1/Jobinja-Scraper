# جاب‌اينجا اسکرپر

این پروژه یک اسکرپر برای وب سایت جاب‌اينجا است که با استفاده از زبان پایتون و کتابخانه های BeautifulSoup و requests پیاده سازی شده است. هدف اصلی این پروژه، جمع آوری اطلاعات مربوط به شغل‌های موجود در سایت جاب‌اينجا است. برای دسترسی به این اطلاعات، از صفحات سایت جاب‌اينجا در قالب JSON استفاده شده است.

## نصب

برای استفاده از این اسکرپر، ابتدا باید کتابخانه های `requests` و `BeautifulSoup4` را نصب کنید:

```bash
pip install requests
pip install beautifulsoup4
```

سپس فایل `scraper.py` را در پروژه خود بگنجانید.

## استفاده

برای استفاده از این اسکرپر، ابتدا یک شی از کلاس `JobinjaScraper` بسازید:

```python
from scraper import JobinjaScraper

scraper = JobinjaScraper()
```

سپس با استفاده از تابع `scrape_jobs` می‌توانید اطلاعات مربوط به فرصت های شغلی را دریافت کنید:

```python
jobs_data = scraper.scrape_jobs(location='تهران', keywords=['برنامه نویس'], categories=['فناوری اطلاعات'], min_salary=10000000, max_salary=20000000, page=1)
```

تابع `scrape_jobs` یک سری پارامتر ورودی می‌گیرد:

- `location`: محل کار (اختیاری)
- `keywords`: لیست کلمات کلیدی مربوط به شغل (اختیاری)
- `categories`: لیست دسته بندی های مربوط به شغل (اختیاری)
- `min_salary`: حداقل حقوق (اختیاری)
- `max_salary`: حداکثر حقوق (اختیاری)
- `page`: شماره صفحه (اختیاری، با مقدار پیشفرض 1)

تابع `scrape_jobs` لیستی از فرصت های شغلی را برمی‌گرداند. هر فرصت شغلی یک دیکشنری است که شامل اطلاعات زیر است:

- `job_title`: عنوان شغل
- `company_name`: نام شرکت
- `company_img`: لینک عکس شرکت
- `job_location`: محل کار
- `job_salary`: حقوق
- `detail_url`: آدرس صفحه جزئیات فرصت شغلی

## مثال

برای نمونه، در ادامه یک کد ساده نوشته شده است که با استفاده از این اسکرپر، اطلاعات مربوط به فرصت های شغلی مربوط به برنامه نویسی در شهر تهران را دریافت می‌کند:

```python
from scraper import JobinjaScraper

scraper = JobinjaScraper()

jobs_data = scraper.scrape_jobs(location='تهران', keywords=['برنامه نویس'], categories=['فناوری اط
