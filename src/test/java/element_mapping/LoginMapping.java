package element_mapping;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import org.openqa.selenium.support.PageFactory;

public class LoginMapping {

	// *******Constructor*******//
	
	public LoginMapping(AppiumDriver<MobileElement> appiumDriver) {
		PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
	}

	// *******Elements*******//

	@AndroidFindBy(id = "background_layout")
	private MobileElement screenLogin;

	@AndroidFindBy(xpath = "//android.widget.LinearLayout[1]/android.widget.TextView")
	private MobileElement btnAccount;

	@AndroidFindBy(id = "tutorial_title")
	private MobileElement presentationSlide;

	@AndroidFindBy(id = "start_button")
	private MobileElement btnStart;

	@AndroidFindBy(id = "ratingRbRating")
	private MobileElement btnRating;

	@AndroidFindBy(id = "ratingAddNotesText")
	private MobileElement txtAddNotes;

	@AndroidFindBy(xpath = "//android.widget.TextView[contains(@text,'Damaged')]")
	private MobileElement btnQuestion;

	@AndroidFindBy(id = "ratingSubmitButton")
	private MobileElement btnRatingSubmit;

	@AndroidFindBy(id = "sentCloseButton")
	private MobileElement btnFinishClassification;

	@AndroidFindBy(id = "loginLogo")
	private MobileElement imgLogoLogin;

	@AndroidFindBy(id = "view_pager")
	private MobileElement imgCarousel;

	// *******getter and setters*******//

	public MobileElement getScreenLogin() {
		return screenLogin;
	}

	public MobileElement getBtnAccount() {
		return btnAccount;
	}

	public MobileElement getPresentationSlide() {
		return presentationSlide;
	}

	public MobileElement getBtnStart() {
		return btnStart;
	}

	public MobileElement getBtnRating() {
		return btnRating;
	}

	public MobileElement getBtnRatingSubmit() {
		return btnRatingSubmit;
	}

	public MobileElement getTxtAddNotes() {
		return txtAddNotes;
	}

	public MobileElement getBtnFinishClassification() {
		return btnFinishClassification;
	}

	public MobileElement getBtnQuestion() {
		return btnQuestion;
	}

	public MobileElement getImgLogoLogin() {
		return imgLogoLogin;
	}

	public MobileElement getImgCarousel() {
		return imgCarousel;
	}

	// *******Elements Custom*******//

	public String getRb_Ambiente(String enviroment) {
		return "//android.widget.RadioButton[contains(@text,'"+ enviroment +"')]";
	}

}
