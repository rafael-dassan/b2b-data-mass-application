package pages.ios.common;

import element_mapping.ios.LoginMapping;
import io.appium.java_client.MobileBy;
import io.appium.java_client.MobileElement;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;
import pages.ios.IosAppiumActions;
import support.ReadJsonFile;

public class LoginCommonPageIos extends IosAppiumActions {


    public LoginMapping loginMapping;

    public LoginCommonPageIos() {
        this.loginMapping = new LoginMapping(driver);
    }

    public void fillLoginFieldsWithValidValues(){
        waitUntilElementIsVisible(loginMapping.getEmailField());
        loginMapping.getEmailField().sendKeys(ReadJsonFile.getInfoInsideJsonByPath(new String[]{"users", "adm", "email"}));
        loginMapping.getPasswordField().sendKeys(ReadJsonFile.getInfoInsideJsonByPath(new String[]{"users", "adm", "password"}));
    }

    public void accessTheLoginScreen(){
        waitUntilElementIsVisible(loginMapping.getCloseRewardDialog());
        loginMapping.getCloseRewardDialog().click();
        for (int i = 0; i < 4; i++){
            swipe(0.3,0.5,0.1,0.5,1.0);
        }
        waitUntilElementIsVisible(loginMapping.getBegin());
        loginMapping.getBegin().click();
        loginMapping.getIntroEnterOption().click();

    }
}
