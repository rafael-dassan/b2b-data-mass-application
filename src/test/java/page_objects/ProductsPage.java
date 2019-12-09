package page_objects;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.PageFactory;

public class ProductsPage {

    public ProductsPage(AppiumDriver<MobileElement> appiumDriver) {
        PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
    }

    // *******Elements*******//

    @AndroidFindBy(id = "beerRecommenderAdd")
    private MobileElement btn_recommenderAdd;

    @AndroidFindBy(xpath = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout")
    private MobileElement lbl_loadingTruck;

    @AndroidFindBy(id = "recommender_popup_close")
    private MobileElement btn_closePopupPedidoFacil;

    @AndroidFindBy(id = "recommender_popup_title")
    private MobileElement lbl_popupTitle;

   @AndroidFindBy(id = "truck")
    private MobileElement btn_truck;


    // *******getter and setters*******//

    public MobileElement getBtn_recommenderAdd() {
        return btn_recommenderAdd;
    }

    public MobileElement getLbl_loadingTruck() {
        return lbl_loadingTruck;
    }

    public MobileElement getBtn_closePopupPedidoFacil() {
        return btn_closePopupPedidoFacil;
    }

    public MobileElement getLbl_popupTitle() {
        return lbl_popupTitle;
    }

    public MobileElement getBtn_truck() {
        return btn_truck;
    }


    // *******getter and setters string*******//

}
