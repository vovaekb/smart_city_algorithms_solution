# -*- coding: utf-8 -*-

import requests
import re
import json
import time
import os
from bs4 import BeautifulSoup as bs


class HHScraper:
    def __init__(self, keyword, json_file=None):
        self.base_url = 'https://api.hh.ru/'
        self.json_file = json_file
        self.keyword = keyword
        self.vacancies = []

    def scrape_vacancies(self):
        print('Scraping ...')
        url = '%svacancies' % self.base_url

        cnt = 0
        for page in range(0, 20):
            page_data = json.loads(self.get_page(url, page=page))
            #print(page_data.keys())

            #print('items' in page_data)

            # load vacancies
            for v in page_data['items']:
                # if cnt == 4:
                #     break
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
                # print(type(data['name']))
                vacancy_data = {
                    'id': data['id'],
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

    def get_page(self, url,  page = 0):
        print('get_page ', page)
        print('search keyword: ', self.keyword)
        params = {
            'text': 'NAME:%s' % self.keyword, # Текст фильтра. В имени должно быть слово "Аналитик"
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
        
        # self.save_json()
        return self.vacancies
