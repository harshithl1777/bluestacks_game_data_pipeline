import pandas as pd

# 0. Uploading CSV file as dataframe (df)
df = pd.read_csv('raw_data.csv')

# 1. Deleting unnecessary columns, blank rows, rows before Feb'21
df = df.drop(axis=1, labels=[
    'Card ID', 'Card URL', 'Members', 
    'Due Date', 'Attachment Count', 'Attachment Links', 
    'Checklist Item Total Count', 'Checklist Item Completed Count', 
    'Vote Count', 'Comment Count', 'Last Activity Date', 
    'List ID', 'Board ID', 'Board Name', 'Archived'])
df = df.dropna()

# 1.1 Locating game data for before February and deleting
count1 = -1
rowsToDel = []
for listName in df[['List Name'][0]]:
    count1 = count1 + 1
    if (listName != "Feb'21 game launches" and listName != "Past Feb'21"):
        rowsToDel.append(count1)

df = df.drop(df[(df['List Name'] != "Feb'21 game launches") & (df['List Name'] != "Past Feb'21")].index)
df = df.drop(axis=1, labels=['List Name'])

# 2. Extracting card name, tier and geo from Card Name
cardNames = []
tiers = []
geos = []
for value in df[['Card Name'][0]]:
    cardName = value[:value.find('Tier')-3]
    cardNames.append(cardName)
    tier = value[value.find('Tier'):value.find('Tier')+6]
    tiers.append(tier)
    geo = value[value.find('Tier')+8:]
    geos.append(geo.upper())

# 2.2 Creating new columns for card name, tier and geo data
df = df.drop(axis=1, labels=['Card Name'])
df['Card Name'] = cardNames
df['Tier'] = tiers
df['Geo'] = geos

# 3. Extracting pkg, CPI, creator, developer, game category from Card Desc
fullDescs = []
for descVal in df[['Card Description'][0]]:
    packageIndex = descVal.find('Package')
    fullDescs.append(descVal[packageIndex:])

# 3.1 Extracting required data from card desc
pkgNames = []
cpiDeals = []
submitters = []
developers = []
categories = []

for fullDescSingle in fullDescs:
    descArray = fullDescSingle.split('\n ')
    pkgPos = 0
    dealPos = 0
    submitterPos = 0
    devPos = 0
    categoryPos = 0
    for x in range(len(descArray)):
        if (descArray[x].find('Package name:') != -1):
            pkgPos = x
        elif (descArray[x].find('CPI Deal?:') != -1):
            dealPos = x
        elif (descArray[x].find('Brought to us by:') != -1):
            submitterPos = x
        elif (descArray[x].find('App developer:') != -1):
            devPos = x
        elif (descArray[x].find('App Category:') != -1):
            categoryPos = x
    
    pkgIndex = descArray[pkgPos].find(': ')+2
    pkgNames.append(descArray[pkgPos][pkgIndex:])
    
    dealIndex = descArray[dealPos].find(': ')+2
    cpiDeals.append(descArray[dealPos][dealIndex:])
    
    submitterIndex = descArray[submitterPos].find(': ')+2
    submitterEmailIndex = descArray[submitterPos].find('@')
    submitters.append(descArray[submitterPos][submitterIndex:submitterEmailIndex].capitalize())
    
    devIndex = descArray[devPos].find(': ')+2
    developers.append(descArray[devPos][devIndex:])
    
    categoryIndex = descArray[categoryPos].find(': ')+2
    categories.append(descArray[categoryPos][categoryIndex:].upper())

# 3.2 Adding new columns using data acquired
df['Package Name'] = pkgNames
df['CPI'] = cpiDeals
df['Submitted By'] = submitters
df['Developer'] = developers
df['Category'] = categories
df = df.drop(axis=1, labels=['Card Description'])

# 4. Extracting CPC, Branding, Status from Labels
def labelExtractor():
    cpcs = []
    brandings = []
    statuses = []
    gametvs = []

    for label in df[['Labels'][0]]:
        cpcBool = label.find('CPC (yellow)')
        liveBool = label.find('live (green)')
        notliveBool = label.find('not live (red)')
        brandBool = label.find('Branding (orange)')
        gametvBool = label.find('Game.tv (purple)')
        if (cpcBool != -1):
            cpcs.append('Yes')
        else:
            cpcs.append('No')
        if (liveBool != -1):
            statuses.append('Live')
        elif (liveBool == -1 and notliveBool == -1):
            statuses.append('No Data')
        elif (notliveBool != -1):
            statuses.append('Not Live')
        if (brandBool != -1):
            brandings.append('Yes')
        else:
            brandings.append('No')
        if (gametvBool != -1):
            gametvs.append('Yes')
        else:
            gametvs.append('No')
    df['CPC'] = cpcs
    df['Branding'] = brandings
    df['Status'] = statuses
    df['Game.tv'] = gametvs

labelExtractor()
df = df.drop(axis=1, labels=['Labels'])


# 5. Reordering columns in dataframe
df = df[['Card Name', 'Package Name', 'Developer', 'Category', 'Tier', 'Geo', 'Submitted By', 'Game.tv', 'CPI', 'Branding', 'CPC', 'Status']]
print(df)

# 6. Saving data as new CSV file
df.to_csv('processed_data.csv')