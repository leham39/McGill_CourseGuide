const courseCardTemplate = document.querySelector('[course-card-template]');
const courseInput = document.querySelector('#course');

let courses = [];

courseInput.addEventListener('input', e => {
    const value = e.target.value.toLowerCase();
    //console.log(`Filtering courses with value: ${value}`);
    courses.forEach(course => {
        const isVisible = course.code.includes(value) || course.title.includes(value);
        course.element.classList.toggle('hide', (!isVisible) || value === '');
       //console.log(`${value} + ${isVisible} + ${course.code} + ${course.code.includes(value)}`);
    });
})

async function fetchCSV(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.text();
        return data;
    } catch (error) {
        console.error("Error fetching CSV:", error);
        throw error;
    }
}

function validateCSV(csv) {
    const requiredHeaders = ["Academic Unit","Course Number","Course Title","Credits","Semester","Prerequisites","Restrictions","Offered By","Description"];
    const headers = csv[0];
    return requiredHeaders.every(header => headers.includes(header));
}

function loadFacultyCourses(faculty) {
    const url = `https://leham39.github.io/McGill_CourseGuide/courses/${faculty}_courses.csv`;
    fetchCSV(url)
        .then(csvText => {
            const csv = csvText.split('\n').map(row => row.split(','));
                document.getElementById('course-list').innerHTML = ''; // Clear existing courses
                document.getElementById('initialOption').style.display = 'none';
                courseInput.removeAttribute('disabled');
                courseInput.placeholder = "Search courses...";
            if (validateCSV(csv)) {
                courses = csv.slice(1, -1).map(row => {
                    const courseCard = courseCardTemplate.content.cloneNode(true).children[0];
                    courseCard.classList.add('hide');
                    const header = courseCard.querySelector('.header');
                    const body = courseCard.querySelector('.body');
                    const button = courseCard.querySelector('.button');
                    header.textContent = row[0] + " " + row[1]; // Assuming course number is in column 1, 2
                    body.textContent = row[2]; // Assuming course title is in column 3
                    button.textContent = "Course Page";
                    button.href = `https://coursecatalogue.mcgill.ca/courses/${row[0].toLowerCase()}-${row[1]}`; // Construct course page URL
                    document.getElementById('course-list').appendChild(courseCard);
                    //console.log(`Loaded course: ${row[0]} ${row[1]} - ${row[2]}`);
                    return { code: (row[0] + " " + row[1]).toLowerCase(), title: row[2].toLowerCase(), element: courseCard };
                })
                
            } else {
                console.error("CSV validation failed");
            }
        })
        .catch(error => {
            console.error("Error loading faculty courses:", error);
        });
}