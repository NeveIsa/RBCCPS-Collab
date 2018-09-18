import yaml,pprint,pika


with open("config.yaml") as f:
    config = yaml.load(f)
    print("==="*30)
    pprint.pprint(config)
    print("==="*30)



# Step #1: Connect to RabbitMQ using the default parameters

credentials = pika.PlainCredentials(config["device"]["name"],config["device"]["apikey"])
parameters = pika.ConnectionParameters(config["server"]["host"],config["server"]["port"],'/',credentials)


