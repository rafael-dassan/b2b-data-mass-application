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
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtn_Account()));
        this.loginPage.getBtn_Account().click();
    }

    public boolean validarTelaLogin(){
        wait.until(ExpectedConditions.visibilityOfAllElements(this.loginPage.getImg_LogoLogin()));
        return this.loginPage.getImg_LogoLogin().isDisplayed();
    }

    public boolean validarCarrousselLogin(){
        wait.until(ExpectedConditions.visibilityOfAllElements(this.loginPage.getImg_Carroussel()));
        return this.loginPage.getImg_Carroussel().isDisplayed();
    }

    public void passarApresentacao() {
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getTlt_PresentationSlide()));
        for(int i=0; i<=4; i++){
            Helper.swipeHorizontalRightToLeftElement(this.loginPage.getTlt_PresentationSlide());
        }
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtn_Start()));
        this.loginPage.getBtn_Start().click();
    }

    public void classificacaoApp() {
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtn_Rating()));
        this.loginPage.getBtn_Rating().click();
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtn_Question()));
        this.loginPage.getBtn_Question().click();
        this.loginPage.getTxt_AddNotes().sendKeys("Executing automated test...");
        this.loginPage.getBtn_RatingSubmit().click();
        wait.until(ExpectedConditions.elementToBeClickable(this.loginPage.getBtn_FinishClassification()));
        this.loginPage.getBtn_FinishClassification().click();
    }
}
