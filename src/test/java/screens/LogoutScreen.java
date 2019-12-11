package screens;

import base_screen.BaseScreen;
import org.openqa.selenium.support.ui.ExpectedConditions;
import page_objects.LogoutPage;

public class LogoutScreen extends BaseScreen {

    private LogoutPage logoutPage;

    public LogoutScreen() {
        this.logoutPage = new LogoutPage(driver);
    }

    public void openMenu() {
        wait.until(ExpectedConditions.elementToBeClickable(this.logoutPage.getBtnOpenMenu()));
        this.logoutPage.getBtnOpenMenu().click();
    }

}