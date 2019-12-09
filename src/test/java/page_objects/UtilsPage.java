package page_objects;

import io.appium.java_client.MobileDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import org.openqa.selenium.support.PageFactory;

public class UtilsPage {

    // *******Construtor*******//

    public UtilsPage(MobileDriver appiumDriver) {
        PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
    }

    // *******Elements*******//

    @AndroidFindBy(id = "logIn")
    private MobileElement btn_Entrar;

    @AndroidFindBy(id = "username")
    private MobileElement lbl_email;

    @AndroidFindBy(id = "newPassword")
    private MobileElement lbl_senha;

    @AndroidFindBy(id = "login")
    private MobileElement btn_Login;

    @AndroidFindBy(id = "logout")
    private MobileElement btn_Logout;

    // *******getter and setters*******//

    public MobileElement getBtn_Entrar() {
        return btn_Entrar;
    }

    public MobileElement getLbl_email() {
        return lbl_email;
    }

    public MobileElement getLbl_senha() {
        return lbl_senha;
    }

    public MobileElement getBtn_Login() {
        return btn_Login;
    }

    public MobileElement getBtn_Logout() {
        return btn_Logout;
    }

    // *******getter and setters String*******//

}
