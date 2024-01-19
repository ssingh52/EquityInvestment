#code to read companies history

class ReadCompanyFile:
	def __init__(self,company):
		text = "Companies"
		filename = text+("/")+company+".txt"
		with open(filename,"r") as ins:
			array = []
			for line in ins:
				array.append(line)

		self.Year = []
		self.Revenues = []
		self.NetProfit = []
		self.OutstandingNumOfShares = []
		self.shareFund = []
		self.Price = []
		self.ebit = []
		self.int = []
		self.totalDebt = []				
		self.opCF = []
		self.capE = []
		self.liquidAssets = []
		self.minorInt = []
		self.assets = []
		self.liabilities = []
		self.debtQ = []
		self.py = []
		self.cy = []
		self.py_p = []
		self.cy_p = []
		self.sf_q = []
		self.cl_q = []
		self.ta_q = []
		self.dividend = []
		self.beta = []
		self.growth = []
		for val in array:
			list = val.split(",")
			if(list[0] == 'Y'):
				for i in range(len(list)-1):
					self.Year.append(int(list[i+1]))
			elif(list[0] == 'R'):
				for i in range(len(list)-1):
					self.Revenues.append(float(list[i+1]))
			elif(list[0] == 'NP'):
				for i in range(len(list)-1):
					self.NetProfit.append(float(list[i+1]))
			elif(list[0] == 'S'):
				for i in range(len(list)-1):
					self.OutstandingNumOfShares.append(float(list[i+1]))
			elif(list[0] == 'SF'):
				for i in range(len(list)-1):
					self.shareFund.append(float(list[i+1]))
			elif(list[0] == 'P'):
				for i in range(len(list)-1):
					self.Price.append(float(list[i+1]))
			elif(list[0] == 'EBIT'):
				for i in range(len(list)-1):
					self.ebit.append(float(list[i+1]))
			elif(list[0] == 'I'):
				for i in range(len(list)-1):
					self.int.append(float(list[i+1]))
			elif(list[0] == 'Debt'):
				for i in range(len(list)-1):
					self.totalDebt.append(float(list[i+1]))			
			elif(list[0] == 'OCF'):
				for i in range(len(list)-1):
					self.opCF.append(float(list[i+1]))
			elif(list[0] == 'capital_ex'):
				for i in range(len(list)-1):
					self.capE.append(float(list[i+1]))
			elif(list[0] == 'cash'):
				for i in range(len(list)-1):
					self.liquidAssets.append(float(list[i+1]))
			elif(list[0] == 'mi'):
				for i in range(len(list)-1):
					self.minorInt.append(float(list[i+1]))
			elif(list[0] == 'TA'):
				for i in range(len(list)-1):
					self.assets.append(float(list[i+1]))
			elif(list[0] == 'CL'):
				for i in range(len(list)-1):
					self.liabilities.append(float(list[i+1]))
			elif(list[0] == 'debt_q'):
				for i in range(len(list)-1):
					self.debtQ.append(float(list[i+1]))
			elif(list[0] == 'PY_S'):
				for i in range(len(list)-1):
					self.py.append(float(list[i+1]))					
			elif(list[0] == 'CY_S'):
				for i in range(len(list)-1):
					self.cy.append(float(list[i+1]))
			elif(list[0] == 'PY_P'):
				for i in range(len(list)-1):
					self.py_p.append(float(list[i+1]))					
			elif(list[0] == 'CY_P'):
				for i in range(len(list)-1):
					self.cy_p.append(float(list[i+1]))
			elif(list[0] == 'SF_q'):
				for i in range(len(list)-1):
					self.sf_q.append(float(list[i+1]))		
			elif(list[0] == 'CL_q'):
				for i in range(len(list)-1):
					self.cl_q.append(float(list[i+1]))		
			elif(list[0] == 'TA_q'):
				for i in range(len(list)-1):
					self.ta_q.append(float(list[i+1]))		
			elif(list[0] == 'D'):
				for i in range(len(list)-1):
					self.dividend.append(float(list[i+1]))
			elif(list[0] == 'beta'):
				for i in range(len(list)-1):
					self.beta.append(list[i+1])
			elif(list[0] == 'growth'):
				for i in range(len(list)-1):
					self.growth.append(float(list[i+1]))
											
	def year(self):
		return self.Year
	def revenues(self):
		return self.Revenues
	def netprofit(self):
		return self.NetProfit
	def numofshares(self):
		return self.OutstandingNumOfShares[0]
	def shareHoldersFund(self):
		return self.shareFund
	def shareprice(self):
		return self.Price
	def EBIT(self):
		return self.ebit
	def interest(self):
		return self.int
	def debt(self):
		return self.totalDebt
	def OCF(self):
		return self.opCF
	def capex(self):
		return self.capE
	def liquidCash(self):
		return self.liquidAssets
	def mi(self):
		return self.minorInt
	def totalAssets(self):
		return self.assets
	def currentLiabilities(self):
		return self.liabilities
	def debtQuarter(self):
		return self.debtQ
	def salesCY(self):
		return self.cy
	def salesPY(self):
		return self.py
	def salesCY_p(self):
		return self.cy_p
	def salesPY_p(self):
		return self.py_p	
	def shareF_q(self):
		return self.sf_q
	def currentL_q(self):
		return self.cl_q
	def assets_q(self):
		return self.ta_q
	def dividends(self):
		return self.dividend
	def Beta(self):
		return self.beta
	def Growth(self):
		return self.growth
		
			