

import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest



result = requests.get("https://candidat.pole-emploi.fr/offres/recherche?motsCles=data+engineer&offresPartenaires=true&range=0-19&rayon=10&tri=0")


#you can enter link of job you are searching for

src = result.content


#the data that will scraped : job title / company_name / job_city / contrat_type / pub_date / salaries / number of working hour


job_titles = []
company_names = []
job_city = []
contrat_types = []
pub_date = []
links = []
hamid = []
salaries = []
horaires = []






soup = BeautifulSoup(src, "lxml")





job_title = soup.find_all("h2", {"class":"t4 media-heading"})
company_name = soup.find_all("p", {"class" :"subtext"})
contrat_type = soup.find_all("p", {"class" :"contrat visible-xs"})
pub_dates = soup.find_all("p", {"class" :"date"})

links = soup.find_all("a", {"class" :"media with-fav"})

'https://candidat.pole-emploi.fr' + links[0]['href']
urls = ['https://candidat.pole-emploi.fr' + link['href'] for link in links]






jobs = [item.text.strip() for item in job_title]

companies = [item.text.strip().split()[0] for item in company_name]



cities  = [item.text.strip().split('\n')[1].split('- ')[1] for item in company_name]



contrat = [item.text.replace('\n\xa0-\xa0',"-") for item in contrat_type]

dates = [item.text.strip() for item in pub_dates]




for i in range(len(job_title)):
    job_titles.append(jobs[i])
    pub_dates.append(dates[i])
    contrat_types.append(contrat[i])
    job_city.append(cities[i])
    
    
for link in urls :
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    
    horaire = soup.find("dd", {'itemprop' : 'workHours'})
    salary = soup.find("dl", {"class":"icon-group"})
    
    salary = list(salary.stripped_strings)[-1]
 
    salaries.append(salary)
    
    
    
    horaire = horaire.text.strip()
    
    horaires.append(horaire)
   





file_list = [jobs, companies, contrat, cities, dates, urls, salaries, horaires]
exported = zip_longest(*file_list)

with open("C:\\Users\\**\\OneDrive\\Bureau\\pyproject\\p.csv type csv file path to store the information", "w", encoding = 'utf-8') as myfile:
        wr = csv.writer(myfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        wr.writerow(["job_title", "company_name", "contrat_type", "job_city", "dates", "links", "salaries", "horaires de travail"])
        wr.writerows(exported)



