package pages.ios;

import pages.ios.common.AccountListCommonPageIos;
import pages.ios.common.LoginCommonPageIos;

public class PagesIos extends PageFactoryIos {


    public static LoginCommonPageIos loginPage() {
        return getLoginPageIos();
    }

    public static AccountListCommonPageIos accountListPage() {
        return getAccountListPage();
    }

}
