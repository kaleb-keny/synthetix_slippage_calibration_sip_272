from utils.model_fit import Fit
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class Chart(Fit):
    
    def __init__(self,exponentList=[0,0.5,1,2]):
        super().__init__(exponentList)

    def chart_data(self):

        outputModelDict = dict()
        outputList      = list()
        fig, ax = plt.subplots()

        #get slippage data from uniswap / cex
        df = pd.read_csv("input/input_slippage.csv")
        outputList.append(df.trade_amount.to_list())
                
        #take only positive part, assuming symmetry
        dfModel = df[df["trade_amount"]>0]
        
        #model slippage
        for targetModelName in list(df.columns[1:]):
            
            #fit model
            self.fit_model(x=dfModel.trade_amount.to_numpy(), 
                           y=dfModel[targetModelName].to_numpy())
            
            coefList      = self.model.x
            modelSlippage = self.apply_poly_model(x=dfModel.trade_amount.to_numpy(), coefList=coefList)
            modelSlippage = np.array([-modelSlippage,modelSlippage]).flatten()
            outputList.append(modelSlippage)
            modelSlippage.sort()
            modelSlippageString = self.poly_print(exponentList=[0,0.5,1,2],coefList=coefList.round(5))
            outputModelDict[targetModelName] = self.poly_print(exponentList=[0,0.5,1,2],coefList=coefList)
                        
            #chart model & target
            sns.lineplot(x=df.trade_amount,y=df[targetModelName].to_numpy(),label=targetModelName,ax=ax)
            sns.lineplot(x=df.trade_amount,y=modelSlippage,label=f'{modelSlippageString}',ax=ax,ls='--')

        ax.grid(linestyle='--',lw=0.3)
        ax.set_title('Slippage Chart')
        ax.set_xlabel('Market Order - USD Millions')
        ax.set_ylabel('slippage - bp')
        ax.legend(loc='upper left',fontsize=6)
        plt.savefig("output/slippage.jpeg",format='jpeg',dpi=300)
        
        df = pd.DataFrame(outputList).T
        df.columns = ["trade_amount","uni_model_slippage","cex_model_slippage"]
        df.to_csv("output/model_slippage.csv",index=False)
        with open("output/model.json","w") as f:
            json.dump(outputModelDict,f,indent=6)

    def poly_print(self,exponentList,coefList):
        polyStr = f'{coefList[0]} '
        for exponent, coef in zip(exponentList[1:],coefList[1:]):
            polyStr = polyStr + '{0:+}'.format(coef) + f'x^{exponent} '
        return polyStr