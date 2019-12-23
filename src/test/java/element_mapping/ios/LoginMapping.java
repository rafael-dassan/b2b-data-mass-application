package element_mapping.ios;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileBy;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.PageFactory;
import support.DriverConfig;

public class LoginMapping extends DriverConfig {
    public LoginMapping(AppiumDriver<MobileElement> appiumDriver) {
        PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
    }
    @iOSXCUITFindBy(accessibility = "Close In App Message")
    private MobileElement closeRewardDialog;
    public MobileElement getCloseRewardDialog() { return closeRewardDialog; }

    @iOSXCUITFindBy(xpath = "//XCUIElementTypeButton[@name=\"Inicio\"]")
    private MobileElement begin;
    public MobileElement getBegin() {
        return begin;
    }

    @iOSXCUITFindBy(accessibility = "landingLoginButton")
    private MobileElement introEnterOption;
    public MobileElement getIntroEnterOption() {
        return introEnterOption;
    }

    @iOSXCUITFindBy(accessibility = "Create an Account")
    private MobileElement introCreateAccountOption;
    public MobileElement getIntroCreateAccountOption() {
        return introCreateAccountOption;
    }

    @iOSXCUITFindBy(accessibility = "tst-login-txt-username")
    private MobileElement emailField;
    public MobileElement getEmailField() {
        return emailField;
    }

    @iOSXCUITFindBy(accessibility = "tst-login-txt-password")
    private MobileElement passwordField;
    public MobileElement getPasswordField() { return passwordField; }

    @iOSXCUITFindBy(accessibility = "tst-btn-login")
    private MobileElement enterOption;
    public MobileElement getEnterOption() { return enterOption; }

}
