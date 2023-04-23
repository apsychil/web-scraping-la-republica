import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

#XPATH_LINK_TO_ARTICLE = '//h2/a[contains(concat( " ", @class, " " ), concat( " ", "globoeconomiaSect", " " ))]/@href | //h2/a[contains(concat( " ", @class, " " ), concat( " ", "empresasSect", " " ))]/@href | //h2/a[contains(concat( " ", @class, " " ), concat( " ", "economiaSect", " " ))]/@href | //h2/a[contains(concat( " ", @class, " " ), concat( " ", "ocioSect", " " ))]/@href | //h2/a[contains(concat( " ", @class, " " ), concat( " ", "finanzasSect", " " ))]/@href | //h2/a[contains(concat( " ", @class, " " ), concat( " ", "internet-economySect", " " ))]/@href | //h2/a[contains(concat( " ", @class, " " ), concat( " ", "caja-fuerteSect", " " ))]/@href | //h2/a[contains(concat( " ", @class, " " ), concat( " ", "opa-por-nutresa-especialesSect", " " ))]/@href'
XPATH_LINK_TO_ARTICLE = '//text-fill/a[@class="economiaSect" or @class="empresasSect" or @class="ocioSect" or @class="globoeconomiaSect" or @class="analistas-opinionSect"]/@href'
XPATH_TITLE = '//div[@class = "mb-auto"]//h2/span/text()'
XPATH_SUMMARY = '//div[contains(@class, "lead")]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p/text()'

def get_title(link):
    #separamos por "/" y nos quedamos con el ultimo que elemento 
    url = link.split('/')[-1]
    #separamos por "-" y eliminamos el ultimo elemento
    title_list=url.split('-')[:-1]
    #Unimos lo anterior
    title = " ".join(title_list)

    return(title)


def parse_news(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            try:
                title = get_title(link)
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return
            
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_news = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_news:
                parse_news(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()
    
if __name__ == '__main__':
    run()