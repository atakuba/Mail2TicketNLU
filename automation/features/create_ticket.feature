Feature: Create Ticket

  Scenario: Manual login and create new ticket
    Given the automation is started and browser is open
    When the tech user logs in manually
    And the user navigates to the favorites page
    Given the Excel file is loaded into context
    Then each record from the Excel file is submitted as a new ticket