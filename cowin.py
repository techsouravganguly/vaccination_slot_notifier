# skipped your comments for readability



#imports for the project
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import requests
from datetime import date
import time
import mysql.connector


#intialzing the base url for get request
url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"


#gmail from  which email is sent 
my_mail = "name of the gmail from u want to send the mail"
my_password = r"passwd of the given mail"


#header for get request
h = {
    'accept': 'application/json',
    "Accept-Language": "en_US",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}


#mapping of district name and district id
d=[{'d_id': 74, 'd_name': 'Araria'}, {'d_id': 78, 'd_name': 'Arwal'}, {'d_id': 77, 'd_name': 'Aurangabad'}, {'d_id': 83, 'd_name': 'Banka'}, {'d_id': 98, 'd_name': 'Begusarai'}, {'d_id': 82, 'd_name': 'Bhagalpur'}, {'d_id': 99, 'd_name': 'Bhojpur'}, {'d_id': 100, 'd_name': 'Buxar'}, {'d_id': 94, 'd_name': 'Darbhanga'}, {'d_id': 105, 'd_name': 'East Champaran'}, {'d_id': 79, 'd_name': 'Gaya'}, {'d_id': 104, 'd_name': 'Gopalganj'}, {'d_id': 107, 'd_name': 'Jamui'}, {'d_id': 91, 'd_name': 'Jehanabad'}, {'d_id': 80, 'd_name': 'Kaimur'}, {'d_id': 75, 'd_name': 'Katihar'}, {'d_id': 101, 'd_name': 'Khagaria'}, {'d_id': 76, 'd_name': 'Kishanganj'}, {'d_id': 84, 'd_name': 'Lakhisarai'}, {'d_id': 70, 'd_name': 'Madhepura'}, {'d_id': 95, 'd_name': 'Madhubani'}, {'d_id': 85, 'd_name': 'Munger'}, {'d_id': 86, 'd_name': 'Muzaffarpur'}, {'d_id': 90, 'd_name': 'Nalanda'}, {'d_id': 92, 'd_name': 'Nawada'}, {'d_id': 97, 'd_name': 'Patna'}, {'d_id': 73, 'd_name': 'Purnia'}, {'d_id': 81, 'd_name': 'Rohtas'}, {'d_id': 71, 'd_name': 'Saharsa'}, {'d_id': 96, 'd_name': 'Samastipur'}, {'d_id': 102, 'd_name': 'Saran'}, {'d_id': 93, 'd_name': 'Sheikhpura'}, {'d_id': 87, 'd_name': 'Sheohar'}, {'d_id': 88, 'd_name': 'Sitamarhi'}, {'d_id': 103, 'd_name': 'Siwan'}, {'d_id': 72, 'd_name': 'Supaul'}, {'d_id': 89, 'd_name': 'Vaishali'}, {'d_id': 106, 'd_name': 'West Champaran'}]

#function for sending the email through given gmail
def email(s_mail,body):
    you = s_mail
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Alert"
    msg['From'] = my_mail
    msg['To'] = ", ".join(you)
    html = '<html><body><p>'+body+'</p></body></html>'
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    s.login(my_mail, my_password)
    s.sendmail(my_mail, you, msg.as_string())
    s.quit()


#function for calling the api with the district id and genrate body for the email which satisfied our condition in this 18+ vactionation
def api_call(d_id):
    count =0
    today = date.today()
    d = str(today.strftime("%d-%m-%Y"))
    para = {
        'district_id': d_id,
        'date' : d
    }
    res = requests.get(url, params = para, headers = h)
    list_center = (res.json())['centers']
    req_body =""
    for center in list_center:
        name = center['name']
        day = center['sessions']
        for number in day:
            if number['min_age_limit'] == 18 and number['available_capacity'] >0:
                req_body += name + "<br>"
                req_body += number['date'] + "<br>"
                req_body += str(number['available_capacity']) + "<br>"
                req_body += "<br>"
                count+=1
    req_body += "please de register your mail through the given link <br> so we can help others also"
    req = {'body' : req_body , 'c' :count}
    return req


#running it infinitely so it email u when the slot is availabe
while 1:
	mydb = mysql.connector.connect(host="host name", user="username", passwd="passwd", database="database")
	mycursor = mydb.cursor()
	mycursor.execute("select * from person where email is not NULL")
	for i in mycursor:
    	mail_body = (api_call(i[0]))['body']
    	email(i[1],mail_body)
    	time.sleep(20)
	mydb.close()
	time.sleep(60)