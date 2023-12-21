import os
import pandas as pd
path = os.path.abspath(__file__)
relate_df = pd.read_excel(os.path.join('./G6PD关系/对应关系.xlsx'))
relate_dict = relate_df.set_index('结果')['对应图片'].to_dict()
# print( d['结果'] )

# print( d['对应图片'] )
# print(d)
binpath = os.path.split(os.path.realpath(__file__))[0]
print(binpath)