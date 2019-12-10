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
    private MobileElement btn_RecommenderAdd;

    @AndroidFindBy(id = "recommender_popup_close")
    private MobileElement btn_ClosePopupPedidoFacil;

    @AndroidFindBy(id = "recommender_popup_title")
    private MobileElement lbl_PopupTitle;

   @AndroidFindBy(id = "truck")
    private MobileElement btn_Truck;


    // *******getter and setters*******//

    public MobileElement getBtn_recommenderAdd() {
        return btn_RecommenderAdd;
    }

    public MobileElement getBtn_ClosePopupPedidoFacil() {
        return btn_ClosePopupPedidoFacil;
    }

    public MobileElement getLbl_PopupTitle() {
        return lbl_PopupTitle;
    }

    public MobileElement getBtn_Truck() {
        return btn_Truck;
    }

}
