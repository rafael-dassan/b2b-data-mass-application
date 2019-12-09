package screens;

import base_screen.BaseScreen;
import org.openqa.selenium.support.ui.ExpectedConditions;
import page_objects.LogoutPage;

public class LogoutScreen extends BaseScreen {

    private LogoutPage logoutPage;

    public LogoutScreen() {
        this.logoutPage = new LogoutPage(driver);
    }

    public void abrirMenu() {
        wait.until(ExpectedConditions.elementToBeClickable(this.logoutPage.getBtn_abrirMenu()));
        this.logoutPage.getBtn_abrirMenu().click();
    }

}