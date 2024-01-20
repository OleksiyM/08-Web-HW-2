# Contact Management and Messaging System

## Overview

This Python project demonstrates a robust contact management system integrated with a message delivery mechanism using a message queue. It efficiently handles contact data storage, message generation, and message delivery to simulate a streamlined communication process.

## Features

- **Contact Management:**
    - Stores contact information (name, email, password, birthdate, location, description) in a MongoDB database.
    - Generates realistic contact data using the Faker library.
- **Message Delivery:**
    - Leverages RabbitMQ to manage message queues for efficient message handling.
    - Simulates message sending to contacts.
    - Tracks message delivery status.
- **Asynchronous Processing:**
    - Employs separate consumer processes to handle message delivery asynchronously, promoting scalability and responsiveness.

## Installation

### Prerequisites

- Python 3.11 or later
- MongoDB database (cloud or Docker)
- RabbitMQ instance (Docker recommended)

### Steps

1. **Set up MongoDB:**
    - Choose a cloud-based MongoDB service (e.g., MongoDB Atlas) or deploy a local instance using Docker.
2. **Set up RabbitMQ:**
    - Download 
        ```bash
        docker pull rabbitmq:3-management
        ```
    - Start a RabbitMQ instance using Docker:
        ```bash
        docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
        ```
3. **Install dependencies:**
   - **Install dependencies using Poetry:**
        ```bash
        poetry install --no-root
        ```
   - **Activate the virtual environment:**
        ```bash
        poetry shell
        ```

4. **Create a .env file:**
    - In the project's root directory, create a file named `.env`.
    - Add the following lines, replacing the placeholders with your actual MongoDB credentials:
        ```
        DB_USER = your_mongodb_username
        DB_PASSWORD = your_mongodb_password
        DB_HOST = your_mongodb_host
        ```

## Usage

1. **Seed the database with sample contacts and fill messages queue:**
    ```bash
    python producer.py
    ```
2. **Start the consumer processes:**
    ```bash
    python consumer.py
    ````
    * For email-specific message delivery

    ```bash
    python ./email_sms/consumer_email.py

    ```
    * For sms-specific message delivery
    ```bash
    python ./email_sms/consumer_sms.py
    ```

## Project Structure

- **models.py:** Defines MongoEngine models for Contact.
- **producer.py:** Generates and sends contact data and messages to RabbitMQ.
- **consumer.py:** Consumes messages from the main queue and simulates message delivery.
- **.env:** Stores environment variables for MongoDB configuration.
- **pyproject.toml:** Poetry configuration file for managing dependencies.
- **`email_sms` dir:** See below

### Content of the `email_sms` directory:
  Here's a detailed explanation of how the producer.py and consumer_sms.py, consumer_email.py files work in conjunction to achieve message routing and delivery based on contact preferences:

**Producer (email_sms/producer.py):**

1. **Generates Contacts with Preferred Methods:**
   - Creates new contacts using Faker data, including a randomly assigned `preferred_contact_methods` field that specifies either "email" or "sms".
   - Stores these contacts in the MongoDB database.

2. **Sends Messages to RabbitMQ with Routing:**
   - Establishes a connection to the RabbitMQ server.
   - Declares an exchange named `HW_8_Exchange` of type `direct`.
   - Declares two queues: "hw_8_exchange_sms" for SMS messages and "hw_8_exchange_email" for email messages.
   - Binds each queue to the exchange with its respective routing key.
   - Iterates through generated contacts:
     - Retrieves the preferred method for each contact.
     - Constructs a message containing the contact's ID, message text, and preferred method.
     - Publishes the message to the exchange, using the appropriate routing key based on the preferred method:
       - `hw_8_exchange_sms` for SMS messages
       - `hw_8_exchange_email` for email messages

**Consumers (email_sms/consumer_sms.py and consumer_email.py):**

1. **Start Consuming Messages:**
   - Each consumer establishes a connection to RabbitMQ.
   - They declare the respective queue they're responsible for:
     - `hw_8_exchange_sms` for the SMS consumer
     - `hw_8_exchange_email` for the email consumer
   - They initiate message consumption from their respective queues.

2. **Process and Deliver Messages:**
   - Upon receiving a message, the consumer:
     - Decodes the message content.
     - Retrieves the contact ID and preferred method from the message.
     - Fetches the corresponding contact from the MongoDB database.
     - Simulates message delivery using a placeholder function (send_message) that logs a message indicating delivery via the preferred method.
       (In a real-world implementation, this function would integrate with actual SMS or email providers.)
     - Updates the contact's `msg_delivered` field in the database to track delivery status.
     - Acknowledges message receipt to RabbitMQ.


## Technologies Used

- Python
- MongoDB
- MongoEngine (MongoDB ODM)
- RabbitMQ
- Pika (RabbitMQ client library)
- Faker (data generation)
- Redis (optional for caching, not currently implemented)
- Python-dotenv (for managing environment variables)
