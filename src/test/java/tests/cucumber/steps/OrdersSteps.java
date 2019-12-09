package tests.cucumber.steps;

import screens.LoginScreen;
import screens.OrdersScreen;

public class OrdersSteps {

    OrdersScreen ordersScreen;
    LoginScreen loginScreen;

    public OrdersSteps() {
        loginScreen = new LoginScreen();
        ordersScreen = new OrdersScreen();
    }

}
