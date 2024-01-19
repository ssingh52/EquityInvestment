from Ratios import *
from ReadCompanyData import *
from plotChart import *
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import FileIO as file
from CompanyCode import *
import numpy as np
import sys
import json
import urllib.request
import os
import time,datetime
from Bank_Analysis import *

def get_stock_quote(ticker_symbol):	
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

def append_pdf(input,output):
	[output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]
	
def temp(user_input):	
	
	grade = 0
	stockCode = user_input.upper()		
	readCompData = ReadCompanyFile(stockCode)		
	
	corporate = cc.company(stockCode)
	companyList.append(corporate)
	
	yearList = readCompData.year()	
	netProfitList = readCompData.netprofit()
	shares = readCompData.numofshares()
			
	epsList = []
	iter = 0
	for val in netProfitList:
		epsList.append(netProfitList[iter]/shares)				
		iter = iter + 1
				
	priceList = readCompData.shareprice()	
		
	priceGrowth = []
	nseGrowth = []
	iter = 0
		
	#Book Value		
	netWorthList = readCompData.shareHoldersFund()
			
	#Revenue Values
	revenueList = readCompData.revenues()		
	debtList = readCompData.debt()	
	ebit = readCompData.EBIT()
	interest = readCompData.interest()
		
	interestCoverage = []
	iter = 0
	for val in ebit:
		if(interest[iter] == 0.0):
			interestCoverage.append(0.0)
		else:
			interestCoverage.append(ebit[iter]/interest[iter])
		iter = iter + 1
		
	debtEquityRatio = []
	iter = 0
	for val in debtList:
		if(iter < len(netWorthList)):
			if(netWorthList[iter] == 0.0):
				debtEquityRatio.append(0.0)
			else:
				debtEquityRatio.append(val/netWorthList[iter])
		iter = iter + 1
	
	#Return on Equity
	iter = 0
	ROE = []	
	for val in netWorthList:
		if(iter < len(netWorthList)):
			if(netWorthList[iter] == 0.0):
				ROE.append(0.0)
			else:
				if(iter < len(netProfitList)):
					ROE.append(netProfitList[iter]/netWorthList[iter]*100.0)
				else:
					ROE.append(0.0)
		iter = iter + 1
	
	# Net worth / share holders fund on a quarterly basis
	present_shareHolders_fundList = readCompData.shareF_q()
	present_current_liabilitiesList = readCompData.currentL_q()
	present_assetsList = readCompData.assets_q()
	
	present_sf_fund = present_shareHolders_fundList[0]
	present_current_liabilities = present_current_liabilitiesList[0]
	present_asset = present_assetsList[0]
	
	present_ROE = netProfitList[len(netProfitList)-1]/present_sf_fund * 100.0
	
	#Return on Assets
	ROA = []
	iter = 0
	assets = readCompData.totalAssets()	
	for val in netProfitList:
		if(assets[iter] == 0.0):
			ROA.append(0.0)
		else:
			ROA.append(val/assets[iter]*100.0)
		iter = iter + 1
		
	present_ROA = netProfitList[len(netProfitList)-1]/present_asset * 100.0
		
	#Return on Capital Employed
	ROCE = []
	curLiabilities = readCompData.currentLiabilities()
	iter = 0
	for val in ebit:
		denom = assets[iter] - curLiabilities[iter]
		if(denom == 0.0):
			ROCE.append(0.0)
		else:
			ROCE.append(val/denom*100.0)
		iter = iter + 1	
	
	roce_list.append(ROCE[len(ROCE)-1])
	
	present_ROCE = ebit[len(ebit)-1]/(present_asset-present_current_liabilities) * 100.0
	
	pBV = []
	BV = []
	for val in netWorthList:
		BV.append(val/shares)
		
	iter = 0
	for val in BV:
		if(val != 0.0):
			if(iter < len(priceList)):
				pBV.append(priceList[iter]/val)
			else:
				pBV.append(0.0)
		else:
			pBV.append(0.0)
		iter = iter + 1
	
	topline_growth = []
	bottomline_growth = []
	
	Rf = 7.8 #Risk free rate
	Rm = 13 #Expected Return from the market (based on past data)
	Rd = 10.0 #lending rates	
	
	present_revenue = revenueList[len(revenueList)-1]
		
	op_cash_flow = readCompData.OCF()
	pcf_ratio = []
	iter = 0
    
	for val in priceList:
		pcf_ratio.append(val/(op_cash_flow[iter]/shares))
		iter = iter + 1
		
	free_cash_flow =  []
	capital_expenditure = readCompData.capex()
	iter = 0
	for val in op_cash_flow:
		fcf = val-capital_expenditure[iter]
		free_cash_flow.append(fcf)
		iter = iter + 1
	
	iter = 0
	
	cash = readCompData.liquidCash()
	minorityInterest = readCompData.mi()	
	debt_in_quarter = readCompData.debtQuarter()
	current_year_sales = readCompData.salesCY()
	previous_year_sales = readCompData.salesPY()
	current_year_profit = readCompData.salesCY_p()
	previous_year_profit = readCompData.salesPY_p()
	
	QoQ_growth = []
	QoQ_growth_profit = []
	sequential_sales_growth = []
	sequential_profit_growth = []
	margin = []
	iter = 0
	for val in current_year_sales:
		growth = val-previous_year_sales[iter]
		if(previous_year_sales[iter] != 0):
			QoQ_growth.append(growth/previous_year_sales[iter]*100)
		else:
			QoQ_growth.append(0)
			
		growth = current_year_profit[iter]-previous_year_profit[iter]
		if(previous_year_profit[iter] != 0):
			QoQ_growth_profit.append(growth/previous_year_profit[iter]*100)
		else:
			QoQ_growth_profit.append(0)
			
		if(val != 0.0):
			margin.append(current_year_profit[iter]/val*100)	
		else:
			margin.append(0.0)
			
		iter = iter + 1
		
	s1 = 0.0
	s2 = 0.0
	s3 = 0.0
	s4 = 0.0
	q1 = 0.0
	q2 = 0.0
	q3 = 0.0
	q4 = 0.0
	
	if(current_year_sales[3] != 0.0):
		s1 = (current_year_sales[0]-current_year_sales[3])/current_year_sales[3]*100.0
	if(current_year_sales[0] != 0.0):
		s2 = (current_year_sales[1]-current_year_sales[0])/current_year_sales[0]*100.0
	if(current_year_sales[1] != 0.0):
		s3 = (current_year_sales[2]-current_year_sales[1])/current_year_sales[1]*100.0
	if(current_year_sales[2] != 0.0):
		s4 = (current_year_sales[3]-current_year_sales[2])/current_year_sales[2]*100.0
	if(current_year_profit[3] != 0.0):
		q1 = (current_year_profit[0]-current_year_profit[3])/current_year_profit[3]*100.0
	if(current_year_profit[0] != 0.0):
		q2 = (current_year_profit[1]-current_year_profit[0])/current_year_profit[0]*100.0
	if(current_year_profit[1] != 0.0):
		q3 = (current_year_profit[2]-current_year_profit[1])/current_year_profit[1]*100.0
	if(current_year_profit[2] != 0.0):
		q4 = (current_year_profit[3]-current_year_profit[2])/current_year_profit[2]*100.0

	t1 = str(round(s1,1))+'~'+str(round(q1,1))
	t2 = str(round(s2,1))+'~'+str(round(q2,1))
	t3 = str(round(s3,1))+'~'+str(round(q3,1))
	t4 = str(round(s4,1))+'~'+str(round(q4,1))
	
	Q1Seq.append(t1)
	Q2Seq.append(t2)
	Q3Seq.append(t3)
	Q4Seq.append(t4)
	
	qoq = ''
	qoq = str(round(QoQ_growth[0],0))+' ~ '+str(round(QoQ_growth_profit[0],0))+'/'+str(round(margin[0],0))
	Q1QoQ.append(qoq)
	
	qoq = ''
	qoq = str(round(QoQ_growth[1],0))+' ~ '+str(round(QoQ_growth_profit[1],0))+'/'+str(round(margin[1],0))
	Q2QoQ.append(qoq)
	
	qoq = '' 
	qoq = str(round(QoQ_growth[2],0))+' ~ '+str(round(QoQ_growth_profit[2],0))+'/'+str(round(margin[2],0))
	Q3QoQ.append(qoq)
	
	qoq = '' 
	qoq = str(round(QoQ_growth[3],0))+' ~ '+str(round(QoQ_growth_profit[3],0))+'/'+str(round(margin[3],0))
	Q4QoQ.append(qoq)
	
	present_DE_Ratio = debt_in_quarter[0]/netWorthList[len(netWorthList)-1]
			
	if(corporate != 'stock not in database'):
		
		quote = ""		
		try:
			quote = get_stock_quote(cc.NSEStockCode(stockCode))								
			present_price = quote['l_fix'].replace('Rs.','')
			present_price = present_price.replace(',','')
			print(present_price)
			present_price = float(present_price)
			
		except urllib.error.URLError as e:
			print('\n')
			print(e.code)
			print('Current stock ',stockCode)
			present_price = input('Enter stock price :')
			present_price = float(present_price)
			
		market_cap.append(shares*present_price)
	
		enterpriseValue = shares*present_price + debt_in_quarter[0] + minorityInterest[0] - cash[0]
		free_cash_flow_yield.append((free_cash_flow[len(free_cash_flow)-1]/enterpriseValue)*100.0)
				
		debtFCFRatio.append(debt_in_quarter[0]/free_cash_flow[len(free_cash_flow)-1])
		
		price_bv_ratio.append(present_price/(present_sf_fund/shares))
		
		r = Ratios(priceList,epsList)
		peRatioRecomputed = r.peRatioList()
		epsGrowthRateRecomputed = r.epsGrowthRateList()
		
		title = corporate+'(stock price = '+ str(round(present_price,1))+' as on '+time.strftime("%d/%m/%Y")+')'
		print(title)
		print('---------------------------------------------------')			
		print('present stock price = '+ str(round(present_price,1)))			
		print('-----------------------------------------------------')
		print('Year','	','PE Ratio','	','EPS')
		present_price_list.append(round(present_price,1))
		iter = 0		
		for val in peRatioRecomputed:
			print(yearList[iter],'	',peRatioRecomputed[iter],'		',round(epsList[iter],1))
			iter = iter + 1
			
		current_PE = present_price/float(epsList[len(epsList)-1])
		current_pbv = 0.0
		if(BV[len(BV)-1] != 0.0):
			current_pbv = present_price/BV[len(BV)-1]
			
		meanPERatio = np.average(peRatioRecomputed)
		averagePE.append(meanPERatio)
		pe_variance.append(((current_PE-meanPERatio)/meanPERatio)*100.0)
			
		#PlotData(yearList,epsList,debtEquityRatio,revenueList,peRatioRecomputed,op_cash_flow,free_cash_flow,corporate,interestCoverage,ebit,current_PE,title,present_DE_Ratio)
		#PlotQuarterlyResult(corporate,previous_year_sales,current_year_sales,ROCE,yearList,pBV,ROE,current_pbv,QoQ_growth)
		
		peList.append(current_PE)				
				
		present_op_cash_flow = op_cash_flow[len(op_cash_flow) - 1]
		price_to_OCF = present_price/(present_op_cash_flow/shares)
		mean_price_ocf_ratio.append(np.average(pcf_ratio))
		price_cf_ratio_latest.append(price_to_OCF)
		
		if(current_pbv < (present_ROE/100.0)/100.0):
			sss = corporate + ' has P/BV less than ROE'
			print(sss)
		
		ocf1 = op_cash_flow[0]
		ocf2 = op_cash_flow[len(op_cash_flow)-1]
				
		if(ocf1 != 0.0):
			ocfGrowth = (((ocf2-ocf1)/abs(ocf1))*100)/len(op_cash_flow)
		else:
			ocfGrowth = 100.0
		ocfGrowthList.append(ocfGrowth)		
		
		eps1 = epsList[0]
		eps2 = epsList[len(epsList)-1]
				
		if(eps1 != 0.0):
			epsGrowth = (((eps2-eps1)/abs(eps1))*100)/len(epsList)
		else:
			epsGrowth = 100.0
		epsGrowthList.append(epsGrowth)		
		
		if(epsGrowth != 0.0):
			peg = abs(current_PE)/epsGrowth
		else:
			peg = 0.0
		pegRatio.append(peg)
		
		rev1 = revenueList[0]
		rev2 = revenueList[len(revenueList)-1]
		
		if(rev1 != 0.0):
			revGrowth = (((rev2-rev1)/abs(rev1))*100)/len(revenueList)
		else:
			revGrowth = 100.0		
				
		#PE Ratio - 1
		pe_grade = 0.0
		if(current_PE <= 12.0 and current_PE >= 0.0):
			pe_grade = pe_grade + 1
		elif(current_PE > 12.0 and current_PE <= 16.0):
			pe_grade = pe_grade + 0.8
		elif(current_PE > 16.0 and current_PE <= 20.0):
			pe_grade = pe_grade + 0.6
		elif(current_PE > 20.0 and current_PE <= 24.0):
			pe_grade = pe_grade + 0.3
			
		temp = ''
		temp = 'PE Grade : '
		temp = temp + str(pe_grade)
		print(temp)
			
		#indicates "Bottom Line" performance - 2
		bottomline_grade = 0.0
		if(ocfGrowth >= 0.0 and ocfGrowth <= Rf):
			bottomline_grade = 0.2
		elif(ocfGrowth > Rf and ocfGrowth <= Rm):
			bottomline_grade = 0.5
		elif(ocfGrowth > Rm):
			bottomline_grade = 1
			
		temp = ''
		temp = 'Bottom Line performance Grade : '
		temp = temp + str(bottomline_grade)
		print(temp)
		
		#indicates "Top Line" performance - 3
		topline_grade = 0.0
		if(revGrowth >= 0.0 and revGrowth <= Rf):
			topline_grade = 0.2
		elif(revGrowth > Rf and revGrowth <= Rm):
			topline_grade = 0.5
		elif(revGrowth > Rm):
			topline_grade = 1
		
		temp = ''
		temp = 'Top line performance grade : '
		temp = temp + str(topline_grade)
		print(temp)
		
		#interest coverage - 4
		interestCoverage_grade = 0.0
		if(interestCoverage[len(interestCoverage)-1] >= 5.0 or interestCoverage[len(interestCoverage)-1] == 0.0):
			interestCoverage_grade = 1
		elif(interestCoverage[len(interestCoverage)-1] >= 2.0 and interestCoverage[len(interestCoverage)-1] < 5.0):
			interestCoverage_grade = 0.5		

		temp = ''
		temp = 'Interest Coverage Grade : '
		temp = temp + str(interestCoverage_grade)
		print(temp)
		
		#improving interest coverage - 5
		improvingInterestCoverage_grade = 0.0
		if(interestCoverage[len(interestCoverage)-1] > interestCoverage[len(interestCoverage)-2]):
			improvingInterestCoverage_grade = 1
		elif(interestCoverage[len(interestCoverage)-1] == 0.0):
			improvingInterestCoverage_grade = 1
			
		temp = ''
		temp = 'Improving Interest Coverage grade : '
		temp = temp + str(improvingInterestCoverage_grade)
		print(temp)
			
		#debt equity ratio - 6
		debtEquity_grade = 0.0
		if(present_DE_Ratio >= 0.0 and present_DE_Ratio <= 0.1):
			debtEquity_grade = 1
		elif(present_DE_Ratio >= 0.1 and present_DE_Ratio <= 0.5):
			debtEquity_grade = 0.8			
		elif(present_DE_Ratio > 0.5 and present_DE_Ratio <= 1.0):
			debtEquity_grade = 0.6
		elif(present_DE_Ratio > 1.0 and present_DE_Ratio <= 1.5):
			debtEquity_grade = 0.4
		elif(present_DE_Ratio > 1.5 and present_DE_Ratio <= 2.0):
			debtEquity_grade = 0.2			
			
		temp = ''
		temp = 'Debt Equity grade : '
		temp = temp + str(debtEquity_grade)
		print(temp)
			
		#PEG ratio - 7
		peg_grade = 0.0
		if(peg <= 1.0 and peg > 0.7):
			peg_grade = 0.3
		elif(peg > 0.4 and peg <= 0.7):
			peg_grade = 0.6
		elif(peg > 0.1 and peg <= 0.4):
			peg_grade = 0.9
		elif(peg >=0.0 and peg <=0.1):
			peg_grade = 1
					
		temp = ''
		temp = 'PEG ratio grade : '
		temp = temp + str(peg_grade)
		print(temp)
					
		# price / operating cash flow - 8
		price_ocf_grade = 0.0
		if(price_to_OCF <= 12.0 and price_to_OCF >= 0.0):
			price_ocf_grade = 1
		elif(price_to_OCF > 12.0 and price_to_OCF <= 16.0):
			price_ocf_grade = 0.8
		elif(price_to_OCF > 16.0 and price_to_OCF <= 20.0):
			price_ocf_grade = 0.6
		elif(price_to_OCF > 20.0 and price_to_OCF <= 24.0):
			price_ocf_grade = 0.3				
		
		temp = ''
		temp = 'P/OCF grade : '
		temp = temp + str(price_ocf_grade)
		print(temp)		
		
		# ROCE - 9
		roceGrade = 0.0
		if(present_ROCE >= Rd and present_ROCE < 15.0):
			roceGrade = 0.5
		elif(present_ROCE >= 15.0):
			roceGrade = 1.0
		
		temp = ''
		temp = 'ROCE grade : '
		temp = temp + str(roceGrade)
		print(temp)		
		
		grade = price_ocf_grade + peg_grade + debtEquity_grade + improvingInterestCoverage_grade + interestCoverage_grade + topline_grade + bottomline_grade + pe_grade+roceGrade
							
		grade = grade/9.0*10.0
		gradeStr = 'Grade : '+str(round(grade,1))
		print(gradeStr)
		print('\n')
		gradeList.append(round(grade,1))

		#management effectiveness grades
		roeList.append(present_ROE)
		roaList.append(present_ROA)
		roceList.append(present_ROCE)
		
		mGrade = 0
		roceGrade = 0
		roceGrowthGrade = 0
		roaGrade = 0
		roeGrade = 0
		if(ROCE[len(ROCE)-1] > ROCE[len(ROCE)-2]):
			roceGrowthGrade = 1
					
		if(present_ROA >= 5.0):
			roaGrade = 1
			
		if(present_ROE >= 15.0):
			roeGrade = 1

		mGrade = roceGrowthGrade + roceGrade + roaGrade + roeGrade
		managementGrade.append(mGrade)
		present_grade = 0.0
		present_grade = price_ocf_grade + debtEquity_grade + interestCoverage_grade + pe_grade  + roceGrade + roaGrade + roeGrade
		present_grade = present_grade/7.0*10.0
		present_gradeList.append(present_grade)
		#if(all_stock == 'y'):
		# output = PdfFileWriter()
		# path = 'Companies/Report/'
		# fd = None
		# fn = path + corporate + '.pdf'
		# fd = file(fn,"rb")
		# append_pdf(PdfFileReader(fd),output)
		
		# fn1 = path + corporate+'_Q'+'.pdf'
		# fd1 = file(fn1,"rb")
		# append_pdf(PdfFileReader(fd1),output)
								
		# op = path + corporate+'_summary'+'.pdf'
		# output.write(file(op,"wb"))	
		# fd.close()
		# fd1.close()
		
		# os.remove(fn)
		# os.remove(fn1)
	else:
		print('stock not in database')
			
if __name__ == '__main__':	
			
	start_time = time.time()
	all_stock = input('Evaluate all companies in database?(y/n):')
	
	companyCodeList = []
	if(all_stock == 'y'):
		companyCodeList = ['hinlev','inftec','suzene','tattim','fagpre',
		'grinor','cersan','hinsan','solexp','sunpha','pfizer','motsum','voltas','asipai',
		'gooner','itc','mincon','amaraj','supind','avantifeed','welspunind',
		'lupin','eclerx','neyvelilig','lt','aiaeng','hindzinc','hcltech','tatamotors','hexaware',
		'edelweiss','powergrid','ashiana','grasim','jbma','hmvl','tubeinvest','equitas']	
	else:
		user_input = input('\nEnter Stock Code: ')
		companyCodeList.append(user_input)
	
	user_input = []	
	historicEPSList = []
	peList = []
	companyList = []
	ocfGrowthList = []
	epsGrowthList = []
	gradeList = []
	present_gradeList = []
	pegRatio = []
	present_price_list = []
	price_cf_ratio_latest = []
	price_bv_ratio = []
	free_cash_flow_yield = []
	roce_list = []
	managementGrade = []
	presentGrade_list = []
	mean_price_ocf_ratio = []
	roeList = []
	roaList = []
	roceList = []
	debtFCFRatio = []
	market_cap = []
	Q1QoQ = []
	Q2QoQ = []
	Q3QoQ = []
	Q4QoQ = []
	Q1Seq = []
	Q2Seq = []
	Q3Seq = []
	Q4Seq = []
	
	averagePE = []
	pe_variance = []
		
	cc = CompanyCode()	
	
	print('\n')
	for user_input in companyCodeList:	
		temp(user_input)
		
	sortedCompanyList = []
	sortedPEList = []
	sortedOCFGrowth = []
	sortedGradeList = []
	sortedPEGList = []
	sortedPresentPriceList = []
	sortedPCFList = []
	sortedPBVRatio = []
	sortedFCFYield = []
	sorted_roce_list = []
	sortedmanagementGrade = []
	sortedPresentGradeList = []
	sortedroeList = []
	sortedroaList = []
	sortedroceList = []
	sortedDebtFCFRatio = []
	sortedQ1QoQ = []
	sortedQ2QoQ = []
	sortedQ3QoQ = []
	sortedQ4QoQ = []
	sortedQ1Seq = []
	sortedQ2Seq = []
	sortedQ3Seq = []
	sortedQ4Seq = []	
	sortedmean_price_ocf_ratio = []
	sortedaveragePE = []
	sortedpe_variance = []
	sorted_market_cap = []
		
	temp = peList[:]
	
	while(len(sortedCompanyList) != len(peList)):
		val = min(temp)
		iter = 0
		for num in peList:
			if(num == val):
				sortedCompanyList.append(companyList[iter])
				sortedPEList.append(num)
				sortedOCFGrowth.append(ocfGrowthList[iter])
				sortedGradeList.append(gradeList[iter])
				sortedPEGList.append(pegRatio[iter])
				sortedPresentPriceList.append(present_price_list[iter])
				sortedPCFList.append(price_cf_ratio_latest[iter])
				sortedFCFYield.append(free_cash_flow_yield[iter])
				sortedPBVRatio.append(price_bv_ratio[iter])
				sorted_roce_list.append(roce_list[iter])
				sortedmanagementGrade.append(managementGrade[iter])
				sortedroeList.append(roeList[iter])
				sortedroaList.append(roaList[iter])
				sortedroceList.append(roceList[iter])
				sortedPresentGradeList.append(present_gradeList[iter])
				sortedDebtFCFRatio.append(debtFCFRatio[iter])
				sortedQ1QoQ.append(Q1QoQ[iter])
				sortedQ2QoQ.append(Q2QoQ[iter])
				sortedQ3QoQ.append(Q3QoQ[iter])
				sortedQ4QoQ.append(Q4QoQ[iter])
				sortedQ1Seq.append(Q1Seq[iter])
				sortedQ2Seq.append(Q2Seq[iter])
				sortedQ3Seq.append(Q3Seq[iter])
				sortedQ4Seq.append(Q4Seq[iter])
				sortedaveragePE.append(averagePE[iter])
				sortedpe_variance.append(pe_variance[iter])
				sortedmean_price_ocf_ratio.append(mean_price_ocf_ratio[iter])
				sorted_market_cap.append(market_cap[iter])
				
				temp.remove(val)
				break
			iter = iter + 1
	
	end_time = time.time()
	print('\nTime taken: ',round(end_time-start_time,0))
	
	path = os.getcwd()
	path = path + "/past_present_performance.txt"
	fo = open(path,"w")
	iter = 0
	fo.write('Company	PE	P/CF	PEG	OCF-G	ROCE	Grade(/10)	Q1-YoY	Q2-YoY	Q3-YoY	Q4-YoY	mean-PE	PE-Var	mean-PCF\n')
	for val in sortedCompanyList:
		temp = val+'	'+str(round(sortedPEList[iter],1))+'	'+str(round(sortedPCFList[iter],1))+'	'+str(round(sortedPEGList[iter],1))+'	'+str(round(sortedOCFGrowth[iter],1))+'	'+str(round(sorted_roce_list[iter],1))+'	'+str(sortedGradeList[iter])+'	'+sortedQ1QoQ[iter]+'	'+sortedQ2QoQ[iter]+'	'+sortedQ3QoQ[iter]+'	'+sortedQ4QoQ[iter]+'	'+str(round(sortedaveragePE[iter],1))+'	'+str(round(sortedpe_variance[iter],1))+'	'+str(round(sortedmean_price_ocf_ratio[iter],1))
		fo.write(temp)
		fo.write('\n')
		iter = iter + 1
		
	fo.close()
	
	path = os.getcwd()
	path = path + "/present_performance.txt"
	fo = open(path,"w")
	iter = 0
	fo.write('Company	PE	P/CF	P/BV	FCF-yield	Debt/FCF	current-ratings	ROE	ROA	ROCE	MR(/4)	Q1-Seq	Q2-Seq	Q3-Seq	Q4-Seq\n')
	for val in sortedCompanyList:
		temp = val +'	'+str(round(sortedPEList[iter],1))+'	'+str(round(sortedPCFList[iter],1))+'	'+str(round(sortedPBVRatio[iter],1))+'	'+str(round(sortedFCFYield[iter],1))+'	'+str(round(sortedDebtFCFRatio[iter],1))+'	'+str(sortedPresentGradeList[iter])+'	'+str(round(sortedroeList[iter],1))+'	'+str(round(sortedroaList[iter],1))+'	'+str(round(sortedroceList[iter],1))+'	'+str(sortedmanagementGrade[iter])+'	'+sortedQ1Seq[iter]+'	'+sortedQ2Seq[iter]+'	'+sortedQ3Seq[iter]+'	'+sortedQ4Seq[iter]
		fo.write(temp)
		fo.write('\n')
		iter = iter + 1
		
	fo.close()
	
	path = os.getcwd()
	path = path + "/Portfolio" + "/market_cap.txt"
	fo = open(path,"w")
	iter = 0
	fo.write('Company,Market-cap\n')
	for val in sortedCompanyList:
		temp = val +','+str(round(sorted_market_cap[iter],1))
		fo.write(temp)
		fo.write('\n')
		iter = iter + 1				
	
	fo.close()
	
	print('Meet all the parameters below before buying a stock')
	print('\n 1. Identify stocks with good topline and bottomline quarterly growths (both good - must for top line)')
	print('2. Ideally, Invest in stocks with high grades')
	print('3. Identify stocks with high free cash flow yield (> 4%)')
	print('4. Invest in stock with current PE ratio close to historic PE ratios')
	print('5. Check debt / free cash flow ratio')
	print('6. If Point 3 & 4 is not met, still okay, but has to be positive')