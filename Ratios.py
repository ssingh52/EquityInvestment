import numpy as np
class Ratios:
	def __init__(self,priceList,epsAdjustedList):
		self.peRatio = []
		self.epsGrowthRate = []
		self.pepbRatioCalculate(priceList,epsAdjustedList)
						
	def pepbRatioCalculate(self,priceList,epsAdjustedList):
		index = 0
		
		for val in range(0,len(epsAdjustedList)):
			if(epsAdjustedList[index] != 0.0):
				ratio1 = round(float(priceList[index])/epsAdjustedList[index],1)
				index = index + 1
				self.peRatio.append(ratio1)
			else:
				self.peRatio.append(0.0)
				index = index + 1			
						
	def peRatioList(self):
		return self.peRatio
				
	def epsGrowthRateList(self):
		return self.epsGrowthRate
		
	