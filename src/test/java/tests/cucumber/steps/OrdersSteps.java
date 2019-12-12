package tests.cucumber.steps;

import pages.common.LoginPage;
import pages.common.OrdersPage;

public class OrdersSteps {

    OrdersPage ordersPage;
    LoginPage loginPage;

    public OrdersSteps() {
        loginPage = new LoginPage();
        ordersPage = new OrdersPage();
    }

}
