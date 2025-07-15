Guide to the Project

This project is designed to assess your ability to work with FastAPI by building a user profile management feature, focusing on async endpoint design, custom validation using advanced Pydantic features, and uniform error handling.

Requirements:
- Implement endpoints for creating, retrieving, and updating user profiles.
- Enforce field validation, including email (using appropriate Pydantic types) and phone number (custom format constraint).
- Use async FastAPI route handlers and ensure avatar updates are handled as background tasks.
- Provide consistent, structured error responses via custom exceptions and error response models.
- Integrate your router properly with the FastAPI app so that all endpoints are accessible under the "/profiles" path prefix.

Verifying Your Solution:
Your solution will be verified using the provided automated test suite (already included in the project). The tests will check that all profile-related REST endpoints work as expected, with correct async behavior, validation, and error formats.

Focus on implementing the specified endpoints, validation logic, and background processing, using only the allowed files and patterns.