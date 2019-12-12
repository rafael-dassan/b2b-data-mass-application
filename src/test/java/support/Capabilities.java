package support;

import java.io.IOException;
import java.util.Scanner;

import org.openqa.selenium.remote.DesiredCapabilities;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import interfaces.MobileApplication;

public enum Capabilities implements MobileApplication {

    ANDROID {
        @Override
        public AppiumDriver<MobileElement> getDriver() {
            return getDriver(getCapabilitiesAndroid());
        }
    },

    IOS {
        @Override
        public AppiumDriver<MobileElement> getDriver() {
            return getDriver(getCapabilitiesIos());
        }
    };

    private AppiumDriver<MobileElement> driver;

    @Override
    public AppiumDriver<MobileElement> getDriver(DesiredCapabilities caps) {
        driver = new AppiumDriver<MobileElement>(caps);
        return driver;
    }

    private static DesiredCapabilities getCapabilitiesAndroid() {
        Scanner scanner = null;
        try {
            scanner = new Scanner(Runtime.getRuntime()
                    .exec(new String[]{"/bin/bash", "-l", "-c", "adb get-serialno"}).getInputStream());
        } catch (IOException e1) {
            e1.printStackTrace();
        }

        String deviceSerialNumber = (scanner != null && scanner.hasNext()) ? scanner.next() : "";
        scanner.close();

        DesiredCapabilities caps = new DesiredCapabilities();
        caps.setCapability("noReset", "true");
        caps.setCapability("autoGrantPermission", "true");
        caps.setCapability("deviceName", "emulator-5554");
        caps.setCapability("platformName", "Android");
        caps.setCapability("udid", deviceSerialNumber);
        caps.setCapability("appPackage", "com.abinbev.android.tapwiser.dominicanRepublic.qa");
        caps.setCapability("appActivity", "com.abinbev.android.tapwiser.app.StartupActivity");
        return caps;
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
