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
    private MobileElement btn_abrirMenu;

    @AndroidFindBy(id = "action_close")
    private MobileElement btn_closeAction;

    // *******getter and setters*******//

    public MobileElement getBtn_abrirMenu() {
        return btn_abrirMenu;
    }

    public MobileElement getBtn_closeAction() {
        return btn_closeAction;
    }

}
