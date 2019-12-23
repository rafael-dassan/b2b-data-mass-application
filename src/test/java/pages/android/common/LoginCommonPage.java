package pages.android.common;

import element_mapping.android.LoginMapping;
import pages.android.AndroidAppiumActions;
import support.ReadJsonFile;

public class LoginCommonPage extends AndroidAppiumActions {

    public LoginMapping loginMapping;

    public LoginCommonPage() {
        this.loginMapping = new LoginMapping(driver);
    }

    public void fillLoginFieldsWithValidValues(){
        loginMapping.getEmailField().sendKeys(ReadJsonFile.getInfoInsideJsonByPath(new String[]{"users", "adm", "email"}));
        loginMapping.getPasswordField().sendKeys(ReadJsonFile.getInfoInsideJsonByPath(new String[]{"users", "adm", "password"}));
    }

    public void accessTheLoginScreen(){
        waitUntilElementIsVisible(loginMapping.getIntroEnterOption());
        loginMapping.getIntroEnterOption().click();
    }


//    public void swipePresentation() {
//        wait.until(ExpectedConditions.elementToBeClickable(this.loginMapping.getPresentationSlide()));
//        for(int i=0; i<=4; i++){
//            Common.swipeHorizontalRightToLeftElement(this.loginMapping.getPresentationSlide());
//        }
//        wait.until(ExpectedConditions.elementToBeClickable(this.loginMapping.getBtnStart()));
//        this.loginMapping.getBtnStart().click();
//    }
//
//    public void appRating() {
//        wait.until(ExpectedConditions.elementToBeClickable(this.loginMapping.getBtnRating()));
//        this.loginMapping.getBtnRating().click();
//        wait.until(ExpectedConditions.elementToBeClickable(this.loginMapping.getBtnQuestion()));
//        this.loginMapping.getBtnQuestion().click();
//        this.loginMapping.getTxtAddNotes().sendKeys("Executing automated test...");
//        this.loginMapping.getBtnRatingSubmit().click();
//        wait.until(ExpectedConditions.elementToBeClickable(this.loginMapping.getBtnFinishClassification()));
//        this.loginMapping.getBtnFinishClassification().click();
//    }
}
