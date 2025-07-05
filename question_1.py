import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'STSong'

# 数据读取和预处理

df_sorts = pd.read_excel("附件C1.xlsx")
df_data1 = pd.read_excel("附件C2题目1处理.xlsx")
# 空白

# 存放单品编码与分类编码、销量的字典
sales_dict = {}
# 年份-月份-种类-销量的字典
fir_mon_cat_sale = {1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{}}
sec_mon_cat_sale = {1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{}}
thi_mon_cat_sale = {1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{}}
year_list = [fir_mon_cat_sale,sec_mon_cat_sale,thi_mon_cat_sale]

for _, row in df_sorts.iterrows():
    product_id = row['单品编码']
    category = row['分类编码']
    sales_dict[product_id] = [category,0]

for _, row1 in df_data1.iterrows():
    product_id = row1['单品编码']
    sale = row1['销量(千克)']
    year = row1['销售年份']
    month = row1['销售月份']
    sales_dict[product_id][1] += sale
    category = sales_dict[product_id][0]
    if category not in year_list[year-1][month]:
        year_list[year-1][month][category] = 0
    year_list[year-1][month][category] += sale 

# 图一，分类和三年总销量的直方图
# 种类-名称
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

# 不同年份下的各个种类每月销量统计
# 基本数据分析
data = []
for year_idx in range(3):
    for month in range(1, 13):
        for cat, sale in year_list[year_idx][month].items():
            data.append({
                '年份': year_idx + 1,
                '月份': month,
                '分类编码': cat,
                '分类名称':cat_name[cat],
                '销量': sale
                })
            
df = pd.DataFrame(data)

# 先计算标准统计量
basic_stats = df.groupby('分类名称')['销量'].agg(
    mean='mean',
    std='std',
    max='max',
    min='min',
    kurt=pd.Series.kurt,
    skew=pd.Series.skew
)

cv_stats = df.groupby('分类名称')['销量'].apply(
    lambda x: np.std(x)/np.mean(x) if np.mean(x) != 0 else np.nan
).rename('变异系数')

yearly_stats = pd.concat([basic_stats, cv_stats], axis=1)
yearly_stats.columns = ['平均值', '标准差', '最大值', '最小值', '峰度', '偏度', '变异系数']
print(yearly_stats)
