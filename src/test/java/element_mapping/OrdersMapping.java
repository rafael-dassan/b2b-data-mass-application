package element_mapping;

import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import org.openqa.selenium.support.PageFactory;

import io.appium.java_client.MobileDriver;

public class OrdersMapping {

	// *******Constructor*******//
	
	public OrdersMapping(MobileDriver appiumDriver) {
		PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
	}

	// *******Elements*******//

 	// *******getter and setters*******//

	// *******getter and setters String*******//
}
