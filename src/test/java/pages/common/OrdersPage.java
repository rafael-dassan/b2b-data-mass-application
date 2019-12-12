package pages.common;

import support.DriverConfig;
import element_mapping.OrdersMapping;

public class OrdersPage extends DriverConfig {

	private OrdersMapping ordersMapping;
	
    public OrdersPage() {
    	this.ordersMapping = new OrdersMapping(driver);
    }

//============================================METODOS=========================================================================

}
