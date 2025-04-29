package org.acme;

public class LoginData {
    private String email;
    private String role;

    LoginData(){}
    LoginData(String email, String role){this.email = email; this.role = role;}

    public String getEmail() {
        return email;
    }
    public String getRole() {
        return role;
    }
    public void setEmail(String email) {
        this.email = email;
    }
    public void setRole(String role) {
        this.role = role;
    }
}
