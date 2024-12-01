from bs4 import BeautifulSoup
from tkinter import*
import requests
urls=["https://www.medipol.edu.tr/en/announcements?page=0",
     "https://www.medipol.edu.tr/en/announcements?page=1",
     "https://www.medipol.edu.tr/en/announcements?page=2",
     "https://www.medipol.edu.tr/en/announcements?page=3",
     "https://www.medipol.edu.tr/en/announcements?page=4",
     "https://www.medipol.edu.tr/en/announcements?page=5"]
def retrieval_article_adress(url):
        req=requests.get(url)
        soup = BeautifulSoup(req.content,"html.parser")
        tags=soup.find_all(True)
        adress=[]
        for tag in tags :
            adress.append(tag.text)
        return adress
def retrieve_title(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    links = soup.find_all("a")
    titles=[]
    for link in links:
        title = link.get("title")
        if title:
            titles.append(title)
    return titles
def retrieve_time(urls):
        req = requests.get(urls)
        soup = BeautifulSoup(req.content, "html.parser")
        dates=[]
        for i in soup.find_all('time'):
            if i.has_attr('datetime'):
                dates.append(i['datetime'])
        return dates
class announce:
    def __init__(self,title,adress,time):
        self.title=title
        self.adress=adress
        self.time=time
#https://youtu.be/QhD015WUMxE?si=Fm7q1wRvNa6Xwzds
def retreive_all_announcement(urls):
    all_announcement=[]
    for url in urls:
        adress=retrieval_article_adress(url)
        titles=retrieve_title(url)
        time=retrieve_time(url)
        for title,adress,time in zip (titles,adress,time):
            all_announcement.append(announcement(title,adress,time))
            print (f"{len(all_announcement)} announcements scraped from {url}")
    return all_announcement



class Gui(Frame):
    def __init__(self,parent):
        Frame.__init__(self, parent)
        self.parent=parent
        self.list_of_web=retreive_all_announcement(urls)
        self.urls=urls
        self.initUI()
    def initUI(self):


        self.lb = Listbox(self.parent, selectmode="single",width=25,height=15)
        self.lb.grid(row=1, column=0, sticky='SW')

        for i in self.list_of_web:
            self.lb.insert(END, i)

        l1=Label(self.parent,text="Announcements")
        l1.grid(row=0,column=0,sticky='NW')

        l2=Label(self.parent,text="content of announcement")
        l2.grid(row=0,column=1,columnspan=1,sticky='W')

        output = Text(self.parent,width=67,height=20)
        output.grid(row=1,column=1,sticky='NE')

        self.lb.bind('<<ListSelect>>', self.OnSelection)

    def OnSelection(self, event):
        if self.lb.curselection ():
            index = self.lb.curselection()[0]
            selected_item = self.list_of_web[index]
            self.output.delete(1.0, END)
            self.output.insert(END, f"Title: {selected_item['titles'][0]}\n")
            self.output.insert(END, f"Address: {selected_item['addresses'][0]}\n")
            self.output.insert(END, f"Time: {selected_item['times'][0]}\n")
            #https://stackoverflow.com/


def main():
    root = Tk()
    root.title("tk")
    root.geometry("700x700")
    app = Gui(root)
    app.grid()
    root.mainloop()


main()
