from .adminAccountManagement import (upgrade_customer_to_admin as admin_signup, downgrade_customer_to_admin,
                                     change_account_status as status_control,
                                     admin_login, admin_logout, get_all_users)

from .customerAccountManagement import create_new_customer as user_signup, remove_customer_account as delete_account, \
    display_customer_account_details as get_customer, update_customer_account_details as update_customer, user_login
