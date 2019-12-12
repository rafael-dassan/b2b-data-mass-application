package pages;

import data.CredentialsImpl;
import org.openqa.selenium.support.ui.ExpectedConditions;

import support.DriverConfig;
import element_mapping.UtilsMapping;

public class UtilsPage extends DriverConfig {

    private UtilsMapping utilsMapping;

    public UtilsPage() {
        this.utilsMapping = new UtilsMapping(driver);
    }

    public void loginData(String zona) {
        typeEmail(zona);
        typePassword(zona);
    }

    public boolean checkInitialScreen(){
        wait.until(ExpectedConditions.visibilityOfAllElements(this.utilsMapping.getBtnEnter()));
        return this.utilsMapping.getBtnEnter().isDisplayed();
    }

    public void clickEnter(){
        wait.until(ExpectedConditions.elementToBeClickable(this.utilsMapping.getBtnEnter()));
        this.utilsMapping.getBtnEnter().click();
    }

    public void typeEmail(String zona) {
        wait.until(ExpectedConditions.elementToBeClickable(this.utilsMapping.getLblEmail()));
        this.utilsMapping.getLblEmail().sendKeys(CredentialsImpl.valueOf(zona.toUpperCase().replaceAll(" ", "")).email());
    }

    public void typePassword(String zona) {
        wait.until(ExpectedConditions.elementToBeClickable(this.utilsMapping.getLblPassword()));
        this.utilsMapping.getLblPassword().sendKeys(CredentialsImpl.valueOf(zona.toUpperCase().replaceAll(" ", "")).senha());
    }

    public void clickLogin(){
        wait.until(ExpectedConditions.elementToBeClickable(this.utilsMapping.getBtnLogin()));
        this.utilsMapping.getBtnLogin().click();
    }

    public void clickLogout() {
        this.utilsMapping.getBtnLogout().click();
    }

}
