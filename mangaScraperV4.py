#get website and choose title
#choose english title as a condition
#find the number of pages and use as a looping condition
#total number of pages on the bottom right as a condition for looping
#store into a folder
#rename the folder based on the manga chapter
#what if I only want to scrape chapter x to y?
#separate by chapter and volume
#would be nice to have a GUI with search
import time
import re
import urllib.request
import os
from os import path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


browser = webdriver.Firefox()



def getMaxPageCount():
    maxPageCount = browser.find_element_by_class_name('total-pages').text
    return int(maxPageCount)

def getCurrentPage():
    currentPage = browser.find_element_by_class_name('current-page').text
    return int(currentPage)

def getChapterTitle():
    chapterTitle = browser.find_element_by_class_name('chapter-title').text
    illegalChars = ['NUL','\',''//',':','*','"','<','>','|']
    for i in illegalChars:
        chapterTitle = chapterTitle.replace(i, '')
    return str(chapterTitle)

def getImageSource():
    imgSrc = browser.find_element_by_class_name('noselect.nodrag.cursor-pointer').get_attribute('src')
    return imgSrc

def getChapterNo():
    #get chapter no. using the link value
    url = browser.current_url
    #valueRegex = re.compile(r'\d\d\d\d\d\d') #not all manga has the same
    #valueRegex = re.compile(r'(\d){4,7}?')
    valueRegex = re.compile(r'\d\d\d\d\d\d')
    matchText = valueRegex.search(url).group()

    #get Jump title
    jumpTitle = browser.find_element_by_xpath("//option[@value='" + matchText + "']").text

    #chapterRegex
    chapterRegex = re.compile(r'Ch. \d+')
    return chapterRegex.search(jumpTitle).group()

def isDownloadedAndSaved(imgSrc):
    currentPage = getCurrentPage()
    fileName = str(currentPage) +'.jpg'
    #check if file exists in directory
    if not path.exists(fileName):
        img = urllib.request.urlretrieve(imgSrc, fileName)
        print('Page: ' + str(getCurrentPage()) + '/' + str(getMaxPageCount()) + ' Downloaded')
        return True
    else:
        print('Failed to download')
        return False

def isPageReady():
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'noselect.nodrag.cursor-pointer'))) #classes with spaces, combine with .
        #print('Page is ready!')
        return True
    except TimeoutException:
        print('Loading took too much time!')
        return False

def moveToNextPage():
    htmlElem = browser.find_element_by_tag_name('html')
    htmlElem.send_keys(Keys.ARROW_RIGHT)

    #if currentpage == maxPageCount start new chapter
    #print if successfull 'saved in directory x'

def EoC(): #End of Chapter
    if (getCurrentPage() == getMaxPageCount()):
        #download page
        downloadPage()
        #move next
        moveToNextPage()
        #create new and set new working directory
        #createDir(getChapterNo(browser), getchapterTitle())
        return True
    else:
        return False

def downloadChapter():
    dirName = createDir(getChapterNo(), getChapterTitle())
    changeDir(dirName)

    currentPage = getCurrentPage()
    maxPageCount = getMaxPageCount()

    if isPageReady():
        while not EoC():
            downloadPage()
            moveToNextPage()
            currentPage += 1

def downloadPage():
    if isPageReady():
        src = getImageSource()
        if isDownloadedAndSaved(src):     #download and store image
          return True
        else:
            return False

def changeDir(dirName):
    os.chdir(dirName)

def createDir(chapterNo, chapterTitle):
    #create anime folder directory
    dirName = 'C:\\Users\\razon\\PythonScripts\\One Piece Chapters\\' + chapterNo + ' ' + chapterTitle
    print('Now downloading: ' + dirName)
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
        return dirName
    else:
        print("Directory " , dirName ,  " already exists")
        return dirName

def startDownload(src, chapters):
    browser.get(src)
    #x = 0
    #while x < chapters:
    for i in range(chapters):
        print('Downloading chapter ' + str(i+1) + ' of ' + str(chapters))
        if isPageReady():
            time.sleep(5)
            print('===================')
            downloadChapter()
            print('Successfully downloaded chapter ' + str(i+1))
    #x += 1



#ask for input, starting chapter and how many chapters to download
startDownload('https://mangadex.org/chapter/109495/1', 3)


#check if files already exists with same folder names
