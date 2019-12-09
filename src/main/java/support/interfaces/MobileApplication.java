package support.interfaces;


import io.appium.java_client.MobileDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.DesiredCapabilities;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;

public interface MobileApplication {

	public AppiumDriver<MobileElement> getDriver();

	AppiumDriver<MobileElement> getDriver(DesiredCapabilities caps);
}
