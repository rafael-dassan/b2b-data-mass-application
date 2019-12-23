package support;

import capabilities.AndroidCapabilities;
import capabilities.IosCapabilities;
import cucumber.api.java.After;
import cucumber.api.java.Before;

public class Hooks extends DriverConfig {

    @Before()
    public void beforeMobile() {
        if (StaticVariable.getPlatformType().equalsIgnoreCase("android"))
            createAndroidDriver(AndroidCapabilities.ANDROID);
        else
            createIosDriver(IosCapabilities.IOS);
    }

//    @After()
//    public void afterMobile() {
//        super.closeApp();
//    }

}
