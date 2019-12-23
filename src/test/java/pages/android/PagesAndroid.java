package pages.android;

import pages.android.common.AccountListCommonPage;
import pages.android.common.LoginCommonPage;

public class PagesAndroid extends PageFactoryAndroid {

    public PagesAndroid() {
    }

    public static LoginCommonPage loginPage() {
        return getLoginPage();
    }

    public static AccountListCommonPage accountListPage() {
        return getAccountPage();
    }

}
