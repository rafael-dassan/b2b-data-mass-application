package tests.cucumber.steps;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;
import screens.LoginScreen;
import screens.LogoutScreen;
import screens.UtilsScreen;

import static junit.framework.TestCase.assertTrue;

public class LogoutSteps {

    LogoutScreen logoutScreen;
    LoginScreen loginScreen;
    UtilsScreen utilsScreen;

    public LogoutSteps() throws Exception {
        logoutScreen = new LogoutScreen();
        loginScreen = new LoginScreen();
        utilsScreen = new UtilsScreen();
    }

    @Given("that I am logged")
    public void that_I_am_logged() {
        utilsScreen.clicarEntrar();
        utilsScreen.logar("REPUBLICADOMINICANA");
        utilsScreen.clicarEntrarLogin();
        loginScreen.selecionarConta();
        loginScreen.passarApresentacao();
        loginScreen.classificacaoApp();
        logoutScreen.abrirMenu();
    }

    @When("I click on the logout button")
    public void i_click_on_the_logout_button() {
        utilsScreen.clicarLogout();
    }

    @Then("I must be logged out")
    public void i_must_be_logged_out() {
        assertTrue(utilsScreen.validarTelaInicial());
    }

}
