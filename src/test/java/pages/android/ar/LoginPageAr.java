package pages.android.ar;

import element_mapping.android.LoginMapping;
import pages.android.common.LoginCommonPage;

public class LoginPageAr extends LoginCommonPage {

    private LoginMapping loginMapping;

    public LoginPageAr() {
        this.loginMapping = new LoginMapping(driver);
    }
}
