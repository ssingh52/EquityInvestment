import requests
from bs4 import BeautifulSoup
import sys

def magic(number):
	return float(''.join(str(i) for i in number))
		
def beta_growth(company):
	
	argv = link(company)
	r = requests.get(argv)	
	
	soup = BeautifulSoup(r.content,"html.parser")
	table = soup.find('table', {'class': 'dataTable'})
	array1 = []	

	for row in table.findAll("tr"):
		array1.append(row.text)
		
	digits = []

	for arr in array1:
		if "Beta:" in arr:		
			for i in array1[0]:
				if i.isdigit() or i == ".":
					digits.append(i)
					
			break
			
	beta = magic(digits)
	print("Beta extracted:")
	print(beta)
	analystLink = argv.replace("overview","analyst")

	r = requests.get(analystLink)
	soup = BeautifulSoup(r.content,"html.parser")
	table = soup.find('table',{'class':'dataTable'})
	array = []
	for row in table.findAll("td"):
		array.append(row.text)
		break

	for val in array:
		print(array[0])	

	consensus_estimate = array[0]

	table_array = []
	table = soup.find("table",{"class":"dataTable"})
	for row in soup.findAll("table",{"class":"dataTable"}):
		table_array.append(row)
		
	rows_of_interest = []
	iter = 0
	start_row = 0
	for row in table_array[4].findAll("td"):
		iter = iter + 1
		if(row.text == "Earnings (per share)"):
			start_row = iter
			rows_of_interest.append(row.text)				
		
	iter = 0
	first_year_ending_row = 0
	second_year_ending_row = 0
	third_year_ending_row = 0
	first_year_ending = []
	second_year_ending = []
	third_year_ending = []
	index = 0
	for row in table_array[4].findAll("td"):
		iter = iter + 1
		if(iter >= start_row):
			if("Year Ending" in row.text):
				if(index == 0):
					first_year_ending_row = iter
					index = index + 1
				elif(index == 1):
					second_year_ending_row = iter
					index = index + 1
				elif(index == 2):
					third_year_ending_row = iter
					index = index + 1
		
	iter = 0	
	for row in table_array[4].findAll("td"):
		iter = iter + 1
		if(iter >= first_year_ending_row and iter < second_year_ending_row):
			first_year_ending.append(row.text)
		elif(iter >= second_year_ending_row and iter < third_year_ending_row):
			second_year_ending.append(row.text)
		elif(iter >= third_year_ending_row):
			third_year_ending.append(row.text)
				
	print("1st year estimates")
	print(first_year_ending)
	print("2nd year estimates")
	print(second_year_ending)
	print("3rd year estimates")	
	print(third_year_ending)

	growth1 = 0
	growth2 = 0
	try:
		present_eps = float(first_year_ending[1])
		year_1_eps = float(second_year_ending[1])
		year_2_eps = float(third_year_ending[1])

		growth1 = (year_1_eps-present_eps)/present_eps*100
		growth2 = (year_2_eps-year_1_eps)/year_1_eps*100

		print(round(growth1,1))
		print(round(growth2,1))
	except (ValueError,IndexError):
		growth1 = 0
		growth2 = 0
		print("Could not compute growth numbers")
	
	return [beta,consensus_estimate,growth1,growth2]

def link(company):
	
	if(company == "HINDZINC"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=HZNC.NS"
	elif(company == "FAGPRE"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=FAGB.BO"
	elif(company == "NESIND"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=NEST.NS"
	elif(company == "INFTEC"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=INFY.NS"
	elif(company == "HINLEV"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=HLL.NS"
	elif(company == "ASIPAI"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=ASPN.NS"
	elif(company == "GOONER"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=KANE.NS"
	elif(company == "PFIZER"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=PFIZ.NS"
	elif(company == "CERSAN"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=CERA.NS"
	elif(company == "ITC"):
		return  "http://in.reuters.com/finance/stocks/overview?symbol=ITC.NS"
	elif(company == "GRASIM"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=GRAS.NS"
	elif(company == "MINCON"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=MINT.NS"
	elif(company == "ECLERX"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=ECLE.NS"
	elif(company == "GRINOR"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=GRNN.NS"
	elif(company == "WELSPUNIND"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=WLSP.NS"
	elif(company == "TUBEINVEST"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=TUBE.NS"
	elif(company == "LUPIN"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=LUPN.NS"
	elif(company == "AIAENG"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=AIAE.NS"
	elif(company == "AMARAJ"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=AMAR.NS"
	elif(company == "TATAMOTORS"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=TAMO.NS"
	elif(company == "TATTIM"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=TIMK.NS"
	elif(company == "EQUITAS"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=EQHL.NS"
	elif(company == "EDELWEISS"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=EDEL.NS"
	elif(company == "AVANTIFEED"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=AVNT.NS"	
	elif(company == "VOLTAS"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=VOLT.NS"
	elif(company == "LT"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=LART.NS"
	elif(company == "MOTSUM"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=MOSS.NS"
	elif(company == "JBMA"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=JBMA.NS"
	elif(company == "HEXAWARE"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=HEXT.NS"
	elif(company == "HINSAN"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=HSNT.NS"
	elif(company == "HMVL"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=HINS.NS"
	elif(company == "POWERGRID"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=PGRD.NS"
	elif(company == "SUNPHA"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=SUN.NS"
	elif(company == "NEYVELILIG"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=NLCI.BO"
	elif(company == "SOLEXP"):
		return "http://in.reuters.com/finance/stocks/overview?symbol=SLIN.BO"
		
	
	
	
