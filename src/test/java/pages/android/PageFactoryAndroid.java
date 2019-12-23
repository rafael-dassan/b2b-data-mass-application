package pages.android;

import pages.android.ar.AccountListPageAr;
import pages.android.ar.LoginPageAr;
import pages.android.cl.AccountListPageCl;
import pages.android.cl.LoginPageCl;
import pages.android.common.AccountListCommonPage;
import pages.android.common.LoginCommonPage;
import pages.android.dr.AccountListPageDr;
import pages.android.dr.LoginPageDr;
import pages.android.za.AccountListPageZa;
import pages.android.za.LoginPageZa;
import support.StaticVariable;

public class PageFactoryAndroid {
    private static String zone_name = StaticVariable.getZone();

    public PageFactoryAndroid(){}

    public static LoginCommonPage getLoginPage() {
        LoginCommonPage page = null;
        switch (zone_name.toLowerCase()) {
            case "ar":
                page = new LoginPageAr();
                break;
            case "cl":
                page = new LoginPageCl();
                break;
            case "dr":
                page = new LoginPageDr();
                break;
            case "za":
                page = new LoginPageZa();
                break;
        }
        return page;
    }

    public static AccountListCommonPage getAccountPage() {
        AccountListCommonPage page = null;
        switch (zone_name.toLowerCase()) {
            case "ar":
                page = new AccountListPageAr();
                break;
            case "cl":
                page = new AccountListPageCl();
                break;
            case "dr":
                page = new AccountListPageDr();
                break;
            case "za":
                page = new AccountListPageZa();
                break;
        }
        return page;
    }
}
