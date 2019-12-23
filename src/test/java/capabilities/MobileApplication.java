package capabilities;

import org.openqa.selenium.remote.DesiredCapabilities;
import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;

public interface MobileApplication {

	AppiumDriver<MobileElement> getDriver();
	AppiumDriver<MobileElement> getDriver(DesiredCapabilities caps);
}
