package com.travelsupermarket.job.template;

import java.util.ArrayList;
import java.util.List;

import static java.lang.String.format;

public class Runner {

    public static void main(String[] args) throws Throwable {
        final String[] arguments = createCucumberArgs(args);
        System.out.println("Arguments: " + String.join(" ", arguments));
        cucumber.api.cli.Main.main(arguments);
    }

    private static String[] createCucumberArgs(String[] args) {
        final String packageName = Runner.class.getPackage().getName();
        final List<String> arguments = new ArrayList<>();
        arguments.add("--strict");
        arguments.add("--plugin pretty");
        arguments.add(format("--glue %s", packageName));
        includeGivenArguments(args, arguments);
        arguments.add(format("classpath:%s", packageName.replaceAll("\\.", "/")));
        return String.join(" ", arguments).split(" ");
    }

    private static void includeGivenArguments(String[] args, List<String> arguments) {
        for (final String arg : args)
            arguments.add(arg);
    }

}