package org.acme;

import org.eclipse.microprofile.jwt.Claims;

import io.smallrye.jwt.build.Jwt;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

@Path("/login")
public class LoginResource {

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String login() {
        return generateToken();
    }

    private String generateToken(){
        String token = Jwt.issuer("https://example.com/issuer")
            .upn("jdoe@quarkus.io")
            .groups("Researcher")
            .claim(Claims.birthdate.name(), "2001-07-13")
            .sign();
        return token;
    }
}
