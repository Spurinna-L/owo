import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'STSong'

# 数据读取和预处理

df_sorts = pd.read_excel("附件C1.xlsx")
df_data1 = pd.read_excel("附件C2题目1处理.xlsx")
df_data2 = pd.read_excel("附件C3.xlsx")

# 存放单品编码与分类编码、销量的字典
sales_dict = {}
for _, row in df_sorts.iterrows():
    product_id = row['单品编码']
    category = row['分类编码']
    sales_dict[product_id] = [category,0]
for _, row1 in df_data1.iterrows():
    product_id = row1['单品编码']
    sale = row1['销量(千克)']
    sales_dict[product_id][1] += sale


# 图一，分类和销量的直方图
# 种类——名称
cat_name = {1011010101:"花叶类",1011010201:"花菜类",1011010402:"水生根茎类",1011010501:"茄类",1011010504:"辣椒类",1011010801:"食用菌"}
# 种类和销量的关系
cat_sale = {}
for cat_temp, sal_temp in sales_dict.values():
    if cat_temp not in cat_sale:
        cat_sale.update({cat_temp:sal_temp})
    else:
        cat_sale[cat_temp] += sal_temp
# 绘图
x = []
for i in cat_sale.keys():
    x.append(cat_name[i])
y = list(cat_sale.values())
plt.bar(x,y)
plt.title('种类-销量分布柱状图')
plt.xlabel('种类')
plt.ylabel('销量')
plt.show()

