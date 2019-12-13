package support;

import interfaces.MobileApplication;
import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import org.openqa.selenium.remote.DesiredCapabilities;
import java.io.IOException;
import java.util.Scanner;

public enum AndroidCapabilities implements MobileApplication {
    ANDROID {
        public AppiumDriver<MobileElement> getDriver() {
            return getDriver(getCapabilitiesAndroid());
        }
    };

    private AppiumDriver<MobileElement> driver;

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
}
