package tests.cucumber.steps;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;
import pages.LoginPage;
import pages.OrdersPage;
import pages.ProductsPage;
import pages.UtilsPage;

import static org.junit.Assert.assertTrue;

public class ProductsSteps {

    OrdersPage ordersPage;
    LoginPage loginPage;
    UtilsPage utilsPage;
    ProductsPage productsPage;

    public ProductsSteps() {
        loginPage = new LoginPage();
        ordersPage = new OrdersPage();
        utilsPage = new UtilsPage();
        productsPage = new ProductsPage();
    }

    @Given("that I want to buy some products")
    public void that_I_want_to_buy_some_products() {
        utilsPage.clickEnter();
        utilsPage.loginData("REPUBLICADOMINICANA");
        utilsPage.clickLogin();
        loginPage.selectAccount();
        loginPage.swipePresentation();
        loginPage.appRating();
    }

    @When("I select one or more products")
    public void i_select_one_or_more_products() {
        productsPage.addProduct();
        productsPage.openTruck();
    }

    @Then("the products must be added into my cart")
    public void the_products_must_be_added_into_my_cart() {
        //Assertion
    }
}
