# -*- coding: utf-8 -*-

import requests
import re
import json
import time
import os
from bs4 import BeautifulSoup as bs

BASE_URL = 'https://career.habr.com/vacancies?type=all'
GROUP_URL = 'https://vk.com/@yvkurse'
CSV_FILE = 'yvkurse_articles.csv'
CSV_FIELDS = {
    'TITLE': 'Title',
    'COMPANY': 'Company',
    'IMAGE_URL': 'ImageURL'
}


class Scraper:
    """
    Base class for parsing vacancies from  and saving to CSV

    Methods
    -------
    scrape()
            Performs parsing articles from VK group

    save_csv()
            Performs saving parsed data to CSV
            
    process_data()
            Main method performing processing articles. It calling methods scrape() and save_csv()
    """
    def __init__(self):
        self.url = BASE_URL
        self.session = requests.Session()

    def scrape_vacancies(self):
        print('Scraper.scrape_vacancies')
        pass

    def scrape_skills(self):
        print('Scraper.scrape_skills')
        pass

    def save_csv(self):
        print('Scraper.save_csv')
        pass

    def process_data(self):
        print('Processing data ...')
        pass

class HabrScraper (Scraper):
    def __init__(self, json_file):
        Scraper.__init__(self)
        self.base_url = 'https://career.habr.com/'
        self.json_file = json_file


    def scrape_vacancies(self):
        print('Scraping ...')
        self.vacancies = []
        cnt = 0

        vacancies_url = '%s/vacancies?type=all' % self.base_url
    
        # get group page
        response = self.session.get(vacancies_url)

        soup = bs(response.text, 'lxml')

        vacancy_elements = soup.findAll('div', {'class': 'vacancy-card'})

        for vacancy_element in vacancy_elements:
            if cnt < 5: # 10:
                title = vacancy_element.find('a', {'class': 'vacancy-card__title-link'}).text
                link = vacancy_element.find('a', {'class': 'vacancy-card__title-link'})["href"]
                company = vacancy_element.find('a', {'class': 'link-comp'}).text
                publish_date = vacancy_element.find('time', {'class': 'basic-date'}).text
                # print(title)
                # print(link)

                vacancy_skills = []

                vacancy_page = '%s%s' % (self.base_url, link)
                # print(vacancy_page)

                vacancy_page_response = self.session.get(vacancy_page)

                vacancy_soup = bs(vacancy_page_response.text, 'lxml')
                # print(vacancy_page_response.text)
                # print(vacancy_soup)

                # print('Skills')

                content_sections = vacancy_soup.findAll('div', {'class': 'content-section'})
                # print(len(content_sections))
                for content_section in content_sections:
                    content_section_title = content_section.find('h2', {'class': 'content-section__title'}).text # 
                    # print(content_section_title)
                    if content_section_title == u"Требуемые навыки":
                        skill_elements = content_section.findAll('span', {'class': 'preserve-line'}) # 
                        # print(len(skill_elements))
                        for skill_element in skill_elements:
                            # print(skill_element.text)
                            # print(skill_element_text)
                            vacancy_skills.append(skill_element.text.encode('utf-8'))

                vacancy_data = {
                    'title': title,
                    'company': company,
                    'vacancy_skills': vacancy_skills,
                    'publish_date': publish_date
                }

                # print(vacancy_data)

                # print('\n')

                self.vacancies.append(vacancy_data)
            cnt += 1
        print(self.vacancies)
    
    def scrape_skills(self):
        print('Scraping ...')

    def save_json(self):
        print('Saving json...')
        # articles_df = pd.DataFrame.from_dict(self.vacancies)
        # articles_df.rename(columns={ 'title': CSV_FIELDS['TITLE'], 'text': CSV_FIELDS['TEXT'] }, inplace=True)
        # articles_df['skills'] = articles_df['vacancy_skills'].apply(lambda x: ', '.join([str(i) for i in x.encode('utf-16')])) # [','.join(vacancy['vacancy_skills'] for vacancy in self.vacancies)] # articles_df['vacancy_skills'].apply(lambda x: ','.join(map(str, x.encode('utf-8')))) # 
        # articles_df.to_csv(self.csv_file, encoding='utf-16')
        with open(self.json_file, 'w') as fp:
            json.dump(self.vacancies, fp)


    def process_data(self):
        print('Processing data ...')
        self.scrape_vacancies()
        
        self.save_json()


class HHScraper (Scraper):
    def __init__(self, json_file):
        Scraper.__init__(self)
        self.base_url = 'https://api.hh.ru/'
        self.json_file = json_file
        self.vacancies = []

    def scrape_vacancies(self):
        print('Scraping ...')
        url = '%svacancies' % self.base_url

        cnt = 0
        for page in range(0, 20):
            page_data = json.loads(self.get_page(url, page))
            #print(page_data.keys())

            #print('items' in page_data)

            # load vacancies
            for v in page_data['items']:
                if cnt == 4:
                    break
                req = requests.get(v['url'])
                data = req.content.decode()
                data = json.loads(data)
                #print(data['key_skills'])
                #print(data.keys())
                req.close()
                vacancy_skills = []
                for skill in data['key_skills']:
                    # print(skill_element.text)
                    # print(skill_element_text)
                    vacancy_skills.append(skill['name']) #.encode('utf-8'))
                print(type(data['name']))
                vacancy_data = {
                    'title': data['name'], #.encode('utf-8'),
                    'description': data['description'], #.encode('utf-8'),
                    'vacancy_skills': vacancy_skills,
                    'publish_date': data['published_at'], #.encode('utf-8'),
                }
                self.vacancies.append(vacancy_data)
                cnt += 1
                
                time.sleep(0.25)

            if page == 1: # if (page_data['pages'] - page) <= 1: # jsObj['pages'] - page
                break
            
            # optional timeout to make load on API lower, set to 5 sec
            time.sleep(0.25)
        print(self.vacancies[0])
            
        print('Parsing complete')

    def get_page(self, url, page = 0):
        print('get_page ', page)
        params = {
            'text': 'NAME:Аналитик', # Текст фильтра. В имени должно быть слово "Аналитик"
            'area': 1, # Поиск ощуществляется по вакансиям города Москва
            'page': page, # Индекс страницы поиска на HH
            'per_page': 100 # Кол-во вакансий на 1 странице
        }
        
        req = requests.get(url, params) # Send request to HH.ru API
        data = req.content.decode() # decode it to support non ascii symbols
        req.close()
        return data

    def save_json(self):
        print('Saving json...')
        # articles_df = pd.DataFrame.from_dict(self.vacancies)
        # articles_df.rename(columns={ 'title': CSV_FIELDS['TITLE'], 'text': CSV_FIELDS['TEXT'] }, inplace=True)
        # articles_df['skills'] = articles_df['vacancy_skills'].apply(lambda x: ', '.join([str(i) for i in x.encode('utf-16')])) # [','.join(vacancy['vacancy_skills'] for vacancy in self.vacancies)] # articles_df['vacancy_skills'].apply(lambda x: ','.join(map(str, x.encode('utf-8')))) # 
        # articles_df.to_csv(self.csv_file, encoding='utf-16')
        with open(self.json_file, 'w') as fp:
            json.dump(self.vacancies, fp)
            #fp.write(json.dumps(self.vacancies, ensure_ascii=False))


    def process_data(self):
        print('Processing data ...')
        self.scrape_vacancies()
        
        self.save_json()
