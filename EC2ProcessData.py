from boto import kinesis
import mysql.connector
import time
import json


mydb = mysql.connector.connect(
  host=HOST,
  user=USER,
  passwd=PASSWORD,
  db=DB
)

cursor = mydb.cursor()

kinesis = kinesis.connect_to_region('us-east-1')

shard_id = 'shardId-0000000000000'

shard_it = kinesis.get_shard_iterator(MYSTREAM, shard_id, 'LATEST')['ShardIterator']



while 1==1:
  print("getting record")
  out = kinesis.get_records(shard_it,limit=1)
  for i in out['Records']:
    recordId = json.loads(i['Data'])['SaleId']['N']
    productId = json.loads(i['Data'])['ProductId']['N']
    quantity = json.loads(i['Data'])['Quantity']['N']
    saleDate = json.loads(i['Data'])['SaleDate']['S']
    inv_quantity = 0 - int(quantity)

    add_record = "INSERT INTO FactInventory (idFactInventory, ProductID, QuantityChange, DateTime) VALUES (%s, %s, %s, %s)"
data_record = {
      'record_no': recordId,
      'productID': productId,
      'quantity': quantity,
      'dateTime': saleDate,
    }
    cursor.execute(add_record, (str(recordId), str(productId), str(inv_quantity), str(saleDate)))
    mydb.commit()
  shard_it = out['NextShardIterator']
  time.sleep(5)
