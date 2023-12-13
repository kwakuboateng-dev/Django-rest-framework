# Django REST Framework API

## Introduction

This document outlines the structure and functionality of a Django REST Framework API with authentication and user-related endpoints.

## Endpoints

### 1. Login

#### Endpoint: `POST /login`

Handles user authentication by verifying the provided username and password.

- **Parameters:**
  - `username`: The username of the user attempting to log in.
  - `password`: The password of the user attempting to log in.

- **Responses:**
  - `200 OK`: Successful authentication. Returns a JSON object with a user token and user details.
  - `400 Bad Request`: Invalid or missing username/password.

```python
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({"error": "Both username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=username)
    if not user.check_password(password):
        return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

    # User authentication successful, generate token and return response
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})
```
### 2. Signup

#### Endpoint: `POST /signup`

Registers a new user by creating a user account and generating an authentication token.

- **Parameters:**
  - User details (username, email, password, etc.) provided in the request body.

- **Responses:**
  - `201 Created`: Successful user creation. Returns a JSON object with a user token and user details.
  - `400 Bad Request`: Invalid user data.

```python
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user_data = serializer.validated_data
        user = User.objects.create_user(**user_data)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
```
### 3. Test Token

#### Endpoint: `GET /test_token`

A protected endpoint requiring authentication to test the validity of a user's token.

- **Authentication:** Token-based authentication is enforced.
- **Permissions:** Only authenticated users are allowed.

- **Responses:**
  - `200 OK`: Token authentication successful. Returns a simple message indicating success.
  - `401 Unauthorized`: User is not authenticated or token is invalid.

```python
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))
```
## Authentication and Permissions

### Authentication Classes:

- `TokenAuthentication`: Ensures that requests include a valid token for authentication.

### Permission Classes:

- `IsAuthenticated`: Requires that the user making the request is authenticated.

