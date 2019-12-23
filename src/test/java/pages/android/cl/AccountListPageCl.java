package pages.android.cl;

import element_mapping.android.LoginMapping;
import pages.android.common.AccountListCommonPage;

public class AccountListPageCl extends AccountListCommonPage {
    private LoginMapping loginMapping;

    public AccountListPageCl() {
        this.loginMapping = new LoginMapping(driver);
    }
}
