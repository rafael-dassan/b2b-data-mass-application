package element_mapping;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import org.openqa.selenium.support.PageFactory;

public class ProductsMapping {

    public ProductsMapping(AppiumDriver<MobileElement> appiumDriver) {
        PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
    }

    // *******Elements*******//

    @AndroidFindBy(id = "beerRecommenderAdd")
    private MobileElement btnRecommenderAdd;

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
