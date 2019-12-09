package screens;

import base_screen.BaseScreen;
import common.Helper;
import org.openqa.selenium.support.ui.ExpectedConditions;
import page_objects.ProductsPage;

public class ProductsScreen extends BaseScreen {

	private ProductsPage productsPage;

    public ProductsScreen() {
    	this.productsPage = new ProductsPage(driver);
    }

    public void adicionarProdutos() {
        wait.until(ExpectedConditions.elementToBeClickable(this.productsPage.getBtn_recommenderAdd()));
        this.productsPage.getBtn_recommenderAdd().click();
        wait.until(ExpectedConditions.elementToBeClickable(this.productsPage.getLbl_loadingTruck()));
    }

    public void fecharPedidoFacil() {
        wait.until(ExpectedConditions.elementToBeClickable(this.productsPage.getBtn_closePopupPedidoFacil()));
        this.productsPage.getBtn_closePopupPedidoFacil().click();
    }

    public void irCaminhao() {
        productsPage.getBtn_truck().click();
    }

}
