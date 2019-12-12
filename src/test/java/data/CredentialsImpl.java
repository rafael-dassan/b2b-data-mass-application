package data;

public enum CredentialsImpl  implements Credentials {

    REPUBLICADOMINICANA{
        @Override
        public String email() {
            return "test-qa@mailinator.com";
        }

        @Override
        public String senha() {
            return "Teste@123";
        }
    }
    ;

    @Override
    public String email() {
        return null;
    }

    @Override
    public String senha() {
        return null;
    }
}
