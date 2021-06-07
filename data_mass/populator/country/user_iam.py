from data_mass.populator.log import *
from data_mass.user.assertion import assert_email_request
from data_mass.user.authorization import authorize_load_request
from data_mass.user.creation import create_user
from data_mass.user.user import get_iam_b2c_params

logger = logging.getLogger(__name__)


def populate_users_iam_b2c(country, environment, dataframe_users):
    if dataframe_users is not None:
        dataframe_users.apply(apply_populate_user_iam_b2c, args=(country, environment), axis=1)


def apply_populate_user_iam_b2c(row, country, environment):
    populate_user_iam_b2c(country, environment, row['username'], row['password'], row['account_ids'])


def populate_user_iam_b2c(country, environment, email, password, account_id):
    params = get_iam_b2c_params(environment, country)

    authorize_load_response = authorize_load_request(params)
    if authorize_load_response == "fail":
        logger.error('[authorize_load_request] User creation error for {0}.'.format(email))
    else:
        self_asserted_email_response = assert_email_request(
            email, params, authorize_load_response)
        if self_asserted_email_response == "user_exists":
            logger.debug('[self_asserted_email_request] User {0} already exists.'.format(email))
        elif self_asserted_email_response == "fail":
            logger.error('[self_asserted_email_request] User creation error for {0}.'.format(email))
        else:
            if len(account_id) > 0:
                for x in range(len(account_id)):
                    if not create_user(environment, country, email, password, account_id, account_id):
                        logger.error(log(Message.CREATE_USER_IAM_ERROR, {'email': email, 'account_id': account_id[x]}))
