#get faceit queue data

from requests import Session
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import sql_test as sql

db_path = r"D:\Daily Shit\Programming\UTD Bot\users.db"


options = webdriver.ChromeOptions()
options.add_argument('user-data-dir=C:\\Users\\Tony\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1')
options.add_argument('profile-directory=Profile 1')
browser = webdriver.Chrome(executable_path="./resources/chromedriver.exe", chrome_options=options)


def faceit_login():
	with Session() as s:
		site = s.get("https://www.faceit.com/en/login")
		soup = bs(site.content, 'html.parser')
		print(soup.prettify())

		

		s.post("https://www.faceit.com/en/login", login_data)
		dashboard = s.get("https://www.faceit.com/en/dashboard")
		print(dashboard.content)
		exit()

def sel_login():
	

	browser.get("https://www.faceit.com/en/hub/860cace2-43ef-490d-ab72-ca4c760d959c/Ten%20Mans%20-%20Hosted%20by%20UTD")


	

	hub_page = "https://www.faceit.com/en/hub/860cace2-43ef-490d-ab72-ca4c760d959c/Ten%20Mans%20-%20Hosted%20by%20UTD"
	

	while True:
		print('Proceed to UTD 10man hub.')
		input('Press enter to continue...')

		curr_page = browser.current_url

		if(curr_page == hub_page):
			break
		else:
			print('Error: Not at hub page')

	print('Connected to hub')


def queue_data():
	print("The number of people queuing is:")
	#print(browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div/div/fi-navbar/div/div[2]/fi-navbar-actions/queuing-counter/div/div[6]/span').text)

	#num_in_q = int(browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div/div/fi-navbar/div/div[2]/fi-navbar-actions/queuing-counter/div/div[6]/span').text)
	num_in_q = int(browser.find_element_by_css_selector('span[ng-bind="vm.totalCount | thousandSuffix"]').text)
	return num_in_q
#Returns a list of the members in the queue
def members_in_queue():
	builder = ActionChains(browser)
	member_list = []

	#Simulates a mouse hover over the queue number to retrieve the list of players
	counter = browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div/div/fi-navbar/div/div[2]/fi-navbar-actions/queuing-counter/div/div[6]/span')
	builder.move_to_element(counter).perform()
	#Seperates the members in a list of elements that contains the skill level and the name
	try:
		wait = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[2]/div/div/div/ng-transclude/ul')))
	except:
		return member_list
	data = browser.find_element_by_xpath('/html/body/div[8]/div[2]/div/div/div/ng-transclude/ul')
	members = data.find_elements_by_tag_name('li')

	

	for value in members:
		#Split the skill level and name
		msg = value.text
		split = msg.split('\n', 1)
		skill_level = split[0].split(' ', 2)
		skill_number = skill_level[2]

		name = split[1]

		#store values in a list of dicts

		user = {
			"username": name,
			"skill": skill_number

		}

		member_list.append(user)

	return member_list

def shiloh_pic():
	photos = [
	"D:\\Daily Shit\\Programming\\UTD Bot\\photos\\derpy.jpg",
	"D:\\Daily Shit\\Programming\\UTD Bot\\photos\\good_boye.png",
	"D:\\Daily Shit\\Programming\\UTD Bot\\photos\\sleepy.jpg",
	"D:\\Daily Shit\\Programming\\UTD Bot\\photos\\smily.png",
	"D:\\Daily Shit\\Programming\\UTD Bot\\photos\\togo.MP4",
	"D:\\Daily Shit\\Programming\\UTD Bot\\photos\\wut.png"
	]

	return random.choice(photos)
#Team A and team B provice a list of faceit names
def place_teams(teamA, teamB):
	conn = sql.create_connection(db_path)
	cur = conn.cursor()
#TODO, place players in correct voice channel
	for player in teamA:
		#returns discord ID matched with faceit account
		discord_username = sql.get_discord(conn, player)
		




	
	
	

	

	

