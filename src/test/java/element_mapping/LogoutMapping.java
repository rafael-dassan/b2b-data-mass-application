package element_mapping;

import io.appium.java_client.MobileDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import org.openqa.selenium.support.PageFactory;

public class LogoutMapping {

    public LogoutMapping(MobileDriver appiumDriver) {
        PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
    }

    @AndroidFindBy(xpath = "//android.widget.ImageButton[@content-desc='Menu btn']")
    private MobileElement btnOpenMenu;

    @AndroidFindBy(id = "action_close")
    private MobileElement btnCloseAction;

    // *******getter and setters*******//

    public MobileElement getBtnOpenMenu() {
        return btnOpenMenu;
    }

    public MobileElement getBtnCloseAction() {
        return btnCloseAction;
    }

}
