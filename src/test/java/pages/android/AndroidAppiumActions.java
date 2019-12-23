package pages.android;

import io.appium.java_client.MobileElement;
import io.appium.java_client.TouchAction;
import io.appium.java_client.touch.TapOptions;
import io.appium.java_client.touch.WaitOptions;
import io.appium.java_client.touch.offset.ElementOption;
import io.appium.java_client.touch.offset.PointOption;
import org.openqa.selenium.By;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.support.ui.ExpectedConditions;
import support.DriverConfig;
import support.StaticVariable;

import java.time.Duration;
import java.util.List;

public class AndroidAppiumActions extends DriverConfig {

    public void waitUntilElementIsVisible(MobileElement element){
        wait.until(ExpectedConditions.visibilityOf(element));
    }

    public MobileElement getElementByText(List<MobileElement> list, String text) {
        for(int i = 0; i < list.size();i++){
            if (list.get(i).getText().toLowerCase().equalsIgnoreCase(text.toLowerCase())){
                return list.get(i);
            }
        }
        return null;
    }

    /**
     * Verifica se o elemento existe
     */
    public static boolean elementExists(String xpath) {
        return driver.findElements(By.xpath(xpath)).size() != 0;
    }

    /**
     * Clicar em um elemento customizado
     */
    public static void clicarElementoCustom(String xpath) {
        driver.findElementByXPath(xpath).click();
    }

    /**
     * Fechar o teclado
     */
    public static void fecharTeclado() {
        if(StaticVariable.getPlatformType().equals("android")){
            driver.hideKeyboard();
        }else{
            //Implementar para iOS
        }
    }

    /**
     * Realiza swipe vertical na tela por porcentagem
     */
    public static void swipeVertical(double startPercentage, double finalPercentage, int durantion) {
        try {
            TouchAction action = new TouchAction(driver);
            Dimension size = driver.manage().window().getSize();
            int widht = (int) size.width / 2;
            int startPoint = (int) (size.height * startPercentage);
            int endPoint = (int) (size.height * finalPercentage);
            action.press(PointOption.point(widht, startPoint))
                    .waitAction(WaitOptions.waitOptions(Duration.ofSeconds(durantion)))
                    .moveTo(PointOption.point(widht, endPoint)).release().perform();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Realiza swipe pressionado horizontal na tela por coordenadas
     */
    public static void swipeHorizontalLongCoordinate(int startX, int startY, int endX, int endY) {
        try {
            TouchAction action = new TouchAction(driver);
            action.longPress(PointOption.point(startX, startY))
                    .moveTo(PointOption.point(endX, endY))
                    .release()
                    .perform();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Realiza swipe horizontal na tela por coordenadas
     */
    public static void swipeHorizontalCoordinate(int startX, int startY, int endX, int endY) {
        try {
            TouchAction action = new TouchAction(driver);
            action.press(PointOption.point(startX, startY))
                    .moveTo(PointOption.point(endX, endY))
                    .release()
                    .perform();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Realiza swipe pressionando horizontalmente da Direita para Esquerda na tela por elemento
     * Utilizado para selecionar o ambiente
     */
    public static void swipeForEnvironment(MobileElement elemento) {

        Integer start_x, start_y, end_x, end_y;

        try {
            start_x = elemento.getSize().width - ((elemento.getSize().width * 2) / 100); //Retirar 2% por conta da borda
            start_y = elemento.getSize().width;
            end_x = elemento.getSize().width - ((elemento.getSize().width * 80) / 100); //Swipe ate 80% da outra borda
            end_y = elemento.getSize().width;

            TouchAction action = new TouchAction(driver);
            action.longPress(PointOption.point(start_x, start_y))
                    .moveTo(PointOption.point(end_x, end_y))
                    .release()
                    .perform();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Realiza swipe horizontalmente da Direita para Esquerda na tela por elemento
     */
    public static void swipeHorizontalRightToLeftElement(MobileElement elemento) {

        Integer start_x, start_y, end_x, end_y;

        try {
            start_x = elemento.getSize().width;
            start_y = elemento.getSize().width;
            end_x = elemento.getLocation().x;
            end_y = elemento.getSize().width;

            TouchAction action = new TouchAction(driver);
            action.press(PointOption.point(start_x, start_y))
                    .moveTo(PointOption.point(end_x, end_y))
                    .release()
                    .perform();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Realiza swipe ate encontrar o elemento desejado
     */
    public static void swipeAteEncontrarElemento(String xpath) {
        int num = 0;
        while (!elementExists(xpath) && num <= 9) {
            swipeVertical(0.5, 0.08, 0);
            num++;
        }
    }

    /**
     * Clicar no elemento com TouchAction
     */
    public static void clicaElementoTouchAction(MobileElement elemento) {
        TouchAction touchAction = new TouchAction(driver);
        touchAction.tap(TapOptions.tapOptions().withElement(ElementOption.element(elemento))).perform();
    }
}
