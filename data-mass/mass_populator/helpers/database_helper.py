import ssl
import pymongo
from mass_populator.log import *

logger = logging.getLogger(__name__)


def get_database_params(country, environment, microservice):
    microservice_uris = {
        'order-service-ms': {
            'SIT': 'mongodb+srv://order:khKNakyFgPfSpTPPyhg4nWY9RJAxeG@europe-sit.qi3as.azure.mongodb.net/?readPreference=nearest&'
                   'maxStalenessSeconds=90&retryWrites=true&w=majority',
            'UAT': 'mongodb+srv://order:ZJT7QGYGFhudpvZfnM2NSBtcXTWVL9@vienna.rmqag.mongodb.net/?readPreference=nearest&'
                   'maxStalenessSeconds=90&retryWrites=true&w=majority'
        }
    }
    mongo_uri = microservice_uris[microservice][environment]

    try:
        client = pymongo.MongoClient(mongo_uri, ssl_cert_reqs = ssl.CERT_NONE)

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
                    'DMA-IOS',
                    'DM-'
                ]
            }
        }
    except pymongo.errors.PyMongoError as e:
        logger.error(e)
        SystemExit()

    return params[microservice]


def delete_from_database_by_id(client, db_name, collection_name, prefix):
    try:
        db = client[db_name]
        for i in range(len(collection_name)):
            collection = db[collection_name[i]]
            for j in range(len(prefix)):
                collection.remove({'_id': {'$regex': '{0}.*'.format(prefix[j])}})
    except pymongo.errors.PyMongoError as e:
        logger.error(e)
        SystemExit()


def delete_from_database_by_account(client, db_name, collection_name, account_id):
    try:
        db = client[db_name]
        for i in range(len(collection_name)):
            collection = db[collection_name[i]]
            collection.remove({'accountId': account_id})
    except pymongo.errors.PyMongoError as e:
        logger.error(e)
        SystemExit()
