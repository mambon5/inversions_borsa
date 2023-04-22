"""
this scritp tries to retrieve after hours stock prices using the github > https://github.com/datawrestler/after-hours
"""


from afterhours.afterhours import AfterHours

# AFTER HOURS TRADING DATA
AH = AfterHours('aapl', typeof = 'after')

# get the low price from after hours trading
print(AH.getdata(datatype='lowprice'))
# 102.18

# get the high price of after hours trading
print(AH.getdata(datatype='highprice'))
# 109.055

# get the timestamp of after hours high trade
print(AH.getdata(datatype='hightime'))
# '12/15/2017 18:58:46 PM'

print(AH.getdata(datatype='lowtime'))
# '12/15/2017 19:58:46 PM'

# get all data points for after hours trading
print(AH.secure_all())
# Pandas DataFrame

# PRE HOURS TRADING DATA
# get pre hours trading info for apple
AH = AfterHours('aapl', typeof='pre')

# get the low price from pre hours trading
print(AH.getdata(datatype='lowprice'))
# 102.18