courseFile = open("courses_raw.csv", "r", encoding='utf-8')
lines = courseFile.readlines()
courseFile.close()

faculties = []
for line in lines[1:]:
    data = line.split(",")
    faculty = (data[7])[data[7].find('(')+1:data[7].find(')')]
    if(not faculty in [f[2] for f in faculties]):
        faculties.append((data[0], data[1], faculty))

print("Faculties found:", faculties)