package support;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public final class ReadJsonFile {
    private static Map<String, String> map = new HashMap<>();
    private static JSONParser jsonParser = new JSONParser();
    private static String jsonPath =
            "src/test/java/data/"
                    + StaticVariable.getZone().toLowerCase() +
                    "/" + StaticVariable.getZone().substring(0, 1).toUpperCase() +
                    StaticVariable.getZone().substring(1) + "StaticData.json";

    public ReadJsonFile() {
    }

    public static String getInfoInsideJsonByPath(String[] strings) {
        String value = null;
        try (FileReader reader = new FileReader(jsonPath)) {
            Object obj = jsonParser.parse(reader);
            JSONObject json = (JSONObject) obj;
            for (int i = 0; i < strings.length - 1; i++) {
                json = (JSONObject) json.get(strings[i]);
            }
            value = json.get(strings[strings.length - 1]).toString();
        } catch (IOException | ParseException e) {
            e.printStackTrace();
        }
        return value;
    }

}

