package support;

import cucumber.api.java.After;
import cucumber.api.java.Before;

public class Hooks extends DriverConfig {

	@Before(value = "@android")
	public void beforeMobileAndroid() {
		createAndroidDriver(AndroidCapabilities.ANDROID);
	}

	@Before(value = "@ios")
	public void beforeMobileIos() {
		createIosDriver(IosCapabilities.IOS);
	}

	@After(value = "@android")
	public void afterMobileAndroid() {
		super.closeApp();
	}

	@After(value = "@ios")
	public void afterMobileIos() {
		super.closeApp();
	}

}
