package support;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import org.openqa.selenium.support.ui.WebDriverWait;
import interfaces.MobileApplication;

public class DriverConfig {

    public static AppiumDriver<MobileElement> driver;
    protected static WebDriverWait wait;

    public AppiumDriver<MobileElement> createAndroidDriver(MobileApplication mobileApplication) {
        driver = mobileApplication.getDriver();
        wait = new WebDriverWait(driver,20);
        return driver;
    }

    public AppiumDriver<MobileElement> createIosDriver(MobileApplication mobileApplication) {
        driver = mobileApplication.getDriver();
        wait = new WebDriverWait(driver,20);
        return driver;
    }

    public void closeApp(){
        driver.closeApp();
    }
}
