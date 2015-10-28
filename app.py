# Copyright 2015 Ananth Rao. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, jsonify, request
import MySQLdb
from flask import render_template
import json

# mysql.connector functionality used with help from @jayr13's repository njit-course-scraper

app = Flask(__name__)
appContext = app.app_context()
if 'VCAP_SERVICES' in os.environ:
    # bluemix database setup
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    mysql_info = vcap_services[u'cleardb'][0]
    cred = mysql_info[u'credentials']

    host = cred[u'hostname'].encode('utf8')
    dbusername = cred[u'username'].encode('utf8')
    dbpassword = cred[u'password'].encode('utf8')
    dbname = cred[u'name'].encode('utf8')
else:
    # local database setup
    host = "localhost"
    dbusername = "root"
    dbpassword = ""
    dbname = "API-CHOOSERINATOR"

# establish MySQL connection
db = MySQLdb.connect(user = dbusername, passwd = dbpassword, host = host, db = dbname)
cursor = db.cursor()


def get_records_from_cursor():
    def get_record_from_list(elem):
        return elem[0]

    return map(get_record_from_list, cursor.fetchall())

def validate(input):
    if(input == '' or input.find(";") != -1):
        return False
    return True

@app.route('/')
def Welcome():
    query = """SELECT api_name FROM api ORDER BY RAND() LIMIT 5"""
    cursor.execute(query)
    db.commit()
    apis = get_records_from_cursor()

    query = """SELECT action_class_name FROM action_class ORDER BY RAND() LIMIT 5"""
    cursor.execute(query)
    db.commit()
    actions = get_records_from_cursor()

    return render_template('home.html', apis=apis, actions=actions)

def exists(query):
    print query
    cursor.execute(query)
    db.commit()
    return int(cursor.rowcount) > 0

@app.route('/add', methods=["GET"])
def add():
    api_name = request.args.get("api_name")
    action_class_name = request.args.get("action_class_name")
    print api_name

    if(api_name and action_class_name):
        if(validate(api_name) and validate(action_class_name)):
            query1 = """SELECT *
                FROM api
                WHERE api_name = %s%s%s""" % ('\'',api_name,'\'')

            query2 = """SELECT *
                FROM action_class
                WHERE action_class_name = %s%s%s""" % ('\'',action_class_name,'\'')

            if(not exists(query1)):
                query = """INSERT INTO api (api_name) VALUES (%s%s%s)""" % ('\'',api_name,'\'')
                print query
                cursor.execute(query)
                db.commit()
            if(not exists(query2)):
                query = """INSERT INTO action_class (action_class_name) VALUES (%s%s%s)""" % ('\'',action_class_name,'\'')
                cursor.execute(query)
                db.commit()

            query = """INSERT INTO action2api VALUES (
            (SELECT action_class_id FROM action_class WHERE action_class_name = %s%s%s),
            (SELECT api_id FROM api WHERE api_name = %s%s%s)
            )""" % ('\'',action_class_name,'\'','\'',api_name,'\'')
            cursor.execute(query)
            db.commit()

            return render_template("add.html", message="Added. Thanks for contributing!")
        return render_template("add.html", message="Failed to add. Maybe you didn't sanitize your inputs :)")
    else:
        return render_template("add.html")


@app.route('/api/<name>')
def api(name):
    if validate(name):
        query = """SELECT *
            FROM api
            WHERE api_name = %s%s%s""" % ('\'',name,'\'')
        if exists(query):
            query = """SELECT action_class_name
                FROM action_class
                WHERE action_class_id in (
                    SELECT action_class_id
                    FROM action2api
                    WHERE api_id = (
                        SELECT DISTINCT api_id
                        FROM api
                        WHERE api_name = %s%s%s
                    )
                );
            """ % ('\'',name,'\'')

            cursor.execute(query)
            db.commit()

            actions = get_records_from_cursor()

            return render_template('api.html', api_name=name, results=actions)

    return render_template('home.html')

@app.route('/action/<name>')
def action(name):
    if validate(name):
        query = """SELECT *
            FROM action_class
            WHERE action_class_name = %s%s%s""" % ('\'',name,'\'')
        if exists(query):
            query = """SELECT api_name
                FROM api
                WHERE api_id in (
                    SELECT api_id
                    FROM action2api
                    WHERE action_class_id = (
                        SELECT DISTINCT action_class_id
                        FROM action_class
                        WHERE action_class_name = %s%s%s
                    )
                );
            """ % ('\'',name,'\'')

            cursor.execute(query)
            db.commit()

            apis = get_records_from_cursor()

            return render_template('action.html', action_class_name=name, results=apis)

    return render_template('home.html')

@app.route('/search/<searchString>')
def search(searchString):
    if validate(searchString):
        # try action_class
        query = """SELECT *
            FROM action_class
            WHERE action_class_name = %s%s%s""" % ('\'',searchString,'\'')
        if exists(query):
            return action(searchString)

        #try api
        query = """SELECT *
            FROM api
            WHERE api_name = %s%s%s""" % ('\'',searchString,'\'')
        if exists(query):
            return api(searchString)

        message = "Sorry, invalid API or action class. If you think the API or action class should exist in our system, feel free to add it as a connection to one of our existing APIs/action classes using the handy dandy plus button up top. Or open up an issue on our Github repository!"
        return render_template('home.html', message=message)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=True)
