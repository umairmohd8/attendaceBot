from selenium import webdriver
import tweepy
import vars

CONSUMER_KEY = vars.apikey
CONSUMER_SECRET = vars.apisecret
ACCESS_KEY = vars.Accesstoken
ACCESS_SECRET = vars.Accesstokensecret

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)  
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

browser = webdriver.Firefox()


def login():

    browser.get('https://campus.uno/Student/Attendance')
    user = browser.find_element_by_id('LoginId').send_keys(vars.username)
    password = browser.find_element_by_id('Password').send_keys(vars.passw)
    login = browser.find_element_by_css_selector(
        '#intro > div > div > div:nth-child(2) > section > footer > button').click()
# logs into my account

def store_last_dict(last_attend, file_name):  #for storing currrent attendace data
    f_write = open(file_name, 'w')
    f_write.write(str(last_attend))
    f_write.close()
    return

def retrieve_last_dict(file_name): #for retriving past attendace data
    f_read = open(file_name, 'r')
    lastDic = eval(str(f_read.read().strip()))
    f_read.close()
    return lastDic

def tweet(out,absent):  #for messaging the attendace data to my profile
    api.send_direct_message(3250564195,out)
    api.send_direct_message(3250564195,absent)

def table(fin):    #creating the table for attendace data
    finOld = retrieve_last_dict('last_dict.txt')
    out = "{:<8} {:<8} {:<8} {:<8}\n".format('Subject','Held','present','percent')
    a = 'You were absent for '
    absent = a
    for (k1,v1), (k2,v2) in zip(finOld.items(),fin.items()):
        h1, a1, percent = v1    #h1, a1 are past week held and attended classes
        h2, a2, _ =v2            #h2, a2 are current week held and attended classes
        not_present = (h2-h1) - (a2-a1)    # number of absent classes
        out += "{:<8} {:<8} {:<8} {:<8}\n".format(k1,h1,a1,percent)
        if not_present:       #prints the absent classes
            absent += "{cls} of {sub}, ".format(cls = not_present,sub = k1)
    if absent == a: #if absent for no classes
        absent = a + 'no classes.'
    tweet(out,absent)
    print(out)        
    print(absent)
    store_last_dict(fin,'last_dict.txt')
            
def subjects():
    browser.implicitly_wait(30)                
    # xpath of table rows
    loo = '//*[@id="div-data-display"]/table/tbody/tr[{row}]/'
    subs = ['a', 'b', 'DSA', 'ADE', 'CO', 'SE', 'DMS', 'ADEL', 'DSAL', 'MATH']
    fin = {}  # dict for subs n percentage
    for i in range(2, 10):
        sub = subs[i]
        perc = browser.find_element_by_xpath(loo.format(row=i) + "td[6]").text
        held = browser.find_element_by_xpath(loo.format(row=i) + "td[4]").text
        pres = browser.find_element_by_xpath(loo.format(row=i) + "td[5]").text
        if held == '':  # if the tab is empty it coverts it to 0
            perc = 0
            held = 0
            pres = 0
        fin.setdefault(sub, [int(held),int(pres),float(perc)])
    print(fin)
    table(fin)

login()
subjects()
