package pages.ios.dr;

import element_mapping.ios.LoginMapping;
import pages.ios.common.LoginCommonPageIos;

public class LoginPageDrIos extends LoginCommonPageIos {

    private LoginMapping loginMapping;

    public LoginPageDrIos() { this.loginMapping = new LoginMapping(driver); }

}
