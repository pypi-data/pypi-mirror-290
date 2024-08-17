# Hikaru Microservice

This is a Python package that provides some shared logic for registering an
email and website with a microservice.

## Installation

    pip install hikaru-microservice

## Usage

In main.py:

    from hikaru_microservice import microservice

    app = microservice('Service Name', 'service.example.org', SENDGRID_API_KEY)

    @app.post('/endpoint')
    async def endpoint(...):
        ...

This provides the following endpoints:

 - **/register** - POST endpoint accepting **email**.
 - **/confirm/{code}** - GET endpoint for confirming registration.

You can iterate through all registrations like this:

    for email, website in app.registrations():
        ... process (email, website) here ...

Or you can check if a single registration is confirmed like this:

    if app.is_confirmed(email, website):
        ... process (email, website) here ...

And you can send an email like this:

    # attachments = List[MIMEApplication]
    app.send_email(recipient, subject, html, attachments=[])

To run in production mode:

    fastapi run

## Dependencies

 - FastAPI
