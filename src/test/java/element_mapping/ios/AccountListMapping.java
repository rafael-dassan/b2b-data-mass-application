package element_mapping.ios;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import org.openqa.selenium.support.PageFactory;
import support.DriverConfig;

public class AccountListMapping extends DriverConfig {
    public AccountListMapping(AppiumDriver<MobileElement> appiumDriver) {
        PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
    }

  @iOSXCUITFindBy(xpath = "(//XCUIElementTypeImage[@name=\"padlock\"])[1]")
  private MobileElement accountList;
    public MobileElement getAccountList() {
        return accountList;
    }
}