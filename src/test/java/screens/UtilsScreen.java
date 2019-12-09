package screens;

import enums.CredentialsImpl;
import org.openqa.selenium.support.ui.ExpectedConditions;

import base_screen.BaseScreen;
import page_objects.UtilsPage;

public class UtilsScreen extends BaseScreen {

    private UtilsPage utilsPage;

    public UtilsScreen() {
        this.utilsPage = new UtilsPage(driver);
    }

    public void logar(String zona) {
        digitarEmail(zona);
        digitarSenha(zona);
    }

    public boolean validarTelaInicial(){
        wait.until(ExpectedConditions.visibilityOfAllElements(this.utilsPage.getBtn_Entrar()));
        return this.utilsPage.getBtn_Entrar().isDisplayed();
    }

    public void clicarEntrar(){
        wait.until(ExpectedConditions.elementToBeClickable(this.utilsPage.getBtn_Entrar()));
        this.utilsPage.getBtn_Entrar().click();
    }

    public void digitarEmail(String zona) {
        wait.until(ExpectedConditions.elementToBeClickable(this.utilsPage.getLbl_email()));
        this.utilsPage.getLbl_email().sendKeys(CredentialsImpl.valueOf(zona.toUpperCase().replaceAll(" ", "")).email());
    }

    public void digitarSenha(String zona) {
        wait.until(ExpectedConditions.elementToBeClickable(this.utilsPage.getLbl_senha()));
        this.utilsPage.getLbl_senha().sendKeys(CredentialsImpl.valueOf(zona.toUpperCase().replaceAll(" ", "")).senha());
    }

    public void clicarEntrarLogin(){
        wait.until(ExpectedConditions.elementToBeClickable(this.utilsPage.getBtn_Login()));
        this.utilsPage.getBtn_Login().click();
    }

    public void clicarLogout() {
        this.utilsPage.getBtn_Logout().click();
    }

}
