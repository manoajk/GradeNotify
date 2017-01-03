from contextlib import closing
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from userinfo import username, password
import re

base_url = 'https://t-square.gatech.edu/portal'
login_site = 'https://login.gatech.edu/cas/login?service=https%3A%2F%2Ft-square.gatech.edu%2Fsakai-login-tool%2Fcontainer'
chrome_options = ChromeOptions()
chrome_options.add_argument("--incognito")

with closing(Chrome(chrome_options=chrome_options)) as browser:	
	browser.get(login_site)
	usrn = browser.find_element_by_id('username')
	usrn.clear()
	usrn.send_keys(username)
	pssw = browser.find_element_by_id('password')
	pssw.clear()
	pssw.send_keys(password)
	login = browser.find_element_by_name('submit')
	login.click()
	try:
		courseLinks = [link.get_attribute('href') for link in browser.find_elements_by_xpath('//ul[@id="siteLinkList"]/li/a')]
		del courseLinks[0]
		for courseLink in courseLinks:
			browser.get(courseLink)
			gradebookTab = browser.find_element_by_class_name('icon-sakai-gradebook-tool')
			gradebookTab.click()
			try:
				gradebookURL = re.search(base_url + '/tool.*panel=Main', browser.page_source).group(0)
				browser.get(gradebookURL)
				table = browser.find_element_by_css_selector('table.listHier')
				lookup = [el.text for el in table.find_elements_by_xpath('//thead/tr/th')]
				print(lookup)
				grades = [el.text for el in table.find_elements_by_xpath('//tbody/tr')]
				print("")
				for grade in grades:
					print(grade)
			except:
				print("Finished checking " + courseLink.text + "...")
				pass
		text = grades
	finally:
		browser.get(base_url)
		logout1 = browser.find_element_by_id('loginLink1')
		logout1.click()
		logout2 = browser.find_element_by_link_text('Logout of the Georgia Tech Login Service')
		logout2.click()
