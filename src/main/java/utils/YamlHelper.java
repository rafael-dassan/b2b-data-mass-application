package utils;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Map;
import org.yaml.snakeyaml.Yaml;

public class YamlHelper {

    public static Object getAtributo(String... param) throws Exception {
        String caminho = new File("src/main/java/utils").getAbsolutePath() + File.separator + "utilsProperties.Yaml";
        File file = new File(caminho);
        InputStream input = new FileInputStream(caminho);
        Map<?, ?> mapAux = (Map<?, ?>) new Yaml().load(input);
        if (mapAux == null) {
            throw new Exception(String.format("A massa de dados não foi localizada no arquivo %s", file.getName()));
        }
        int cont;
        for (cont = 0; cont < (param.length - 1); cont++) {
            mapAux = (Map<?, ?>) mapAux.get(param[cont]);
        }
        return mapAux.get(param[cont]);
    }
}
