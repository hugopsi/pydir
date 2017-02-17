'''I strongly recommend that you encapsulate your code. This way, all your variables are global and you can by mistake
assign a value to variable that already exists.'''
''' I change the order of a few line to make comment ease'''


#    energy = energy[['Unnamed: 1', 'Petajoules', 'Gigajoules', '%']]
#    energy = energy.rename(columns = {'Unnamed: 1' : 'Country', 'Petajoules' : 'Energy Supply',
#                                             'Gigajoules' : 'Energy Supply per Capita', '%' : '% Renewable'}).replace(to_replace = '...', value = np.NaN)


energy = pd.read_excel('Energy Indicators.xls', skiprows=17, skip_footer=38)
energy.drop(energy.columns[[0, 1]], axis=1, inplace=True) 
energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']

energy['Country'] = energy['Country'].map(lambda x: x.rstrip('0123456789'))
energy['Country'] = energy['Country'].map(lambda x: x.rstrip(' '))
energy['Country'].str.replace(r"\(.*\)","")

#Study this line, it's great to clean numbers and signals from strings.
#energy['Country'] = energy['Country'].str.replace("^([a-zA-Z]+(?:\s+[a-zA-Z]+)*).*", r"\1")

energy = energy.replace('Republic of Korea','South Korea')
energy = energy.replace('United States of America','United States')
energy = energy.replace('United Kingdom of Great Britain and Northern Ireland','United Kingdom')
energy = energy.replace('China, Hong Kong Special Administrative Region3','Hong Kong')
energy = energy.replace('China, Macao Special Administrative Region','China, Macao Special Administrative Region')
energy = energy.replace('Iran (Islamic Republic of)','Iran')
energy['Energy Supply'] = energy['Energy Supply'].replace("...",np.NaN)
energy['Energy Supply per Capita'] = energy['Energy Supply per Capita'].replace('...',np.NaN)
energy['Country'] = energy['Country'].replace(' (...',np.NaN)

# You can passa a dictionary an replace a various columns at same time and using a more pandorable code. 
# exemple
#energy['Country'] = energy['Country'].replace({'China, Hong Kong Special Administrative Region':'Hong Kong',
#                                               'United Kingdom of Great Britain and Northern Ireland':'United Kingdom',
#                                               'Republic of Korea':'South Korea',
#                                               'United States of America':'United States'})
energy['Energy Supply'] *= 1000000


GDP = pd.read_csv('world_bank.csv', index_col=0, header=0) # with skiprows = 4 you get the table almost formated. 
GDP = GDP.drop(['Data Source'])# this line dosen't do anything. If you want to delet an index title you must use the folowing line:
#del GDP.index.name
GDP = GDP.dropna()
GDP = GDP.reset_index()
GDP.columns = GDP.iloc[0]
GDP.drop(GDP.index[[0]], inplace=True)
GDP = GDP.rename(columns={'Country Name': 'Country'})

GDP['Country'] = GDP['Country'].replace(to_replace = 'Korea, Rep.', value = 'South Korea')
GDP['Country'] = GDP['Country'].replace(to_replace = 'Iran, Islamic Rep.', value = 'Iran')
GDP['Country'] = GDP['Country'].replace(to_replace = 'Hong Kong SAR, China', value ='Hong Kong')

GDP.replace(',','-', inplace=True)
GDP['Country'] = GDP['Country'].map(lambda x: x.rstrip(' '))



ScimEn = pd.read_excel('scimagojr-3.xlsx')
ScimEn2 = pd.read_excel('scimagojr-3.xlsx').head(15) #<-compare with line above

df = pd.merge(pd.merge(energy,GDP,on='Country'),ScimEn2,on='Country') #Here is your problem!

df = df.sort(['Rank'], ascending=[True])
col_list = [0, 63, 64, 65, 66, 67, 68, 69, 1, 2, 3, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62]
df = df[col_list]
df.columns = ['Country','Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document','H index','Energy Supply','Energy Supply per Capita','% Renewable','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
df = df.set_index('Country')
def answer_one():
    return df
answer_one()
