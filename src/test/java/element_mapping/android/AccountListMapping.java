package element_mapping.android;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import org.openqa.selenium.support.PageFactory;
import support.DriverConfig;

public class AccountListMapping extends DriverConfig {
    public AccountListMapping(AppiumDriver<MobileElement> appiumDriver) {
        PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
    }

    @AndroidFindBy(id = "name")
    private MobileElement enterOption;
    public MobileElement getEnterOption() {
        return enterOption;
    }

    @AndroidFindBy(id = "account_recyclerview")
    private MobileElement accountListSection;
    public MobileElement getAccountListSection() {
        return accountListSection;
    }

    public MobileElement[] accountList = driver.findElementsById("name").toArray(new MobileElement[0]);
}
