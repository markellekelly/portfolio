import pandas as pd
data = pd.read_csv('../Iowa_Liquor_Sales.csv', header=1,
                 names=["invoice", "date", "store_num", "store_name", "address",
                        "city", "zipcode", "county_num", "county","store_loc",
                        "category", "category_name", "vendor_num", "vendor_name",
                        "item_num", "item_desc", "pack", "bottle_vol_ml",
                        "state_bottle_cost", "state_bottle_retail", "bottles_sold",
                        "sale", "volume_sold_l", "volume_sold_gal"])

print("read in csv")
grp = data[['invoice','volume_sold_l','vendor_name']].groupby('vendor_name').agg({
                      'invoice':'count',
                      'volume_sold_l':'sum'
                     })
grp['avg_volume'] = grp['volume_sold_l']/grp['invoice']
std = grp['avg_volume'].std() *1.7
mean = grp['avg_volume'].mean()
grp['diff'] = grp['avg_volume']-mean
vendors = grp[grp['diff']>std].reset_index()['vendor_name'].unique()
def big_vol_vendors(x):
    if x in vendors:
        return 1
    return 0
data['big_vol_vendor'] = data['vendor_name'].apply(big_vol_vendors)
print("finished cleaning part 1")
data.drop(["invoice", "store_name", "address", "city", "zipcode", "county_num", "store_loc",
           "category", "vendor_num", "item_num", "item_desc",
           "pack", "bottle_vol_ml", "state_bottle_cost", "sale", "volume_sold_gal"], axis=1, inplace=True)
data["cost"] = data["state_bottle_retail"].apply(lambda x: str(x).replace("$", "")).astype(float)
data["total_retail"] = data["cost"] * data["bottles_sold"]
data["date"] = pd.to_datetime(data["date"])
print("finished cleaning part 2")
import numpy as np
def assign_type(x):
    if type(x) != str:
        return "Other"
    if "vodka" in x.lower():
        return "Vodka"
    if "tequila" in x.lower():
        return "Tequila"
    if "whiskey" in x.lower() or "whiskies" in x.lower():
        return "Whiskey"
    if "rum " in x.lower() or " rum" in x.lower():
        return "Rum"
    if "gin " in x.lower() or " gin" in x.lower():
        return "Gin"
    else:
        return "Other"
data['alcohol_type'] = data['category_name'].apply(assign_type)
data["vodka_bottles"] = np.where(data['alcohol_type']=='Vodka', data['bottles_sold'], 0)
data["tequila_bottles"] = np.where(data['alcohol_type']=='Tequila', data['bottles_sold'], 0)
data["whiskey_bottles"] = np.where(data['alcohol_type']=='Whiskey', data['bottles_sold'], 0)
data["rum_bottles"] = np.where(data['alcohol_type']=='Rum', data['bottles_sold'], 0)
data["gin_bottles"] = np.where(data['alcohol_type']=='Gin', data['bottles_sold'], 0)
data["other_bottles"] = np.where(data['alcohol_type']=='Other', data['bottles_sold'], 0)
data.drop('alcohol_type', axis=1, inplace=True)
print("finished cleaning part 3")
def big_vendor(x):
    #vendors with over 1000 entries in full dataset
    if x in ["BACARDI USA INC","Bacardi U.S.A., Inc.","Brown Forman Corp.","Brown-Forman Corporation",
            "Constellation Wine Company, Inc.","DIAGEO AMERICAS","Diageo Americas","E & J Gallo Winery",
            "E AND J GALLO WINERY","Heaven Hill Brands","Jim Beam Brands","Laird & Company",
             "Laird And Company","Luxco-St Louis","Phillips Beverage","Phillips Beverage Company",
            "Proximo","SAZERAC COMPANY INC", "SAZERAC NORTH AMERICA", "Sazerac Co., Inc.",
             "Sazerac North America"]:
        return 1
    return 0
data['big_vendor']= data['vendor_name'].apply(big_vendor) * data['bottles_sold']
print("finished all cleaning")
agg_data = (data.groupby([pd.Grouper(key='date', freq='2w'), data['county'].str.lower()])
                .agg({'store_num':'nunique', 
                      'volume_sold_l':'sum',
                      'total_retail':'sum',
                      'cost':'sum', 
                      'bottles_sold':'sum',
                      'vodka_bottles':'sum',
                      'tequila_bottles':'sum',
                      'whiskey_bottles':'sum',
                      'rum_bottles':'sum',
                      'gin_bottles':'sum',
                      'other_bottles':'sum',
                      'big_vendor':'sum',
                      'big_vol_vendor':'sum'
                     })
                .rename(columns={'store_num':'num_purchasers'}))
print("aggregated")
agg_data['avg_bottle_price'] = agg_data['cost'] / agg_data['bottles_sold']
agg_data['avg_vendor_size'] = agg_data['big_vendor'] / agg_data['num_purchasers']
agg_data['avg_vendor_vol'] = agg_data['big_vol_vendor'] / agg_data['num_purchasers']
agg_data.drop(['bottles_sold','big_vendor','big_vol_vendor','cost'], axis=1, inplace=True)
agg_data.to_csv("output.csv")