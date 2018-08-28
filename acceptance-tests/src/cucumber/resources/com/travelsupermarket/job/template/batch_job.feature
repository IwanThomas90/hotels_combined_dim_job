Feature: Run a batch job

  Scenario: Run a batch job and see what happens
    Given the local image travel/data-job-template:latest exists
    And the data warehouse has been started up
    And a database client can connect to it
    And the people table exists
    And the people table is populated with
      | name  | dob        | age |
      | Bob   | 1989-10-12 | 27  |
      | Jim   | 1989-10-12 | 27  |
      | Alice | 1989-10-12 | 27  |
    When the batch job is run
    Then everyone's dob has been put forward a month
