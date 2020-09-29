import requests
from bs4 import BeautifulSoup

user_agent = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}

# def read_data(filename):
#     with open(filename, 'r', encoding='utf-8') as f:
#         request_list = f.readlines()

#     for link in request_list:
#         try:
#             r = requests.get(link, header=user_agent)
#             soup = BeautifulSoup(r.text, 'html.parser')
#         except:
#             with open('bug_report.txt', 'w') as f:
#                 f.write(f"{link}\n")
#     return soup

def get_questions(soup):
    heading_area = soup.find('div', {'class': 'c-heading__title'})
    question_area = soup.find('div',{'class':'c-heading__content'})
    data = {
        'title': heading_area.text.replace('\t','').replace('\n',''),
        'description': question_area.text.replace('\t','').replace('\n','')
    }
    return data

def get_answer(soup):
    adopt_check = soup.find('div', {'class': 'adopt-check-box'})
    answer_area = adopt_check.find_parent('div', {'class': 'answer-content__item'})
    answer_area = answer_area.find('div', {'class': 'c-heading-answer__content'})
    data = {
        'description': ' '.join(answer_area.find('div', {'class': 'se-main-container'}).text.split()).replace('\t','').replace('\n','')
    }
    return data
