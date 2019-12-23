package pages.android.za;

import element_mapping.android.AccountListMapping;
import pages.android.common.AccountListCommonPage;

public class AccountListPageZa extends AccountListCommonPage {
    private AccountListMapping accountListMapping;
    public AccountListPageZa() {
        this.accountListMapping = new AccountListMapping(driver);
    }
}