package com.travelsupermarket.job.template;

import ch.qos.logback.classic.Logger;
import com.spotify.docker.client.DefaultDockerClient;
import com.spotify.docker.client.LogStream;
import com.spotify.docker.client.exceptions.DockerCertificateException;
import com.spotify.docker.client.exceptions.DockerException;
import com.spotify.docker.client.exceptions.ImageNotFoundException;
import com.spotify.docker.client.messages.ContainerConfig;
import com.spotify.docker.client.messages.ContainerCreation;
import com.spotify.docker.client.messages.ContainerInfo;
import com.spotify.docker.client.messages.HostConfig;
import cucumber.api.java.After;
import cucumber.api.java.en.And;
import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;
import cucumber.api.java.en_tx.Whenyall;
import org.slf4j.LoggerFactory;

import java.sql.*;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import static ch.qos.logback.classic.Level.WARN;
import static com.spotify.docker.client.DockerClient.LogsParam.stderr;
import static com.spotify.docker.client.DockerClient.LogsParam.stdout;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;
import static org.slf4j.Logger.ROOT_LOGGER_NAME;

public class BatchJobDefinition {

    private final DefaultDockerClient dockerClient = DefaultDockerClient.fromEnv().build();
    private String warehouseHostIp;
    private String warehouseExternalPort;
    private Connection warehouseConnection;
    private String warehouseContainerId;
    private String image;

    private static final Logger ROOT_LOGGER = (Logger) LoggerFactory.getLogger(ROOT_LOGGER_NAME);

    static {
        ROOT_LOGGER.setLevel(WARN);
    }


    public BatchJobDefinition() throws DockerCertificateException {
    }

    @Given("^the local image (\\S+) exists$")
    public void theLocalImageExists(String image) throws Throwable {
        try{
            this.dockerClient.inspectImage(image);
        } catch (ImageNotFoundException e){
            fail("Unable to find " + image + "locally. The image to be tested should be built before running acceptance tests");
        }
        this.image = image;
    }

    @Whenyall("the data warehouse has been started up")
    public void theDataWarehouseHasBeenStartedUp() throws Exception {
        final String image = "postgres:9-alpine";
        final HostConfig hostConfig = HostConfig.builder().publishAllPorts(true).build();
        dockerClient.pull(image);
        final ContainerConfig containerConfig = ContainerConfig.builder()
                .image(image)
                .hostConfig(hostConfig)
                .build();
        final ContainerCreation creation = dockerClient.createContainer(containerConfig);
        this.warehouseContainerId = creation.id();
        dockerClient.startContainer(this.warehouseContainerId);
        final ContainerInfo info = dockerClient.inspectContainer(this.warehouseContainerId);
        this.warehouseExternalPort = info.networkSettings().ports().get("5432/tcp").get(0).hostPort();
        this.warehouseHostIp = info.networkSettings().ipAddress();
    }

    @And("a database client can connect to it")
    public void aDatabaseClientCanConnectToIt() throws Exception {

        final int attempts = 15;
        final int sleepMillis = 1000;
        Statement statement = null;
        ResultSet results = null;
        Exception exception = null;

        final String jdbcUrl = String.format("jdbc:postgresql://localhost:%s/postgres", this.warehouseExternalPort);
        final String user = "postgres";
        final String password = "postgres";

        for (int i = 1; i <= attempts; i++) {
            try {
                Thread.sleep(sleepMillis);
                this.warehouseConnection = DriverManager.getConnection(jdbcUrl, user, password);
                statement = this.warehouseConnection.createStatement();
                results = statement.executeQuery("SELECT VERSION()");
                if (results.next()) {
                    return;
                }
            } catch (Exception e) {
                exception = e;
            } finally {
                if (results != null) {
                    results.close();
                }
                if (statement != null) {
                    statement.close();
                }
            }
        }
        fail(String.format("Could not connect to db after %s attempts. Exception: %s", attempts, exception));
    }

    @And("the people table exists")
    public void thePeopleTableExists() throws SQLException {
        String createTableStatement = "CREATE TABLE people (\n" +
                "    name VARCHAR(255),\n" +
                "    dob DATE,\n" +
                "    age INT\n" +
                ");";
        Statement statement = this.warehouseConnection.createStatement();
        statement.execute(createTableStatement);
    }

    @And("the (\\S+) table is populated with")
    public void thePeopleTableIsPopulatedWith(String table, List<Map<String, String>> records) throws SQLException {
        System.out.println("TABLE: " + table);
        // TODO - do all of this better
        String fieldNameString = String.join(",", records.get(0).keySet());

        for (Map<String, String> record : records) {
            List<String> quotedFields = new ArrayList<>();
            for (String value: record.values()) {
                quotedFields.add(String.format("'%s'", value));
            }
            String valuesString = String.join(",", quotedFields);
            String fullStatementString = String.format(
                    "INSERT INTO %s (%s) VALUES (%s)", table, fieldNameString, valuesString);
            Statement statement = this.warehouseConnection.createStatement();
            System.out.println(fullStatementString);
            statement.executeUpdate(fullStatementString);
        }

    }

    @When("the batch job is run")
    public void theBatchJobIsRun() throws Exception {
        final ContainerConfig containerConfig = ContainerConfig.builder()
                .image(image)
                .attachStdout(true)
                .attachStderr(true)
                .cmd("--warehouse_port", "5432",
                        "--warehouse_host", this.warehouseHostIp,
                        "--mart_db_user", "postgres",
                        "--mart_db_password", "postgres",
                        "--mart_db_name", "postgres")
                .build();
        final ContainerCreation creation = dockerClient.createContainer(containerConfig);
        final String id = creation.id();
        dockerClient.startContainer(id);
        dockerClient.waitContainer(id);
        final LogStream output = dockerClient.logs(id, stdout(), stderr());
        final String log = output.readFully();
        System.out.println(String.format("%nJOB OUTPUT:%n%s", log));
    }

    @Then("everyone's dob has been put forward a month")
    public void everyonesDobHasBeenPutForwardAMonth() throws Exception {
        Statement statement = this.warehouseConnection.createStatement();
        ResultSet resultSet = statement.executeQuery("SELECT * FROM people");
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
        while (resultSet.next()) {
            assertEquals(simpleDateFormat.parse("1989-11-12"), resultSet.getDate("dob"));
        }
    }

    @After
    public void shutdownWarehouse() throws DockerCertificateException, DockerException, InterruptedException {
        if (this.warehouseContainerId != null) {
            dockerClient.stopContainer(this.warehouseContainerId, 0);
            dockerClient.removeContainer(this.warehouseContainerId);
        }
    }

}
