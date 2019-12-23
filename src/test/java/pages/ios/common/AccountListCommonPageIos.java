package pages.ios.common;

import element_mapping.ios.AccountListMapping;
import element_mapping.ios.LoginMapping;
import pages.ios.IosAppiumActions;

public class AccountListCommonPageIos extends IosAppiumActions {
    public AccountListMapping accountListMapping;

    public AccountListCommonPageIos() {
        this.accountListMapping = new AccountListMapping(driver);
    }

}
