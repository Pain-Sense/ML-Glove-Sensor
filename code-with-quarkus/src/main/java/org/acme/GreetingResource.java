package org.acme;

import org.eclipse.microprofile.jwt.JsonWebToken;

import jakarta.annotation.security.PermitAll;
import jakarta.annotation.security.RolesAllowed;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.InternalServerErrorException;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.Context;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.SecurityContext;

@Path("/hello")
public class GreetingResource {
    @Inject
    JsonWebToken jwt;

    @GET
    @Path("permit-all")
    @PermitAll
    @Produces(MediaType.TEXT_PLAIN)
    public String hello(@Context SecurityContext ctx) {
        return getResponseString(ctx);
    }

    @GET
    @Path("researcher-path")
    @RolesAllowed({"Researcher", "Healthcare Professional"})
    @Produces(MediaType.TEXT_PLAIN)
    public String helloResearcher(@Context SecurityContext ctx) {
        return getResponseString(ctx) + ", Security level: Researcher";
    }

    @GET
    @Path("healthcare-path")
    @RolesAllowed({"Healthcare Professional"})
    @Produces(MediaType.TEXT_PLAIN)
    public String helloHealthcareProfessional(@Context SecurityContext ctx) {
        return getResponseString(ctx) + ", Security level: Healthcare Professional";
    }

    private String getResponseString(SecurityContext ctx){
        String name;
        if(ctx.getUserPrincipal() == null) {
            name = "anonymous";
        } else if(!ctx.getUserPrincipal().getName().equals(jwt.getName())){
            throw new InternalServerErrorException("Principal and JsonWebToken names do not match");
        } else {
            name = ctx.getUserPrincipal().getName();
        }
        return String.format("hello %s, "
            + " isHttps: %s, "
            + " authScheme: %s, "
            + " hasJwt: %s",
            name, ctx.isSecure(), ctx.getAuthenticationScheme(), hasJwt()
        );
    }

    private boolean hasJwt() {
        return jwt.getClaimNames() != null;
    }
}
