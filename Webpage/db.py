#!/usr/bin/python3
print('Content-type: text/html\n\n')
import psycopg2
import cgi
import cgitb; cgitb.enable()
import html

class UniversityData:
    def __init__(self):
        self.conn_params = {
            'host': '192.168.56.20',
            'dbname': 'postgres',
            'user': 'webuser1',
            'password': 'student',
            'port': '5432'
        }

    def get_db_connection(self):
        try:
            return psycopg2.connect(**self.conn_params)
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    def fetch_faculty(self, sort_by=None, keyword=None):
        conn = self.get_db_connection()
        if conn is None:
            return []
        cur = conn.cursor()
        sql_query = 'SELECT * FROM public."Faculty"'
        if keyword:
            sql_query += f" WHERE \"First\" ILIKE '%{keyword}%' OR \"Last\" ILIKE '%{keyword}%' OR \"Rank\" ILIKE '%{keyword}%'"
        if sort_by == 'name':
            sql_query += ' ORDER BY "Last", "First"'
        elif sort_by == 'rank':
            sql_query += ' ORDER BY "Rank", "Last", "First"'
        cur.execute(sql_query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def fetch_prerequisites(self):
        conn = self.get_db_connection()
        if conn is None:
            return []
        cur = conn.cursor()
        cur.execute('SELECT * FROM public."Prerequisites"')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def fetch_courses(self):
        conn = self.get_db_connection()
        if conn is None:
            return []
        cur = conn.cursor()
        cur.execute('SELECT * FROM public."Schedule History"')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def calculate_fte(self, ch, enrollment, course_type):
        divisors = {
            'CSCI_graduate': 186.23,
            'CSCI_undergraduate': 406.24,
            'SENG_graduate': 90.17,
            'SENG_undergraduate': 232.25,
            'DASC': 186.23
        }
        divisor = divisors.get(course_type)
        if divisor:
            return (ch * enrollment) / divisor
        else:
            raise ValueError("Invalid course type")

    def fetch_courses_for_fte(self, faculty=None, year=None, semester=None):
        conn = self.get_db_connection()
        if conn is None:
            return []
        cur = conn.cursor()
        query = 'SELECT ch, enrollment, course_type FROM public."Courses" WHERE True'
        if faculty:
            query += f" AND faculty = '{faculty}'"
        if year:
            query += f" AND year = {year}"
        if semester:
            query += f" AND semester = '{semester}'"
        cur.execute(query)
        courses = cur.fetchall()
        cur.close()
        conn.close()
        return courses

    def print_html(self, data, tab="faculty"):
        print("""
        <html>
        <head>
            <title>East Carolina University Computer Science Department Data</title>
            <style>
                body { font-family: Arial, sans-serif; }
                ul {
                    list-style-type: none;
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                    background-color: #333;
                }
                li {
                    float: left;
                }
                li a {
                    display: block;
                    color: white;
                    text-align: center;
                    padding: 14px 16px;
                    text-decoration: none;
                }
                li a:hover, li a.active {
                    background-color: #111;
                }
                table {
                    border-collapse: collapse;
                    width: 100%;
                }
                th, td {
                    border: 1px solid black;
                    text-align: left;
                    padding: 8px;
                }
                tr:nth-child(even) {background-color: #f2f2f2;}
            </style>
        </head>
        <body>
            <ul>
                <li><a href="?tab=faculty" """ + ('class="active"' if tab=="faculty" else '') + """>Faculty</a></li>
                <li><a href="?tab=prerequisites" """ + ('class="active"' if tab=="prerequisites" else '') + """>Prerequisites</a></li>
                <li><a href="?tab=courses" """ + ('class="active"' if tab=="courses" else '') + """>Courses</a></li>
                <li><a href="?tab=fte" """ + ('class="active"' if tab=="fte" else '') + """>FTE</a></li>
            </ul>
            <form method="GET" action="">
                <input type="hidden" name="tab" value="fte">
                <label for="faculty">Faculty:</label>
                <input type="text" id="faculty" name="faculty">
                <label for="year">Year:</label>
                <input type="text" id="year" name="year">
                <label for="semester">Semester:</label>
                <input type="text" id="semester" name="semester">
                <input type="submit" value="Calculate FTE">
            </form>
        """)
        if tab == "faculty":
            print("<h2>Faculty</h2>")
        elif tab == "prerequisites":
            print("<h2>Prerequisites</h2>")
        elif tab == "courses":
            print("<h2>Courses</h2>")
        elif tab == "fte":
            print("<h2>FTE</h2>")
            if data:
                print("<table>")
                print("<tr><th>Credit Hours</th><th>Enrollment</th><th>Course Type</th><th>FTE</th></tr>")
                for ch, enrollment, course_type in data:
                    fte = self.calculate_fte(ch, enrollment, course_type)
                    print(f"<tr><td>{ch}</td><td>{enrollment}</td><td>{course_type}</td><td>{fte:.2f}</td></tr>")
                print("</table>")
        print("</body></html>")

    def validate_input(self, value):
        if value is None or not value.strip():
            return None
        return html.escape(value.strip())

if __name__ == "__main__":
    form = cgi.FieldStorage()
    tab = form.getvalue('tab')
    university_data = UniversityData()

    if tab == "prerequisites":
        data = university_data.fetch_prerequisites()
        university_data.print_html(data, tab="prerequisites")
    elif tab == "courses":
        data = university_data.fetch_courses()
        university_data.print_html(data, tab="courses")
    elif tab == "faculty":
        search_keyword = university_data.validate_input(form.getvalue('search'))
        sort_by = university_data.validate_input(form.getvalue('sort'))
        data = university_data.fetch_faculty(sort_by=sort_by, keyword=search_keyword)
        university_data.print_html(data, tab="faculty")
    elif tab == "fte":
        faculty = university_data.validate_input(form.getvalue('faculty'))
        year = university_data.validate_input(form.getvalue('year'))
        semester = university_data.validate_input(form.getvalue('semester'))
        data = university_data.fetch_courses_for_fte(faculty, year, semester)
        university_data.print_html(data, tab="fte")
