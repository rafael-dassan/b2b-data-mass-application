from mass_populator.log import *
from user_creation_v3 import create_user
from user_creation_v3 import authenticate_user_iam
from account import check_account_exists_microservice

logger = logging.getLogger(__name__)


def populate_users_iam_b2c(country, environment, dataframe_users):
    if dataframe_users is not None:
        dataframe_users.apply(apply_populate_user_iam_b2c, args=(country, environment), axis=1)


def apply_populate_user_iam_b2c(row, country, environment):
    populate_user_iam_b2c(country, environment, row['username'], row['password'], row['account_ids'])


def populate_user_iam_b2c(country, environment, email, password, account_id):
    authenticate_response = authenticate_user_iam(environment, country, email, password)
    if authenticate_response == 'wrong_password':
        logger.info('The user {email} already exists, but the password is wrong'. format(email=email))
    elif authenticate_response != 'fail':
        logger.debug('The user {email} already exists. Skipping...'.format(email=email))
    else:
        if len(account_id) > 0:
            for x in range(len(account_id)):
                account_response = check_account_exists_microservice(account_id[x], country, environment)
                if account_response == 'false':
                    logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
                else:
                    if 'success' != create_user(environment, country, email, password, account_id, account_id):
                        logger.error(log(Message.CREATE_USER_IAM_ERROR, {'email': email, 'account_id': account_id[x]}))
