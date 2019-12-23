package pages.ios;

import io.appium.java_client.ios.IOSTouchAction;
import io.appium.java_client.touch.offset.PointOption;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import support.DriverConfig;

import java.awt.*;

public class IosAppiumActions extends DriverConfig {

    public void waitUntilElementIsVisible(WebElement element){
        wait.until(ExpectedConditions.visibilityOf(element));
    }

    public void swipe(
//            WebElement element,
            Double fromX_percent, Double fromY_percent,
            Double toX_percent, Double toY_percent,
            Double duration
    ){
        IOSTouchAction touch = new IOSTouchAction (driver);
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        screenSize.getHeight();
        touch.longPress(PointOption.point(400,(int) (screenSize.getHeight() * fromY_percent)))
                .moveTo(PointOption.point(50,(int) (screenSize.getHeight() * toY_percent)))
                .release().perform();
    }
}
