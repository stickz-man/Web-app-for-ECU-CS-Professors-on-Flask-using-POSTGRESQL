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
    
    def fetch_ch(self):
        conn = self.get_db_connection()
        if conn is None:
            return []
        cur = conn.cursor()
        cur.execute('SELECT * FROM public."CH"')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

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
                <input type="hidden" name="tab" value="faculty">
                <label for="search">Search:</label>
                <input type="text" id="search" name="search">
                <label for="sort">Sort by:</label>
                <select id="sort" name="sort">
                    <option value="">--Select--</option>
                    <option value="name">Name</option>
                    <option value="rank">Rank</option>
                </select>
                <input type="submit" value="Search/Sort">
            </form>
        """)

        if tab == "faculty":
            print("<h2>Faculty</h2>")
        elif tab == "prerequisites":
            print("<h2>Prerequisites</h2>")
        elif tab == "courses":
            print("<h2>Courses</h2>")
        elif tab == "fte":
            print("<h2>FTE</h2>") # Placeholder for FTE tab content

        print("<table>")
        if tab == "prerequisites":
            print("<tr><th>Prefix</th><th>Number</th><th>PC Prefix</th><th>PC Number</th><th>PC Code</th></tr>")
        elif tab == "courses":
            print("<tr><th>Year</th><th>Semester</th><th>Prefix</th><th>Number</th><th>Section</th><th>CRN</th><th>Enrollment</th><th>Instructor</th><th>Days</th><th>Begin Time</th><th>End Time</th><th>Remarks</th></tr>")
        elif tab == "fte":
            print("<tr><th>Prefix</th><th>Number</th><th>Title</th><th>GU</th><th>CH</th><th>Frequency</th><th>Active</th><th>Description</th><th>Remarks</th></tr>")
        else:  # Default to faculty
            print("<tr><th>ID</th><th>Honorific</th><th>First</th><th>MI</th><th>Last</th><th>Email</th><th>Phone</th><th>Office</th><th>Research</th><th>Rank</th><th>Remarks</th><th>Currently Employed</th></tr>")

        for row in data:
            print("<tr>" + "".join(f"<td>{html.escape(str(col))}</td>" for col in row) + "</tr>")
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
    elif tab == "fte":
        data = university_data.fetch_ch()
        university_data.print_html(data, tab="fte")
    elif tab == "faculty":
        search_keyword = university_data.validate_input(form.getvalue('search'))
        sort_by = university_data.validate_input(form.getvalue('sort'))
        data = university_data.fetch_faculty(sort_by=sort_by, keyword=search_keyword)
        university_data.print_html(data, tab="faculty")
    # No data fetching or printing for FTE tab as per the instructions
