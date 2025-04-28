package org.acme;

import org.eclipse.microprofile.jwt.Claims;

import io.smallrye.jwt.build.Jwt;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

@Path("/login")
public class LoginResource {

    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.TEXT_PLAIN)
    public String login(LoginData loginData) {
        return generateToken(loginData);
    }

    private String generateToken(LoginData loginData){
        String token = Jwt.issuer("https://example.com/issuer")
            .upn(loginData.getEmail())
            .groups(loginData.getRole())
            .claim(Claims.birthdate.name(), "2001-07-13")
            .sign();
        return token;
    }
}
