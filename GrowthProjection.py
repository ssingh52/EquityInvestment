from ReadCompanyData import *
from CompanyCode import *
import sys
import json
import urllib.request
import os
import shutil
from reuters_dcf import beta_growth
import win32com.client
from Ratios import *

def get_stock_quote(ticker_symbol):
	#print(ticker_symbol)
	url = 'http://finance.google.com/finance/info?q={}'.format(ticker_symbol) 
	lines = ""
	try:
		lines = urllib.request.urlopen(url).readlines() 
	except urllib.error.URLError as e:
		e.code = 'No Internet Connection'
		raise e
		
	lines_string = [x.decode('utf-8').strip('\n') for x in lines] 
	merged = ''.join([x for x in lines_string if x not in ('// [', ']')]) 
	return json.loads(merged) 
	
def dcf_analysis(share_price,stock,retention_per):

	#risk free rate
	rf = 0.0742
	#growth in perpetuity
	perpetuity_growth = 0.065
	#borrowing rate
	borrowing_rate = 0.10
	#equity risk premium
	risk_premium = 0.07
	#tax rate
	tax_rate = 0.28
	
	intrinsic_value = 0.0
	exit_multiple = 0.0
	equity_cost = 0.0
	debt_cost = 0.0
	wacc = 0.0
	#copy template to DCF folder and renaming
	path = os.getcwd()
	src_dir = path + '/Templates'
	dst_dir = path + '/DCF'
	src_file = src_dir + '/DCF_Calculator_10years.xlsm'
	dst_file = dst_dir + '/DCF_Calculator_10years.xlsm'
	dst_file_name = path + '/DCF' + '/' + stock + '.xlsm'
	
	if(os.path.exists(dst_file_name) == True):
		os.remove(dst_file_name)
	
	shutil.copy(src_file,dst_dir)
	os.rename(dst_file,dst_file_name)
	
	readCompData = ReadCompanyFile(stock)
	
	try:
		list = beta_growth(stock)
	except ValueError:
		list = [1.0,perpetuity_growth*100,perpetuity_growth*100,perpetuity_growth*100]
		pass
		
	print("List")
	print(list)	
	beta = list[0]
	consensus_recommendation.append(list[1])
	growthList = readCompData.Growth()
	revList = readCompData.revenues()
	ebitList = readCompData.EBIT()
	ocfList = readCompData.OCF()
	interestList = readCompData.interest()
	capexList = readCompData.capex()
	shares = readCompData.numofshares()
	debt = readCompData.debtQuarter()
		
	#Run excel goal seek code
	xl=win32com.client.Dispatch("Excel.Application")
	xl.Visible = False	
	wb = xl.Workbooks.Open(Filename=dst_file_name)
	ws = wb.Worksheets(1)
	growthList.insert(0,list[2])
	growthList.insert(1,list[3])
	col = 3
	for val in growthList:
		ws.Cells(12, col).Value = val/100
		col = col + 1
	ws.Cells(1,8).Value = share_price
	
	ws.Cells(10,15).Value = beta
	ws.Cells(4,2).Value = revList[len(revList)-1]
	ws.Cells(5,2).Value = ebitList[len(revList)-1]
	
	#unlevered operating cash flow
	ws.Cells(8,2).Value = ocfList[len(ocfList)-1]+interestList[len(interestList)-1]	
	ws.Cells(9,2).Value = capexList[len(capexList)-1]
	
	ws.Cells(19,2).Value = shares
	ws.Cells(5,15).Value = debt
	ws.Cells(17,2).Value = perpetuity_growth
	ws.Cells(3,15).Value = rf
	ws.Cells(12,15).Value = risk_premium
	ws.Cells(12,15).Value = borrowing_rate
	ws.Cells(13,15).Value = tax_rate
	#ws.Cells(16,2).Value = retention_per
	ws.Cells(16,2).Value = 1.0
	
	xl.Application.Run("GoalSeek")
	
	intrinsic_value = ws.Cells(22,2).Value
	exit_multiple = ws.Cells(18,7).Value
	equity_cost = ws.Cells(11,15).Value
	debt_cost = ws.Cells(14,15).Value
	wacc = ws.Cells(15,15).Value
	ev = ws.Cells(21,2).Value
	wb.Close(SaveChanges=1)
	xl.Application.Quit()	
	
	return (intrinsic_value, exit_multiple, equity_cost, debt_cost, wacc, ev)
	
def temp(user_input):
	stockCode = user_input.upper()		
	readCompData = ReadCompanyFile(stockCode)	
	corporate = cc.company(stockCode)
	company.append(corporate)
		
	shares = readCompData.numofshares()
	netWorth = readCompData.shareF_q()
	shareHoldersFundList = readCompData.shareHoldersFund()	
	Revenues = readCompData.revenues()
	presentRevenue = Revenues[len(Revenues)-1]
	ocfList = readCompData.OCF()
	presentOCF = ocfList[len(ocfList)-1]
	capexList = readCompData.capex()
	presentCapex = capexList[len(capexList)-1]
	
	fcf = presentOCF - presentCapex
	free_cash_revenue_ratio.append(fcf/presentRevenue*100)
	
	print("\n")
	print(corporate)
	print("---------------------------------")	
	
	iter = 0
	ocfList = readCompData.OCF()
	capexList = readCompData.capex()
	dividendList = readCompData.dividends()
	interestList = readCompData.interest()
	
	print("Free_cash/Revenue ratio")
	print(fcf/presentRevenue*100)
	
	print("Past Operating Cash flow")
	print(ocfList)
	print("Past Growth in Free Cash flow")
	fcfList = []
	
	iter = 0
	#unlevered free cash flow list
	for val in ocfList:
		#fcfList.append(val-capexList[iter]-dividendList[iter]+interestList[iter])
		fcfList.append(val-capexList[iter]+interestList[iter])
		iter = iter + 1
		
	print(fcfList)
	iter = 0
	for val in fcfList:
		if(val == 0):
			iter = iter + 1
			continue
		if(iter < len(fcfList)-1):
			t1 = fcfList[iter+1]
			print(round(((t1-val)/val)*100,1))
		iter = iter+1
	
	op_cash_flow = readCompData.OCF()
	
	rr = (op_cash_flow[len(op_cash_flow)-1]-dividendList[len(op_cash_flow)-1])/op_cash_flow[len(op_cash_flow)-1]
	retention_rate.append(rr)
			
	if(corporate != 'stock not in database'):
		
		quote = ""
		
		try:
			quote = get_stock_quote(cc.NSEStockCode(stockCode))				
			present_price = quote['l_fix'].replace('Rs.','')
			present_price = present_price.replace(',','')
			present_price = float(present_price)			
		except urllib.error.URLError as e:
			print('\n')
			print(e.code)
			print('Current stock ',stockCode)
			present_price = input('Enter stock price :')
			present_price = float(present_price)
		
		#rate of return assumed / expected		
		print("Present Stock price")
		print(present_price)
		pbv = present_price/(netWorth[0]/shares)
		pFCF = "Present price to Free Cash : " + str(round(present_price/fcfList[len(fcfList)-1]))
		print(pFCF)
		#holding period in years
		intrinsic_value, exit_multiple, cost_of_equity, cost_of_debt, WACC, enterpriseVal = dcf_analysis(present_price, stockCode, rr)
		
		ebv = present_price/(enterpriseVal/shares)
			
		intrinsicValue = 'Intrinsic Value as per Gordon Growth Model : '+str(round(intrinsic_value,0))
		nw = 'Present book value : '+str(round(pbv,1))
		enw = 'Estimated book value : '+str(round(ebv,1))
		retention = 'Retention rate : '+str(round(rr,2))
		exitMultiple = 'Exit Multiple as per Exit Multiple Method : '+str(round(exit_multiple,1))		
		costOfCapital = 'Total Weighted Average Cost of Capital : '+str(round(WACC*100,1))
		
		share_price.append(present_price)
		present_bookValue.append(pbv)
		estimated_bookValue.append(ebv)
		intrinsic_value_val.append(intrinsic_value)
		exit_multiple_val.append(exit_multiple)
		cost_of_equity_val.append(cost_of_equity*100)
		cost_of_debt_val.append(cost_of_debt*100)
		cost_of_capital_val.append(WACC*100)
		
		asset = readCompData.assets_q()
		cl = readCompData.currentL_q()
		ebitList = readCompData.EBIT()
		ebit = ebitList[len(ebitList)-1]
		
		computed_growth.append(rr*ebit/(asset[0]-cl[0])*100)
		print(intrinsicValue)
		print(nw)
		print(enw)
		print(retention)
		print(exitMultiple)		
		print(costOfCapital)
		
if __name__ == '__main__':

	companyCodeList = []
	company = []
	all_stock = input('Evaluate all companies in database?(y/n):')
	if(all_stock == 'y'):
		# companyCodeList = ['goodyear','hinlev','godcon','inftec','suzene','tattim','fagpre','skfbea','briind','colpal','pidind','strarc',
		# 'grinor','cersan','hinsan','solexp','sunpha','pfizer','motsum','emami','acc','smibc','voltas','cumind','tattea','progam','asipai','iciind',
		# 'gooner','itc','mincon','amaraj','dabind','nesind','supind','avantifeed','ambujacem','concor','hgs','welspunind',
		# 'lupin','balmlawrie','eclerx','neyvelilig','nationalum','lt','ofss','aiaeng','hindzinc','gujfluoro','ntpc',
		# 'hcltech','tatamotors','tatachem','hexaware','siemens','bhartiartl','powergrid','piind','3mindia','upl']	
		companyCodeList = ['fagpre','inftec','hindzinc','hinlev','asipai','gooner','pfizer','cersan','itc','grasim','mincon','eclerx',
		'grinor','welspunind','tubeinvest','lupin','amaraj','tatamotors','aiaeng','tattim','equitas','edelweiss','avantifeed','voltas',
		'lt','motsum','jbma','hexaware','hinsan','hmvl','powergrid','sunpha','neyvelilig','solexp']		
	else:
		user_input = input('\nEnter Stock Code: ')
		companyCodeList.append(user_input)
	
	share_price = []
	retention_rate = []
	intrinsic_value_val = []
	exit_multiple_val = []
	cost_of_equity_val = []
	cost_of_debt_val = []
	cost_of_capital_val = []
	present_bookValue = []
	estimated_bookValue = []	
	free_cash_revenue_ratio = []
	computed_growth = []
	consensus_recommendation = []
	
	cc = CompanyCode()	
	
	print('\n')
	for user_input in companyCodeList:	
		temp(user_input)
		
	path = os.getcwd()
	path = path + "/future_performance.txt"
	fo = open(path,"w")
	iter = 0
	fo.write('Company	share_price	P/BV	P/eBV	Retention-Rate	Intrinsic-value	exit-multiple	equity-cost	debt-cost	cost_of_capital	free_cash/revenue	Computed-Growth	Recommendation	Rating	%Gap\n')
	for val in company:
		try:
			temp = val+'	'+str(round(share_price[iter],0))+'	'+str(round(present_bookValue[iter],1))+'	'+str(round(estimated_bookValue[iter],1))+'	'+str(round(retention_rate[iter],2))+'	'+str(round(intrinsic_value_val[iter],1))+'	'+str(round(exit_multiple_val[iter],1))+'	'+str(round(cost_of_equity_val[iter],1))+'	'+str(round(cost_of_debt_val[iter],1))+'	'+str(round(cost_of_capital_val[iter],1))+'	'+str(round(free_cash_revenue_ratio[iter],1))+'	'+str(round(computed_growth[iter],1))+'	'+consensus_recommendation[iter]
		except TypeError:
			print("***********")
			print(round(share_price[iter],0))
			print(round(retention_rate[iter],2))
			print(round(computed_growth[iter],1))
			print(consensus_recommendation[iter])
			temp = val+'	'+str(round(share_price[iter],0))+'	'+'-'+'	'+'-'+'	'+str(round(retention_rate[iter],2))+'	'+'-'+'	'+'-'+'	'+'-'+'	'+'-'+'	'+'-'+'	'+str(round(free_cash_revenue_ratio[iter],1))+'	'+str(round(computed_growth[iter],1))+'	'+'-'
		fo.write(temp)
		fo.write('\n')
		iter = iter + 1
		
	fo.close()
	