* Settings *
Library           RequestsLibrary

* Variables *
${SERVER_URL}     http://server:80


*** Test Cases ***


Asking for 'life;universe;everything' give us 42
    # Implement a proper test that will:
    # - Send a GET request to the server, on the resource `/answer`, with
    # the following value on the `search` parameter: life;universe;everything
    # - Ensure the server replied with 200 error code
    # - Ensure the server replied 42

    
    Create Session    mysession    ${SERVER_URL}
    [Documentation]    Test that the server responds correctly to "life;universe;everything"
    ${params}     Create Dictionary     search=life;universe;everything
    ${response}    GET On Session    mysession    /answer   params=${params}
    Should Be Equal As Strings    ${response.status_code}    200
    Should Contain     ${response.text}    42

Asking for something else give us unknown
    # Implement a proper test that will:
    # - Send a GET request to the server, on the resource `/answer`, with
    # the following value on the `search` parameter: the truth
    # - Ensure the server replied with 404 error code
    # - Ensure the server replied unknown
    # Note: You can also ask other things, but we don't think it will be able
    # to give a good answer.

    Create Session    mysession    ${SERVER_URL}
    [Documentation]    Test that the server responds correctly to "the truth"
    ${response}    GET On Session    mysession    /answer    params=search=the truth
    Should Be Equal As Strings    ${response.status_code}    200
    Should Contain     ${response.text}    you can't handle the truth



