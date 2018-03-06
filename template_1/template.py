
'''
    这是一个数据可是化的样例，模板数据是一个贷款分析项目。

    数据中有文字，有时间，还有不同国家的分类

'''

# 1 对特定数据的分布分析，一般会成正太分布
print("Description of distribuition")
print(df_kiva[['funded_amount','loan_amount']].describe())

plt.figure(figsize=(12,10))

plt.subplot(221)
g = sns.distplot(np.log(df_kiva['funded_amount'] + 1))
g.set_title("Funded Amount Distribuition", fontsize=15)
g.set_xlabel("")
g.set_ylabel("Frequency", fontsize=12)

plt.subplot(222)
g1 = plt.scatter(range(df_kiva.shape[0]), np.sort(df_kiva.funded_amount.values))
g1= plt.title("Funded Amount Residual Distribuition", fontsize=15)
g1 = plt.xlabel("")
g1 = plt.ylabel("Amount(US)", fontsize=12)

plt.subplot(223)
g2 = sns.distplot(np.log(df_kiva['loan_amount'] + 1))
g2.set_title("Loan Amount Distribuition", fontsize=15)
g2.set_xlabel("")
g2.set_ylabel("Frequency", fontsize=12)

plt.subplot(224)
g3 = plt.scatter(range(df_kiva.shape[0]), np.sort(df_kiva.loan_amount.values))
g3= plt.title("Loan Amount Residual Distribuition", fontsize=15)
g3 = plt.xlabel("")
g3 = plt.ylabel("Amount(US)", fontsize=12)

plt.subplots_adjust(wspace = 0.3, hspace = 0.3,
                    top = 0.9)

plt.show()




# 2 对数据的排名分析
lenders = df_kiva.lender_count.value_counts()

plt.figure(figsize=(12,10))

plt.subplot(222)
g = sns.distplot(np.log(df_kiva['lender_count'] + 1))

g.set_title("Dist Lenders Log", fontsize=15)
g.set_xlabel("")
g.set_ylabel("Frequency", fontsize=12)

plt.subplot(221)
g1 = sns.distplot(df_kiva[df_kiva['lender_count'] < 1000]['lender_count'])

g1.set_title("Dist Lenders", fontsize=15)
g1.set_xlabel("")
g1.set_ylabel("Frequency", fontsize=12)

plt.subplot(212)
g2 = sns.barplot(x=lenders.index[:40], y=lenders.values[:40])
g2.set_xticklabels(g2.get_xticklabels(),rotation=90)
g2.set_title("Top 40 most frequent numer of Lenders to the transaction", fontsize=15)
g2.set_xlabel("")
g2.set_ylabel("Count", fontsize=12)

plt.subplots_adjust(wspace = 0.2, hspace = 0.3,top = 0.9)

plt.show()




# 3 对数据的分类的分析
df_kiva['loan_amount_log'] = np.log(df_kiva['loan_amount'])
df_kiva['funded_amount_log'] = np.log(df_kiva['funded_amount'] + 1)
df_kiva['diff_fund'] = df_kiva['loan_amount'] / df_kiva['funded_amount'] 

plt.figure(figsize=(12,14))

plt.subplot(312)
g1 = sns.boxplot(x='sector', y='loan_amount_log',data=df_kiva)
g1.set_xticklabels(g1.get_xticklabels(),rotation=45)
g1.set_title("Loan Distribuition by Sectors", fontsize=15)
g1.set_xlabel("")
g1.set_ylabel("Loan Amount(log)", fontsize=12)

plt.subplot(311)
g2 = sns.boxplot(x='sector', y='funded_amount_log',data=df_kiva)
g2.set_xticklabels(g2.get_xticklabels(),rotation=45)
g2.set_title("Funded Amount(log) by Sectors", fontsize=15)
g2.set_xlabel("")
g2.set_ylabel("Funded Amount", fontsize=12)

plt.subplot(313)
g3 = sns.boxplot(x='sector', y='term_in_months',data=df_kiva)
g3.set_xticklabels(g3.get_xticklabels(),rotation=45)
g3.set_title("Term Frequency by Sectors", fontsize=15)
g3.set_xlabel("")
g3.set_ylabel("Term Months", fontsize=12)

plt.subplots_adjust(wspace = 0.2, hspace = 0.6,top = 0.9)
plt.show()



# 4 根据某种数据分类，看他们有没有相同的分布
(sns
  .FacetGrid(df_kiva, 
             hue='repayment_interval', 
             size=5, aspect=2)
  .map(sns.kdeplot, 'loan_amount_log', shade=True)
 .add_legend()
)
plt.show()


# 5 生成heatmap来看不同数据之间的联系
sector_repay = ['sector', 'repayment_interval']
cm = sns.light_palette("green", as_cmap=True)
pd.crosstab(df_kiva[sector_repay[0]], df_kiva[sector_repay[1]]).style.background_gradient(cmap = cm)


# 6 来看不同一个二值，比如 性别之间的比较。
plt.figure(figsize=(10,6))

g = sns.countplot(x='sex_borrowers', data=df_kiva, 
                  hue='repayment_interval')
g.set_title("Exploring the Genders by Repayment Interval", fontsize=15)
g.set_xlabel("")
g.set_ylabel("Count Distribuition", fontsize=12)

plt.show()


# 7 对时间的处理
df_kiva['date'] = pd.to_datetime(df_kiva['date'])
df_kiva['funded_time'] = pd.to_datetime(df_kiva['funded_time'])
df_kiva['posted_time'] = pd.to_datetime(df_kiva['posted_time'])

df_kiva['date_month_year'] = df_kiva['date'].dt.to_period("M")
df_kiva['funded_year'] = df_kiva['funded_time'].dt.to_period("M")
df_kiva['posted_month_year'] = df_kiva['posted_time'].dt.to_period("M")
df_kiva['date_year'] = df_kiva['date'].dt.to_period("A")
df_kiva['funded_year'] = df_kiva['funded_time'].dt.to_period("A")
df_kiva['posted_year'] = df_kiva['posted_time'].dt.to_period("A")


# 8 wordcloud 的处理
from wordcloud import WordCloud, STOPWORDS

plt.figure(figsize = (12,10))

stopwords = set(STOPWORDS)
wordcloud = WordCloud(
                          background_color='black',
                          stopwords=stopwords,
                          max_words=150,
                          max_font_size=40, 
                          width=600, height=300,
                          random_state=42,
                         ).generate(str(df_kiva['use']))

print(wordcloud)
fig = plt.figure(1)
plt.imshow(wordcloud)
plt.title("WORD CLOUD - DESCRIPTION")
plt.axis('off')
plt.show()