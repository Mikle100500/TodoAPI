package com.restapi;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class RESTfulTaskTest {

    private final String URL = "http://127.0.0.1:5000/todo/api/tasks";

    @Test
    public void testBeingAuthorized() throws UnirestException {
        HttpResponse<JsonNode> jsonResponse = Unirest.get(URL).basicAuth("john", "malkovich").asJson();
        assertEquals(200, jsonResponse.getStatus());
    }

    @Test
    public void testGetAllTasks() throws UnirestException {
        HttpResponse<JsonNode> jsonResponse = Unirest.get(URL).basicAuth("john", "malkovich").asJson();
        jsonResponse.getBody().getObject();
        assertEquals(200, jsonResponse.getStatus());

    }
}
