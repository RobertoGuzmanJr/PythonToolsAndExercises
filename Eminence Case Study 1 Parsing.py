import pandas as pd
import csv

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

merchant_names = []
user_ids = []
order_numbers = []
order_times = []
order_total_amounts = []
order_points = []
order_shipping = []
order_taxes = []
order_subtotals = []
order_total_qtys = []
product_descriptions = []
product_subtitles = []
order_quantities = []
item_prices = []
digital_transactions = []
product_resellers = []
product_categories = []
order_discounts = []
skus = []
item_ids = []
order_pickups = []
email_subjects = []

def ExtractHeaders(file):
    with open(file, mode='r') as csv_file:
        read = csv.reader(csv_file)
        for row in read:
            return row

def FetchRow(file):
    with open(file, mode='r') as csv_file:
        read = csv.reader(csv_file)
        counter = 0
        for row in read:
            if counter == 0:
                counter += 1
                continue
            else:
                yield row
                counter += 1

def ProcessRow(row):
    global merchant_names
    global user_ids
    global order_numbers
    global order_times
    global order_total_amounts
    global order_points
    global order_shipping
    global order_taxes
    global order_subtotals
    global order_total_qtys
    global product_descriptions
    global product_subtitles
    global order_quantities
    global item_prices
    global digital_transactions
    global product_resellers
    global product_categories
    global order_discounts
    global skus
    global item_ids
    global order_pickups
    global email_subjects

    merchant_names.append(row[0])
    user_ids.append(row[1])
    order_numbers.append(row[2])
    order_times.append(row[3])
    order_total_amounts.append(row[7])
    order_points.append(row[8])
    order_shipping.append(row[9])
    order_taxes.append(row[10])
    order_subtotals.append(row[11])
    order_total_qtys.append(row[12])
    product_descriptions.append(row[13])
    product_subtitles.append(row[14])
    order_quantities.append(row[15])
    item_prices.append(row[16])
    digital_transactions.append(row[17])
    product_resellers.append(row[19])
    product_categories.append(row[20])
    order_discounts.append(row[21])
    skus.append(row[22])
    item_ids.append(row[23])
    order_pickups.append(row[24])
    email_subjects.append(row[26])

"""
Not all data appears relevant. Here are the fields that we want:

column 0 => merchant_name
    We will want to get the unique merchants and figure out how many of each we got.
column 1 => user_id
    We will want to bring this in and mask it with a different number, since it is a massive GUID. We will want to see
    how many times each customer went in. We will also want to see if there is any overlap between vendors; are 
    user_ids unique across vendors?
column 2 => order_number
    This should  be unique. If it is not, there is a chance that it is repeated across vendors.
column 3 => order_time
    This is interesting and should be captured. We are going to want to see what the highest and lowest times are.
column 4 => email_time
    This does not seem terribly interesting on its own. It is possible that we should look into whether there is a gap
    between this time and the order time. We will not need it immediately.
column 5 => insert_time
    We can safely ignore this.
column 6 => update_time
    We can safely ignore this.
column 7 => order_total_amount
    We want this. There should be some QA checks to see if this is accurate.
column 8 => order_points
    We want this. Less interesting, but maybe keep it.
column 9 => order_shipping
    We want this. Will factor into QA checks for total.
column 10 => order_tax
    We will want this. It will factor into QA checks for total.
column 11 => order_subtotal
    We will want this. It will factor into QA checks for total.
column 12 => order_total_qty
    We will want this. Should be some QA on this field.
column 13 => product_description
    We will want this, it is an interesting data point.
column 14 => product_subtitle
    Not sure what this is. Let's look into it.
column 15 => order_quantity
    We will want this and should do some QA on it.
column 16 => item_price
    We will want to examine this and should do some QA on it.
column 17 => digital_transaction
    I wonder what this is for. Let's collect the values.
column 18 => checksum
    I think we can ignore this.
column 19 => product_reseller
    Let's see what this is.
column 20 => Product_category
    Is this the same for everything?
column 21 => order_discount
    Load it, let's use it for QA
column 22 => SKU
    collect it to see what we get
column 23 => item_id
    should be the same as the SKU. Let's review it.
column 24 => order_pickup
    Wonder what this is for.
column 25 => from_domain
    Probably ignore.
column 26 => email_subject
    We can use this for a date QA.
column 27 => delivery_date
    date the row got delivered from the source? ignore
column 28 => start_source_folder_date
    ignore
column 29 => end_source_folder_date
    ignore
column 30 => file_id
    ignore
column 31 => source_dttimestamp
    ignore
column 32 => dttimestamp
    ignore                

"""
fileName = "C:/Users/rg255/Downloads/Data_Rideshare/Data_RideShare.csv"
header = ExtractHeaders(fileName)
gen = FetchRow(fileName)

    for g in gen: ProcessRow(g)

    #How many of these have no Merchant Name? For each merchant, how many records do we have?
    numUber = 0
    numLyft = 0
    numOther = 0
    for merchant_name in merchant_names:
        if merchant_name == 'Uber':
            numUber += 1
        elif merchant_name == 'Lyft':
            numLyft += 1
        else:
            numOther += 1

print("In terms of merchants, we have {0} rows for Lyft and {1} rows for Uber. We also have {2} other rows.".format(numLyft,numUber,numOther))

#For the order_total_amounts, are they all positive? Are they all numeric?
numNotNumeric = 0
numNegative = 0
numZero = 0

for i in range(len(order_total_amounts)):
    convertable = True
    try:
        float(order_total_amounts[i])
    except:
        numNotNumeric += 1
        convertable = False
    if convertable and float(order_total_amounts[i]) < 0:
        numNegative += 1
    if convertable and float(order_total_amounts[i]) == 0.0:
        numZero += 1
print("There are {0} non-numeric totals and {1} negative totals.".format(numNotNumeric,numNegative))
print("There are {0} totals that are 0.".format(numZero))

#Does every row have a user_id? How many do not have a userId? How many customers does each place have? What is the average number of
#orders per customer for each? What is the distribution of spend per customer?
uberCustomers = {}
lyftCustomers = {}
uberUnknowns = 0
lyftUnknowns = 0
trulyUnknowns = 0

for i in range(len(user_ids)):
    if user_ids[i] == '' and merchant_names[i] == 'Uber':
        uberUnknowns += 1
    elif user_ids[i] == '' and merchant_names[i] == 'Lyft':
        lyftUnknowns += 1
    elif merchant_names[i] == 'Uber':
        if user_ids[i] in uberCustomers:
            uberCustomers[user_ids[i]][0] += 1
            uberCustomers[user_ids[i]][1] += order_total_amounts[i]
        else:
            uberCustomers[user_ids[i]] = [1,order_total_amounts[i]]
    elif merchant_names[i] == 'Lyft':
        if user_ids[i] in lyftCustomers:
            lyftCustomers[user_ids[i]][0] += 1
            lyftCustomers[user_ids[i]][1] += order_total_amounts[i]
        else:
            lyftCustomers[user_ids[i]] = [1, order_total_amounts[i]]
    else:
        trulyUnknowns += 1

print("There are {0} Uber unknown customers and {1} Lyft unknown customers".format(uberUnknowns,lyftUnknowns))
print("There are {0} truly unknown customers.".format(trulyUnknowns))
print("There are {0} distinct Uber customers.".format(len(uberCustomers.keys())))
print("There are {0} distinct Lyft customers.".format(len(lyftCustomers.keys())))
print("The average number of orders per customer for Uber is {0}.".format(sum([x[0] for x in uberCustomers.values()])/len(uberCustomers.keys())))
print("The average number of orders per customer for Lyft is {0}.".format(sum([x[0] for x in lyftCustomers.values()])/len(lyftCustomers.keys())))


#what is the median number of orders per customeer for Lyft and Uber?
#what is the standard deviation of orders per customeer for Lyft and Uber?

#what do the below stats really tell us?
print("The average spend per customer for Uber is {0}.".format(sum([float(x[1]) for x in uberCustomers.values() if is_number(x[1]) and float(x[1]) > 0])/len(uberCustomers.keys())))
print("The average spend per customer for Lyft is {0}.".format(sum([float(x[1]) for x in lyftCustomers.values() if is_number(x[1]) and float(x[1]) > 0])/len(lyftCustomers.keys())))

#what is the max and min for  the spends per customer at Uber and Lyft?



#we may want to process each row, one at a time, and create an exception list.

#are there any missing ordernumbers? which firm do they belong to?

#for order times, let's figure out the most poular and least popular times for each firm, per order and per dollar spend? also, are they formatted properly? are they
#in UTC?



