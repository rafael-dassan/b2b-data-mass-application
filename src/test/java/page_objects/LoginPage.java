package page_objects;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.AppiumFieldDecorator;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import org.openqa.selenium.support.PageFactory;

import java.awt.event.MouseListener;
import java.util.List;

public class LoginPage {

	// *******Construtor*******//
	
	public LoginPage(AppiumDriver<MobileElement> appiumDriver) {
		PageFactory.initElements(new AppiumFieldDecorator(appiumDriver), this);
	}

	// *******Elements*******//

	@AndroidFindBy(id = "background_layout")
	private MobileElement tlt_Login;

	@AndroidFindBy(xpath = "//android.widget.LinearLayout[1]/android.widget.TextView")
	private MobileElement btn_Account;

	@AndroidFindBy(id = "tutorial_title")
	private MobileElement tlt_PresentationSlide;

	@AndroidFindBy(id = "start_button")
	private MobileElement btn_Start;

	@AndroidFindBy(id = "ratingRbRating")
	private MobileElement btn_Rating;

	@AndroidFindBy(id = "ratingAddNotesText")
	private MobileElement txt_AddNotes;

	@AndroidFindBy(xpath = "//android.widget.TextView[contains(@text,\"Damaged\")]")
	private MobileElement btn_Question;

	@AndroidFindBy(id = "ratingSubmitButton")
	private MobileElement btn_RatingSubmit;

	@AndroidFindBy(id = "sentCloseButton")
	private MobileElement btn_FinishClassification;

	@AndroidFindBy(id = "loginLogo")
	private MobileElement img_LogoLogin;

	@AndroidFindBy(id = "view_pager")
	private MobileElement img_Carroussel;

	// *******getter and setters*******//

	public MobileElement getTlt_Login() {
		return tlt_Login;
	}

	public MobileElement getBtn_Account() {
		return btn_Account;
	}

	public MobileElement getTlt_PresentationSlide() {
		return tlt_PresentationSlide;
	}

	public MobileElement getBtn_Start() {
		return btn_Start;
	}

	public MobileElement getBtn_Rating() {
		return btn_Rating;
	}

	public MobileElement getBtn_RatingSubmit() {
		return btn_RatingSubmit;
	}

	public MobileElement getTxt_AddNotes() {
		return txt_AddNotes;
	}

	public MobileElement getBtn_FinishClassification() {
		return btn_FinishClassification;
	}

	public MobileElement getBtn_Question() {
		return btn_Question;
	}

	public MobileElement getImg_LogoLogin() {
		return img_LogoLogin;
	}

	public MobileElement getImg_Carroussel() {
		return img_Carroussel;
	}

	// *******Elements Custom*******//

	public String getRb_Ambiente(String ambiente) {
		return "//android.widget.RadioButton[contains(@text,'"+ ambiente +"')]";
	}

}
