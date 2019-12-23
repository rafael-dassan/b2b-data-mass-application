package element_mapping.android;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import org.openqa.selenium.support.PageFactory;

public class LoginMapping {


    public LoginMapping(AppiumDriver<MobileElement> appiumDriver) {
        PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
    }

    @AndroidFindBy(id = "logIn")
    private MobileElement introEnterOption;
    public MobileElement getIntroEnterOption() {
        return introEnterOption;
    }

    @AndroidFindBy(id = "createAccount")
    private MobileElement introCreateAccountOption;
    public MobileElement getIntroCreateAccountOption() {
        return introCreateAccountOption;
    }

    @AndroidFindBy(xpath = "//android.widget.EditText[contains(@resource-id,'sername')]")
    private MobileElement emailField;
    public MobileElement getEmailField() {
        return emailField;
    }

    @AndroidFindBy(xpath = "//android.widget.EditText[contains(@resource-id,'Password')]")
    private MobileElement passwordField;
    public MobileElement getPasswordField() {
        return passwordField;
    }

    @AndroidFindBy(xpath = "//android.widget.Button[contains(@resource-id,'login')]")
    private MobileElement enterOption;
    public MobileElement getEnterOption() {
        return enterOption;
    }

}
