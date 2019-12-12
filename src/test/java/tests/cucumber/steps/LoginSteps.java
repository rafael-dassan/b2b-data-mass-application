package tests.cucumber.steps;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;
import pages.LoginPage;
import pages.LogoutPage;
import pages.UtilsPage;

import static junit.framework.TestCase.assertTrue;

public class LoginSteps {

    LoginPage loginPage;
    LogoutPage logoutPage;
    UtilsPage utilsPage;

    public LoginSteps() throws Exception {
        loginPage = new LoginPage();
        utilsPage = new UtilsPage();
        logoutPage = new LogoutPage();
    }

    @Given("I am on Initial screen")
    public void i_am_on_initial_screen() {
        assertTrue(utilsPage.checkInitialScreen());
    }

    @When("I selected the enviroment {string}")
    public void i_selected_the_enviroment(String enviroment) {
        loginPage.selectEnviroment(enviroment);
    }

    @Then("I go to screen login")
    public void i_go_to_screen_login() {
        assertTrue(utilsPage.checkInitialScreen());
    }

    @Given("that I have an existing account")
    public void that_I_have_an_existing_account() {
        utilsPage.clickEnter();
    }

    @When("I insert my credentials {string}")
    public void i_insert_my_credentials(String zona) {
        utilsPage.loginData(zona);
        utilsPage.clickLogin();
    }

    @When("I click on the login button")
    public void i_click_on_the_login_button() {
        loginPage.selectAccount();
        loginPage.swipePresentation();
        loginPage.appRating();
    }

    @Then("I must be logged successfully")
    public void i_must_be_logged_successfully() {
        assertTrue(loginPage.checkCarouselLogin());
    }
}
