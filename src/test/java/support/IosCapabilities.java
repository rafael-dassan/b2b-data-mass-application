package support;

import interfaces.MobileApplication;
import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import org.openqa.selenium.remote.DesiredCapabilities;

public enum IosCapabilities implements MobileApplication {

    IOS {
        public AppiumDriver<MobileElement> getDriver() {
            return getDriver(getCapabilitiesIos());
        }
    };

    private AppiumDriver<MobileElement> driver;

    public AppiumDriver<MobileElement> getDriver(DesiredCapabilities caps) {
        driver = new AppiumDriver<MobileElement>(caps);
        return driver;
    }

    private static DesiredCapabilities getCapabilitiesIos() {
        DesiredCapabilities caps = new DesiredCapabilities();
        caps.setCapability("platformName", "iOS");
        caps.setCapability("platformVersion", "12.1");
        caps.setCapability("udid", "");
        caps.setCapability("deviceName", "");
        caps.setCapability("automationName", "XCUITest");
        caps.setCapability("bundleId", "");
        caps.setCapability("usePrebuiltWDA", "true");
        caps.setCapability("app", "");
        caps.setCapability("noReset", "true");
        caps.setCapability("useNewWDA", "false");
        return caps;
    }
}





