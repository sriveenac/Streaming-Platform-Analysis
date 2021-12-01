#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk,Image  


# In[2]:


all = pd.read_csv('Data/all_data_processed.csv')
all_ = all.fillna('')
def lower(x):
    return str.lower(x.replace(' ', ''))
def comma(x):
    return str.lower(x.replace(' ', ','))

def bow(x):
    return x['title'] + ' ' + x['director'] + ' ' + x['cast'] + ' ' + x['listed_in'] + ' ' + x['description']

all_.country = all_.country.apply(lower)
all_.title = all_.title.apply(lower)
all_.listed_in = all_.listed_in.apply(lower)
all_.cast = all_.cast.apply(lower)
all_.director = all_.director.apply(lower)
all_.description = all_.description.apply(lower)
all_.description = all_.description.apply(comma)
all_['bow'] = all_.apply(bow,axis = 1)
vec = CountVectorizer(stop_words='english')
counts = vec.fit_transform(all_['bow'])
cosine_sim = cosine_similarity(counts, counts)
all_ = all_.reset_index()
indices = pd.Series(all_.index, index=all_['title'])


# In[3]:


def getRecommendations(movie_title):
    movie_title = movie_title.replace(' ', '').lower()
    ind = indices[movie_title]
    
    try:
        l = len(ind)
        new = np.zeros((len(ind),22916))
        for i in range(len(ind)):
            new[i,:] = cosine_sim[ind[i]]
        sol = np.max(new, axis = 0)
        Score = list(enumerate(sol))
        
    except:
        Score = list(enumerate(cosine_sim[ind]))

    Score.sort(key=lambda x:x[1],reverse = True)

    index = [Score[i][0] for i in range(1,21)]
    try:
        index = [i for i in index if i not in list(ind)]
    except:
        index = index

    
    return all['title'].iloc[index]


# In[4]:


def filt(name,country_choice, age,type_choice,length_choice, ry_choice,genre_choice, director_choice, cast_choice, platform_choice):
    def country_filter(df,choice):

        df_up = df.copy()
        if choice == None or choice == 'None':
            return df_up   
        else:
            df_up.country = df_up.country.str.split(', ')
            df_up = df_up.explode('country')
            return df_up[df_up.country == choice]

    def rating_filter(df,choice):
        df_up = df.copy()
        if choice == '' or choice == None:
            return df_up
        else:
            if int(choice) <= 13:
                return df_up[df_up.rating == 7]
            elif int(choice) > 13 and int(choice) <= 18:
                return df_up[df_up.rating.isin([7,13])]
            else:
                return df_up

    def type_filter(df,choice):
        df_up = df.copy()
        if choice == 'None' or choice == None:
            return df_up
        else:
            return df_up[df_up.type == choice]

    def length_filter(df,choice):
        df_up = df.copy()
        if choice == 'None' or choice == None:
            return df_up
        else:
            if choice == '1 hr':
                choice = 60
            elif choice == '1.5 hrs':
                choice = 90
            elif choice == '2 hrs':
                choice = 120
            elif choice == '3 hrs':
                choice = 180
            elif choice == 'no restriction':
                return df_up
            if choice != 'no restriction':
                return df_up[df_up.length <= choice]

    def ry_filter(df,choice):
        df_up = df.copy()
        if choice == 'None' or choice == None:
            return df_up
        else:
            if choice == '1920-1950':
                return df_up.loc[(df_up.release_year >= 1920) & (df_up.release_year < 1960)]
            elif choice == '1950-1970':
                return df_up.loc[(df_up.release_year >= 1950) & (df_up.release_year < 1980)]
            elif choice == '1980s':
                return df_up.loc[(df_up.release_year >= 1980) & (df_up.release_year < 1990)]
            elif choice == '1990s':
                return df_up.loc[(df_up.release_year >= 1990) & (df_up.release_year < 2000)]
            elif choice == '2000s and later':
                return df_up.loc[(df_up.release_year >= 2000) ]
  
    def genre_filter(df,choice):
        df_up = df.copy()
        if choice == 'None' or choice == None:
            return df_up
        else:
            df_up.listed_in = df_up.listed_in.str.split(', ')
            df_up = df_up.explode('listed_in')
            return df_up[df_up.listed_in == choice]

    def director_filter(df,choice):
        df_up = df.copy()
        if choice == 'None' or choice == None:
            return df_up
        else:
            df_up.director = df_up.director.str.split(', ')
            df_up = df_up.explode('director')
            return df_up[df_up.director==choice]

    def cast_filter(df,choice):
        df_up = df.copy()
        if choice == 'None' or choice == None:
            return df_up
        else:
            df_up.cast = df_up.cast.str.split(', ')
            df_up = df_up.explode('cast')
            return df_up[df_up.cast==choice]

    def platform_filter(df,choice):
        df_up = df.copy()
        if choice == 'None' or choice == None:
            return df_up
        else:
            return df_up[df_up.platform==choice]
        
    output = country_filter(all,country_choice)

    output = rating_filter(output,age)

    output = type_filter(output,type_choice)

    output = length_filter(output,length_choice)

    output = ry_filter(output,ry_choice)

    output = genre_filter(output,genre_choice)

    output = director_filter(output,director_choice)

    output = cast_filter(output,cast_choice)

    output = platform_filter(output,platform_choice)

    return output.loc[:,['title', 'platform', 'description']]


# In[5]:


def Recommender():
    title_options = sorted(list(pd.unique(all.title)))
    rec = Tk()
    rec.title("Recommender System")
    rec.geometry('500x500')
    img = ImageTk.PhotoImage(Image.open("rs_header.png"),master = rec)  
    def printDF():
        top = Toplevel(rec)
        top.geometry('1000x1000')
        out = getRecommendations(titles.get())
        Label(top, text= f'Recommended Content for {name}').place(y = 0, x = 300, height = 50, width = 300 )
        if out.empty:
            Label(top, text= 'No content matches your criteria').place(y = 50, x = 300, height = 50, width = 200 ) 
            Button(top,text="Try Again!", command=Quiz).place(x = 500,y = 50,height=50,width = 50)

        k = 0
        for i in list(out):
            desc = all[all.title == i].loc[:,'description'].iloc[0]
            p= all[all.title == i].loc[:,'platform'].iloc[0]
            Label(top, text= i).place(y=50+60*k,x = 0,height=60,width = 300)
            Label(top,text=f'Platform: {p}. Description: {desc}',wraplength=700,justify = LEFT).place(y=50+60*k,x=300,height=60,width = 700)
            k +=1
            if k == 11:
                break
        top.mainloop()
    def printName():
        global name
        name = player_name.get()
        Label(rec, text=f'Hi,{name}!').place(x=300,y=65,height=30,width = 80)
                                                                   
    
                                                                   
                                                                   

    Label(rec, image = img).place(x = 0, y = 0, width = 500, height = 60)
    L = Label(rec,text="What's Your Name?").place(x = 0, y = 65, height=30,width = 150)
    player_name = Entry(rec)
    player_name.place(x = 151 ,y = 65,height=30,width = 150)
    Nb = Button(rec,text="OK", command=printName)
    Nb.place(x = 300,y = 65,height=30,width = 80)

    Label(rec,text="Choose Your Favourite Title").place(x = 0, y = 100, height=30,width = 200)
    titles = StringVar(rec)
    titles.set(title_options[0])
    title_menu = OptionMenu(rec, titles, *title_options)
    title_menu.place(y = 100,x=200,height=30,width = 200)
    Tb = Button(rec, text="OK", command=printDF)
    Tb.place(y = 100,x=400,height=30,width = 80)  
    rec.mainloop()
    
    


# In[10]:


def Quiz():
    ws = Tk()
    ws.title("Quiz")
    ws.geometry('800x800')
    style = Style()
    style.theme_use('aqua')
    img = ImageTk.PhotoImage(Image.open("quiz_header.png"),master = ws)   
    
    df_up = all.copy()
    df_up.country = df_up.country.str.split(', ')
    df_up = df_up.explode('country')
    country_options = sorted(list(pd.unique(df_up.country.astype(str))))
    type_options = sorted(list(pd.unique(all.type.astype(str))))
    length_options = ['1 hr','1.5 hrs','2 hrs','3 hrs','no restriction']
    release_year_options = ['1920-1950','1950-1970','1980s','1990s','2000s and later']
    df_up = all.copy()
    df_up.listed_in = df_up.listed_in.str.split(', ')
    df_up = df_up.explode('listed_in')
    genre_options = sorted(list(pd.unique(df_up.listed_in.astype(str))))
    df_up = all.copy()
    df_up.director = df_up.director.str.split(', ')
    df_up = df_up.explode('director')
    director_options = sorted(list(pd.unique(df_up.director.astype(str))))
    df_up = all.copy()
    df_up.cast = df_up.cast.str.split(', ')
    df_up = df_up.explode('cast')
    cast_options = sorted(list(pd.unique(df_up.cast.astype(str))))
    platform_options = sorted(list(pd.unique(all.platform.astype(str))))
    
    global name,country_choice, age,type_choice,length_choice, ry_choice,genre_choice, director_choice, cast_choice, platform_choice
    name,country_choice, age,type_choice,length_choice, ry_choice,genre_choice, director_choice, cast_choice, platform_choice = None,None,None,None,None,None,None,None,None,None

    Label(ws, image = img).place(x = 0, y = 0, width = 800, height = 60)
   
    def printName():
        global name
        name = player_name.get()
        Label(ws, text=f'Hi,{name}!').place(x=420,y=65,height=30,width = 80)

    L = Label(ws,text="What's Your Name?").place(x = 119, y = 65, height=30,width = 150)
    player_name = Entry(ws)
    player_name.place(x = 270 ,y = 65,height=30,width = 150)
    Nb = Button(ws,text="OK", command=printName)
    Nb.place(x = 420,y = 65,height=30,width = 80)

    def printCountry():
        global country_choice
        country_choice = countries.get()
        Label(ws, text=f'I Love {country_choice}').place(y = 100,x=420,height=30,width = 500)

    countries = StringVar(ws)
    countries.set(None)
    Label(ws,text="Country of Title?").place(y=100,x=119,height=30,width = 150)
    countries_menu = OptionMenu(ws, countries, *country_options)
    countries_menu.place(y = 100,x=270,height=30,width = 150)
    Cb = Button(ws, text="OK", command=printCountry)
    Cb.place(y = 100,x=420,height=30,width = 80)
    
    def printRating():
        global age
        age = age_.get()
        Label(ws, text=f'Wow!{age} is really old!').place(y = 135,x=420,height=30,width = 500)

    ages = StringVar(ws)
    ages.set(None)
    Label(ws,text="How Old Are You?").place(y=135,x=119,height=30,width = 150)
    age_ = Entry(ws)
    age_.place(x = 270 ,y = 135,height=30,width = 150)
    Ab = Button(ws,text="OK", command=printRating)
    Ab.place(y=135,x = 420,height=30,width = 80)
    
    def printType():
        global type_choice
        type_choice = types.get()
        Label(ws, text=f'{type_choice} is a good choice').place(y = 170,x=420,height=30,width = 500)

    types = StringVar(ws)
    types.set(None)
    Label(ws,text="Movie or TV Show?").place(y=170,x=119,height=30,width = 150)
    type_menu = OptionMenu(ws, types, *type_options)
    type_menu.place(y = 170,x=270,height=30,width = 150)
    Tb = Button(ws, text="OK", command=printType)
    Tb.place(y = 170,x=420,height=30,width = 80)
    
    def printLength():
        global length_choice
        length_choice = lengths.get()
        Label(ws, text=f'Glad you have {length_choice} to spare ').place(y = 205,x=420,height=30,width = 500)

    lengths = StringVar(ws)
    lengths.set(None)
    Label(ws,text="Length of Movie?").place(y=205,x=119,height=30,width = 150)
    length_menu = OptionMenu(ws, lengths, *length_options)
    length_menu.place(y = 205,x=270,height=30,width = 150)
    Lb = Button(ws, text="OK", command=printLength)
    Lb.place(y = 205,x=420,height=30,width = 80)
    
    def printReleaseYear():
        global ry_choice 
        ry_choice = rys.get()
        Label(ws, text=f'{ry_choice} is a perfect decade').place(y = 240,x=420,height=30,width = 500)

    rys = StringVar(ws)
    rys.set(None)
    Label(ws,text="Release Year?").place(y=240,x=119,height=30,width = 150)
    rys_menu = OptionMenu(ws, rys, *release_year_options)
    rys_menu.place(y = 240,x=270,height=30,width = 150)
    Lb = Button(ws, text="OK", command=printReleaseYear)
    Lb.place(y = 240,x=420,height=30,width = 80)
    
    def printGenre():
        global genre_choice 
        genre_choice = genres.get()
        Label(ws, text=f'ooo I love {genre_choice}').place(y = 275,x=420,height=30,width = 500)

    genres = StringVar(ws)
    genres.set(None) 
    Label(ws,text="Genre?").place(y=275,x=119,height=30,width = 150)
    genres_menu = OptionMenu(ws, genres, *genre_options)
    genres_menu.place(y = 275,x=270,height=30,width = 150)
    Gb = Button(ws, text="OK", command=printGenre)
    Gb.place(y = 275,x=420,height=30,width = 80)
    
    def printDirector():
        global director_choice 
        director_choice = ds.get()
        Label(ws, text=f'{director_choice} is a great director').place(y = 310,x=420,height=30,width = 500)

    ds = StringVar(ws)
    ds.set(None)
    Label(ws,text="Director?").place(y=310,x=119,height=30,width = 150)
    ds_menu = OptionMenu(ws, ds, *director_options)
    ds_menu.place(y = 310,x=270,height=30,width = 150)
    Db = Button(ws, text="OK", command=printDirector)
    Db.place(y = 310,x=420,height=30,width = 80)
    
    def printCast():
        global cast_choice 
        cast_choice = None
        cast_choice = cast.get()
        Label(ws, text=f'{cast_choice} is amazing').place(y = 345,x=420,height=30,width = 500)

    cast = StringVar(ws)
    cast.set(None)
    Label(ws,text="Cast?").place(y=345,x=119,height=30,width = 150)
    cast_menu = OptionMenu(ws, cast, *cast_options)
    cast_menu.place(y = 345,x=270,height=30,width = 150)
    Cb = Button(ws, text="OK", command=printCast)
    Cb.place(y = 345,x=420,height=30,width = 80)
    
    def printPlatform():
        global platform_choice
        cast_choice = None
        platform_choice = platforms.get()
        Label(ws, text=f'{platform_choice} is the only good platform').place(y = 380,x=420,height=30,width = 200)

    platforms = StringVar(ws)
    platforms.set(None)
    Label(ws,text="Platform?").place(y=380,x=119,height=30,width = 150)
    platform_menu = OptionMenu(ws, platforms, *platform_options)
    platform_menu.place(y = 380,x=270,height=30,width = 150)
    Pb = Button(ws, text="OK", command=printPlatform)
    Pb.place(y = 380,x=420,height=30,width = 80)
    
    def printDF():
        top = Toplevel(ws)
        top.geometry('1000x1000')
        out = filt(name,country_choice, age,type_choice,length_choice, ry_choice,genre_choice, director_choice, cast_choice, platform_choice)
        Label(top, text= f'Recommended Content for {name}').place(y = 0, x = 300, height = 50, width = 300 )
        if out.empty:
            Label(top, text= 'No content matches your criteria').place(y = 60, x = 50, height = 50, width = 300 ) 
            Button(top,text="Try Again!", command=Quiz).place(x = 300,y = 50,height=50,width = 150)

        k = 0
        
        for i in list(out.title):
            desc = out[out.title == i].loc[:,'description'].iloc[0]
            p= out[out.title == i].loc[:,'platform'].iloc[0]
            Label(top, text= i).place(y=50+60*k,x = 0,height=60,width = 300)
            Label(top,text=f'Source: {p}. Description: {desc}',wraplength=700,justify = LEFT).place(y=50+60*k,x=300,height=60,width = 700)
            k +=1
            if k == 11:
                break
        top.mainloop()

    Label(ws,text="Do You Want To Lock Your Choices?").place(y=415,x=250,height=40,width = 250)
    b = Button(ws,text="Yes", command=printDF)
    b.place(y = 415,x = 500,height=40,width = 100)

    
    ws.mainloop()   


# In[ ]:



main = Tk()

main.title("Movie Recommender")
main.geometry('800x400')
style = Style()
style.theme_use('aqua')  
img = ImageTk.PhotoImage(Image.open("heading.png"),master = main)   

Label(main, image = img).pack()
#Label(main, text = 'MOVIE RECOMMENDER', font = ('Georgia', 30)).pack()
Label(main, text = "Get recommendations based on something you've seen").pack()
Button(main,text="Let's Go", command=Recommender).pack()
Label(main, text = "Get recommendations by taking a quiz").pack()
Button(main,text="Let's Go", command=Quiz).pack()
main.mainloop()

