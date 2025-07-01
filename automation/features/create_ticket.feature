Feature: Create Ticket

  Scenario: Manual login and create new ticket
    Given the automation is started and browser is open
    When the tech user logs in manually
    And the user navigates to the favorites page
    And clicks on "new" button
    Then enters all the input information and clicks on submit button
