package pages.android.cl;

import element_mapping.android.LoginMapping;
import pages.android.common.LoginCommonPage;

public class LoginPageCl extends LoginCommonPage {

    private LoginMapping loginMapping;

    public LoginPageCl() {
        this.loginMapping = new LoginMapping(driver);
    }
}
