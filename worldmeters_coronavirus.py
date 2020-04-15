import requests
import csv
from bs4 import BeautifulSoup


def get_data():
    url = 'https://www.worldometers.info/coronavirus/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.163 Safari/537.36 '
    }

    main_table_selector = "table#main_table_countries_today"
    rows_selector = "tbody > tr"
    tds_selector = "td"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = list()
        soup = BeautifulSoup(response.content, features='html.parser')
        main_table = soup.select(main_table_selector)[0]
        rows = main_table.select(rows_selector)
        rows = rows[8:220]
        for row in rows:
            tds = row.select(tds_selector)
            entry = {
                "country": tds[0].text,
                "total_cases": tds[1].text,
                "new_cases": tds[2].text,
                "total_deaths": tds[3].text,
                "new_deaths": tds[4].text,
                "total_recovered": tds[5].text,
                "active_cases": tds[6].text,
                "serious_critical": tds[7].text,
                "tot_case_per_1m_pop": tds[8].text,
                "deaths_per_1m_pop": tds[9].text,
                "total_tests": tds[10].text,
                "test_per_1m_pop": tds[11].text,
            }
            data.append(entry)
        return data
    return None


def main():
    data = get_data()
    with open('coronavirus.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data[0].keys())
        for country in data:
            writer.writerow(country.values())
    print("Data saved to coronavirus.csv")


if __name__ == "__main__":
    main()