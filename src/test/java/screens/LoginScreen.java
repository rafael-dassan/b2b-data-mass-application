package screens;

import base_screen.BaseScreen;
import common.Helper;
import org.openqa.selenium.support.ui.ExpectedConditions;
import page_objects.LoginPage;

public class LoginScreen extends BaseScreen {

    private LoginPage loginPage;

    public LoginScreen() {
        this.loginPage = new LoginPage(driver);
    }

    public void selecionarAmbiente(String ambiente){
        wait.until(ExpectedConditions.visibilityOfAllElements(this.loginPage.getTlt_Login()));
        Helper.swipeForEnvironment(this.loginPage.getTlt_Login());
        Helper.clicarElementoCustom(this.loginPage.getRb_Ambiente(ambiente));
    }

    public void selecionarConta() {
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtn_account()));
        this.loginPage.getBtn_account().click();
    }

    public boolean validarTelaLogin(){
        wait.until(ExpectedConditions.visibilityOfAllElements(this.loginPage.getImg_logoLogin()));
        return this.loginPage.getImg_logoLogin().isDisplayed();
    }

    public boolean validarCarrousselLogin(){
        wait.until(ExpectedConditions.visibilityOfAllElements(this.loginPage.getImg_Carroussel()));
        return this.loginPage.getImg_Carroussel().isDisplayed();
    }

    public void passarApresentacao() {
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getPresentationSlide()));
        for(int i=0; i<=4; i++){
            Helper.swipeHorizontalRightToLeftElement(this.loginPage.getPresentationSlide());
        }
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtn_start()));
        this.loginPage.getBtn_start().click();
    }

    public void classificacaoApp() {
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtn_rating()));
        this.loginPage.getBtn_rating().click();
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtn_question()));
        this.loginPage.getBtn_question().click();
        this.loginPage.getTxt_addNotes().sendKeys("Executing automated test...");
        this.loginPage.getBtn_ratingSubmit().click();
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtn_finishClassification()));
        this.loginPage.getBtn_finishClassification().click();
    }
}
