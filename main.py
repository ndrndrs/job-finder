import json
import io
from bs4 import BeautifulSoup
import requests


def get_vacancies():
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"
    }
    url = "https://rabota.by/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&text=junior+Python+developer"
    response = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")
    vacancy_title = soup.find_all("div", class_="vacancy-serp-item__layout")

    job = {}
    for value in vacancy_title:
        try:
            title = value.find("a", class_="serp-item__title").text.strip()
            link = value.find("a", class_="serp-item__title").get("href")
            city = value.find(attrs={
                "class": "bloko-text",
                "data-qa": "vacancy-serp__vacancy-address"
            }).text
            key = link.split('/')[4].split('?')[0]
            job[key] = {
                "title": title,
                "link": link,
                "city": city
            }
        except AttributeError:
            continue
    with io.open("new_jobs.json", "w", encoding="utf-8") as file:
        json.dump(job, file, indent=4, ensure_ascii=False)


def check_vacancy():
    with open("new_jobs.json", encoding="utf-8") as file:
        jobs = json.load(file)
        headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"
        }
        url = "https://rabota.by/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&text=junior+Python+developer"
        response = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")
        vacancy_title = soup.find_all("div", class_="vacancy-serp-item__layout")
        for value in vacancy_title:
            link = value.find("a", class_="serp-item__title").get("href")
            key = link.split('/')[4].split('?')[0]
            if key not in jobs:
                try:
                    title = value.find("a", class_="serp-item__title").text.strip()
                    city = value.find(attrs={
                        "class": "bloko-text",
                        "data-qa": "vacancy-serp__vacancy-address"
                    }).text
                    jobs[key] = {
                        "title": title,
                        "link": link,
                        "city": city
                    }
                except AttributeError:
                    continue


def main():
    get_vacancies()
    check_vacancy()



if __name__ == "__main__":
    main()
