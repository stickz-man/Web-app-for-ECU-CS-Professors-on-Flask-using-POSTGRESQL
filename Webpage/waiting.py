#!/usr/bin/python3
print('Content-type: text/html\n\n')
import psycopg2
import cgi
import cgitb; cgitb.enable()
import html

class Faculty:
    def __init__(self, host, dbname, user, password, port):
        self.conn_params = {
            'host': host,
            'dbname': dbname,
            'user': user,
            'password': password,
            'port': port
        }
    
    def get_db_connection(self):
        try:
            return psycopg2.connect(**self.conn_params)
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            return None
    
    def fetch_faculty(self, sort_by='name'):
        conn = self.get_db_connection()
        if conn is not None:
            cur = conn.cursor()
            if sort_by == 'name':
                cur.execute('SELECT * FROM public."Faculty" ORDER BY "Last", "First"')
            elif sort_by == 'rank':
                cur.execute('SELECT * FROM public."Faculty" ORDER BY "Rank", "Last", "First"')
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows
        else:
            return []

    def print_html(self, data):
        print("<html><head><title>Faculty</title></head><body>")
        print("<table border = '1'>")
        print("<tr><th>ID</th><th>Honorific</th><th>First</th><th>MI</th><th>Last</th><th>Email</th><th>Phone</th><th>Office</th><th>Research</th><th>Rank</th><th>Remarks</th><th>CurrentlyEmployed</th></tr>")
        
        for row in data:
            print("<tr>")
            for col in row:
                print("<td>{}</td>".format(html.escape(str(col))))
            print("</tr>")
        print("</table>")
        print("</body></html>")

    # Placeholder for search functionality
    def search_faculty(self, keyword):
        # Implement search functionality based on keyword
        pass

    # Add methods for Courses and FTE tabs as needed
    # def fetch_courses(self):
    #     pass

    # def fetch_fte(self):
    #     pass

if __name__ == "__main__":
    faculty_obj = Faculty('192.168.56.20', 'postgres', 'webuser1', 'student', '5432')
    faculty_data = faculty_obj.fetch_faculty(sort_by='name')  # or 'rank' for sorting by rank
    faculty_obj.print_html(faculty_data)
