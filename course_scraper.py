import requests as reqs
from bs4 import BeautifulSoup
from bs4 import Tag
import time


allClassStart = time.perf_counter()
url = 'https://coursecatalogue.mcgill.ca/courses/'

response = reqs.get(url)
print()

#print("Response Type:", type(response))
print(response.url)
html_data = response.text
print("Response Data:", html_data)

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
        classes[text[:4]].append(text[5:].split(' - '))

allClassEnd = time.perf_counter()
print("Initial Scraping of All Classes took:", allClassEnd-allClassStart)
print("Num Academic Units:", len(categories))

eachClassStart = time.perf_counter()
#go through each unit and scrape the page for each class in the unit
for academicUnit in categories:
    print(academicUnit, )

    unitStart = time.perf_counter()
    for academicClass in classes[academicUnit]:

        classUrl = f'https://coursecatalogue.mcgill.ca/courses/{academicUnit.lower()}-{academicClass[0].lower()}'
        response = reqs.get(classUrl)

        #print("Response Type:", type(response))
        #print(response.url)
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

        academicClass.extend([credits, semester, preReqs, restricts, unit, classDesc.get_text()[14:-1]])
        #print(academicClass)
    unitEnd = time.perf_counter()
    print(f"Done {academicUnit} in {unitEnd-unitStart}s")

eachClassEnd = time.perf_counter()
print("DONE", eachClassEnd-eachClassStart)