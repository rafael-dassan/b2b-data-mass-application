import ssl
import pymongo


def get_database_params(country, environment, microservice):
    microservice_clients = {
        'order-service-ms': {
            'SIT': pymongo.MongoClient('mongodb+srv://order:khKNakyFgPfSpTPPyhg4nWY9RJAxeG@europe-sit.qi3as.azure.'
                                       'mongodb.net/?readPreference=nearest&maxStalenessSeconds=90&retryWrites=true&'
                                       'w=majority', ssl_cert_reqs=ssl.CERT_NONE),
            'UAT': pymongo.MongoClient('mongodb+srv://order:ZJT7QGYGFhudpvZfnM2NSBtcXTWVL9@europe-uat.cqllk.azure.'
                                       'mongodb.net/?readPreference=nearest&maxStalenessSeconds=90&retryWrites=true&'
                                       'w=majority', ssl_cert_reqs=ssl.CERT_NONE)
        }
    }
    client = microservice_clients[microservice][environment]

    params = {
        'order-service-ms': {
            'client': client,
            'db_name': 'Order',
            'collection_name': [
                '{0}-Orders'.format(country),
                '{0}-OrdersTransaction'.format(country),
                '{0}-OrdersTransparency'.format(country)
            ],
            'prefix': [
                'DMA-WEB',
                'DMA-ANDROID',
                'DMA-IOS'
            ]
        }
    }

    return params[microservice]


def delete_from_database(client, db_name, collection_name, prefix):
    db = client[db_name]

    for i in range(len(collection_name)):
        collection = db[collection_name[i]]
        for j in range(len(prefix)):
            collection.remove({'_id': {'$regex': '{0}.*'.format(prefix[j])}})
