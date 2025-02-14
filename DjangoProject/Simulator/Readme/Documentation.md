# **Project Documentation**

## **How to Run the Project**

### **Step 1: Set Up Virtual Environment**

1. **Download the Project Files**: After downloading the project files, open a terminal window in the project directory.

2. **Create a Virtual Environment**: Use the following command to create a virtual environment:
   ```bash
   python -m venv my_env
   ```

3. **Activate the Virtual Environment**: Once created, activate the virtual environment with the following command:
   ```bash
   my_env\Scripts\activate
   ```

4. **Install Required Packages**: Install all dependencies listed in `requirements.txt` by running:
   ```bash
    pip install -r requirements.txt
   ```


### **Files Structure**:

```ruby
    Part 2/
    │
    ├── kpi_project/                # Main project directory
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py             # Django settings
    │   ├── urls.py                 # Project URLs
    │   └── wsgi.py
    │
    ├── kpi_app/                    # KPI application directory
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── models.py               # KPI, Asset, Attribute models
    │   ├── serializers.py          # Serializers for API output
    │   ├── urls.py                 # Application-specific URLs
    │   ├── views.py                # API views for KPI, Asset, and Attribute
    │   ├── test_models.py          # Unit tests for models
    │   ├── test_serializers.py     # Unit tests for serializers
    │   └── test_views.py           # Unit tests for views
    │
    ├── interpreter_app/            # Interpreter application directory
    │   ├── __init__.py
    │   ├── interpreter_engine.py   # Core interpreter logic and SimpleInterpreterFactory
    │   ├── models.py               # Models related to the interpreter, if needed
    │   ├── views.py                # API view to interpret expressions
    │   ├── urls.py                 # URLs for interpreter API
    │   ├── test_interpreter_engine.py  # Unit tests for interpreter logic
    │   └── test_views.py               # Unit tests for API view (ComputeValueAPIView)
    │
    ├── readme/                     # Documentation directory
    │   ├── README.md               # Main documentation file
    │   └── test_cases.txt          # Contains details on test cases
    │
    ├── db.sqlite3                  # SQLite database file
    └── manage.py                   # Django management script
    
```

### **Step 2: Run The Project**

1. **Navigate to the Django Project Directory**: Ensure you're in the directory containing `manage.py`.

2. **Start the Django Server**:  Run the following command to start the server:
   ```bash
    python manage.py runserver
   ```
3. **Access the API Endpoint**:  Once the server is running, you can interact with the API using the link that appear in the terminal:
    ```ruby
    http://127.0.0.1:8000/api/
    ```
4. **Access the other API Endpoints**: You can create KPIs, assets and link them together:
    ```ruby
    http://127.0.0.1:8000/api/KPIs/
    ```
    or 

    ```ruby
    http://127.0.0.1:8000/api/Assets/
    ```
    or 

    ```ruby
    http://127.0.0.1:8000/api/Linker/
    ```
    **Note**: Use Get to list all the instances for KPI, Assets and Attributes

    ### You can List KPIs, Assets and Attributes by using Get 
5. **Send a Request Using URL**: 
* Method: `POST`
* URL: `http://127.0.0.1:8000/api/input/ingester/`
* Body:

  ```json
    {
        "asset_id": "1",
        "attribute_id": "1",
        "timestamp": "2022-07-31T23:28:47Z[UTC]",
        "value": "15"
    }


    {
        "asset_id": "1",
        "attribute_id": "3",
        "timestamp": "2022-07-31T23:28:47Z[UTC]",
        "value": "cathouse"
    }

    {
        "asset_id": "5",
        "attribute_id": "2",
        "timestamp": "2022-07-31T23:28:47Z[UTC]",
        "value": "15"
    }
  ```
    **Note**: Just use one of these examples to check the functionality
6. **Expected API Response: After sending the request, you should receive a response similar to this**
    ```json
    
    {
    "asset_id": "1",
    "attribute_id": "output_1",
    "timestamp": "2022-07-31T23:28:47Z[UTC]",
    "value": 44.5
    }
    
    {
    "asset_id": "1",
    "attribute_id": "output_3",
    "timestamp": "2022-07-31T23:28:47Z[UTC]",
    "value": true
    }
    
    {
    "asset_id": "5",
    "attribute_id": "output_2",
    "timestamp": "2022-07-31T23:28:47Z[UTC]",
    "value": 90.0
    }
    ```

7. **How to use Swagger:**
    ```ruby
    http://127.0.0.1:8000/api/schema/swagger-ui/
    ```
    and    
    ```ruby
    http://127.0.0.1:8000/api/schema/redoc/
    ```

8. **How to run test:**
    ```terminal
    python manage.py test
    ```
    This is used to run all the test cases
    
    Even more, you can handle each app with it's test cases alone
    ```terminal
    python manage.py test interpreter_app
    ```
    or
    ```terminal
    python manage.py test kpi_app
    ```

9. **Deactivate Virtual Environment**: deactivate the virtual environment when you are done, like this in the terminal:
    ```bash
    deactivate
    ```

**Ensure you keep the virtual environment activated while running the project and installing any additional dependencies in the future.**

**Enjoy using the project!**