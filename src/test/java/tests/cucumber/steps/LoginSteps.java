package tests.cucumber.steps;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;
import screens.LoginScreen;
import screens.LogoutScreen;
import screens.UtilsScreen;

import static junit.framework.TestCase.assertTrue;

public class LoginSteps {

    LoginScreen loginScreen;
    LogoutScreen logoutScreen;
    UtilsScreen utilsScreen;

    public LoginSteps() throws Exception {
        loginScreen = new LoginScreen();
        utilsScreen = new UtilsScreen();
        logoutScreen = new LogoutScreen();
    }

    @Given("I am on Initial screen")
    public void i_am_on_initial_screen() {
        assertTrue(utilsScreen.validarTelaInicial());
    }

    @When("I selected the enviroment {string}")
    public void i_selected_the_enviroment(String ambiente) {
        loginScreen.selecionarAmbiente(ambiente);
    }

    @Then("I go to screen login")
    public void i_go_to_screen_login() {
        assertTrue(loginScreen.validarTelaLogin());
    }

    @Given("that I have an existing account")
    public void that_I_have_an_existing_account() {
        utilsScreen.clicarEntrar();
    }

    @When("I insert my credentials {string}")
    public void i_insert_my_credentials(String zona) {
        utilsScreen.logar(zona);
        utilsScreen.clicarEntrarLogin();
    }

    @When("I click on the login button")
    public void i_click_on_the_login_button() {
        loginScreen.selecionarConta();
        loginScreen.passarApresentacao();
        loginScreen.classificacaoApp();
    }

    @Then("I must be logged successfully")
    public void i_must_be_logged_successfully() {
        assertTrue(loginScreen.validarCarrousselLogin());
    }
}
