import json
import requests
import ipaddress
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import pandas as pd

class URLCollector():
    def __init__(self):
        pass

    def james_webb(self):
        #JAMES WEBB
        jameswebb='https://www.stsci.edu/contents/news/jwst/2022/jwst-cycle-1-science-and-commissioning-data-now-available'
        #NASA
        self.nasa=[]
        for i in range(1,18):
            self.nasa.append(f"https://images-api.nasa.gov/search?q=galaxies&page={i}")
        for i in range(1,66):
            self.nasa.append(f"https://images-api.nasa.gov/search?q=stars&page={i}")
        for i in range(1,73):
            self.nasa.append(f"https://images-api.nasa.gov/search?q=planets&page={i}")
        for i in range(1,11):
            self.nasa.append(f"https://images-api.nasa.gov/search?q=black%20hole&page={i}")
    
    def european_southern_observatory(self):
        #EUROPEAN SOUTHERN OBSERVATORY
        self.eso=[
            "https://www.eso.org/public/images/archive/category/stars/",
            "https://www.eso.org/public/images/archive/category/360pano/",
            "https://www.eso.org/public/images/archive/category/alma/",
            "https://www.eso.org/public/images/archive/category/apex/",
            "https://www.eso.org/public/images/archive/category/chile/",
            "https://www.eso.org/public/images/archive/category/cosmology/",
            "https://www.eso.org/public/images/archive/category/elt/",
            "https://www.eso.org/public/images/archive/category/eso-supernova/",
            "https://www.eso.org/public/images/archive/category/exoplanets/",
            "https://www.eso.org/public/images/archive/category/fulldome/",
            "https://www.eso.org/public/images/archive/category/galaxies/",
            "https://www.eso.org/public/images/archive/category/galaxyclusters/",
            "https://www.eso.org/public/images/archive/category/illustrations/",
            "https://www.eso.org/public/images/archive/category/lasilla/",
            "https://www.eso.org/public/images/archive/category/nebulae/",
            "https://www.eso.org/public/images/archive/category/paranal/",
            "https://www.eso.org/public/images/archive/category/peopleandevents/",
            "https://www.eso.org/public/images/archive/category/premises/",
            "https://www.eso.org/public/images/archive/category/blackholes/",
            "https://www.eso.org/public/images/archive/category/solarsystem/",
            "https://www.eso.org/public/images/archive/category/starclusters/",
            "https://www.eso.org/public/images/archive/category/surveytelescopes/"
            ]

        for i in range(2,16):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/stars/list/{i}/")
        for i in range(2,11):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/360pano//list/{i}/")
        for i in range(2,35):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/alma//list/{i}/")
        for i in range(2,5):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/apex//list/{i}/")
        for i in range(2,8):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/chile//list/{i}/")
        for i in range(2,5):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/cosmology//list/{i}/")
        for i in range(2,17):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/elt//list/{i}/")
        for i in range(2,13):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/eso-supernova//list/{i}/")
        for i in range(2,6):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/exoplanets//list/{i}/")
        for i in range(2,5):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/fulldome//list/{i}/")
        for i in range(2,15):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/galaxies//list/{i}/")
        for i in range(2,4):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/galaxyclusters//list/{i}/")
        for i in range(2,32):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/illustrations//list/{i}/")
        for i in range(2,31):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/lasilla//list/{i}/")
        for i in range(2,12):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/nebulae//list/{i}/")
        for i in range(2,70):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/paranal//list/{i}/")
        for i in range(2,52):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/peopleandevents//list/{i}/")
        for i in range(2,16):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/premises//list/{i}/")
        for i in range(2,5):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/blackholes//list/{i}/")
        for i in range(2,13):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/solarsystem//list/{i}/")
        for i in range(2,5):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/starclusters//list/{i}/")
        for i in range(2,5):
            self.eso.append(f"https://www.eso.org/public/images/archive/category/surveytelescopes//list/{i}/")

class PhotosCollector(URLCollector):
    super().__init__()

    def gen_ips(self):
        network=ipaddress.IPv4Network("192.168.1.0/24")
        self.hosts=[]
        for host in network.hosts():
            self.hosts.append(host)
            
    def scraping_data(self):
        self.dados=[]
        x=0
        y=0
        for data in self.nasa+self.eso:
            if 'galax' in data:
                host=self.hosts[y]
                network=ipaddress.IPv4Network(host)
                self.dados.append(requests.get(data).content)
                x+=1
                if x==8:
                    y+=1
            sleep(randint(1,3))

class StoringData(PhotosCollector):
    super().__init__()

    def nasa_imgs(self):
        imgsnasa=[]
        for dado in self.dados:
            info=dado.decode('utf-8')
        if 'nasa' in info:
            while info != '':
                imgsnasa.append(info.partition('"href":"')[2].partition('"')[0])
                info=info.partition('"href":"')[2].partition('"')[2]
        self.nasa_galaxies=[]
        for img in imgsnasa:
            if '.json' in img:
                img=requests.get(img).content
                try:
                    imgs=json.loads(img)
                    for img in imgs:
                        self.nasa_galaxies.append(img)
                except:
                    self.nasa_galaxies.append(img)
            elif img != '':
                self.nasa_galaxies.append(img)
            else:
                pass
    
    def eso_imgs(self):
        imgseso=[]
        for dado in self.dados:
            info=dado.decode('utf-8')
            if 'nasa.gov' not in str(info):
                json_galaxies=info.partition('var images = ')[2].partition(']')[0]+']'
                if len(json_galaxies) > 15:
                    imgseso.append(json_galaxies)
        self.galaxies=imgseso+self.nasa_galaxies_info

    def source_file(self):
        for data in self.nasa_galaxies:
            with open ('sources_nasa.txt','a') as f:
                try:
                    f.write(data+'\n')
                except:
                    pass
        
        for data in self.galaxies:
            with open ('sources_eso.txt','a') as f:
                try:
                    f.write(data+'\n')
                except:
                    pass
    
    def download(self):
        # opening the file in read mode
        sources_nasa = open("sources_nasa.txt", "r")
        # reading the file
        nasa = sources_nasa.read()
        nasa_list = nasa.split("\n")
        sources_nasa.close()
        self.nasa_galaxies_info=[]
        i=0
        for img_url in nasa_list:
            try:
                if '~small.jpg' in img_url and 'video' not in img_url:
                    starname=img_url.partition('image/')[2].partition('/')[0]
                    self.nasa_galaxies_info.append({"star":starname,"url":img_url,"metadata":""})
                elif '.json' in img_url and 'video' not in img_url:
                    metadata=img_url
                    self.nasa_galaxies_info[i]['metadata']=img_url
                    i+=1
            except:
                pass
        
        with open ('/content/drive/MyDrive/AstroML/sources_nasa.txt') as f:
            data=f.readlines()
        for url in data:
            if '~small.jpg' in url and 'nasa.gov/image' in url:
                filename='/content/drive/MyDrive/AstroML/NASA/'+url.partition('image/')[2].partition('/')[0]+'.jpg'
                url=url.partition('.jpg')[0]+'.jpg'
                request=requests.get(url)
                with open (filename,'wb') as f:
                    f.write(request.content)

        df=pd.read_json('eso_urls.json')
        for i in range(0,len(df)):
            starname=df.iloc[i,0]
            url=df.iloc[i,4]
            filename='/content/drive/MyDrive/PROFISSIONAL/DATA SCIENCE/ESO/'+starname+'.jpg'
            data=requests.get(url).content
            with open (starname,'wb') as f:
                f.write(data)