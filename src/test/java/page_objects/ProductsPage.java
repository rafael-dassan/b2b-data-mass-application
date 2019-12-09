package page_objects;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import org.openqa.selenium.support.PageFactory;

public class ProductsPage {

    public ProductsPage(AppiumDriver<MobileElement> appiumDriver) {
        PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
    }

    // *******Elements*******//

    @AndroidFindBy(id = "beerRecommenderAdd")
    private MobileElement btnRecommenderAdd;

    @AndroidFindBy(xpath = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout")
    private MobileElement lblLoadingTruck;

    @AndroidFindBy(id = "recommender_popup_close")
    private MobileElement btnClosePopupPedidoFacil;

    @AndroidFindBy(id = "recommender_popup_title")
    private MobileElement lblPopupTitle;

   @AndroidFindBy(id = "truck")
    private MobileElement btnTruck;


    // *******getter and setters*******//

    public MobileElement getBtnRecommenderAdd() {
        return btnRecommenderAdd;
    }

    public MobileElement getLblLoadingTruck() {
        return lblLoadingTruck;
    }

    public MobileElement getBtnClosePopupPedidoFacil() {
        return btnClosePopupPedidoFacil;
    }

    public MobileElement getLblPopupTitle() {
        return lblPopupTitle;
    }

    public MobileElement getBtnTruck() {
        return btnTruck;
    }
    

}
