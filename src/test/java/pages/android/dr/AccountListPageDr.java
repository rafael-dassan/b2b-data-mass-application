package pages.android.dr;

import element_mapping.android.AccountListMapping;
import pages.android.common.AccountListCommonPage;

public class AccountListPageDr extends AccountListCommonPage {
    private AccountListMapping accountListMapping;
    public AccountListPageDr() {
        this.accountListMapping = new AccountListMapping(driver);
    }
}
