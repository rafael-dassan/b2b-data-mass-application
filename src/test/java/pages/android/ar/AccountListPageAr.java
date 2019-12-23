package pages.android.ar;

import element_mapping.android.AccountListMapping;
import pages.android.common.AccountListCommonPage;

public class AccountListPageAr extends AccountListCommonPage {
    private AccountListMapping accountListMapping;
    public AccountListPageAr() {
        this.accountListMapping = new AccountListMapping(driver);
    }
}
