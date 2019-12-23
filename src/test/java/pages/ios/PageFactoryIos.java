package pages.ios;

import pages.ios.common.AccountListCommonPageIos;
import pages.ios.common.LoginCommonPageIos;
import pages.ios.dr.AccountListPageDrIos;
import pages.ios.dr.LoginPageDrIos;
import support.StaticVariable;

public class PageFactoryIos {
    private static String zone_name = StaticVariable.getZone();

    public PageFactoryIos(){}

    public static LoginCommonPageIos getLoginPageIos() {
        LoginCommonPageIos page = null;
        switch (zone_name.toLowerCase()) {
            case "ar":
            case "cl":
            case "dr":
                page = new LoginPageDrIos();
                break;
            case "za":
        }
        return page;
    }

    public static AccountListCommonPageIos getAccountListPage() {
        AccountListCommonPageIos page = null;
        switch (zone_name.toLowerCase()) {
            case "ar":
            case "cl":
            case "dr":
                page = new AccountListPageDrIos();
                break;
            case "za":
        }
        return page;
    }
}
