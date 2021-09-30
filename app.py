# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 10:12:00 2021

@author: mathuvanthi.pandia
"""

import requests
from bs4 import BeautifulSoup
import numpy as np 
import pandas as pd
from flask import Flask, render_template, jsonify, make_response, request


app = Flask(__name__)

global final_url

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route('/defaults',methods=['POST'])

def defaults():

    return render_template('index.html')


def transform(text_file_contents):

    return text_file_contents.replace("=", ",")

@app.route('/transform', methods=["POST"])

def transform_view():
    if request.method == 'POST':
        city_name = request.form.get("cityname")
        
       
        link2="forecasts/latest"
        link1="https://www.weather-forecast.com/locations/"
        
        page = requests.get(f'{link1}{city_name}/{link2}')
        soup=BeautifulSoup(page.content,"lxml")
        
        d={}
        day = soup.findAll("div" , {"class":"b-forecast__table-days-name"})
        date= soup.findAll("div" , {"class":"b-forecast__table-days-date"})
        l=[]
        l1 = []
        d = {}
        d1 = {}
        for (i) in range(0,12):
            d = day[i].text
            d1 = date[i].text
            l.append(d)
            l1.append(d1)
        df = pd.DataFrame() 

        df["day"] = l
        df["date"] = l1
        
        
        temp = soup.find("tr" , {"class":"b-forecast__table-max-temperature js-temp"})
        temp_3 = temp.findAll("span" , {"class":"temp b-forecast__table-value"})

        l=[]
        d = {}

        for (i,j) in zip(range(14),range(0,36,3)):
            d = '['+str(temp_3[j].text)+','+ str(temp_3[j+1].text)+','+ str(temp_3[j+2].text)+']'
            l.append(d)

        df['Max_Temp [AM,PM,Night]']= l
        
        min_temp = soup.find("tr" , {"class":"b-forecast__table-min-temperature js-min-temp"})
        mintemp_3 = min_temp.findAll("span" , {"class":"b-forecast__table-value"})
        

        wind = soup.find("tr" , {"class":"b-forecast__table-wind js-wind"})
        wind_final = wind.findAll("text" , {"class":"wind-icon-val"})
        
        rain=soup.find('tr',{'class':"b-forecast__table-rain js-rain"})
        rain_final=rain.findAll('span',{"class":"rain b-forecast__table-value"})
        
     

        chill = soup.find("tr" , {"class":"b-forecast__table-chill js-chill"})
        chill_final = chill.findAll("span" , {"class":"temp b-forecast__table-value"})
        
      

        humidity = soup.find("tr" , {"class":"b-forecast__table-humidity js-humidity"})
        humidity_final = humidity.findAll("span" , {"class":"b-forecast__table-value"})
        
        l = []
        l1 = []
        l2 = []
        l3 = []
        l4 = []
        d = {}
        d1 = {}
        d2 = {}
        d3 = {}
        d4 = {}
        
        for (i,j) in zip(range(14),range(0,36,3)):
            d = '['+str(mintemp_3[j].text)+','+ str(mintemp_3[j+1].text)+','+ str(mintemp_3[j+2].text)+']'
            l.append(d)
            d1 = '['+str(wind_final[j].text)+','+ str(wind_final[j+1].text)+','+ str(wind_final[j+2].text)+']'
            l1.append(d1)
            d2 = '['+str(rain_final[j].text)+','+ str(rain_final[j+1].text)+','+ str(rain_final[j+2].text)+']'
            l2.append(d2)
            d3 = '['+str(chill_final[j].text)+','+ str(chill_final[j+1].text)+','+ str(chill_final[j+2].text)+']'
            l3.append(d3)
            d4 = '['+str(humidity_final[j].text)+','+ str(humidity_final[j+1].text)+','+ str(humidity_final[j+2].text)+']'
            l4.append(d4)

        df['Min_Temp [AM,PM,Night]']= l
        df['Wind [AM,PM,Night]'] = l1
        df['Rain\n[AM,PM,Night]'] = l2
        df['Chill\n[AM,PM,Night]'] = l3
        df['Humidity\n[AM,PM,Night]'] = l4
        response = make_response(df.to_csv())
        response.headers["Content-Disposition"] = "attachment; filename = weather.csv"
        return response    
    
    
if __name__=="__main__":
    app.run(debug=True)