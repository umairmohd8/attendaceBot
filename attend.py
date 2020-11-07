from selenium import webdriver
import vars
browser = webdriver.Firefox()
browser.get('https://campus.uno/Student/Attendance')

user = browser.find_element_by_id('LoginId')
password = browser.find_element_by_id('Password')
login = browser.find_element_by_css_selector('#intro > div > div > div:nth-child(2) > section > footer > button')

user.send_keys(vars.username)
password.send_keys(vars.passw)
login.click()   #logs into my account

browser.implicitly_wait(30)



def subjects():                #
    loo = '//*[@id="div-data-display"]/table/tbody/tr[{row}]/'     #xpath of table rows
    subs = ['a','b','DSA','ADE','CO','SE','DMS','ADEL','DSAL','MATH']
    fin = {}   #dict for subs n percentage
    classes = {}    #dict of classes held vs attended
    for i in range(2,10):
        sub = subs[i]
        perc = browser.find_element_by_xpath(loo.format(row = i) + "td[6]").text
        held = browser.find_element_by_xpath(loo.format(row = i) + "td[4]").text
        pres = browser.find_element_by_xpath(loo.format(row = i) + "td[5]").text
        if held == '':   #if the tab is empty it coverts it to 0
            perc = 0
            held = 0
            pres = 0
        fin.setdefault(sub, float(perc))
        classes.setdefault(int(held),int(pres))
    print(fin)
    print(classes)
subjects()

#//*[@id="div-data-display"]/table/tbody/tr[2]/td[4]
#//*[@id="div-data-display"]/table/tbody/tr[2]/td[5]