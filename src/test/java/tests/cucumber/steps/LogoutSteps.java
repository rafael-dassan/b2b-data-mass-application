package tests.cucumber.steps;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;
import pages.common.LoginPage;
import pages.common.LogoutPage;
import pages.common.UtilsPage;

import static junit.framework.TestCase.assertTrue;

public class LogoutSteps {

    LogoutPage logoutPage;
    LoginPage loginPage;
    UtilsPage utilsPage;

    public LogoutSteps() throws Exception {
        logoutPage = new LogoutPage();
        loginPage = new LoginPage();
        utilsPage = new UtilsPage();
    }

    @Given("that I am logged")
    public void that_I_am_logged() {
        utilsPage.clickEnter();
        utilsPage.loginData("REPUBLICADOMINICANA");
        utilsPage.clickLogin();
        loginPage.selectAccount();
        loginPage.swipePresentation();
        loginPage.appRating();
        logoutPage.openMenu();
    }

    @When("I click on the logout button")
    public void i_click_on_the_logout_button() {
        utilsPage.clickLogout();
    }

    @Then("I must be logged out")
    public void i_must_be_logged_out() {
        assertTrue(utilsPage.checkInitialScreen());
    }

}
