package support;

import base_screen.BaseScreen;
import cucumber.api.java.After;
import cucumber.api.java.Before;

public class Hooks extends BaseScreen {

	@Before(value = "@android")
	public void beforeMobileAndroid() {
		inicializarAppAdroid(Capabilities.ANDROID);
	}

	@Before(value = "@ios")
	public void beforeMobileIos() {
		inicializarAppIos(Capabilities.IOS);
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
