import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as pltticker
from matplotlib.gridspec import GridSpec
import time
class PlotData:
	def __init__(self,yearList,eps,debtEquityRatio,revenues,per,op_cash_flow,free_cash_flow,company,ic,ebit,presentPE,title,presentDE):
		
		year = yearList
				
		fig,Ax = plt.subplots(2,3,figsize=(10,10),sharex=False,sharey=False)
		
		fig.subplots_adjust(hspace=1.0)
		self.plotEPS(fig,Ax[0,0],eps,year)	
		self.plotDebtRatios(fig,Ax[0,1],debtEquityRatio,presentDE,year)		
		self.plotIC(fig,Ax[0,2],ic,year)
		self.plotRevenues(fig,Ax[1,0],revenues,ebit,year)
		self.plotRatios(fig,Ax[1,1],per,presentPE,year)		
		self.plotCashFlow(fig,Ax[1,2],op_cash_flow,free_cash_flow,year)
				
		Ax[0,0].get_xaxis().get_major_formatter().set_useOffset(False)
		Ax[0,1].get_xaxis().get_major_formatter().set_useOffset(False)
		Ax[0,2].get_xaxis().get_major_formatter().set_useOffset(False)
		Ax[1,0].get_xaxis().get_major_formatter().set_useOffset(False)
		Ax[1,1].get_xaxis().get_major_formatter().set_useOffset(False)		
		Ax[1,2].get_xaxis().get_major_formatter().set_useOffset(False)		
				
		Ax[0,0].tick_params(labelsize=10)
		Ax[0,1].tick_params(labelsize=10)
		Ax[0,2].tick_params(labelsize=10)
		Ax[1,0].tick_params(labelsize=10)
		Ax[1,1].tick_params(labelsize=10)
		Ax[1,2].tick_params(labelsize=10)
				
		plt.setp(Ax[0,0].xaxis.get_majorticklabels(),visible=True)
		plt.setp(Ax[0,1].xaxis.get_majorticklabels(),visible=True)
		plt.setp(Ax[0,2].xaxis.get_majorticklabels(),visible=True)
		plt.setp(Ax[1,0].xaxis.get_majorticklabels(),visible=True)
		plt.setp(Ax[1,1].xaxis.get_majorticklabels(),visible=True)		
		plt.setp(Ax[1,2].xaxis.get_majorticklabels(),visible=True)	
				
		plt.setp(Ax[0,0].xaxis.get_majorticklabels(),rotation=45)
		plt.setp(Ax[0,1].xaxis.get_majorticklabels(),rotation=45)
		plt.setp(Ax[0,2].xaxis.get_majorticklabels(),rotation=45)
		plt.setp(Ax[1,0].xaxis.get_majorticklabels(),rotation=45)
		plt.setp(Ax[1,1].xaxis.get_majorticklabels(),rotation=45)		
		plt.setp(Ax[1,2].xaxis.get_majorticklabels(),rotation=45)
				
		fig.suptitle(title)
		fn = company + '.pdf'
		path = 'Companies/Report/'+fn
		plt.savefig(path)
		plt.close()
				
	def __del__(self):
		class_name = self.__class__.__name__
		#print(class_name," destroyed")
	
	def plotIC(self,fig,IC,ic,year):
		width = 0.2		
		diff = len(year)-len(ic)
		
		if(diff != 0):
			for iter in range(0,diff):
				ic.append(0.0)
		
		bvRect = IC.bar(year,ic,width,align='center')
		IC.yaxis.grid(color='gray',linestyle='dashed')
		
		loc = pltticker.MultipleLocator(base=1.0)
		IC.xaxis.set_major_locator(loc)
		fig.autofmt_xdate()
		IC.set_xlabel('Year',fontsize=10,fontweight='bold')
		IC.set_title('Interest Cover',fontsize = 12)
		
	def plotEPS(self,fig,Eps,eps,year):
		width = 0.2
		diff = len(year)-len(eps)
		if(diff != 0):
			for iter in range(0,diff):
				eps.append(0.0)
				
		epsRect = Eps.bar(year,eps,width,align='center')
		Eps.yaxis.grid(color='gray',linestyle='dashed')		
		loc = pltticker.MultipleLocator(base=1.0)
		Eps.xaxis.set_major_locator(loc)
		fig.autofmt_xdate()
		Eps.set_xlabel('Year',fontsize=10,fontweight='bold')
		Eps.set_title('EPS',fontsize = 12)		
		
	def plotDebtRatios(self,fig,Price,debtEquityRatio,pderatio,year):
		width = 0.2
		diff = len(year)-len(debtEquityRatio)
		if(diff != 0):
			for iter in range(0,diff):
				debtEquityRatio.append(0.0)
				
		presentYear = year[len(year)-1]
		priceRect = Price.bar(year,debtEquityRatio,width,align='center')
		presentDERect = Price.bar(presentYear,pderatio,width,color='r')
		Price.yaxis.grid(color='gray',linestyle='dashed')
		loc = pltticker.MultipleLocator(base=1.0)
		Price.xaxis.set_major_locator(loc)		
		Price.yaxis.grid(color='gray',linestyle='dashed')
		loc = pltticker.MultipleLocator(base=1.0)
		Price.xaxis.set_major_locator(loc)
		fig.autofmt_xdate()
		Price.set_xlabel('Year',fontsize=10,fontweight='bold')
		Price.set_title('Debt/Equity',fontsize = 12)		
		Price.legend((priceRect,presentDERect),('historic','present'),fontsize=7,loc='upper left')		
	
	def plotCashFlow(self,fig,IR,ocf,fcf,year):
		width = 0.2
			
		diff = len(year)-len(ocf)
		if(diff != 0):
			for iter in range(0,diff):
				ocf.append(0.0)		

		diff = len(year)-len(fcf)
		if(diff != 0):
			for iter in range(0,diff):
				fcf.append(0.0)
		
		irRect = IR.bar(year,ocf,width,align='center')		
		fcRect = IR.bar(year,fcf,width,color='r')
		IR.yaxis.grid(color='gray',linestyle='dashed')
		loc = pltticker.MultipleLocator(base=1.0)
		IR.xaxis.set_major_locator(loc)
		fig.autofmt_xdate()
		IR.set_xlabel('Year',fontsize=10,fontweight='bold')
		IR.set_title('Cash Flow',fontsize = 12)		
		IR.legend((irRect,fcRect),('Op.Cash','fr.Cash'),fontsize=7,loc='upper left')		
		
	def plotRevenues(self,fig,Revenue,revenues,ebit,year):
		width = 0.2
		diff = len(year)-len(revenues)
		if(diff != 0):
			for iter in range(0,diff):
				revenues.append(0.0)
		
		diff = len(year)-len(ebit)
		if(diff != 0):
			for iter in range(0,diff):
				ebit.append(0.0)
		
		revRect = Revenue.bar(year,revenues,width,align='center')
		ebitRect = Revenue.bar(year,ebit,width,color='r')
		Revenue.yaxis.grid(color='gray',linestyle='dashed')
		loc = pltticker.MultipleLocator(base=1.0)
		Revenue.xaxis.set_major_locator(loc)
		fig.autofmt_xdate()
		Revenue.set_xlabel('Year',fontsize=10,fontweight='bold')
		Revenue.set_title('Revenue & EBIT',fontsize = 12)
		Revenue.legend((revRect,ebitRect),('Revenues','EBIT'),fontsize=7,loc='upper left')
		
	def plotRatios(self,fig,PERatio,ratio,presentPE,year):
		width = 0.2
		diff = len(year)-len(ratio)
		
		if(diff != 0):
			for iter in range(0,diff):
				ratio.append(0.0)
				
		presentYear = year[len(year)-1]
		
		ratioRect = PERatio.bar(year,ratio,width,align='center')
		presentPERect = PERatio.bar(presentYear,presentPE,width,color='r')
		PERatio.yaxis.grid(color='gray',linestyle='dashed')
		loc = pltticker.MultipleLocator(base=1.0)
		PERatio.xaxis.set_major_locator(loc)
		fig.autofmt_xdate()
		PERatio.set_xlabel('Year',fontsize=10,fontweight='bold')
		PERatio.set_title('PE Ratio',fontsize = 12)
		PERatio.legend((ratioRect,presentPERect),('Historic','Present'),fontsize=7,loc='upper left')