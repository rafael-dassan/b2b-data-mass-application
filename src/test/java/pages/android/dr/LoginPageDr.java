package pages.android.dr;

import element_mapping.android.LoginMapping;
import pages.android.common.LoginCommonPage;

public class LoginPageDr extends LoginCommonPage {

    private LoginMapping loginMapping;

    public LoginPageDr() {
        this.loginMapping = new LoginMapping(driver);
    }

    public void accessTheLoginScreen(){
        waitUntilElementIsVisible(loginMapping.getEnterOption());
    }
}
