# -*- coding: utf-8 -*-

import requests
import re
import json

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
    """
    Class for parsing vacancies from Habr Career and saving to JSON file

    Methods
    -------
    scrape_vacancies()
            Performs parsing articles from VK group

    save_json()
            Performs saving parsed data to CSV
            
    process_data()
            Main method performing processing articles. It calling methods scrape() and save_csv()
    """
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
                pubish_date = vacancy_element.find('time', {'class': 'basic-date'}).text
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
                            # skill_element_text = skill_element.find('a').text
                            # print(skill_element_text)
                            vacancy_skills.append(skill_element.text.encode('utf-8'))

                vacancy_data = {
                    'title': title,
                    'company': company,
                    'vacancy_skills': vacancy_skills,
                    'pubish_date': pubish_date
                    # 'text': text
                }

                # print(vacancy_data)

                # print('\n')

                self.vacancies.append(vacancy_data)
            cnt += 1
        '''
        article_elements = soup.findAll('div', {'class': 'author-page-article'})
    
        for article_element in article_elements:
            title = article_element.find('span', {'class': 'author-page-article__title'}).text
            
            # open article page 
            link_element = article_element.find('a', {'class': 'author-page-article__href'})
            link = f'{BASE_URL}{link_element["href"]}'
        
            article_page = self.session.get(link)
            article_content = bs(article_page.text, 'lxml')
        
            # parse text
            text_elements = article_content.findAll('p', {'class': 'article_decoration_before'})

            text_chunks = [text_element.text for text_element in text_elements]
            text = '\n'.join(text_chunks)

            # get images
            image_elements = article_content.findAll('img', {'class': ['article_object_photo__image_blur', 'article_carousel_img']})
            image_urls = [image['src'] for image in image_elements]

            article_data = {
                'title': title,
                'text': text
            }

            for i, image_url in enumerate(image_urls):
                article_data[f'{CSV_FIELDS["IMAGE_URL"]}{i+1}'] = image_url

            self.articles.append(article_data)
        '''
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

def parse_habr_career():
    scraper = HabrScraper(json_file = 'habr_vacancies.json')
    scraper.process_data()

if __name__ == '__main__':
    parse_habr_career()
