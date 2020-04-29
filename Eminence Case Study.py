#!/usr/bin/env python
# coding: utf-8

# # OVERVIEW AND METHODOLOGY
# 
# Welcome to Rob Guzman's case study! In this case study, we begin with data from a CSV file containing Uber and Lyft data. At base, there are two primary goals:
# 
# 1. Understand the data and clean it as best as we can.
# 2. Perform some basic analysis and provide leads to future steps.
# 
# A few additional points:
# 
# - Part of understanding the data is determining which columns are useful, which ones are largely useless, and which ones can be transformed into new columns. We will do all of this. At the end of the process, I will also say a few things about loading and storing this dataset in a relational database (if a file like this were loaded on a routine basis).
# - When we perform our cleaning of the data, not everything will likely be entirely pristine. Capturing every detail would take time and much testing, and future files might contain anomalies that we do not see here. For the sake of this case study, we will pursue the "80-20 rule" and try to get the biggest bang for our buck.
# - This notebook is written in "real-time." What this means is that as you venture down you will see my progression through the data as I did originally. Thus, many statements are run to see results and explore the data. Data cleanining and analysis is an _inductive_ process, so we must look at the way the data actually are in order to gain an idea as to what we should do with it (or to it).
# - Finally, when we get to the end part of the notebook and discuss data anlysis, I will provide several leads to possible future projects that one could pursue with this data. This is also not complete, but is meant to stimulate discussion.
# 
# With that, imagine yourself in the same position that a customer in one of these records: sit back, and enjoy the ride!

# # PART 1: EXPLORATORY ANALYSIS AND DATA CLEANING
# 
# We begin with imports and load the raw data into a Pandas dataframe. We will make extensive use of the Pandas library. We also run the info() function to get an idea as to what the data look like. Note that we receive a warning about mixed types: this is to be expected, since the data are likely filthy.

# In[1]:


import pandas as pd
import csv
import datetime
import numpy as np
import re

fileName = "C:/Users/rg255/Downloads/Data_Rideshare/Data_RideShare.csv"
rawData = pd.read_csv(fileName)

rawData.info()


# One thing to check immediately is whether or not there are any exact duplicates in the data. In rare cases, one might expect such duplicates, but it is generally a bada practice.

# In[2]:


rawData.duplicated().value_counts()


# We are fortunate that there are no exact duplicates. I am sure we will find other reasons to remove rows, though.
# 
# Now that we have loaded the data in its raw form, we want to do some exploratory data analysis on the various columns to ensure that we do not have any bad data. As part of our larger goal of understanding the data, we will need to attach significance and an interpretation to each column in this dataset. At the end, I will summarize our findings here. If you are interested in the progression, read on.
# 
# ## MERCHANT NAME
# 
# We begin with the merchant name, which we expect to have two values: Uber and Lyft. Let's verify this with the value_counts() function.

# In[3]:


rawData["merchant_name"].value_counts()


# As expected, everything is tagged as either Uber or Lyft. Since merchant_name is a string, we would likely want to create our own table for merchants in our relational implementation of this data. That way, we can save space by storing an integer id instead of the full name. Not to mention,  we can catch errors in spelling and new vendors with this approach that might come about in the future.
# 
# ## USER_ID
# 
# The next field to look at is user_id. For this value, we are interested in a few questions, such as:
# 
# 1) what is the intended type?
# 2) what is the cardinality?
# 3) are there any that are missing?
# 
# We can proceed to answer these questions with the following commands. The first command will check the size of the row's contents (which I suspect we will see regularity in, since the field appears to be a GUID of some variety). The second will look for uniqueness across the rows (I do not expect this to hold, since one customer should be able to have multiple orders in the dataset). The third will look for particular values that have a high cardinality, which might indicate some problem. The fourth will look for missing data.

# In[4]:


rawData["user_id"].apply(len).value_counts()


# In[5]:


rawData.groupby("user_id")["merchant_name"].nunique()


# In[6]:


rawData["user_id"].value_counts()


# In[7]:


rawData["user_id"].isnull().value_counts()


# As we can see from the results above:
# 
# 1) There no missing values in the data.
# 2) Everything is a 64 character long string.
# 3) That there are cases where a single user_id has many orders.
# 4) Some user_ids are used by both Lyft and Uber data.
# 
# These findings raise some interesting questions.
# 
# First, what is going on with those customers that have hundreds or thousands of orders? Are these really individuals making thousands of trips? This seems to me to be unlikely; I think it is more likely that this is a shared account, perhaps corporate, that allows for many individuals to take trips, perhaps simultaneously. One way to validate this would be to look for instances where a single user_id has more than one simultaneous trip. This is something we should check later after we have cleaned the date and time data. So let's put a pin in that one (we will revisit it).
# 
# Another question is: is the user_id field universal for this file? Did our vendor consolidate all of their user data into a single table and then assign unique Ids to each of them, so that a user_id that is shared by both Uber and Lyft are really the same person? If so, it means that we could potentially be able to see whether individuals _switch vendors_. That would be something!
# 
# I think it is likely true, given the nature of the field. Assume for the moment that these user_ids were assigned by the vendors themselves. What are the odds that both Uber and Lyft would choose to use the same mechanism for tracking customers (64 character long strings) **and** that they would have a collision with such a gargantuan number of possibilities for assignment of these ids. The number of possible ids is approximately 36^64 = 4.01 x 10^99 give or take a few, since I am sure there are  pathological cases (all 1's or all 0's) removed.
# 
# We can do some basic analysis assuming it is correct and abandon those results if it turns out to be false. This would be something that we would ask the vendor before we went to the bank with it.
# 
# ## ORDER_NUMBER
# 
# Anyways, on to the order_number field. We can ask the same questions as we did for user_id and note that in theory, this field should be particularly cleaned. The reason is that I would expect that **order_number makes sense as a primary key** for this dataset. If there is more than one row for each order_number, that would raise some serious questions about duplication.
# 
# Below, we run a few commands to check for missing values, whether or not the same order_number is used by different merchants, and then, if we find misssing values or dupes, we will try to gain some basic information about some of those rows. 

# In[8]:


rawData["order_number"].isnull().value_counts()


# In[9]:


rawData[rawData["order_number"].isnull() == True]["email_subject"].value_counts()


# There are missing values (that is, null order_numbers) in this dataset. If we are interested in quality data, a record with no order_number is probably not good data. In this case, it is a relatively small amount of data (roughly 2% of the data). If we take a cursory look at the the emails associated with the data that are missing order_numbers, we can see that they do not appear to be passenger pickups. Rather, they refer to getting paid, or buying a ride pass, or getting a tip increase.
# 
# To simplify the analysis, we can remove these rows from the data set and continue with only those rows that have an order_number. We can always do a separate analysis in the future for the data that do not have an order_number. So let's remove those cases. Let's move on to cardinality.

# In[10]:


#Fix for missing order_number
rawData = rawData[rawData['order_number'].notna()]


# In[11]:


multipleOrders = rawData[rawData.groupby('order_number')['merchant_name'].transform('nunique') > 1]
multipleOrders


# In[12]:


rawData[rawData["order_number"] == 'f53f4d13-e355-442a-af0e-385bbab1e20d']


# In[13]:


rawData[rawData["order_number"] == 'eba603be-154a-41fa-9108-3d79437dda0a']


# In[14]:


rawData[rawData["order_number"] == 'c5e4242c-fd0f-40fb-83b3-b7c6da3d5aaa']


# In[15]:


rawData[rawData["order_number"] == '54f01ff4-47f2-4b90-b156-4ad5f6fa3466']


# Another thing that we notice is that there are also cases where the order_number is shared by multiple rows, and they do seem to be the same transaction. We can tell by observing a few examples that nearly everything is the same for these rows, with minor differences. Sometimes, the user_id is different. Sometimes, the user_id is the same and there is a small difference in the insert and update times (which also seem to always be the same, making the columns redundant). We can kill several birds with one stone and look into those cases where there is more than one row for the same order_number and determine how many occur that are of this latter sort (i.e. they have the same data, in essence, but with a minor difference in their datetime of insertion / update). In that case, we can select one of the two and remove the other. But for the first case (i.e. they have different user_ids), this might indicate a potentially duplicate user_id.
# 
# In either case, let's start by checking the assumption that insert_time and update_time are the same.

# In[16]:


rawData[rawData.insert_time != rawData.update_time]


# It looks like many rows have an appreciable difference between the two times, so we should keep both. If we are going to consolidate or dedupe the rows where we have the same user_id on two copies of the same order_number, the story is going to be more complicated. Because the important data (such as the quantitative fields) appear to be the same and the volume of such cases is low, it would make sense to preliminarily delete one of the two rows in these cases and then consult the vendor as to why this would be the case.
# 
# We will count the number of these cases, show an example of one of them, remove the dupes and then check that they have been successfully removed.

# In[17]:


#get the cases where the same order_number shows up more than one, with the same user_id attached.
r = rawData.groupby(['order_number','user_id'])
r.filter(lambda x: len(x) > 1)


# In[18]:


#an example of one of the dupes queried in the cell above.
rawData[rawData['order_number'] == 'e7f516e9-faeb-48da-81b4-54ba7817c4ba']


# There are 2000 such rows, so there should be 1000 rows removed by our dedupe effort. To do this, we will need to define a new rank column which will assign the rows we want to delete a value larger than 1. That way, we can remove them and then remove the column. To select, we will keep the later of the two based on which one has the larger (that is, more recent) update_time.

# In[19]:


rawData['order_rank'] = rawData.sort_values(["update_time"], ascending = [False]).groupby(
    ['order_number','user_id']).cumcount() + 1
rawData = rawData[rawData['order_rank'] == 1]


# In[20]:


#now returns one row, as it should.
rawData[rawData['order_number'] == 'e7f516e9-faeb-48da-81b4-54ba7817c4ba']


# As we can see, the dupes where the same user_id has been selected have been removed. Now all we are left with is the case where order_numbers are duplicated with more than one user_id in the picture. The question to ask here is: are these necessarily bad rows?
# 
# One way to do this is to examine which user_ids are duplicated. When we run the below code, we can see that there are only 29 user_ids that account for the 1126 duplicated order_numbers (queries to validate these figures are below).
# 
# A question that we might want to ask the vendor is whether or not it is possible for two user_ids to legitimately be attached to the same order_number. If that is possible, then user_id would have to be a part of our primary key. Otherwise, we would want to find the causes of the duplication and remove it.
# 
# For now, the more likely scenario is that these are merely duplicates and we should be able to simply dedupe them by taking, uniformly, the smaller value. Because there are not many rows that are affected by this, it seems like a good idea for now. I would reiterate though: it is important that we consult the vendor as to whether or not it would be possible for more than one user_id to be connected to the same order.
# 
# We do this below.

# In[21]:


#this will validatae that there are only 29 user_ids that are responsible for the duplication.
s = rawData[rawData.groupby('order_number')['user_id'].transform('nunique') > 1]["order_number"]
len(rawData[rawData['order_number'].isin(list(s))]['user_id'].unique())


# In[22]:


#this will validate that there are 1126 orders which are affected.
rawData[rawData.groupby('order_number')['user_id'].transform('nunique') > 1]["order_number"]


# In[23]:


#remove the remaining dupes
rawData['order_rank2'] = rawData.sort_values(["user_id"], ascending = [True]).groupby(
    ['order_number']).cumcount() + 1
rawData = rawData[rawData['order_rank2'] == 1]


# In[24]:


#prove that this is fixed
s = rawData[rawData.groupby('order_number')['user_id'].transform('nunique') > 1]["order_number"]
len(rawData[rawData['order_number'].isin(list(s))]['user_id'].unique())


# We are good on missing order_numbers and duplication. A final issue that we need to resolve with regards to the order_numbers is their data type. Is there any regularity to this column? Let's check this last and then we will have a pristine order_number column that we can use as a primary key!

# In[25]:


rawData["order_number"].apply(len).value_counts()


# As we can see from the above, the majority of the data are either 36 characters long or 19 characters long, possibly corresponding to the two different formats that we get from Uber and from Lyft. We will validate this below.
# 
# The others, though, appear to be missing digits. Let's validate the assumption that the two largest categories correspond to Uber and Lyft and then let's look at the remaining cases.

# In[26]:


#given that it is 36 characters long, which vendor is it?
rawData[rawData["order_number"].apply(lambda x: len(x) == 36)]['merchant_name'].value_counts()


# In[27]:


#given that it is 19 characters long, which vendor is it?
rawData[rawData["order_number"].apply(lambda x: len(x) == 19)]['merchant_name'].value_counts()


# In[28]:


#given that it is 13 characters long,which vendor is it?
rawData[rawData["order_number"].apply(lambda x: len(x) == 13)]['merchant_name'].value_counts()


# In[29]:


#given that it is 18 characters long, which vendor is it?
rawData[rawData["order_number"].apply(lambda x: len(x) == 18)]['merchant_name'].value_counts()


# In[30]:


#given that it is 9 characters long, which vendor it is?
rawData[rawData["order_number"].apply(lambda x: len(x) == 9)]['merchant_name'].value_counts()


# In[31]:


#given that it is 8 characters long, which vendor is it?
rawData[rawData["order_number"].apply(lambda x: len(x) == 8)]['merchant_name'].value_counts()


# Looks like our assumption was correct: **Uber order_numbers typically come in with 36 characters and Lyft order_numbers typically come in with 19 characters.** The others are likely deficient or corrupted order_numbers.
# 
# We would need to inquire as to why these came in corrupted. It makes sense for us to remove these bad rows from the data set and continue on, with a pristine order_number column which can be used as a primary key for the row.

# In[32]:


#make sure we keep the good order_numbers.
rawData = rawData[rawData["order_number"].apply(lambda x: len(x) >= 19)]


# In[33]:


rawData["order_number"].apply(len).value_counts()


# That concludes our look at the order_number field. This field should be useable as a primary key, and we will return to it in the later part of the notebook when we build our the final table.
# 
# ## DATE FIELDS
# 
# The next few fields can be treated together, as they are all dates and times for the row. The order_time seems to be the most impotant, since it specifies the date and time that the transaction occurred. Email_time can probably be handy, since I interpret that to be the time that the customer receives an email regarding the order. The next two columns, insert_time and update_time, are likely only used by the data provider to track when the row got inserted and when it was last updated. **These are less useful, I think, because they are likely bound to the data provider's systema and not the source data from Uber and Lyft.**
# 
# While we are on the subject of fields that are bound to the data vendor and likely have little bearing on the analysis, I would also include the following fields in that set:
# 
# - **checksum:** This has the same structure as a standard MD5 hash sum and is not something we need to worry about.
# - **delivery_date:** This seems to be the date that the data was delivered from the vendor.
# - **start_source_folder_date:** This likely corresponds to a date on the backend.
# - **end_source_folder_date:** This is similar to start_source_folder_date.
# - **file_id:** This is likely the ID of the file on the vendor's side.
# - **source_dttimestamp:** This is likely a timestamp indicating when the file was last modified by the source.
# - **dttimestamp:** This may be a field that the reseller of the data uses. It is not immediately clear on how this relates to source_dttimestamp, but it is likely another "bookkeeping" column.
# 
# These fields might be important if we were loading this data into a relational database or archiving it in some sort of data warehouse and would likely be loaded just for completeness, but for the purposes of this exercise, they are ignored since they do not provide any immediate insights.
# 
# We will try to work with order_time, and if for some reason that value is missing, I think that we should use the email_time in its place.
# 
# For order_time, we want to identify if there are any missing values, and to see if they are all the same type (that is, a datetime). Potentially, we will want to split this field into dates and times to faciltate analysis. So let's do that first.

# In[34]:


#Extract the order date.
rawData['date_of_order'] = rawData["order_time"].apply(
    lambda x: str(x).replace(".000","")).apply(
        lambda y: y[0:11])


# In[35]:


#Extract the order time.
rawData['time_of_order'] = rawData["order_time"].apply(
    lambda x: str(x).replace(".000","")).apply(
        lambda y: y[12:21])


# After we have done this, we next need to look into which ones are not valid dates. To replace these, we will want to use the email date and time, since these should be reasonably close to the actual date of the transaction.

# In[36]:


#Get the cases where the time is empty. This is a clear indication that the original was NaN.
rawData[rawData["time_of_order"] == ""]


# In[37]:


#Another way to produce the set above.
rawData[rawData["date_of_order"] == 'nan']


# In[38]:


#For those cases where the order time is empty, use the time from the email_time field.
rawData.loc[rawData.time_of_order == "","time_of_order"] = rawData["email_time"].apply(
    lambda x: str(x).replace(".000","")).apply(
        lambda y: y[12:21])


# In[39]:


#Validate that there is an order time for all rows now.
rawData[rawData["time_of_order"] == ""]


# In[40]:


#For those cases where the order date is empty, use the date from the email_time field.
rawData.loc[rawData.date_of_order == "nan","date_of_order"] = rawData["email_time"].apply(
    lambda x: str(x).replace(".000","")).apply(
        lambda y: y[0:11])


# In[41]:


#Validate that there is an order date for all rows now.
rawData[rawData["date_of_order"] == 'nan']


# That concludes our treatment of the date and time fields.
# 
# ## QUANTITATIVE TRANSACTION FIELDS
# 
# The next fields that we will treat which can be considered together are the quantitative fields associated with the transaction. Those are:
# 
# - **order_total_amount**: Assumed to be a dollar amount.
# - **order_points**: Assumed to be an integer.
# - **order_shipping**: Assumed to be a dollar amount.
# - **order_tax**: Assumed to be a dollar amount.
# - **order_subtotal**: Assumed to be a dollar amount.
# - **order_total_qty**: Assumed to be an integer.
# - **item_quantity**: Assumed to be an integer.
# - **item_price**: Assumed to be a dollar amount.
# - **order_discount**: Assumed to be a dollar amount.
# 
# For each of these, we would expect them all to be numeric. All the dollar values should be floats, and the ones that I would expect to be integral are tagged as such above. Apart from their numerical integrity, we will want to flag any cases where these values are negative and what that would mean. Finally, we will likely want to check that the data are internally consistent. What this means is that there is some equation that holds for the row. Here are a few contenders to check:
# 
# order_total_amount = order_subtotal + order_tax + order_shipping - order_discount
# item_price * item_quantity = order_subtotal
# 
# We will run all of these checks below.

# In[42]:


#check for negative order_total_amount.
rawData[rawData["order_total_amount"] < 0]


# In[43]:


#check for null order_total_amount.
rawData[rawData.order_total_amount.isnull()]


# In[44]:


#check for non-null order_points
rawData[rawData.order_points.notnull()]


# In[45]:


#check for non-null order_shipping.
rawData[rawData.order_shipping.notnull()]


# In[46]:


#check for non-null order_tax.
rawData[rawData.order_tax.notnull()]


# In[47]:


#check for negative order_tax.
rawData[rawData.order_tax.notnull()]['order_tax'].apply(lambda x: x < 0).value_counts()


# In[48]:


#check for non-null order_subtotal.
rawData[rawData.order_subtotal.notnull()]


# In[49]:


#check for negative order_subtotals.
rawData[rawData.order_subtotal.notnull()]['order_subtotal'].apply(lambda x: x < 0).value_counts()


# In[50]:


#check for non-null order_total_qty.
rawData[rawData.order_total_qty.notnull()]


# In[51]:


#check for negative order_total_qty
rawData[rawData.order_total_qty.notnull()]['order_total_qty'].apply(lambda x: x < 0).value_counts()


# In[52]:


#check distribution for order_total_qty.
rawData.order_total_qty.value_counts()


# In[53]:


#check for non-null item_quantity.
rawData[rawData.item_quantity.notnull()]


# In[54]:


#check for negative item_quantity.
rawData[rawData.item_quantity.notnull()]['item_quantity'].apply(lambda x: x < 0).value_counts()


# In[55]:


#check item_quantity distribution.
rawData.item_quantity.value_counts()


# In[56]:


#check for non-null item_price
rawData[rawData.item_price.notnull()]


# In[57]:


#check for negative item_price
rawData[rawData.item_price.notnull()]['item_price'].apply(lambda x: x < 0).value_counts()


# In[58]:


#check for distribution of item_price.
rawData.item_price.value_counts()


# In[59]:


#check for non-null order_discount.
rawData[rawData.order_discount.notnull()]


# In[60]:


#check for negative order_discount.
rawData[rawData.order_discount.notnull()]['order_discount'].apply(lambda x: x < 0).value_counts()


# In[61]:


#Check order_discount distribution.
rawData.order_discount.value_counts()


# Well, I am pleasantly surprised that the numeric integrity checks look pretty solid! Here is a column-by-column summary for the numerical transaction fields:
# 
# - **order_total_amount:** This field is never negative and appears to be mostly correct as a dollar amount, with only a meager 282 rows that are NaN. Action for this field is to simply remove those rows that have a NaN for their order_total_amount (these are likely bad rows).
# 
# - **order_points, order_shipping:** These are ALWAYS NaN and as such, we can dismiss them. Be gone, children of the void!
# 
# - **order_tax:** This field is never negative, but does have a value of NaN most of the time. The fact that it does have non-zero and well-defined numbers the rest of the time means that we will want to include it, and set the cases where it is NaN to be 0.
# 
# - **order_subtotal:** This field is never negative, but does have some NaNs. For these cases, we should set the subtotal to 0 and see what the order_total_amount gives us. We may also be able to manually calculate it based on the other values (item_quantity and item_price).
# 
# - **order_total_qty, item_quantity:** These fields are always present, and always equal to the same value: 1. As a result, we can safely ignore them, and they greatly simplify the formulae I wrote in the earlier blocks.
# 
# - **item_price:** This is never negative nor is it NaN. We can use this for calculation checks in the next section.
# 
# - **order_discount:** This field is never negative, and has a numeric value some of the time. Other times, it is NaN. For these cases, we will handle it like order_tax and set those equal to 0.
# 
# In the below blocks, we implement the changes I mentioned above.

# In[62]:


rawData = rawData[rawData.order_total_amount.notnull()]
rawData.loc[rawData.order_tax.isnull(),"order_tax"] = 0
rawData.loc[rawData.order_discount.isnull(),"order_discount"] = 0
rawData.loc[rawData.order_subtotal.isnull(),"order_subtotal"] = 0


# Now we want to implement our formulae to do some integrity checks. The formulae that we were considering before were:
# 
# order_total_amount = order_subtotal + order_tax + order_shipping - order_discount
# item_price * item_quantity = order_subtotal
# 
# Note that the first formula simplifies to:
# 
# order_total_amount = order_subtotal + order_tax - order_discount
# 
# And the second simplifies to:
# 
# item_price = order_subtotal
# 
# Let's check these out.

# In[63]:


#Check formula 1
(rawData.order_total_amount == rawData.order_subtotal + rawData.order_tax - rawData.order_discount).value_counts()


# In[64]:


#Check formula 2
(rawData.item_price == rawData.order_subtotal).value_counts()


# As we can see, formula 2 looks pretty good; most of the rows satisfy it. As fara as formula 1 goes, it looks as though something is definitely missing. One possibility is that the discount should not be subtracted. Let's look at this possibility:

# In[65]:


#Modified formula 1
(rawData.order_total_amount == rawData.order_subtotal + rawData.order_tax).value_counts()


# This does even worse! Let's try one more:

# In[66]:


#Modified formula 1, one more time
(rawData.order_total_amount == rawData.order_subtotal).value_counts()


# Marginally better than the first, but still nothing to write home about.
# 
# Given the uncertain nature of these checks and the huge number of rows effected, I would say that we should not implement these integrity checks without further consultation from the vendor as far as removing rows. However, a follow-up to this case study should inquire as to why these formula checks are not passing. The question will be noted; for now, let's move on.

# ## PRODUCT FIELDS
# 
# The next round of fields that we need to investigate are those concerened with products. These are the following:
# 
# - product_description
# - product_subtitle
# - product_reseller
# - product_category
# - SKU
# - item_id
# 
# For these fields, the question is: what are their values? Are they informative? Are they redundant? Let's take a look.

# In[67]:


#What does this field show us?
rawData["product_description"]


# As the above snippet of the results indicates, this field is **rich** with information about the trip. In particular, we have access to the following information:
# 
# - trip duration, in hours, minutes and seconds.
# - trip distance, in miles
# - whether it was a shared fare (or pool), a standard fare, or an Uberx, as well as sometimes what sort of vehicle was used
# 
# We need to first identify the formats for each of these (their formats appear to differ from merchant to merchant) and separate out the data that is contained in these fields with some string manipulation.
# 
# There is a lot of potential here for us to further decompose this data. We can use a battery of regex expressions to identify the various patterns and store the data in their own columns. I will demonstrate this with a few regex expressions below for both Uber and Lyft.

# In[68]:


#Let's use some code to identify the regexes that we want for Uber.
uber = rawData[rawData.merchant_name == 'Uber']
[x for x in uber.product_description.astype(str) if 'miles' in x]

#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberX Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberX VIP Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   VIP Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   Express POOL Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberXL Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   Select Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberPOOL Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   LUX Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   BLACK CAR Car

#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberX Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberX VIP Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   VIP Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   Express POOL Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberXL Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   Select Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberPOOL Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   LUX Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   BLACK CAR Car


# In[69]:


#some other formats for the Uber cases.
[x for x in uber.product_description.astype(str) if 'miles' not in x]

#regex: UberX {d}.{d}{d} mi | {d}{d} min
#regex: UberX {d}.{d}{d} mi | {d} min
#regex: UberX {d}{d}.{d}{d} mi | {d}{d} min
#regex: UberX {d}{d}.{d}{d} mi | {d} min


# Looks promising from a regex perspective. Let's define some new columns and extract the data from this field.

# In[70]:


rawData.loc[:,"Distance_Traveled"] = 'NaN'
rawData.loc[:,"Trip_Time"] = 'NaN'
rawData.loc[:,"Product_Type"] = 'NaN'


# Now we use some of our regex magic to parse the data into these fields for Uber.

# In[71]:


rawData.loc[rawData.product_description.str.contains('^\d\.\d\d miles',na = False) == True,
            "Distance_Traveled"] = rawData[rawData.product_description.str.contains(
    '^\d\.\d\d miles',na = False)].product_description.apply(lambda x: x[0:4])

rawData.loc[rawData.product_description.str.contains('^\d\d\.\d\d miles',na = False) == True,
            "Distance_Traveled"] = rawData[rawData.product_description.str.contains(
    '^\d\d\.\d\d miles',na = False)].product_description.apply(lambda x: x[0:5])

rawData.loc[rawData.product_description.str.contains('^UberX \d\.\d\d',na = False) == True,
            "Distance_Traveled"] = rawData[rawData.product_description.str.contains(
    '^UberX \d\.\d\d',na = False)].product_description.apply(lambda x: x[6:10])

rawData.loc[rawData.product_description.str.contains('^UberX \d\d\.\d\d',na = False) == True,
            "Distance_Traveled"] = rawData[rawData.product_description.str.contains(
    '^UberX \d\d\.\d\d',na = False)].product_description.apply(lambda x: x[6:11])

rawData.loc[rawData.product_description.str.contains('^\d\.\d\d miles',na = False) == True,
            "Trip_Time"] = rawData[rawData.product_description.str.contains(
    '^\d\.\d\d miles',na = False)].product_description.apply(lambda x: x[13:21])

rawData.loc[rawData.product_description.str.contains('^\d\d\.\d\d miles',na = False) == True,
            "Trip_Time"] = rawData[rawData.product_description.str.contains(
    '^\d\d\.\d\d miles',na = False)].product_description.apply(lambda x: x[14:22])

rawData.loc[rawData.product_description.str.contains('^UberX \d\.\d\d mi \| \d\d min',na = False) == True,
            "Trip_Time"] = rawData[rawData.product_description.str.contains(
    '^UberX \d\.\d\d mi \| \d\d min',na = False)].product_description.apply(lambda x: x[16:18])

rawData.loc[rawData.product_description.str.contains('^UberX \d\.\d\d mi \| \d min',na = False) == True,
            "Trip_Time"] = rawData[rawData.product_description.str.contains(
    '^UberX \d\.\d\d mi \| \d min',na = False)].product_description.apply(lambda x: x[16:17])

rawData.loc[rawData.product_description.str.contains('^\d\.\d\d miles',na = False) == True,
            "Product_Type"] = rawData[rawData.product_description.str.contains(
    '^\d\.\d\d miles',na = False)].product_description.apply(lambda x: x[31:])

rawData.loc[rawData.product_description.str.contains('^\d\d\.\d\d miles',na = False) == True,
            "Product_Type"] = rawData[rawData.product_description.str.contains(
    '^\d\d\.\d\d miles',na = False)].product_description.apply(lambda x: x[32:])

rawData.loc[rawData.product_description.str.contains('^UberX \d\.\d\d mi',na = False) == True,
            "Product_Type"] = rawData[rawData.product_description.str.contains(
    '^UberX \d\.\d\d mi',na = False)].product_description.apply(lambda x: "UberX")

rawData.loc[rawData.product_description.str.contains('^UberX \d\.\d\d mi',na = False) == True,
            "Product_Type"] = rawData[rawData.product_description.str.contains(
    '^UberX \d\d\.\d\d mi',na = False)].product_description.apply(lambda x: "UberX")

#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberX Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberX VIP Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   VIP Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   Express POOL Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberXL Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   Select Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberPOOL Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   LUX Car
#regex: {d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   BLACK CAR Car

#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberX Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberX VIP Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   VIP Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   Express POOL Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberXL Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   Select Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   uberPOOL Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   LUX Car
#regex: {d}{d}.{d}{d} miles   {d}{d}:{d}{d}:{d}{d} Trip time   BLACK CAR Car

#regex: UberX {d}.{d}{d} mi | {d}{d} min
#regex: UberX {d}.{d}{d} mi | {d} min
#regex: UberX {d}{d}.{d}{d} mi | {d}{d} min
#regex: UberX {d}{d}.{d}{d} mi | {d} min


# In[72]:


#Now we do the same thing for Lyft
lyft = rawData[rawData.merchant_name == 'Lyft']
lyft["product_description"]

#regex: Lyft Fare (d.ddmi, ddm, dds)


# In[73]:


rawData.loc[rawData.product_description.str.contains(
    'Lyft fare',na = False) == True,"Distance_Traveled"] = rawData[rawData.product_description.str.contains(
    'Lyft fare',na=False)].product_description.apply(
    lambda x: x[x.find('('):x.find(')')+1]).apply(
    lambda y: y[y.find('(')+1:y.find(',')-2])

rawData.loc[rawData.product_description.str.contains(
    'Lyft fare',na = False) == True,"Trip_Time"] = rawData[rawData.product_description.str.contains(
    'Lyft fare',na=False)].product_description.apply(
    lambda x: x[x.find('('):x.find(')')+1]).apply(
    lambda y: y[y.find(',')+1:y.find('s')]).apply(
    lambda z: ('00:' + z[0:z.find('m')] + ':' + z[z.find('m') + 2:]).replace(' ','')).apply(
    lambda w: w[0:3] + '0' + w[3:] if w[4] == ':' else w).apply(
    lambda q: q[0:6] + '0' + q[6:] if len(q) == 7 else q)

rawData.loc[rawData.product_description.str.contains(
    'Lyft fare',na = False) == True,"Product_Type"] =rawData[rawData.product_description.str.contains(
    'Lyft fare',na=False)].product_description.apply(
    lambda x: x[0:x.find('(')])


# In[74]:


#distribution for product_type.
rawData.Product_Type.value_counts()


# In[75]:


#distribution for product_subtitle
rawData.product_subtitle.unique()


# In[76]:


#distribution for product_reseller.
rawData.product_reseller.value_counts()


# In[77]:


#product_category distribution.
rawData.product_category.value_counts()


# In[78]:


#distribution for SKU.
rawData.SKU.value_counts()


# In[79]:


#item_id distribution.
rawData.item_id.value_counts()


# So as we can see from all of the above, the only truly useful field is product_description, which allows us to infer several fields: travel time, distance traveled, and details about the ride itself (such as which car was used, whether it was VIP or pool, etc.).
# 
# ## MISCELLANEOUS FIELDS
# 
# This leaves us with the last bit of analysis on the the following miscellaneous columns:
# 
# - digital_transaction
# - order_pickup
# - from_domain
# - email_subject
# 
# We analyze the data in these fields below to see if there is anything useful that we can get out of them.

# In[80]:


#digital_transaction distribution.
rawData.digital_transaction.value_counts()


# In[81]:


#order_pickup distribution.
rawData.order_pickup.value_counts()


# In[82]:


#what happens when order_pickup is not 1?
rawData[rawData.order_pickup != 1]["email_subject"]


# In[83]:


#from_domain distribution
rawData.from_domain.value_counts()


# As the above code shows, order_pickup seems to indicate whether or not the transaction was a real pick-up or whether or not it was some sort of informational message, such as a correction. It makes sense on this basis, given the relatively small number of rows, to remove those values for order_pickup that are not 1.
# 
# Digital_Transaction is a useless field since it is always 0. The from_domain seems to have some regional data for the receipts that come from upstate or other countries (such as Israel). Other than that, I cannot see much use for it immediately for this analysis.
# 
# As such, we will reject rows with the condition that order_pickup is not 1, and select only those rows that we care about into a new dataframe, which we can use to perform analysis.

# In[84]:


rawData = rawData[rawData.order_pickup == 1]


# ## FINAL TABLE CREATION
# 
# We have gone through all of the columns and ascertained that some are more useful than others. We have also derived some new fields based on the columns that we had. The below code takes the useful fields and loads it into a final table, which also has an index on order_number. Since it is unique, we can now rest happily knowing that our set has a primary key.

# In[85]:


finalData = rawData[['merchant_name','user_id','order_number','order_total_amount','date_of_order',
                     'time_of_order','Distance_Traveled','Trip_Time','Product_Type']].copy()


# In[86]:


finalData.set_index('order_number')


# In[87]:


finalData.index.is_unique


# # PART 2: DATA ANALYSIS IDEAS
# 
# In the last part of this case study, we explore myriad ideas for doing something with this new dataset now that we have it. Here are some ideas for analysis that we could potentially pursue with this data:
# 
# - **Order Date and Time Analysis:** We could look into when orders are placed throughout the day for each merchant. Are they getting more business early in the morning? Late at night? What are the slow periods? We could also look into the _calendar dates_ for orders. For each merchant, what are the slow seasons? What are the busy times? How do weekends compare to holidays and weekdays? How do Fridays look compared to Thursdays?
# 
# - **Traffic Patterns and Speed:** Since we have derived the distance that each trip took and how long each trip took, we can derive the _average speed_ for the trips. We could potentially correlate this with the time of day that the trip occurred to infer traffic patterns on that day, in the region that they traveled!
# 
# - **Market Cap Analysis:** We could look at the sales for each merchant. If this dataset is representative, what is the relative difference between Uber and Lyft in terms of market cap (assuming that these two firms account for nearly 100% of the total rideshare market)? What if we partition the data by season; does that change?
# 
# - **Customer Retention Analysis:** We could look into the distribution of customers for both merchants. Which has more customers? For the customers in each firm's network, what is the average/median for the number of transactions per customer? What is the average/median spend per customer?
# 
# There are no doubt other possible cases to study, but in the interest of time and space, we will restrict ourselves to the first two. We leave the other two for future extensions of the case study.

# ## Order Date and Time Analysis
# 
# For this, we will want to partition each merchant and examine a plot of the order time for each. As a basic first step, we can look at histograms for each firm. The code below generates these histograms for Uber and Lyft.

# In[88]:


from matplotlib import pyplot as plt

uberTimes = finalData[finalData.merchant_name == 'Uber'].time_of_order
lyftTimes = finalData[finalData.merchant_name == 'Lyft'].time_of_order
uberTimes.dropna()
lyftTimes.dropna()

uberTimeInMinutes = uberTimes.apply(
    lambda x: 60*int(x[0:x.find(':')]) + int(x[x.find(':')+1:x.find(':')+3]))

lyftTimeInMinutes = lyftTimes.apply(
    lambda x: 60*int(x[0:x.find(':')]) + int(x[x.find(':')+1:x.find(':')+3]))

b = np.linspace(0,600,30)

plt.hist(uberTimeInMinutes, b, alpha=0.5,label = 'Uber')
plt.legend(loc = 'upper right')
plt.show()


# In[89]:


plt.hist(lyftTimeInMinutes ,b, alpha=0.5,label = 'Lyft')
plt.legend(loc = 'upper right')
plt.show()


# As we can see from the above, Uber and Lyft have some serious differences in their data. Lyft appears to have a valid time component,  which shows high usage in the wee hours of the morning (near 0, which is midnight), and then it gradually sinks in the afternoon, only to pick up again in the evening (just in time for people's evening commute).
# 
# As for Uber, most of the data are clustered around 0, which could either mean that the orders are overwhelmingly being placed close to midnight or (perhaps more likely) the time data for Uber are deficient for some reason. This is something that we could further investigate. As a test, let's see what it looks like if we exclude 0.

# In[90]:


uberTimeInMinutes = uberTimeInMinutes[uberTimeInMinutes > 0]
plt.hist(uberTimeInMinutes, b, alpha=0.5,label = 'Uber')
plt.legend(loc = 'upper right')
plt.show()


# As we can see, there are some nonzero elements here. This indicates that perhaps the time field is not entirely corrupt, but only that our logic for parsing it for Uber rows is insufficient. This would merit more investigation. We could use similar tools to investigate the distribution of dates as well, but we leave that as a future consideration and move on to speed and traffic patterns.

# ## Traffic Patterns and Speed
# 
# Since we have access to the total trip time and total travel time fields, we can determine the average and median speeds for each of Uber and Lyft. The below code handles this.

# In[120]:


uberSpeed = finalData[(finalData.merchant_name == 'Uber') & (finalData.Distance_Traveled.notnull()) & (
    finalData.Distance_Traveled.apply(lambda x: x != "NaN")) & (finalData.Trip_Time.notnull()) & (
    finalData.Trip_Time.apply(lambda x: x != "NaN"))]
uberSpeed = uberSpeed[['Distance_Traveled','Trip_Time']]
uberSpeed["Hours"] = uberSpeed.Trip_Time.apply(
    lambda x: int(x[0:2]) if x.find(":") > 0 else 0)
uberSpeed['Minutes'] = uberSpeed.Trip_Time.apply(
    lambda x: int(x[3:5])/60.00 if x.count(':') == 2 else 0)
uberSpeed = uberSpeed[uberSpeed.Hours + uberSpeed.Minutes > 0]
uberSpeed['Average_Speed'] = uberSpeed.Distance_Traveled.astype(float) / (uberSpeed.Hours.astype(float) + uberSpeed.Minutes.astype(float))
uberSpeed

b1 = np.linspace(0,100,15)

plt.hist(uberSpeed.Average_Speed,b1,alpha=0.5,label='Uber')
plt.legend(loc = 'upper right')
plt.show()


# In[156]:


lyftSpeed = finalData[(finalData.merchant_name == 'Lyft') & (finalData.Distance_Traveled.notnull()) & (
    finalData.Distance_Traveled.apply(lambda x: x != "NaN")) & (finalData.Trip_Time.notnull()) & (
    finalData.Trip_Time.apply(lambda x: x != "NaN"))]
lyftSpeed = lyftSpeed[['Distance_Traveled','Trip_Time']]

lyftSpeed["Hours"] = lyftSpeed.Trip_Time.apply(
    lambda x: int(x[0:2]) if x.find(":") > 0 else 0)

lyftSpeed['Minutes'] = lyftSpeed.Trip_Time.apply(
    lambda x: x[3:5])

lyftSpeed = lyftSpeed[lyftSpeed.Minutes.str.contains(":") == False]

lyftSpeed = lyftSpeed[lyftSpeed.Hours.astype(int) + lyftSpeed.Minutes.astype(int).apply(
lambda x: x/60.00) > 0]

lyftSpeed['Average_Speed'] = lyftSpeed.Distance_Traveled.astype(float) / (lyftSpeed.Hours.astype(float) + lyftSpeed.Minutes.astype(float).apply(
lambda x: x/60.00))


plt.hist(lyftSpeed.Average_Speed,b1,alpha=0.5,label='Lyft')
plt.legend(loc = 'upper right')
plt.show()


# As we can see from the above, the average speed for both firms appears similar.

# # FINAL THOUGHTS: EXTENSIONS AND QUESTIONS
# 
# ## Questions for the Vendor
# 
# Now that we have reached the end of the case study, I want to take this space to collect some of the questions that I would ask of the data provider, if given the opportunity. These come from the previous cells of analysis:
# 
# 1. Are User_Ids universally assigned?
# 2. Why would a row ever be misssing an order_number?
# 3. Why would there be 2 rows with the same order_numbere and the same user_id?
# 4. Is it possible for there to be 2 or more user_ids connected to the same order number?
# 5. Typically, it appears as though order_numbers for Uber are 36 character-long strings and those for Lyft are 19 character-long strings. Why do we get some few that do not conform to these standards?
# 6. Why is it the case that my order_total integrity checks failed? What is the relationship between order total, subtotal, tax, and discount?
# 
# ## Relational Database Modeling
# 
# Another point to make in ending the case study is that there are at least three different, normalized tables that one would create for this dataset. The following are the names of the tables and the fields from the file that I would associate with each:
# 
# - **Merchant**: This would have one row per merchant in the dataset. In this case, we have two: Uber and Lyft. The fields that I would associate with this table include: merchant_name.
# 
# - **User**: This would have one row per customer in the dataset. The fields would include: user_id.
# 
# - **Product**: This would have one row per product.
# 
# - **Order**: This would be our primary fact table. This table would have foreign keys to the Merchant, User, and Product tables. The fields that I would also include in this table from the dataset include: order_number, time_of_order, date_of_order, order_total_amount, order_tax, order_subtotal, order_total_qty, trip_time, distance_traveled, item_quantity, item_price, order_discount
# 
# Altogether, this would constitute a star schema. We could add additional fields to these tables as well, pending answers to some of our questions from the vendor.
