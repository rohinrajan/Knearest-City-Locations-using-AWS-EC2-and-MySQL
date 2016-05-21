from flask import Flask
from flask import render_template
from flask import request
import MySQLdb
import datetime
import memcache

DB_SERVER = 'cloudserverName'
DB_USERNAME = 'username'
DB_PASSWORD = 'password'
DB_DATABASE = 'databasename'

app = Flask(__name__)

user = ""
passwd = ""
key = ""



def connection_mysql():
        mydb = MySQLdb.connect(host = DB_SERVER,
                user = DB_USERNAME,
				passwd= DB_PASSWORD,
                db = DB_DATABASE
                )
        return mydb



def get_information(request):
        city = request.form['kcity']
        country = request.form['kcountry']
        region = request.form['kregion']
        distance = request.form['kdistance']
        cities = request.form['kcities']
        return city,country,region,distance,cities



def get_sql_query(city,country,region,distance,knear):
        if distance != '':
                  sql_query = 'call GEO_DISTANCE(\'' + city + '\',\'' + country + '\',\'' + region + '\',\'' + distance + '\')'
        else:
                  distance = 50
				  sql_query = 'call GEO_KNEAREST(\'' + city + '\',\'' + country + '\',\'' + region + '\',\'' + str(distance) + '\',\'' + knear + '\')'
        return sql_query




@app.route('/kdistance',methods=['POST','GET'])
def get_cities_based_on_distance():
        if request.method == 'POST':
                city,country,region,distance,knear = get_information(request)
                if distance != '':
                        key = str(distance + city.replace(' ','') + country.replace(' ','') + region.replace(' ',''))
                        sql_query = 'call GEO_DISTANCE(\'' + city + '\',\'' + country + '\',\'' + region + '\',\'' + distance + '\')'
                else:
                        key = str(knear + city.replace(' ','') + country.replace(' ','') + region.replace(' ',''))
                        distance = 50
                        sql_query = 'call GEO_KNEAREST(\'' + city + '\',\'' + country + '\',\'' + region + '\',\'' + str(distance) + '\',\'' + knear + '\')'
                dbcon = connection_mysql()
				dbcursor = dbcon.cursor()
                memc = memcache.Client(['memecachenamelist'])
                diff1 = datetime.datetime.now()
                cont = memc.get(key)
                if not cont:
                        dbcursor.execute(sql_query)
                        mydata = dbcursor.fetchall()
                        memc.set(key,mydata,60)
                        rowcnt = dbcursor.rowcount
                        if knear != '' and  rowcnt < int(knear):
                                increment = 10
                                while (rowcnt < int(knear)):
                                        distance = distance + increment
                                        sql_query = get_sql_query()
                                        dbcursor.execute(sql_query)
                                        rowcnt = dbcursor.rowcount
                                mydata = dbcursor.fetchall()
                else:
                        mydata = cont
                        rowcnt = 1
                diff2 = datetime.datetime.now()
                difvalue = diff2 - diff1
				return render_template('mainpage.html',content=mydata,time=difvalue,rows= rowcnt)

@app.route('/')
def startup():
        return render_template('mainpage.html')

if __name__ == '__main__':
        app.run()

