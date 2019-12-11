package screens;

import base_screen.BaseScreen;
import common.Helper;
import org.openqa.selenium.support.ui.ExpectedConditions;
import page_objects.LoginPage;

public class LoginScreen extends BaseScreen {

    private LoginPage loginPage;

    public LoginScreen() {
        this.loginPage = new LoginPage(driver);
    }

    public void selectEnviroment(String enviroment){
        wait.until(ExpectedConditions.visibilityOfAllElements(this.loginPage.getScreenLogin()));
        Helper.swipeForEnvironment(this.loginPage.getScreenLogin());
        Helper.clicarElementoCustom(this.loginPage.getRb_Ambiente(enviroment));
    }

    public void selectAccount() {
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtnAccount()));
        this.loginPage.getBtnAccount().click();
    }

    public boolean checkCarouselLogin(){
        wait.until(ExpectedConditions.visibilityOfAllElements(this.loginPage.getImgCarousel()));
        return this.loginPage.getImgCarousel().isDisplayed();
    }

    public void swipePresentation() {
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getPresentationSlide()));
        for(int i=0; i<=4; i++){
            Helper.swipeHorizontalRightToLeftElement(this.loginPage.getPresentationSlide());
        }
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtnStart()));
        this.loginPage.getBtnStart().click();
    }

    public void appRating() {
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtnRating()));
        this.loginPage.getBtnRating().click();
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtnQuestion()));
        this.loginPage.getBtnQuestion().click();
        this.loginPage.getTxtAddNotes().sendKeys("Executing automated test...");
        this.loginPage.getBtnRatingSubmit().click();
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtnFinishClassification()));
        this.loginPage.getBtnFinishClassification().click();
    }
}
