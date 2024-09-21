# Sprint project 03: Instructions
> FastAPI ML App

## Part 1 - Building the basic service

In this project, we will code and deploy an API for serving our own machine learning models. For this particular case, it will be a Convolutional Neural network for images. You don't need to fully understand how this model works because we will see that in detail later. For now, you can check how to use this model in the notebook [14 - THEORY - CNN Example Extra Material.ipynb](https://drive.google.com/file/d/1ADuBSE4z2ZVIdn66YDSwxKv-58U7WEOn/view?usp=sharing).

The project structure is already defined and you will see the modules already have some code and comments to help you get started.

Below is the full project structure:

```
solved
├── ASSIGNMENT.md
├── Makefile
├── README.md
├── System_architecture_diagram.png
├── api
│   ├── Dockerfile
│   ├── Dockerfile.populate
│   ├── __init__.py
│   ├── app
│   │   ├── auth
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py
│   │   │   ├── router.py
│   │   │   └── schema.py
│   │   ├── db.py
│   │   ├── feedback
│   │   │   ├── models.py
│   │   │   ├── router.py
│   │   │   ├── schema.py
│   │   │   └── services.py
│   │   ├── model
│   │   │   ├── router.py
│   │   │   ├── schema.py
│   │   │   └── services.py
│   │   ├── settings.py
│   │   ├── user
│   │   │   ├── __init__.py
│   │   │   ├── hashing.py
│   │   │   ├── models.py
│   │   │   ├── router.py
│   │   │   ├── schema.py
│   │   │   ├── services.py
│   │   │   └── validator.py
│   │   └── utils.py
│   ├── main.py
│   ├── populate_db.py
│   ├── requirements.txt
│   ├── tests
│   │   ├── __init__.py
│   │   ├── dog.jpeg
│   │   ├── test_router_feedback.py
│   │   ├── test_router_model.py
│   │   ├── test_router_user.py
│   │   └── test_utils.py
│   └── uploads
├── db_data
├── docker-compose.yml
├── fastapi_docs.png
├── model
│   ├── Dockerfile
│   ├── Dockerfile.M1
│   ├── __init__.py
│   ├── ml_service.py
│   ├── requirements.txt
│   ├── settings.py
│   └── tests
│       ├── __init__.py
│       ├── dog.jpeg
│       └── test_model.py
├── stress_test
│   ├── dog.jpeg
│   └── locustfile.py
├── tests
│   ├── __init__.py
│   ├── dog.jpeg
│   ├── requirements.txt
│   └── test_integration.py
├── ui
│   ├── Dockerfile
│   ├── app
│   │   ├── image_classifier_app.py
│   │   └── settings.py
│   ├── requirements.txt
│   └── tests
│       ├── dog.jpeg
│       └── test_image_classifier_app.py
├── ui_classify.png
├── ui_login.png
└── uploads

```

Let's take a quick overview of each module:

- api: It has all the needed code to implement the communication interface between the users and our service. It uses FastAPI and Redis to queue tasks to be processed by our machine learning model.
    - `api/app/auth/jwt.py`: Handles JSON Web Token (JWT) creation and verification for user authentication in a FastAPI application. It includes functions to create access tokens (create_access_token), verify and decode tokens (verify_token), and a dependency (get_current_user) that retrieves the current authenticated user based on the provided token. The module uses the HS256 algorithm for encoding and decoding the tokens, with a token expiration time of 30 minutes.
    - `api/app/aut/router.py`: Defines the authentication routes for a FastAPI application. It includes a /login endpoint that authenticates users by verifying their credentials against the database. If the credentials are valid, it generates a JWT access token using the create_access_token function. The endpoint returns the token in a response that can be used for subsequent authenticated requests. 
    - `api/app/auth/schema.py.py`: Defines the data models used for authentication in a FastAPI application. It includes Pydantic models for Login, which captures the username and password; Token, which represents the JWT access token and its type; and TokenData, which holds optional email information extracted from the token. These models are used for request validation and response formatting in the authentication process.
    - `api/app/feedback/models.py`: Defines the Feedback model for a FastAPI application using SQLAlchemy. This model represents feedback data in the database, with fields such as score, predicted_class, feedback, image_file_name, and a foreign key user_id linking it to the User model. The Feedback class includes a relationship to the User model, allowing for easy access to the associated user's data. This model is used to store and manage user feedback related to predictions made by the application.
    - `api/app/feedback/router.py`: Defines a FastAPI router for handling feedback-related operations. It includes two endpoints:
        POST /feedback/: Creates new feedback. The endpoint requires authentication (using JWT) and expects feedback data to be sent in the request body. The feedback is saved to the database.
        GET /feedback/: Retrieves all feedback associated with the authenticated user. The response is formatted according to the DisplayFeedback schema.
        The router uses dependency injection to access the database session and the current authenticated user.
    - `api/app/feedback/schema.py`: defines two Pydantic models for a feedback system:

        Feedback: Used for creating or submitting new feedback. It includes fields for score (a numerical rating), predicted_class (the classification result), image_file_name (the name of the image file associated with the feedback), and feedback (the user's feedback text).

        DisplayFeedback: Used for displaying feedback data. It includes the same fields as the Feedback model, plus an id field for the feedback's unique identifier. The orm_mode configuration allows compatibility with SQLAlchemy models, enabling seamless conversion between Pydantic models and database records.
    - `api/app/feedback/services.py`: This code defines two asynchronous functions for handling feedback operations:
        1. **`new_feedback`**: Adds new feedback to the database. It retrieves the user associated with the current session based on their email, creates a `Feedback` record with the provided details, and commits this record to the database.
        2. **`all_feedback`**: Retrieves all feedback entries associated with the current user. It queries the database for feedback records that match the user's email and returns the results.
    - `api/app/model/router.py`: This code sets up a FastAPI router for handling model predictions. The `predict` endpoint allows users to upload an image file and get predictions from a model:

        - **File Handling**: The uploaded file is saved to a designated folder after computing its hash.
        - **Prediction**: The file hash is used to make predictions using the `model_predict` function.
        - **Response**: Returns a `PredictResponse` containing the success status, prediction result, score, and file name.
        The router requires user authentication and uses utility functions for file operations.
    - `api/app/model/services.py`: This code interacts with a Redis database to handle model prediction jobs:

        - **Redis Connection**: Connects to Redis using settings for host, port, and database ID from `settings.py`.
        - **`model_predict` Function**: 
        - **Job Creation**: Generates a unique job ID and prepares a job dictionary containing the image name.
        - **Queueing**: Adds the job to a Redis queue using the `lpush` method.
        - **Polling**: Continuously checks Redis for the job result using the job ID, retrieves the prediction and score when available, and deletes the job from Redis.
        The function ensures asynchronous processing of model predictions, with delays to wait for results.

    - `api/app/model/schema.py`: Defines two Pydantic models for handling prediction requests and responses:

        - **`PredictRequest`**: Represents the structure of a prediction request, including a single field, `file`, which is expected to be a string (likely the file name or path).

        - **`PredictResponse`**: Represents the structure of a prediction response, including:
            - `success`: A boolean indicating if the prediction was successful.
            - `prediction`: A string containing the predicted class.
            - `score`: A float representing the confidence score of the prediction.
            - `image_file_name`: A string with the name of the image file associated with the prediction.
    - `api/app/user/hashing.py`: Handles password hashing and verification:
        - **`pwd_context`**: Configures password hashing using the Argon2 algorithm, with automatic handling of deprecated schemes.
        - **`verify_password`**: Verifies if a plain password matches a hashed password.
        - **`get_password_hash`**: Hashes a plain password using Argon2 for secure storage.
    - `api/app/user/models.py`: Defines a `User` model for a SQLAlchemy-based database:

        - **Table Definition**: The `User` class maps to the "users" table with columns for `id`, `name`, `email`, and `password`. It includes a relationship with the `Feedback` model, allowing access to a user's feedback.

        - **Constructor**: Initializes a new user, hashing the password before storing it.

        - **Password Check**: Provides a method to verify the given password against the stored hashed password using the `hashing` module.
    - `api/app/user/router.py`: Defines a FastAPI router for user management with several endpoints:
        - **`POST /user/`**: Registers a new user. Checks if the email is already registered and, if not, creates a new user.
        - **`GET /user/`**: Retrieves a list of all users. Requires authentication to access.
        - **`GET /user/{id}`**: Retrieves a user by their ID. Requires authentication to access and returns user details based on the ID.
        - **`DELETE /user/{id}`**: Deletes a user by their ID. Requires authentication and returns a 204 status code upon successful deletion.

    - `api/app/user/schema.py`: Defines two Pydantic models for user data:
        - **`User`**: Represents user data for registration or updates, including `name` (with constraints on length), `email` (validated as an email address), and `password`.
        - **`DisplayUser`**: Represents user data for display purposes, including `id`, `name`, and `email`. The `orm_mode` configuration enables compatibility with ORM models, allowing seamless conversion between Pydantic models and database records.
    - `api/app/user/services.py`: Defines several asynchronous service functions for managing user data:
        - **`new_user_register`**: Registers a new user by creating a `User` instance, adding it to the database, and committing the changes.
        - **`all_users`**: Retrieves a list of all users from the database.
        - **`get_user_by_id`**: Fetches a user by their ID. Raises a 404 error if the user is not found.
        - **`delete_user_by_id`**: Deletes a user from the database by their ID and commits the changes.
    - `api/app/user/validator.py`: Defines an asynchronous function, `verify_email_exist`, that checks if a user with a given email address exists in the database. It queries the `User` model and returns the user if found, or `None` if the email is not registered.
    - `api/app/db.py`: This code sets up SQLAlchemy for a PostgreSQL database:
        - **Configuration**: Retrieves database connection details (username, password, host, and name) from `config`.
        - **Engine Creation**: Constructs a database URL and creates an SQLAlchemy engine for connecting to the PostgreSQL database.
        - **Session Local**: Defines a session factory (`SessionLocal`) for creating database sessions with automatic handling of transactions.
        - **Base**: Defines a base class for SQLAlchemy models using `declarative_base`.
        - **`get_db` Function**: Provides a database session generator function that ensures sessions are properly opened and closed. This function is used for dependency injection in FastAPI.
    - `app/main.py`: This code sets up a FastAPI application:
        - **`FastAPI` Initialization**: Creates an instance of the FastAPI application with a specified title and version.
        - **Router Inclusion**: Integrates routers from different modules (`auth`, `feedback`, `model`, `user`) into the application, allowing the app to handle routes defined in these modules.
    - `api/app/utils.py`: Implements some extra functions used internally by our api.
    - `api/settings.py`: It has all the API settings..
    - `api/tests`: Test suite.
- model: Implements the logic to get jobs from Redis and process them with our Machine Learning model. When we get the predicted value from our model, we must encode it on Redis again so it can be delivered to the user.
    - `model/ml_service.py`: Runs a thread in which it gets jobs from Redis, processes them with the model, and returns the answers.
    - `model/settings.py`: Settings for our ML model.
    - `model/tests`: Test suite.
- tests: This module contains integration tests so we can properly check our system's end-to-end behavior is expected.

Your task will be to complete the corresponding code on those parts it's required across all the modules. You can validate it's working as expected using the already provided tests. We encourage you to also write extra test cases as needed.

You can also take a look at the file `System_architecture_diagram.png` to have a graphical description of the microservices and how the communication is performed.

### Recommended way to work across all those files

Our recommendation for you about the order in which you should complete these files is the following:

#### 0. `Dockerfile.populate`

Complete the `Dockerfile.populate` file found in `api` folder. You can use as a reference the `Dockerfile` for the API.
Once correctly completed, you should be able to run the `populate_db.py` script.

#### 1. `model` folder

Inside this module, complete:

1. `predict()` function under `model/ml_service.py` file.
2. Then, go for the `classify_process()` function also under `model/ml_service.py` file.

Then run the tests corresponding to this module and check if they are passing correctly.

#### 2. `api` folder

Inside this module, complete:

1. `allowed_file()` and `get_file_hash()` functions under `api/app/utils.py` file.
2. Redis settings and `model_predict()` function under `api/app/model/services.py` file. This will allow to communicate the API with our ML service.
3. `predict()` function in `api/app/model/router.py` file. This endpoint will use previously completed functions to run a complete prediction over an image.
4. `create_user_registration()` function in `api/app/user/router.py`. This endpoint will handle the creation of a new user in the database.

Now run the tests corresponding to this module and check if they are passing correctly

### 3. `ui` folder

Inside this module, complete:

1. `login()` function, under `ui/app/image_classifier_app.py`.
2. Then `predict()` function, also under `ui/app/image_classifier_app.py`.
3. Finally, `send_feedback()` function, also under `ui/app/image_classifier_app.py`.

## Part 2 - Stress testing with *Locust*

For this task, you must complete the file `locustfile.py` from the `stress_test` folder. Make sure to create at least one test for:
- `index` endpoint.
- `predict` endpoint.

### Test scaled services

You can easily launch more instances for a particular service using `--scale SERVICE=NUM` when running `docker-compose up` command (see [here](https://docs.docker.com/compose/reference/up/)). Scale `model` service to 2 or even more instances and check the performance with locust.

Write a short report detailing the hardware specs from the server used to run the service and show a comparison in the results obtained for a different number of users being simulated and instances deployed.

## [Optional] Part 3 - Batch processing

Replace the current model behavior to process the jobs in batches. Check if that improves the numbers when doing stress testing.
