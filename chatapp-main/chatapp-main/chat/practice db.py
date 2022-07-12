import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["newdatabase"]
my_col = mydb["customers"]


def showdb():
    asrt = my_col.find({}, {"_id": False}).sort("name", -1)
    for i in asrt:
        print("db b4 deletion:"+str(k), i)


print("..............................show specific/read specific cols...........................................")
for x in my_col.find({}, {"_id": 0, "name": 1, "address": 1, "phone":1}):
    print(x)

print("..............................Advanced queries...........................................")
print("..............................start with something(D)...........................................")

myquer = {"name": {"$regex": "^D"}}
mydocs = my_col.find(myquer)
for k in mydocs:
    print("names starting with D are :", k)

print("..............................greater than 'R'...........................................")

gthan = {"name": {"$gt": "R"}}
res = my_col.find(gthan)
for z in res:
    print("names starting with greater than R",z)

print("..............................sort in ascending names...........................................")

asrt = my_col.find({},{"_id":False}).sort("name")

for x in asrt:
    print("sorted in ascending order", x)


print("..............................sort in descending names...........................................")

asrt = my_col.find({},{"_id":False}).sort("name",-1)

for x in asrt:
    print("sorted in descending order", x)

print("..............................delete...........................................")
mydict = {"name": "Johnny", "address": "Highway 337"}

record = my_col.insert_one(mydict)
print("one value inserted for deletion:", record)

#
# for i in asrt:
#     print("db b4 deletion:", i)
showdb()

my_col.delete_one(mydict)
print("db after deletion")
showdb()

print("..............................delete many starting with aisa waisa...........................................")


myqueryy = {"name": {"$regex": "^J"}}

x = my_col.delete_many(myqueryy)

print(x.deleted_count, " documents deleted.")





////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["newdatabase"]
my_col = mydb["customers"]


print("........................names of databases..........................................")
print(myclient.list_database_names())

print("........................Single Entry into customer ..........................................")

single_entry = {"name": "Dev", "address": "pimpri", "phone": 7972221220}
x = my_col.insert_one(single_entry)
print("single entry done of:", x)

print("........................multiple Entry into customer ..........................................")

multi_entry = [
    {"name": "Shraddha", "address": "Pune", "phone": "9561959496"},
    {"name": "Maa", "address": "Pimpri", "phone": "9766656370"},
    {"name": "Dad", "address": "Gonda", "phone": "9822889401"},
    {'name': 'John', 'address': 'Highway 37','phone':'1234567897'}
]

y = my_col.insert_many(multi_entry)
print("muliple entires done of \n",y)

print("..............................search one/read 1st data...........................................")

x = my_col.find_one()
print("first data of customers is ", x)

print("..............................search many/read all...........................................")

for x in my_col.find():
    print("all data in customers table is /are \n :", x)


print("..............................search specific/read specific...........................................")
myquery = {'name': 'John', 'address': 'Highway 37','phone':'1234567897'}
mydoc = my_col.find(myquery)
for z in mydoc:
    print('here i m', z)



