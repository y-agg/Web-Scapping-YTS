countermovie=0
def main():
    import time
    import webbrowser
    import requests
    from bs4 import BeautifulSoup
    from spellchecker import SpellChecker

    listofmovie=[]
    listofyear=[]
    listoflink=[]
    finallist=[listofmovie,listofyear,listoflink]    
    class HaltException(Exception):
        pass
    def moviesearch(search,max_pages=1):
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
                listofmovie.append(name)
                listofyear.append(titleyear)
                listoflink.append(href)
            printmovies()
            page+=1
    def printmovies():
        countermovie=1
        for i in range(len(listofmovie)):   
            if len(listofmovie)==1:
                print(f' {listofmovie[i]} ({listofyear[i]})')
            else:
                print(f'{countermovie}. {listofmovie[i]} ({listofyear[i]})')
            countermovie+=1
    def getimbdlinkfromyts(url):
        source_code=requests.get(url)
        pain_code=source_code.text
        soup=BeautifulSoup(pain_code,features="lxml")
        count=0
        for link in soup.findAll('a',{'class':'icon'}):
            count+=1
            imbd=link.get('href')
            index=imbd.find('www.imdb.com')
            if index!=-1:
                getinfo(imbd)
                break
    
    def getinfo(url):
         source_code=requests.get(url)
         pain_code=source_code.text
         soup=BeautifulSoup(pain_code,features="lxml")
         #Summary Of movie
         summary=soup.find('div',{'class':'summary_text'}).string
         if(summary==None):
             link=url+"plotsummary"
             summary=getfullsummary(link)
         print(f'Summary: {summary.strip()}')
         #Name Of Director
         Director=soup.findAll('div',{'class':'credit_summary_item'})[0].text
         print(f'Director: {Director[11:]}')
         #Writers Of Movie
         Writers=soup.findAll('div',{'class':'credit_summary_item'})[1].text
         print(f'Writers :  {Writers[10:]}')
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
    def getfullsummary(url):
        source_code=requests.get(url)
        pain_code=source_code.text
        soup=BeautifulSoup(pain_code,features="lxml")
        link=soup.find('li',{'class':'ipl-zebra-list__item'}).find('',recursive=False).string
        return link
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
    
    def getLink(url):
        source_code=requests.get(url)
        pain_code=source_code.text
        soup=BeautifulSoup(pain_code,features="lxml")
        download_link=[]
        counter=0
        for link in soup.findAll('a',{'class':'download-torrent button-green-download2-big'}):
            name=link.get('title')
            if(name.find('720p')!=-1):
                href=link.get('href')
                download_link.append(href)
                counter+=1
                print(counter,".  720p Torrent"+"  :  ",href)
                print("\r")
            if(name.find('1080p')!=-1):
                href=link.get('href')
                download_link.append(href)
                counter+=1
                print(counter,".  1080p Torrent"+" :  ",href)
                print("\r")
        
        Choice_of_download=str(input("Want to download ?[Yes/No]: ")).lower()
        if(Choice_of_download=='yes' or Choice_of_download=='y'):
            download_choice_link=int(input("Enter Choice:  "))
            if download_choice_link<=len(listoflink) and download_choice_link>0:
                webbrowser.open_new(download_link[download_choice_link-1])
            else:
                raise HaltException("Invalid Choice")
        elif(Choice_of_download=='no' or Choice_of_download=='n'):
            raise HaltException("You Said No...That mean Its time to end of my service")
        else:
            raise HaltException("Invalid choice")
    def options():
        print("       1. Want to Know More About Movies ?")
        print("       2. Or want to Download This Movie ?")
    def choice(a):
        ch=int(input(a+" "))
        return ch
    def checklength(value,maximum):
        if value<=maximum and value>0:
            pass
        else:
            raise HaltException("Invalid Choice")
    def yesno(a,b="no"):
        if(b=="no"):
            chlink=str(input(a)).lower()
        else:
            chlink=str(input(a+"[Yes/No]:   ")).lower()
        if(chlink=='yes' or chlink=='y' ):
            pass
        elif(chlink=='no' or chlink=='n'):
            raise HaltException("Did you Find What You are Looking For ?")
        else:
            raise HaltException("Invalid Choice")
    
    def spellcheck(words):
        spell = SpellChecker()
        misspelled = spell.unknown(words)
        for word in misspelled:
            ind=words.index(word)
            words[ind]=spell.correction(word)
        return (" ".join(words))  
    
    
    if __name__=="__main__":
        try:
            #Accepting movie name from user
            search=input(str("Enter name of movie:")).strip()
            moviesearch(search)
            if(len(listofmovie)==0): 
                search=spellcheck(search.split(" ")).capitalize()
                yesno("Did You Mean "+ search +" ? ","Yes")
                moviesearch(search)
                options()
                ch=choice("Select Option: ")
                checklength(ch,2)
                if(ch==1):
                    getimbdlinkfromyts(listoflink[0])
                    yesno("Want link of this movie to download")
                    getLink(finallist[2][0])
                elif ch==2:
                    getLink(finallist[2][0])
                else:
                    raise HaltException("Something went Wrong...Please Try again")
            
            elif(len(listofmovie)==1):
                options()
                ch=choice("Select Option: ")
                checklength(ch,2)
                if(ch==1):
                    getimbdlinkfromyts(listoflink[0])
                    yesno("Want link of this movie to download")
                    getLink(finallist[2][0])
                elif ch==2:
                    getLink(finallist[2][0])
                else:
                    raise HaltException("Something went Wrong...Please Try again")
            else: 
                cho=choice("Select Movie: ")
                checklength(cho,len(listofmovie))
                print(f"\n{listofmovie[cho-1]}")
                options()
                ch=choice("Select Option: ")
                checklength(ch,2)
                if(ch==1):
                    getimbdlinkfromyts(listoflink[cho-1])
                    yesno("Want link of this movie to download")
                    getimbdlinkfromyts(listoflink[cho-1])
                elif ch==2:
                    getLink(finallist[2][cho-1])
                else:
                    raise HaltException("Something went Wrong...Please Try again")
            raise HaltException("Program Paused")
        
        except HaltException as h:
            print(h)
            restart=str(input("Do You Want to Search more movie again? [Yes/No]:   ")).lower()
            if restart=='yes' or restart=='y':
                main()
            elif restart=='no' or restart=='n':
                print("Bye, Have a good Day !")
            else:
                print("Again, Invalid Choice")
        print("Press Ctrl+ c To Exit ")
        while True: 
            time.sleep(1)
                
#From where Program starts
main()