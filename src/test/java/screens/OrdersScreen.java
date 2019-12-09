package screens;

import base_screen.BaseScreen;
import org.openqa.selenium.support.ui.ExpectedConditions;
import page_objects.OrdersPage;

public class OrdersScreen extends BaseScreen {

	private OrdersPage ordersPage;
	
    public OrdersScreen() {
    	this.ordersPage = new OrdersPage(driver);
    }

//============================================METODOS=========================================================================

}
