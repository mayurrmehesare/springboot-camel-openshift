package com.example.demo;

import org.apache.camel.builder.RouteBuilder;
import org.springframework.stereotype.Component;

@Component
public class HelloRoute extends RouteBuilder {

    @Override
    public void configure() {
        from("timer:hello?period=5000")
            .log("Hello from Apache Camel running on OpenShift!");
    }
}