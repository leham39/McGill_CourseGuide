courseFile = open("courses_raw.csv", "r", encoding='utf-8')
lines = courseFile.readlines()
courseFile.close()

faculties = []
nums = []
facultyOptions = [
    ['misc_courses', 'No College Designated', '', 'GDEU', 'not GDEU', 'Dean'],
    ['management_courses', 'Desautels Faculty Management'],
    ['grad_courses', 'Graduate Studies'],
    ['envisci_courses', 'Faculty of Agric Environ Sci'],
    ['engineering_courses', 'Faculty of Engineering', 'Engineering (Non-Tr'],
    ['arts_courses', 'Faculty of Arts'],
    ['medicine_courses', 'Faculty of Medicine & Hlth Sci', 'Ingram School of Nursing', 'School of Phys & Occ Therapy', 'Post Graduate Medicine'],
    ['science_courses', 'Faculty of Science'],
    ['artsci_courses', 'Interfaculty; B.A. & Sc.', 'Shared'],
    ['law_courses', 'Faculty of Law'],
    ['continuing_studies', 'School of Continuing Studies'],
    ['dentistry_courses', 'Fac Dental Medicine & Oral HS', 'Post Graduate Dentistry'],
    ['education_courses', 'Faculty of Education'],
    ['music_courses', 'Schulich School of Music']
]

for option in facultyOptions:
    file = open("courses/" + option[0] + ".csv", "w", encoding='utf-8')
    file.write("Academic Unit,Course Number,Course Title,Credits,Semester,Prerequisites,Restrictions,Offered By,Description\n")
    option.append(file)

for line in lines[1:]:
    data = line.split(",")
    faculty = (data[7])[data[7].find('(')+1:data[7].find(')')]
    for option in facultyOptions:
        if faculty in option:
            option[-1].write(line)
            break

for option in facultyOptions:
    option[-1].close()

    

    #if(not faculty in faculties):
    #    faculties.append(faculty)
    #    print("Found new faculty:", faculty, "in class", data[0], data[1])
    #    nums.append(0)
    #nums[faculties.index(faculty)] += 1

#print("Faculties found:", [(faculties[i], nums[i]) for i in range(len(faculties))])