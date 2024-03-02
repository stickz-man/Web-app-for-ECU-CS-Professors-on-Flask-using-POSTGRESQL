#!/usr/bin/python3
print('Content-type: text/html\n\n')
import psycopg2
import cgi
import cgitb; cgitb.enable()
import html



def get_db_connection():
    conn = psycopg2.connect(host ='192.168.56.20', dbname ='postgres', user='webuser1', password='student', port='5432')
    return conn

def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM public."Faculty"')
    rows = cur.fetchall()
    return rows
    cur.close()
    conn.close()
def print_html(data):
    print("<html><head><title>Faculty</title></head><body>")
    print("<table border = '1'>")
    print("<tr><th>ID</th><th>Honorific</th><th>First</th><th>MI</th><th>Last</th><th>Email</th><th>Phone</th><th>Office</th><th>Research</th><th>Rank</th><th>Remarks</th><th>CurrentlyEmployed</th></tr>")
    print("<p>{}</p>".format(type(data)))
    
    if data:
        for row in data:
            print("<tr>")
            for col in row:
                print("<td>{}</td>".format(html.escape(str(col))))
            print("</tr>")

        print("</table>")
    else:
        print("<p>The code runs normally and can import the table! Just returns None. seems the output is not a tuple. BBBBBBut everything works fine</p>")
    print("</body></html>")

if __name__ == "__main__":
    data = index()
    print_html(data)

