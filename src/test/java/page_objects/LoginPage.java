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

	@AndroidFindBy(xpath = "//android.support.v7.widget.RecyclerView[@content-desc=\"Account table\"]/android.widget.LinearLayout[1]/android.widget.TextView")
	private MobileElement btn_account;

	@AndroidFindBy(id = "tutorial_image")
	private MobileElement presentationSlide;

	@AndroidFindBy(id = "start_button")
	private MobileElement btn_start;

	@AndroidFindBy(id = "ratingRbRating")
	private MobileElement btn_rating;

	@AndroidFindBy(id = "ratingAddNotesText")
	private MobileElement txt_addNotes;

	@AndroidFindBy(xpath = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.TextView")
	private MobileElement btn_question;

	@AndroidFindBy(id = "ratingSubmitButton")
	private MobileElement btn_ratingSubmit;

	@AndroidFindBy(id = "sentCloseButton")
	private MobileElement btn_finishClassification;

	@AndroidFindBy(id = "loginLogo")
	private MobileElement img_logoLogin;

	@AndroidFindBy(id = "view_pager")
	private MobileElement img_Carroussel;

	// *******getter and setters*******//

	public MobileElement getTlt_Login() {
		return tlt_Login;
	}

	public MobileElement getBtn_account() {
		return btn_account;
	}

	public MobileElement getPresentationSlide() {
		return presentationSlide;
	}

	public MobileElement getBtn_start() {
		return btn_start;
	}

	public MobileElement getBtn_rating() {
		return btn_rating;
	}

	public MobileElement getBtn_ratingSubmit() {
		return btn_ratingSubmit;
	}

	public MobileElement getTxt_addNotes() {
		return txt_addNotes;
	}

	public MobileElement getBtn_finishClassification() {
		return btn_finishClassification;
	}

	public MobileElement getBtn_question() {
		return btn_question;
	}

	public MobileElement getImg_logoLogin() {
		return img_logoLogin;
	}

	public MobileElement getImg_Carroussel() {
		return img_Carroussel;
	}

	// *******Elements Custom*******//

	public String getRb_Ambiente(String ambiente) {
		return "//android.widget.RadioButton[contains(@text,'"+ ambiente +"')]";
	}

}
