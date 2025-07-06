import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
plt.rcParams['font.family'] = 'STSong'
os.chdir(os.path.dirname(os.path.abspath(__file__))) 

# 数据读取和预处理

df_sorts = pd.read_excel("../附件C1.xlsx")
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
plt.savefig('种类-销量分布柱状图.png')

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

basic_stats = df.groupby('分类名称', as_index=False).agg(
    平均值=('销量', 'mean'),
    标准差=('销量', 'std'),
    最大值=('销量', 'max'),
    最小值=('销量', 'min'),
    峰度=('销量', lambda x: x.kurtosis()),
    偏度=('销量', 'skew')
)
cv_stats = df.groupby('分类名称')['销量'].apply(
    lambda x: np.std(x)/np.mean(x) if np.mean(x) != 0 else np.nan
).reset_index(name='变异系数')
yearly_stats = pd.merge(basic_stats, cv_stats, on='分类名称')
csv_path = "销量统计分析结果.csv"
yearly_stats.to_csv(csv_path, 
                 index=False,
                 encoding='utf-8-sig')

# 不同分类月销量
# 月总销量箱线图
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='月份', y='销量')
plt.title('各月份总销量分布对比')
plt.savefig('月度总销量箱线图.png')

# 研究分析不同品类销售量相互作用
df_pivot = df.pivot_table(
    index=['年份', '月份'], 
    columns='分类名称',      
    values='销量',         
    aggfunc='sum'        
)

# 计算皮尔逊和斯皮尔曼矩阵
pearson_corr = df_pivot.corr(method="pearson")
spearman_corr = df_pivot.corr(method="spearman")

# 对比两者的差异
diff = (pearson_corr - spearman_corr).abs().mean().mean()
print(f"皮尔逊和斯皮尔曼平均差异: {diff:.3f}")

if diff > 0.2:  # 如果差异较大，选择斯皮尔曼
    final_corr = spearman_corr
    print("皮尔逊和斯皮尔曼差异较大，推荐使用斯皮尔曼！")
else:
    final_corr = pearson_corr
    print("皮尔逊和斯皮尔曼接近，使用皮尔逊即可。")

# 可视化最终选择的矩阵
sns.heatmap(final_corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("相关系数矩阵")
plt.savefig('不同分类相关系数矩阵.png')