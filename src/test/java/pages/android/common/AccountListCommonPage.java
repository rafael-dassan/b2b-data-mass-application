package pages.android.common;

import element_mapping.android.AccountListMapping;
import pages.android.AndroidAppiumActions;

public class AccountListCommonPage extends AndroidAppiumActions {
    public AccountListMapping accountListMapping;

    public AccountListCommonPage() {
        this.accountListMapping = new AccountListMapping(driver);
    }
}
