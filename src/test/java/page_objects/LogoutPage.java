package page_objects;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import org.openqa.selenium.By;
import org.openqa.selenium.support.PageFactory;

import java.util.List;

import static base_screen.BaseScreen.driver;

public class LogoutPage {

    public LogoutPage(MobileDriver appiumDriver) {
        PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
    }

    @AndroidFindBy(xpath = "//android.widget.ImageButton[@content-desc='Menu btn']")
    private MobileElement btn_AbrirMenu;

    @AndroidFindBy(id = "action_close")
    private MobileElement btn_CloseAction;

    // *******getter and setters*******//

    public MobileElement getBtn_AbrirMenu() {
        return btn_AbrirMenu;
    }

    public MobileElement getBtn_CloseAction() {
        return btn_CloseAction;
    }

}
