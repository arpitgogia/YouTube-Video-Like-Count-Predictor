import json
import urllib
import sqlite3


db_connection = sqlite3.connect(
    './youtube.db')
db = db_connection.cursor()
all_video_ids = []

try:
    for i, row in enumerate(db.execute("SELECT videoId FROM VIDEOS").fetchall()):
        all_video_ids.append(row[0])
except sqlite3.OperationalError, e:
    print 'sqlite3.OperationalError:', e
# db_connection.close()
# db.execute("CREATE TABLE SOCIAL(videoId PRIMARY KEY NOT NULL, total_shares INT, google_shares INT, facebook_shares INT, linkedin_shares INT, pinterest_shares INT)")


def get_shares(videoId):
    try:
        url = "https://www.youtube.com/watch?v=" + str(videoId)
        # print url
        api_url = "https://count.donreach.com/?url=" + url
        response = urllib.urlopen(api_url).read()
        data = json.loads(response)
        print data
        total_shares = data['total']
        google_shares = data['shares']['google']
        facebook_shares = data['shares']['facebook']
        linkedin_shares = data['shares']['linkedin']
        pinterest_shares = data['shares']['pinterest']
        vars_to_insert = (videoId, total_shares, google_shares, facebook_shares,
                          linkedin_shares, pinterest_shares)
        db.execute("INSERT INTO SOCIAL VALUES (?,?,?,?,?,?)",
                   (vars_to_insert))
        db_connection.commit()
    except Exception as e:
        print e.message
        pass
    # print 'total shares', total_shares
    # print 'google_shares', google_shares
    # print 'facebook_shares', facebook_shares
    # print 'linkedin shares', linkedin_shares
    # print 'pinterest shares', pinterest_shares

for _id in all_video_ids:
    get_shares(_id)

db_connection.close()
