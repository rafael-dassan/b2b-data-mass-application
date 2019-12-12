package tests.cucumber.steps;

import pages.LoginPage;
import pages.OrdersPage;

public class OrdersSteps {

    OrdersPage ordersPage;
    LoginPage loginPage;

    public OrdersSteps() {
        loginPage = new LoginPage();
        ordersPage = new OrdersPage();
    }

}
