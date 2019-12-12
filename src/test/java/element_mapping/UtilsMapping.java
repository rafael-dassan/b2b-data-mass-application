package element_mapping;

import io.appium.java_client.MobileDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import org.openqa.selenium.support.PageFactory;

public class UtilsMapping {

    // *******Constructor*******//

    public UtilsMapping(MobileDriver appiumDriver) {
        PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
    }

    // *******Elements*******//

    @AndroidFindBy(id = "logIn")
    private MobileElement btnEnter;

    @AndroidFindBy(id = "username")
    private MobileElement lblEmail;

    @AndroidFindBy(id = "newPassword")
    private MobileElement lblPassword;

    @AndroidFindBy(id = "login")
    private MobileElement btnLogin;

    @AndroidFindBy(id = "logout")
    private MobileElement btnLogout;

    // *******getter and setters*******//

    public MobileElement getBtnEnter() {
        return btnEnter;
    }

    public MobileElement getLblEmail() {
        return lblEmail;
    }

    public MobileElement getLblPassword() {
        return lblPassword;
    }

    public MobileElement getBtnLogin() {
        return btnLogin;
    }

    public MobileElement getBtnLogout() {
        return btnLogout;
    }

}
