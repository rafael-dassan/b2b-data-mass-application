package pages;

import support.DriverConfig;
import support.Common;
import org.openqa.selenium.support.ui.ExpectedConditions;
import element_mapping.LoginMapping;

public class LoginPage extends DriverConfig {

    private LoginMapping loginMapping;

    public LoginPage() {
        this.loginMapping = new LoginMapping(driver);
    }

    public void selectEnviroment(String enviroment){
        wait.until(ExpectedConditions.visibilityOfAllElements(this.loginMapping.getScreenLogin()));
        Common.swipeForEnvironment(this.loginMapping.getScreenLogin());
        Common.clicarElementoCustom(this.loginMapping.getRb_Ambiente(enviroment));
    }

    public void selectAccount() {
        wait.until(ExpectedConditions.elementToBeClickable(this.loginMapping.getBtnAccount()));
        this.loginMapping.getBtnAccount().click();
    }

    public boolean checkCarouselLogin(){
        wait.until(ExpectedConditions.visibilityOfAllElements(this.loginMapping.getImgCarousel()));
        return this.loginMapping.getImgCarousel().isDisplayed();
    }

    public void swipePresentation() {
        wait.until(ExpectedConditions.elementToBeClickable(this.loginMapping.getPresentationSlide()));
        for(int i=0; i<=4; i++){
            Common.swipeHorizontalRightToLeftElement(this.loginMapping.getPresentationSlide());
        }
        wait.until(ExpectedConditions.elementToBeClickable(this.loginMapping.getBtnStart()));
        this.loginMapping.getBtnStart().click();
    }

    public void appRating() {
        wait.until(ExpectedConditions.elementToBeClickable(this.loginMapping.getBtnRating()));
        this.loginMapping.getBtnRating().click();
        wait.until(ExpectedConditions.elementToBeClickable(this.loginMapping.getBtnQuestion()));
        this.loginMapping.getBtnQuestion().click();
        this.loginMapping.getTxtAddNotes().sendKeys("Executing automated test...");
        this.loginMapping.getBtnRatingSubmit().click();
        wait.until(ExpectedConditions.elementToBeClickable(this.loginMapping.getBtnFinishClassification()));
        this.loginMapping.getBtnFinishClassification().click();
    }
}
