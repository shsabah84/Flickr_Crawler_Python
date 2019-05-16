import os
import unicodedata
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
import requests
from requests.exceptions import ConnectionError    

#Definition of mongo db
import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.time_intervlgeoworld
collection = db.intervlgeoworld_collection

#Set Flickr api

import flickr_api
from flickr_api.api import flickr
flickr_api.set_keys(api_key = 'Enter your key', api_secret = 'Enter your key') 
import httplib2

#get standard and unix form of current date

import datetime
import time
dt = datetime.datetime.now()
du = time.mktime(dt.timetuple())
if not os.path.exists('geo_world2005.txt'):
    c = open('geo_world2005.txt','a')
    c.write('((( Definitions )))'+' (1) ==> Photo_id (2) ==> Owner (3) ==> Title (4) ==> Tage (5) ==> Accuracy (6) ==> Date_Upload (7) ==> Date_Taken (8) ==> Place_id (9) ==> Latitude (10) ==> Longitude (11) ==> Discription'+'\n')
else:
    c = open('geo_world2005.txt','a')

#set initial min_upload_date and max_upload_date in unix form

m=1500000
chkno=0
a=0
recno=0
if not os.path.exists('req_world2005.txt'):
    maxupldate=1136073600.0
    collphoto=0
    
else:
    
    with open('req_world2005.txt', "rb") as f:
        first = f.readline()     
        for last in f: pass
        x=re.split(' ',last)
        y=x[11]
        y1=x[5]
        maxupldate= float(y)
        collphoto=int(y1)
    f.close

minupldate=maxupldate-m

npg=1

with open('req_world2005.txt','a') as f:
    with open('error2005.txt','a') as t:
        print 'start'
        #Search about the best time interval with less than 4000 photos
        while (minupldate>915148800):
            try:
                r = requests.get("http://example.com", timeout=0.001)
            except ConnectionError as e: 

                xmlresult= flickr.photos.search(min_upload_date = minupldate , max_upload_date = maxupldate ,has_geo = 1,extras='description, license, date_upload, date_taken, owner_name, icon_server, original_format, last_update, geo, tags, machine_tags, o_dims, views, media, path_alias, url_sq, url_t, url_s, url_q, url_m, url_n, url_z, url_c, url_l, url_o')
                r = "No response"
            from bs4 import BeautifulSoup
            xml = xmlresult
            soup = BeautifulSoup(xml,'lxml')
            search=soup.find('photos')
            nopage=search.attrs['pages']
            nopage= int(nopage)
            totalphotos=search.attrs['total']
            totalphotos= int(totalphotos)
            print 'totalphotos ===>  ',totalphotos
            if totalphotos <= 4000 and totalphotos >= 100 :
                recno=recno+1
                collphoto=collphoto+totalphotos
                print "Record No. ==> ",recno
                print 'Collected Photos So far ==> ',collphoto
                print 'StartDate ==> ',str(datetime.datetime.fromtimestamp(int(maxupldate)).strftime('%Y-%m-%d %H:%M:%S')),'  <<====>> ' +str(maxupldate)
                print 'EndDate ==> ',str(datetime.datetime.fromtimestamp(int(minupldate)).strftime('%Y-%m-%d %H:%M:%S')) , '  <<====>> ' +str(minupldate)
                f.write('TPh = '+str(totalphotos))
                f.write(' CPh = '+str(collphoto))
                f.write(' MaU = '+str(maxupldate))
                f.write(' MiU = '+str(minupldate)+'\n')
                for photo in soup.find_all('photo'):
                    try:
                        c.write("1= "+ photo.attrs['id']+'\n'+"2= "+ photo.attrs['owner']+ '\n'+"3= "+ photo.attrs['title']+ '\n'+"4= "+photo.attrs['tags']+ '\n'+"5= "+photo.attrs['accuracy']+ '\n'+"6= "+photo.attrs['dateupload']+ '\n'+"7= "+photo.attrs['datetaken']+ '\n'+"8= "+photo.attrs['place_id']+'\n'+"9= "+photo.attrs['latitude']+ '\n'+"10= "+photo.attrs['longitude']+ '\n'+"11= "+(str(photo.description.string).replace('\n',' '))+'\n')
                    except (KeyError,AttributeError,TypeError,ValueError,flickr_api.flickrerrors.FlickrError):
                        t.write(photo.attrs['id']+'\n')
                while (npg<nopage):
                    npg=npg+1
                    try:
                        r = requests.get("http://example.com", timeout=0.001)
                    except ConnectionError as e:
                        xmlresult2 = flickr.photos.search(min_upload_date = minupldate , max_upload_date = maxupldate ,has_geo = 1,extras = 'description, license, date_upload, date_taken, owner_name, icon_server, original_format, last_update, geo, tags, machine_tags, o_dims, views , media, path_alias, url_sq, url_t, url_s, url_q, url_m, url_n, url_z, url_c, url_l, url_o', page = npg )
                        r = "No response"
                    xml2 = xmlresult2
                    soup = BeautifulSoup(xml2, 'lxml')
                    for photo in soup.find_all('photo'):
                        try:
                            c.write("1= "+ photo.attrs['id']+'\n'+"2= "+ photo.attrs['owner']+ '\n'+"3= "+ photo.attrs['title']+ '\n'+"4= "+photo.attrs['tags']+ '\n'+"5= "+photo.attrs['accuracy']+ '\n'+"6= "+photo.attrs['dateupload']+ '\n'+"7= "+photo.attrs['datetaken']+ '\n'+"8= "+photo.attrs['place_id']+'\n'+"9= "+photo.attrs['latitude']+ '\n'+"10= "+photo.attrs['longitude']+ '\n'+"11= "+(str(photo.description.string).replace('\n',' '))+'\n')
                        except (KeyError,AttributeError,TypeError,ValueError,flickr_api.flickrerrors.FlickrError):
                            t.write(photo.attrs['id']+'\n')
                maxupldate = minupldate
                minupldate = minupldate-25000
                m=1500000
                chkno=0
                npg=1
            else :

                if totalphotos > 4000:
                    m=m-150000
                else:
                    if totalphotos==0:
                        m=m+500000
                    elif (totalphotos<>0)and((4000/totalphotos)>10):
                        m=m+500000
                    else:
                        m=m+9500000
                    m=int(m)
                
                minupldate=maxupldate - m
                
    t.close()
print 'finish!!!!!!!!!!!!!!!!'
c.close()
f.close()
