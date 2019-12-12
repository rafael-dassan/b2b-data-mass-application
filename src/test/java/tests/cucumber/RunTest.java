package tests.cucumber;

import support.StaticVariable;
import cucumber.api.CucumberOptions;
import cucumber.api.junit.Cucumber;
import org.junit.BeforeClass;
import org.junit.runner.RunWith;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.io.IOException;

@RunWith(Cucumber.class)
@CucumberOptions(features = "src/test/java/tests/cucumber/features",
        glue = {"tests.cucumber.steps", "support"},
        //plugin = {"pretty", "html:reports"},
        tags = {"@logout"},
        dryRun = false)

public class RunTest {
    public WebDriverWait wait;

    @BeforeClass
    public static void setup() throws IOException {
        System.out.println("Test JUnit Before");
        StaticVariable.setPlatformType("android");
        StaticVariable.setZone("ZA");
    }
}