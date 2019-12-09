package tests.cucumber.steps;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;
import screens.LoginScreen;
import screens.OrdersScreen;
import screens.ProductsScreen;
import screens.UtilsScreen;

import static org.junit.Assert.assertTrue;

public class ProductsSteps {

    OrdersScreen ordersScreen;
    LoginScreen loginScreen;
    UtilsScreen utilsScreen;
    ProductsScreen productsScreen;

    public ProductsSteps() {
        loginScreen = new LoginScreen();
        ordersScreen = new OrdersScreen();
        utilsScreen = new UtilsScreen();
        productsScreen = new ProductsScreen();
    }

    @Given("that I want to buy some products")
    public void that_I_want_to_buy_some_products() {
        utilsScreen.clicarEntrar();
        utilsScreen.logar("REPUBLICADOMINICANA");
        utilsScreen.clicarEntrarLogin();
        loginScreen.selecionarConta();
        loginScreen.passarApresentacao();
        loginScreen.classificacaoApp();
    }

    @When("I select one or more products")
    public void i_select_one_or_more_products() {
        productsScreen.adicionarProdutos();
        productsScreen.irCaminhao();
    }

    @Then("the products must be added into my cart")
    public void the_products_must_be_added_into_my_cart() {
        //Assertion
    }
}
