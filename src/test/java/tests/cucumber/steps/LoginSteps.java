package tests.cucumber.steps;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;
import org.junit.Assert;
import pages.android.PagesAndroid;
import pages.ios.PagesIos;
import support.StaticVariable;

public class LoginSteps {
  @Given("that {string} as an {string} user is in the login screen")
  public void that_as_an_user_is_in_the_login_screen(String userName, String accountType) {
    if(StaticVariable.getPlatformType().equals("android"))
      PagesAndroid.loginPage().accessTheLoginScreen();
    else
      PagesIos.loginPage().accessTheLoginScreen();
  }

  @Given("he filled in the login data correctly")
  public void he_filled_in_the_login_data_correctly() {
    if(StaticVariable.getPlatformType().equals("android"))
      PagesAndroid.loginPage().fillLoginFieldsWithValidValues();
    else
      PagesIos.loginPage().fillLoginFieldsWithValidValues();
  }

  @When("he triggers the option to access")
  public void he_triggers_the_option_to_access() {
    if(StaticVariable.getPlatformType().equals("android")){
      PagesAndroid.loginPage().waitUntilElementIsVisible(PagesAndroid.loginPage().loginMapping.getEnterOption());
      PagesAndroid.loginPage().loginMapping.getEnterOption().click();
    } else {
        PagesIos.loginPage().waitUntilElementIsVisible(PagesIos.loginPage().loginMapping.getEnterOption());
        PagesIos.loginPage().loginMapping.getEnterOption().click();
    }
  }

  @Then("the account list page should be displayed")
  public void the_account_list_page_should_be_displayed() {
    if (StaticVariable.getPlatformType().equals("android")) {
      PagesAndroid.accountListPage()
          .waitUntilElementIsVisible(
              PagesAndroid.accountListPage().accountListMapping.getAccountListSection());
      Assert.assertTrue(
          PagesAndroid.accountListPage().accountListMapping.accountList[0].isDisplayed());
      }else{
      PagesIos.accountListPage().waitUntilElementIsVisible(
              PagesIos.accountListPage().accountListMapping.getAccountList()
      );
      Assert.assertTrue(PagesIos.accountListPage().accountListMapping.getAccountList().isDisplayed());
    }
    }
}

