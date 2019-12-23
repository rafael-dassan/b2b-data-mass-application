package capabilities;

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
        caps.setCapability("platformVersion", "13.3");
        caps.setCapability("udid", "6F3CF0FA-DB91-4AEC-A05A-655B6750CBF5");
        caps.setCapability("deviceName", "iPhone 11 Pro Max");
        caps.setCapability("automationName", "XCUITest");
        caps.setCapability("app", "/Users/diogodourado/ProjetosABI/temp-auto-test-internal/src/test/java/app/dr/Socios_Cerveceria.app");
        caps.setCapability("autoAcceptAlert", "true");
        caps.setCapability("autoLaunch","true");
        caps.setCapability("fullReset","false");
        caps.setCapability("newCommandTimeout","1800");
        caps.setCapability("launchTimeout","20000");
        caps.setCapability("language","en");
        caps.setCapability("clearSystemFiles","true");
        return caps;
    }
}
//        "platformName": "iOS",
//        "platformVersion": "12.2",
//                "udid" : "6F3CF0FA-DB91-4AEC-A05A-655B6750CBF5",
//        "deviceName": "iPhone X",
//        "app": "/Users/diogodourado/ProjetosABI/temp-auto-test-internal/src/test/java/app/dr/Socios_Cerveceria.app"





