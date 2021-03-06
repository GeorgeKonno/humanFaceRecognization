import re
import requests
import urllib2
from bs4 import BeautifulSoup
import os
 
 
def Find(url):
    global List
    print('             ///in finding process///')
    num_of_url = 0
    length_of_string = 0
    while num_of_url < 1000:
        Url = url + str(num_of_url)
        try:
            Result = requests.get(Url, timeout=7)
        except BaseException:
            num_of_url = num_of_url + 60
            continue
        else:
            result = Result.text
            pic_url = re.findall('"objURL":"(.*?)",', result, re.S)  
            length_of_string += len(pic_url)
            if len(pic_url) == 0:
                break
            else:
                List.append(pic_url)
                num_of_url = num_of_url + 60
    return length_of_string
 
 
def recommend(url):
    Re = []
    try:
        html = requests.get(url)
    except urllib2.error.HTTPError as e:
        return
    else:
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.find('div', id='topRS')
        if div is not None:
            listA = div.findAll('a')
            for i in listA:
                if i is not None:
                    Re.append(i.get_text())
        return Re
 
 
def dowmloadPicture(html, keyword):
    global num
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)  
    #print('find key word:' + keyword + 'start to download img...')
    for each in pic_url:
        print str(num + 1),
        try:
            if each is not None:
                pic = requests.get(each, timeout=7)
            else:
                continue
        except BaseException:
            print('error, check your connection')
            continue
        else:
            string = filepath + r'/' + keyword + '_' + str(num) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            print " "
            return
 
 
if __name__ == '__main__':
    y = os.path.exists('data')
    if y == 1:
        try:
            for root, dirs, files in os.walk('data', topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir('data')
        except:
            os.remove('data')
        os.mkdir('data')
    else:
        os.mkdir('data')
    for line in open("mingxing.txt","r"): 
        print('----------------------START-----------------------')
        num = 0
        numPicture = 0
        filepath = ''
        List = []
        word = line[:-1]
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + str(word) + '&pn='
        tot = Find(url)
        #Recommend = recommend(url)  
        numPicture = 20
        print('       ///is %s consist of %d imgs///' % (word, numPicture))
        filepath ='data'+'/'+word
        y = os.path.exists(filepath)
        if y == 1:
            print('file exists')
            print('will delete iniital folder')
            try:
                os.rmdir(filepath)
            except:
                os.remove(filepath)
            os.mkdir(filepath)
        else:
            os.mkdir(filepath)
        t = 0
        tmp = url
        while t < numPicture:
            try:
                url = tmp + str(t)
                result = requests.get(url, timeout=10)
                #print(url)
            except urllib2.error.HTTPError as e:
                print('error, check your connection')
                t = t+60
            else:
                dowmloadPicture(result.text, word)
                t = t + 60
     
        print('----------------------END-------------------------\n')
        #print('for more you like')
        #for recommend in Recommend:
            #print(recommend)
            #print '  '