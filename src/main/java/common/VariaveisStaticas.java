package common;

public class VariaveisStaticas {

    static String valorLiquido;
    static String valorConta;

    static String platformType;

    public static String getValorConta() {
        return valorConta;
    }

    public static void setValorConta(String valorConta) {
        VariaveisStaticas.valorConta = valorConta;
    }

    public static String getValorLiquido() {
        return valorLiquido;
    }

    public static void setValorLiquido(String valorLiquido) {
        VariaveisStaticas.valorLiquido = valorLiquido;
    }

    public static String getPlatformType() {
        return platformType;
    }

    public static void setPlatformType(String platformType) {
        VariaveisStaticas.platformType = platformType;
    }
}
