package screens;

import enums.CredentialsImpl;
import org.openqa.selenium.support.ui.ExpectedConditions;

import base_screen.BaseScreen;
import page_objects.UtilsPage;

public class UtilsScreen extends BaseScreen {

    private UtilsPage utilsPage;

    public UtilsScreen() {
        this.utilsPage = new UtilsPage(driver);
    }

    public void loginData(String zona) {
        typeEmail(zona);
        typePassword(zona);
    }

    public boolean checkInitialScreen(){
        wait.until(ExpectedConditions.visibilityOfAllElements(this.utilsPage.getBtnEnter()));
        return this.utilsPage.getBtnEnter().isDisplayed();
    }

    public void clickEnter(){
        wait.until(ExpectedConditions.elementToBeClickable(this.utilsPage.getBtnEnter()));
        this.utilsPage.getBtnEnter().click();
    }

    public void typeEmail(String zona) {
        wait.until(ExpectedConditions.elementToBeClickable(this.utilsPage.getLblEmail()));
        this.utilsPage.getLblEmail().sendKeys(CredentialsImpl.valueOf(zona.toUpperCase().replaceAll(" ", "")).email());
    }

    public void typePassword(String zona) {
        wait.until(ExpectedConditions.elementToBeClickable(this.utilsPage.getLblPassword()));
        this.utilsPage.getLblPassword().sendKeys(CredentialsImpl.valueOf(zona.toUpperCase().replaceAll(" ", "")).senha());
    }

    public void clickLogin(){
        wait.until(ExpectedConditions.elementToBeClickable(this.utilsPage.getBtnLogin()));
        this.utilsPage.getBtnLogin().click();
    }

    public void clickLogout() {
        this.utilsPage.getBtnLogout().click();
    }

}
