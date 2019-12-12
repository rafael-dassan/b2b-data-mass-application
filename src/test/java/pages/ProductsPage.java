package pages;

import support.DriverConfig;
import org.openqa.selenium.support.ui.ExpectedConditions;
import element_mapping.ProductsMapping;

public class ProductsPage extends DriverConfig {

	private ProductsMapping productsMapping;

    public ProductsPage() {
    	this.productsMapping = new ProductsMapping(driver);
    }

    public void addProduct() {
        wait.until(ExpectedConditions.elementToBeClickable(this.productsMapping.getBtnRecommenderAdd()));
        this.productsMapping.getBtnRecommenderAdd().click();
    }

    public void closePedidoFacil() {
        wait.until(ExpectedConditions.elementToBeClickable(this.productsMapping.getBtnClosePopupPedidoFacil()));
        this.productsMapping.getBtnClosePopupPedidoFacil().click();
    }

    public void openTruck() {
        productsMapping.getBtnTruck().click();
    }

}
