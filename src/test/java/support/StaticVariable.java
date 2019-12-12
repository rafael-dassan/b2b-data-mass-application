package support;

public class StaticVariable {

    static String platformType;
    static String zone;

    public static String getPlatformType() {
        return platformType;
    }

    public static void setPlatformType(String platformType) {
        StaticVariable.platformType = platformType;
    }

    public static String getZone() {
        return zone;
    }

    public static void setZone(String zone) {
        StaticVariable.zone = zone;
    }
}
