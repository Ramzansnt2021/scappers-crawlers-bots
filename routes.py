from flask import Flask, redirect, url_for, render_template, request, send_from_directory
# libraries and files
from routerSwitches import *
from easyWorlds import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
import time
import os, glob, shutil
import shutil
from os import path
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
print("base dir",basedir)

posts = [
    {
        'author':'Murtaza Abbas',
        'title': 'Cisco Products',
        'Content':'Cisco Routers Files',
        'Created_on':' Dec 09, 2020',

},    {
        'author':'Mehwish',
        'title': 'Dell Products',
        'Content':'Dell server files',
        'Created_on':' Dec 20, 2020',

}
]

ALLOWED_EXTS = {"txt"}
UPLOAD_DIRECTORY = basedir + r'/static/uploads'
DOWN_DIRECTORY = basedir + r'/static/downloads'
ACCESS_LINKS = basedir + r'/static/uploads/*.txt'
app.config['UPLOAD_DIRECTORY'] = UPLOAD_DIRECTORY
app.config['DOWN_DIRECTORY'] = DOWN_DIRECTORY
app.config['ACCESS_LINKS'] = ACCESS_LINKS
# UPLOAD_DIRECTORY = os.path.join(basedir,'static', 'uploads')
# DOWN_DIRECTORY = os.path.join(basedir,'static', 'downloads')

# ACCESS_LINKS = os.path.join(basedir, "static", "uploads" ,r'*.txt')
# if not os.path.exists(DOWN_DIRECTORY):
#     os.makedirs(os.path.join(basedir,'static', DOWN_DIRECTORY))

# if not os.path.exists(UPLOAD_DIRECTORY):
#     os.makedirs(os.path.join(basedir,'static', UPLOAD_DIRECTORY))

def check_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTS

@app.route('/')
def layout():
    return render_template('select.html' )

@app.route('/home', methods=['post', 'get'])
def home():
    error = None
    filename = None
    if request.method == 'POST':
        if 'file' not in request.files:
            error = "File is not selected"
            return render_template('home.html', error=error)
        
        file = request.files['file']
        filename = file.filename

        if filename == '':
            error = "File name is empty"
            return render_template('home.html', error=error)
        
        if check_file(filename) == False:
            error = "This file isn't allowed"
        elif path.exists(filename):
            # get the path to the file in the current directory
            src = path.realpath(file);
            # rename the original file
            i=1
            for file in os.listdir(file):
                src=file
                dst="new_link_file"+str(i)+".txt"
                os.rename(src,dst)
                i+=1
            return render_template('home.html', error=error)

        

        file.save(os.path.join(UPLOAD_DIRECTORY, filename))
        # file.save(os.path.join(basedir, "static", "uploads", filename))
    return render_template('home.html', title='Home', filename=filename)

@app.route('/routerSwitches')
def about():
    list_of_files = glob.glob(ACCESS_LINKS) # * means all if need specific format then *.csv
    print("error is :", list_of_files)
    latest_file = max(list_of_files, key=os.path.getctime)
    print("error is :", latest_file)
    scraper = product_files(latest_file)
    
    source = r"D://formsProject//scrape//project//static//uploads//scrape.csv"
    destination = r"D://formsProject//scrape//project//static//downloads//"
    filename = os.path.basename(source)
    dest = os.path.join(destination,filename)
    shutil.move(source, dest)
    return render_template('about.html', title='Results', scraper=scraper) 

@app.route('/easyWorlds')
def about():
    list_of_files = glob.glob(ACCESS_LINKS) # * means all if need specific format then *.csv
    print("error is :", list_of_files)
    latest_file = max(list_of_files, key=os.path.getctime)
    print("error is :", latest_file)
    scraper = product_files(latest_file)
    
    source = r"D://formsProject//scrape//project//static//uploads//scrape.csv"
    destination = r"D://formsProject//scrape//project//static//downloads//"
    filename = os.path.basename(source)
    dest = os.path.join(destination,filename)
    shutil.move(source, dest)
    return render_template('about.html', title='Results', scraper=scraper)

@app.route('/downloads/<path:filename>', methods=['GET', 'POST'])
def downloads(filename):
    # uploads = os.path.join("D:/formsProject/scrape/project/downloads/bot.csv", app.config['downloads'])
    return send_from_directory(DOWN_DIRECTORY, filename=filename, as_attachment=True)

@app.route('/admin')
def admin():
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True, threaded=True)