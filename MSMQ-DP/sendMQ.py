import pika

mq_username = '####'
mq_password = '####'
mq_host = '####'
mq_queue = '####'
mq_exchange = '####'
mq_routing_key='####'

#连接字符串
credentials = pika.PlainCredentials(mq_username, mq_password) 
connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host, credentials=credentials))
channel = connection.channel()

#循环消息发送
for i in range(1,101):
	messages = "This is the "+str(i)+"th message."
	channel.basic_publish(exchange=mq_exchange,routing_key=mq_routing_key,body=messages)
	print(" [x] "+messages)

#关闭连接
connection.close()