package page_objects;

import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import org.openqa.selenium.support.PageFactory;

import io.appium.java_client.MobileDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AndroidFindBy;

public class OrdersPage {

	// *******Constructor*******//
	
	public OrdersPage(MobileDriver appiumDriver) {
		PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
	}

	// *******Elements*******//

 	// *******getter and setters*******//

	// *******getter and setters String*******//
}
