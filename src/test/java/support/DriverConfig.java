package support;

import capabilities.MobileApplication;
import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import org.openqa.selenium.support.ui.WebDriverWait;

public class DriverConfig {

    public static AppiumDriver<MobileElement> driver;
//    public static FluentWait<WebDriver> wait;
    public static WebDriverWait wait;

    public AppiumDriver<MobileElement> createAndroidDriver(MobileApplication mobileApplication) {
        driver = mobileApplication.getDriver();
//        wait = new WebDriverWait(driver, 30).ignoring(NoSuchElementException.class);
        wait = new WebDriverWait(driver, 30);
        disableWarning();
        return driver;
    }

    public static void disableWarning() {
        System.err.close();
        System.setErr(System.out);
    }

    public AppiumDriver<MobileElement> createIosDriver(MobileApplication mobileApplication) {
        driver = mobileApplication.getDriver();
//        wait = new WebDriverWait(driver, 30).ignoring(NoSuchElementException.class);
        wait = new WebDriverWait(driver, 30);
        disableWarning();
        return driver;
    }

    public void closeApp(){
        driver.closeApp();
    }
}
