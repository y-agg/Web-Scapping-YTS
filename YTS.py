import requests
from bs4 import BeautifulSoup
def moviesearch(max_pages):
    search=input(str("Enter name of movie:"))
    print("\r")
    page=1
    while page <= max_pages:
        url = 'https://yts.lt/browse-movies/'+search+'/all/all/0/latest'
        source_code=requests.get(url)
        pain_code=source_code.text
        soup=BeautifulSoup(pain_code,features="lxml")
        for link in soup.findAll('div',{'class':'browse-movie-bottom'}):
            downloadtitle=link.find("a",recursive=False)
            titleyear=link.find("div",recursive=False).string
            href=downloadtitle.get('href')
            name=downloadtitle.string
            print(f'{name} ({titleyear}) : {href}')
            getLink(href,titleyear,search)
        page+=1
def getLink(url,titleyear,search):
    source_code=requests.get(url)
    pain_code=source_code.text
    soup=BeautifulSoup(pain_code,features="lxml")
    for link in soup.findAll('a',{'class':'download-torrent button-green-download2-big'}):
        name=link.get('title')
        if(name.find('720p')!=-1):
            href=link.get('href')
            print(name+"  :  "+href)
            print("\r")
            imbdsearch(search,titleyear)        
def imbdsearch(search,titleyear,max_pages=1):
    search=search.strip()
    Year=titleyear.strip()
    name=search +" ("+Year+")"
    search=search.split(" ")
    s = "+"
    s=s.join(search)
    s=s+"+%28"+Year+"%29"
    page=1
    while page <= max_pages:
        url = 'https://www.imdb.com/find?ref_=nv_sr_fn&q='+s+'&s=all'
        source_code=requests.get(url)
        pain_code=source_code.text
        soup=BeautifulSoup(pain_code,features="lxml")
        for link in soup.findAll('td',{'class':'result_text'}):
            title=link.text
            title=title.strip()
            href="https://www.imdb.com"+link.find('a',recursive=False).get('href')
            if(title==name):
                getinfo(href)                        
        page+=1
def getinfo(url):
     source_code=requests.get(url)
     pain_code=source_code.text
     soup=BeautifulSoup(pain_code,features="lxml")
     #Summary Of movie
     summary=soup.find('div',{'class':'summary_text'}).string.strip()
     print(f'Summary: {summary}')
     #Name Of Director
     Director=soup.findAll('div',{'class':'credit_summary_item'})[0].find('a',recursive=False).string
     print(f'Director: {Director}')
     #Writers Of Movie
     Writers=soup.findAll('div',{'class':'credit_summary_item'})[1].find('a',recursive=False).string
     print(f'Writers : {Writers }')
     #Stars Of Movie
     Stars=soup.findAll('div',{'class':'credit_summary_item'})[2].text
     Stars=Stars.split("|")
     Stars=Stars[0].split(",")
     index=Stars[0].index(":\n")
     Stars[0]=Stars[0][index+2:]
     Stars=",".join(Stars)
     print(f'Stars: {Stars}')
     #ReviewsOf Movie
     reviews=soup.find('div',{'class':'user-comments'}).findAll('a',recursive=False)
     reviews="https://www.imdb.com"+reviews[-1].get('href')
     #Function called to get reviews
     getreviews(reviews)
def getreviews(url):
    source_code=requests.get(url)
    pain_code=source_code.text
    soup=BeautifulSoup(pain_code,features="lxml")
    count=0
    print("Rewiews:\r")
    for link in soup.findAll('div',{'class':'review-container'}):
       if(count==5):
           break
       count+=1
       title=link.find('a',{'class':'title'}).string.strip()
       print(f'{count}. {title}')
    print("\r")
moviesearch(1)

# def getLink(url):
#        source_code=requests.get(url)
#        pain_code=source_code.text
#        soup=BeautifulSoup(pain_code,features="lxml")
#        counter=1
#        download_link=[]
#        for link in soup.findAll('a',{'class':'download-torrent button-green-download2-big'}):
#            name=link.get('title')
#            if(name.find('720p')!=-1):
#                href=link.get('href')
#                download_link.append(href)
#                print(counter,".  720p Torrent"+"  :  "+href)
#                print("\r")
#            if(name.find('1080p')!=-1):
#                href=link.get('href')
#                download_link.append(href)
#                print(counter,".  1080p Torrent"+"  :  "+href)
#                print("\r")
#            counter+=1    
#            print(download_link)    
#            Choice_of_download=str(input("Want to download ?[Yes/No]: ")).lower()
#            if(Choice_of_download=='yes'):
#                download_choice_link=int(input("Enter Choice:  "))
#                if download_choice_link<=len(listoflink) and download_choice_link>0:
#                    webbrowser.open_new(download_link[download_choice_link-1])
#                else:
#                    raise HaltException("Invalid Choice....Exiting program")
#            else:
#                raise HaltException("This is end of my service...Exiting program")
#if __name__=="__main__":
#        try:
#            #Accepting movie name from user
#            search=input(str("Enter name of movie:")).strip()
#            moviesearch(search)
#            #if length of list of movies is 0 , this means No movies found by this name
#            if(len(listofmovie)==0): 
#                raise HaltException("Error : No Movies found by this Name")
#            #if length of list of movies is 1 ,
#            # We are skipping asking Choice for which movie You want to search 
#            if(len(listofmovie)==1):
#                print("\r")
#                getimbdlinkfromyts(listoflink[0])
#                chlink=str(input("Want link of this movie to download ?[Yes/No]: ")).lower()
#                if(chlink=='yes' or chlink=='y'):
#                    getLink(finallist[2][0])
#                    raise HaltException("Exiting program>>>>>>>>>>>>>>>>")
#                elif(chlink=='no' or chlink=='n'):
#                     raise HaltException("Exiting program>>>>>>>>>>>>>>>>")
#                else:
#                    raise HaltException("Invalid Choice....Exiting program>>>>>>>>>>>>>>>>")            
#            
#            choice=str(input("Want to Search more about movies from given Chocies ?[Yes/No]:")).lower()
#            chlink=''
#         
#            if(choice=='yes' or choice=='y'):
#                value=int(input("Enter Choice:  "))
#                if value<=len(listoflink) and value>0:
#                    getimbdlinkfromyts(listoflink[value-1])
#                    chlink=str(input("Want link of this movie to download ?[Yes/No]: ")).lower()
#                    if(chlink=='yes' or chlink=='y' ):
#                        getLink(finallist[2][value-1])
#                        raise HaltException("Ahhh...finally my works is over !!!!")
#                    elif(chlink=='no' or chlink=='n'):
#                         raise HaltException("Exiting program>>>>>>>>>>>>>>>>")
#                    else:
#                        raise HaltException("Invalid Choice..........Exiting program>>>>>>>>>>>>>>>>")
#                else:
#                    raise HaltException("Invalid chocice ......Exiting program>>>>>>>>>>>>>>>>")
#            elif(chlink=='no' or chlink=='n'):
#                raise HaltException("Exiting program>>>>>>>>>>>>>>>>")
#            else:
#                raise HaltException("Exiting program>>>>>>>>>>>>>>>>")
#        
#        except HaltException as h:
#            print(h)
#            restart=str(input("Do You Want to Search more movie again? [Yes/No]:   ")).lower()
#            if restart=='yes' or restart=='y':
#                main()
#            elif restart=='no' or restart=='n':
#                print("Bye, Have a good Day !")
#            else:
#                print("Again, Invalid Choice")