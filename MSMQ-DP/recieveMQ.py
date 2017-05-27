import pika
import datetime
import pymysql.cursors

mq_username = '####'
mq_password = '####'
mq_host = '####'
mq_queue = '####'
mq_exchange = '####'
mq_routing_key='####'

# 连接数据库
connect = pymysql.Connect(
    host='####',
    port=####,
    user='####',
    passwd='####',
    db='####',
    charset='####'
)

# 获取游标
cursor = connect.cursor()

# 建立连接connection到localhost
credentials = pika.PlainCredentials(mq_username, mq_password) 
# 默认guest/guest账号
connection = pika.BlockingConnection(pika.ConnectionParameters(mq_host))
# 创建虚拟连接channel
channel = connection.channel()

channel.basic_qos(prefetch_count=100)
print (' [*] Waiting for messages. To exit press CTRL+C')

resArr = []

# MS处理主逻辑
def callback(ch, method, properties, body):
	if body:		
		global resArr
		line = ''
		dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		line += dt+"|"+body.decode()+'\r\n'
		line = line.encode(encoding = "utf-8")
		resArr.append(line)
		channel.basic_ack(delivery_tag = method.delivery_tag)

		# 每100条插一次数据库
		if method.delivery_tag % 100==0:
			print(resArr)
			insertDB(resArr)
			resArr = []
			# time.sleep(5)

# 写库函数
def insertDB(reslines):
	for resline in reslines:
		sql = "INSERT INTO msmq_logs (ms_time, ms_content) VALUES ( '%s', '%s' )"
		ms_time = resline.decode().split('|')[0]
		ms_content = resline.decode().split('|')[1]
		cursor.execute(sql % (ms_time,ms_content))
	connect.commit()

channel.basic_consume(callback,queue=mq_queue,no_ack=False,)
channel.start_consuming()