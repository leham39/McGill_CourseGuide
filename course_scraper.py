import requests as reqs
from bs4 import BeautifulSoup
from bs4 import Tag
import time
import math


allClassStart = time.perf_counter()
url = 'https://coursecatalogue.mcgill.ca/courses/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

with reqs.get(url, headers=headers) as response:
    response.raise_for_status()
    html_data = response.text
print()

print("Response Status:", response.status_code)
print(response.url)

if(not html_data):
    raise ValueError("No data received from the server")

print("Response Data:", html_data[:500])  # Print first 500 chars to avoid too much output

soup = BeautifulSoup(html_data, 'lxml')
content = soup.find(attrs={'id':'textcontainer'}).findChild()

#scrape the name of each class from the list of all classes
categories = []
classes = {}
for child in content.children:
    if(child.name):
        text = child.get_text()
        if(not text[:4] in categories):
            classes[text[:4]] = []
            categories.append(text[:4])
        classes[text[:4]].append(text[5:].split(' - ')[:2])

allClassEnd = time.perf_counter()
print("Initial Scraping of All Classes took:", allClassEnd-allClassStart)
print("Num Academic Units:", len(categories))

outputFile = open("courses_raw.csv", "w", encoding='utf-8')
outputFile.write("Academic Unit,Course Number,Course Title,Credits,Semester,Prerequisites,Restrictions,Offered By,Description\n")

eachClassStart = time.perf_counter()
#go through each unit and scrape the page for each class in the unit
unitCount = 0
for academicUnit in categories:
    unitCount += 1
    print("["+math.floor(unitCount/10 - 0.1)*"="+math.ceil((len(categories)-unitCount)/10)*"."+f"] {round(100*unitCount/len(categories), 1)}%", end=' ')
    print(academicUnit, end=' ')


    unitStart = time.perf_counter()
    classNum = 0
    for academicClass in classes[academicUnit]:
        classNum += 1

        classUrl = f'https://coursecatalogue.mcgill.ca/courses/{academicUnit.lower()}-{academicClass[0].lower()}'
        with reqs.get(classUrl, headers=headers) as response:
            response.raise_for_status()
            html_data = response.text
        #print("Response Data:", html_data)

        soup = BeautifulSoup(html_data, 'lxml')


        content = soup.find_all(attrs={'class':'row noindent'})
        classInfo = content[0].find_all('span', attrs={'class':'value'})
        classDesc = content[1]
        classReqs = content[2].find_all('li')

        #parse data from the top info section
        credits = 0
        unit = ''
        semester = ''
        for info in classInfo:
            infoTxt = info.get_text()
            #check if the line starts with a number, then its the credits
            if(infoTxt[0].isnumeric()):
                credits = int(infoTxt[0])
            elif("Winter " in infoTxt or "Fall " in infoTxt or "Summer " in infoTxt):
                #check if the line has a semester in it
                semester = infoTxt
            else:
                #otherwise its the academic unit
                unit = infoTxt

        #parse data from the bottom requirements section
        preReq = ''
        restrict = ''
        preReqs = []
        restricts = []
        for req in classReqs:
            #check if line is for prereqs or restrictions
            if(req.get_text().find("Prerequisite") != -1):
                preReq = req.get_text()[14:]
            if(req.get_text().find("Restriction") != -1):
                restrict = req.get_text()[13:]

        #check if the name for each academic unit is in the line, if so at it to a list and remove it from the line
        for aUnit in categories:
            while(preReq.find(aUnit) != -1):
                index = preReq.find(aUnit)
                preReqs.append(preReq[index:index+8])
                preReq = preReq[:index] + preReq[index+8:]
            while(restrict.find(aUnit) != -1):
                index = restrict.find(aUnit)
                restricts.append(restrict[index:index+8])
                restrict = restrict[:index] + restrict[index+8:]

        academicClass.extend([str(credits), semester, ";".join(preReqs), ";".join(restricts), unit, classDesc.get_text()[14:-1]])
        if(round(100*classNum/len(classes[academicUnit])) % 10 == 0):
            print('.', end='', flush=True)

        outputFile.write(academicUnit + "," + "||".join(academicClass).replace('\n', ' ').replace('\r', ' ').replace(',', ';').replace('||', ',') + "\n")
        #print(academicClass)
        

    unitEnd = time.perf_counter()

    print(f"Done {academicUnit} in {round(unitEnd-unitStart, 2)}s")

eachClassEnd = time.perf_counter()
print("DONE", eachClassEnd-eachClassStart)