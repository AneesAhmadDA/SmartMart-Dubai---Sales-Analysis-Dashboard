import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
from charts.plot_ppie import plot_professional_pie
from charts.plot_bar import plot_bar_chart
from charts.plot_line import plot_line_chart
from charts.plot_scatter import plot_scatter_chart
from charts.plot_histogram import plot_histogram_chart
from matplotlib.backends.backend_pdf import PdfPages
figs,axis=plt.subplots(2,2,figsize=(13,9),facecolor="#d0d4d1")
plt.suptitle("SmartMart Dubai Sales Dashboard", fontsize=18, fontweight='bold',)
data=pd.read_csv('smartmart_dubai_transactions.csv')
df=pd.DataFrame(data)
# print(df.isnull().any()) no null value found 
print(df.describe())
df['Month']=pd.to_datetime(df["Date"]).dt.to_period('M')
print(df.head(5))
# top 5 product by catergory
top_5_product=df.groupby(['Product_Category'])['Total_Amount'].sum().sort_values(ascending=False).head(5)
print(top_5_product)
plot_professional_pie(top_5_product, title='Top 5 Product Category', top_n=5, value_label='AED',
                          label_font='Verdana', title_font='Arial', show_others=False, start_angle=140,
                          ax=axis[0,0])
# sales per city area :
sale_per_city=df.groupby(['City_Area'])['Total_Amount'].sum().sort_values(ascending=False)
print(sale_per_city)
plot_bar_chart(
    sale_per_city.index,
    sale_per_city.values,
    title='Sales Analysis Per City ',
    title_font='Arial',
    xlabel='Location',
    ylabel='Total Sales',
    axis_font='Verdana',
    figure_facecolor="#f5f5f5",
    thresholds=(130000,144812.2),  # Can be (number, number) OR (str, str)
    colors=("#A92103", "#B19B31", "#dac828"),
    rotation=40,
    show_minor_ticks=True,
    show_minor_labels=False,
    ax=axis[1,0]
)
# payment method used overall 
pay_method=df.groupby(['Payment_Method'])['Total_Amount'].sum().sort_values(ascending=False)
print(pay_method)
plot_professional_pie(pay_method, title='Payment Method Used', top_n=5, value_label='AED',
                          label_font='Verdana', title_font='Arial', show_others=False, start_angle=140,
                          ax=axis[0,1])
# plt.tight_layout()
# plt.show()
# montly trend of sales 
monthly_trend=df.groupby(['Month'])['Total_Amount'].sum()
print(monthly_trend)
plot_line_chart(monthly_trend.index.astype(str),monthly_trend.values, title='Montly_Sales Trend', xlabel='Month', ylabel='Total_Sales', label='SalesTrend', linestyle='solid',
                    linewidth=2, color="#534DA5", marker='o', markersize=8,
                    markerfacecolor=None, markeredgecolor='black', legend=False, ax=axis[1,1],rotation=45)

plt.subplots_adjust(
    left=0.05,    
    right=0.93,   
    top=0.9,      
    bottom=0.17,
    wspace=0.3,   
    hspace=0.4    
)
figs.text(0.5, 0.01, "Source: SmartMart POS Data | Analysis by AneesAhmad", 
          ha='center', fontsize=9, style='italic', color='gray')
# plt.show()
# coustomer age vs sales
sales_ages=df.groupby(['Customer_Age'])['Total_Amount'].sum().sort_values(ascending=False)
fig,axs=plt.subplots(2,2,figsize=(13,9),facecolor="#d0d4d1")
plt.suptitle("SmartMart Dubai Sales Dashboard", fontsize=18, fontweight='bold',)
plot_scatter_chart(sales_ages.index,sales_ages.values, title='Customer Ages & Sales', title_font='Arial', xlabel='Ages',
                        ylabel='Total_Sale',label_font='Verdana', label='',
                       color="#2ca02c", marker='o', markersize=80,
                       edgecolor='black', alpha=0.85, legend=False, annotate=True,
                       ax=axs[0,0])
rolling_avg = sales_ages.rolling(window=7).mean()
axs[0,0].plot(sales_ages.index, rolling_avg, color='red', linewidth=2, label='Ages_sales')
axs[0,0].legend()
axs[0,0].grid(True, linestyle='--', alpha=0.6)
ages=df['Customer_Age']
plot_histogram_chart(
    ages,
    bins=5,
    histtype='bar',
    title='Customers Visiting The Mart',
    title_font='Arial',
    xlabel='Ages',
    ylabel='Frequency',
    axis_font='Verdana',
    figure_facecolor="#f5f5f5",
    thresholds=(150,175),
    colors=("#B42504", "#AB7622", "#1e88e5"),  # (low, mid, high)
    show_minor_ticks=True,
    ax=axs[1,0]   
)
# top products sold 
top_product_quantity=df.groupby(['Product_Name'])['Quantity'].sum().sort_values(ascending=False).head(7)
plot_bar_chart(
    top_product_quantity.index,
    top_product_quantity.values,
    title='Top_Product_Sales ',
    title_font='Arial',
    xlabel='Product_Name',
    ylabel='Quantity_Sold',
    axis_font='Verdana',
    figure_facecolor="#f5f5f5",
    thresholds=(130,140), 
    colors=("#A92103", "#B19B31", "#dac828"),
    rotation=25,
    show_minor_ticks=True,
    show_minor_labels=False,
    ax=axs[1,1]
)
# revenue genertate  per purchasd channel 
Channel_used=df.groupby(['Purchase_Channel'])['Total_Amount'].sum().sort_values(ascending=False)
plot_professional_pie(Channel_used, title='Online vs Local Customers', top_n=5, value_label='AED',
                          label_font='Verdana', title_font='Arial', show_others=False, start_angle=140,
                          ax=axs[0,1])
plt.subplots_adjust(
    left=0.07,    
    right=0.93,   
    top=0.87,     
    bottom=0.1,   
    wspace=0.2,   
    hspace=0.45    
)

with PdfPages("SmartMart_Sales_Report.pdf") as pdf:
    # First dashboard page
    pdf.savefig(figs) 
    # Second dashboard page
    pdf.savefig(fig)  

# print(top_product_quantity)
plt.show()

