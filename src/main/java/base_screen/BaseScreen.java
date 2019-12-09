package base_screen;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileDriver;
import io.appium.java_client.MobileElement;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;
import support.interfaces.MobileApplication;

import java.util.concurrent.TimeUnit;

public class BaseScreen {

    public static AppiumDriver<MobileElement> driver;
    protected static WebDriverWait wait;
    protected static WebDriverWait shortWait;

    public AppiumDriver<MobileElement> inicializarAppAdroid(MobileApplication mobileApplication) {
        driver = mobileApplication.getDriver();
        wait = new WebDriverWait(driver,20);
        return driver;
    }

    public AppiumDriver<MobileElement> inicializarAppIos(MobileApplication mobileApplication) {
        driver = mobileApplication.getDriver();
        wait = new WebDriverWait(driver,20);
        return driver;
    }

    public void closeApp(){
        driver.closeApp();
    }
}
