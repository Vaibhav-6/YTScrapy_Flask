from flask import Flask,render_template,redirect,url_for,session
from flask import request as rq
from urllib.request import urlopen
import pytube,ffmpeg
from bs4 import BeautifulSoup
from urllib import request
import time,json,re,os,glob,random
import requests
                

app = Flask(__name__)


@app.route("/home")
def hello_world():
    return render_template("index.html")
    
    

def start(url):
    s=requests.get(url)
    print(s)
    time.sleep(2)
    soup= BeautifulSoup(s.text,'lxml')
    aid=soup.find('script',string=re.compile('ytInitialData'))
    p = re.compile('var ytInitialData = (.*?);')
    m = p.match(aid.string)
    try:
        stocks = json.loads(m.groups()[0])
    except:
        return 0,0,0
    video_info=stocks["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
    title1=[]
    url1=[]
    thumbnail1=[]
    for item in video_info:
        try:
            video_items=item["videoRenderer"]
            title=video_items["title"]["runs"][0]["text"]
                #print("Title: "+title)
            title1.append(title)
            url=video_items["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
                #print("URL: "+url)
            url1.append(url)
            thumb_nail=video_items["thumbnail"]["thumbnails"][0]["url"]
                #print("Thumbnails: "+thumb_nail+"\n")
            thumbnail1.append(thumb_nail)
        except:
            pass 
    print(title1)
    print(url1)
    print(thumbnail1)
    return title1,url1,thumbnail1


@app.route("/search",methods=['POST','GET'])
def run():
    if rq.method=='POST':
        link= rq.form.get('lin')
        yt_search=rq.form['search1']
        if yt_search!="":
            url="https://www.youtube.com/results?search_query="+yt_search
            title1,url1,thumbnail1=start(url)
        if link!="":
            if link[0:5]!="https":
                return render_template('index.html',label1="Try with anpther input")
            else:
                l=link[23:]
                print(l)
                return render_template('download.html',link=l)
    if(title1==0):
        return render_template('index.html',label="Try with another input")
    else:
        return render_template('show.html',title1=title1,url1=url1,thumbnail1=thumbnail1)
        


def mp4(url):
    youtube = pytube.YouTube(url)
    video = youtube.streams
    print("Fetching Video")
    video.get_by_itag(22).download()#720p
    print('Video Downloaded')
    string='abcdefghijklmnopqrstuvwxyz'
    for file in glob.glob("*.mp4"):
        os.rename(file,'TeamA1_Video_downloader_'+random.choice(string)+'.mp4')

def mp3(url):
    youtube = pytube.YouTube(url)
    audio=youtube.streams.filter(only_audio=True,abr='160kbps').first()
    print("Fetching Audio")
    audio.download()
    print('Audio Downloaded')
    print('converting to mp3')
    string='abcdefghijklmnopqrstuvwxyz'
    for file in glob.glob("*.webm"):
        input_audio = ffmpeg.input(file)
        ffmpeg.output(input_audio,'TeamA1_Audio_downloader_'+random.choice(string)+'.mp3').run()
        os.remove(file)
    print("download success")

        
@app.route("/mp4/<name>",methods=['GET'])
def down(name):
    url="https://www.youtube.com/"+name+"?v="+rq.args.get('v')
    mp4(url)
    return redirect("/home")
    
    
    
@app.route("/mp3/<name>",methods=['GET'])
def down1(name):
    url="https://www.youtube.com/"+name+"?v="+rq.args.get('v')
    mp3(url)
    return redirect("/home")
    
    
    
@app.route("/video/<name>",methods=['GET'])
def play(name):
    data=rq.args.get('v')
    final_url="https://www.youtube.com/"+name+"?v="+data
    return render_template('player.html',ren=final_url)
    
    
    
@app.route("/download/<val>",methods=["GET"])
def download(val):
    print(val)
    link="/"+val+"?v="+rq.args.get('v')
    print(link)
    return render_template('download.html',link=link)
    
    
if __name__ == "__main__":
    app.run(debug=True)