package pages;

import support.DriverConfig;
import org.openqa.selenium.support.ui.ExpectedConditions;
import element_mapping.LogoutMapping;

public class LogoutPage extends DriverConfig {

    private LogoutMapping logoutMapping;

    public LogoutPage() {
        this.logoutMapping = new LogoutMapping(driver);
    }

    public void openMenu() {
        wait.until(ExpectedConditions.elementToBeClickable(this.logoutMapping.getBtnOpenMenu()));
        this.logoutMapping.getBtnOpenMenu().click();
    }

}