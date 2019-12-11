package screens;

import base_screen.BaseScreen;
import org.openqa.selenium.support.ui.ExpectedConditions;
import page_objects.ProductsPage;

public class ProductsScreen extends BaseScreen {

	private ProductsPage productsPage;

    public ProductsScreen() {
    	this.productsPage = new ProductsPage(driver);
    }

    public void addProduct() {
        wait.until(ExpectedConditions.elementToBeClickable(this.productsPage.getBtnRecommenderAdd()));
        this.productsPage.getBtnRecommenderAdd().click();
        wait.until(ExpectedConditions.elementToBeClickable(this.productsPage.getLblLoadingTruck()));
    }

    public void closePedidoFacil() {
        wait.until(ExpectedConditions.elementToBeClickable(this.productsPage.getBtnClosePopupPedidoFacil()));
        this.productsPage.getBtnClosePopupPedidoFacil().click();
    }

    public void openTruck() {
        productsPage.getBtnTruck().click();
    }

}
