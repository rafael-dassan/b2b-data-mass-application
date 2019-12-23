package pages.android.za;

import element_mapping.android.LoginMapping;
import pages.android.common.LoginCommonPage;

public class LoginPageZa extends LoginCommonPage {

    private LoginMapping loginMapping;

    public LoginPageZa() {
        this.loginMapping = new LoginMapping(driver);
    }
}
